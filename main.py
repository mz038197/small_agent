"""
課堂合併作答：challenges-wiki-basic-advanced.md WG-01～WG-21

執行：專案根目錄 `uv run main.py`
環境：`.env` 內 `OPENAI_API_KEY`；可選 `SESSION_JSONL_PATH`、`TOKEN_BUDGET`、`CHAT_MODEL`、`VISION_MODEL`
附圖：輸入 `/image 相對路徑` 後同一行或下一行輸入文字問題（vision 模型預設 gpt-4o）
"""

import base64
import copy
import json
import os
import platform
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    AIMessageChunk,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
    message_chunk_to_message,
)
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI

# ---------------------------------------------------------------------------
# WG-01～03：進入點、變數、f-string（暖身示範，main 內亦呼叫）
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE = PROJECT_ROOT.resolve()
MEMORY_DIR = PROJECT_ROOT / "memory"
MEMORY_FILE = MEMORY_DIR / "MEMORY.md"
HISTORY_FILE = MEMORY_DIR / "HISTORY.md"

TOKEN_BUDGET = int(os.getenv("TOKEN_BUDGET", "8000"))
CONSOLIDATION_MAX_RETRIES = int(os.getenv("CONSOLIDATION_MAX_RETRIES", "3"))
MEMORY_MAX_CHARS = int(os.getenv("MEMORY_MAX_CHARS", "6000"))
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-5.4-mini")
VISION_MODEL = os.getenv("VISION_MODEL", "gpt-5.4-mini")


def print_wg01_to_03_banner() -> None:
    """WG-01～03：進入點區塊內變數與 f-string 問候。"""
    agent_name = "法鬥超人"
    message = f"Hello, 我是{agent_name}，很開心認識你!"
    print(message)


# ---------------------------------------------------------------------------
# WG-04：頂層匯入（langchain_openai、python-dotenv 見 pyproject.toml）
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# WG-13／WG-14：@tool 工具組
# ---------------------------------------------------------------------------


def resolve_workspace_path(path: str) -> Path:
    raw = Path(path)
    if raw.is_absolute():
        raise PermissionError("absolute paths are not allowed")
    target = (WORKSPACE / path).resolve()
    try:
        target.relative_to(WORKSPACE)
    except ValueError as e:
        raise PermissionError(f"path is outside workspace: {path}") from e
    return target


@tool
def add_two(a: int, b: int) -> int:
    """兩個整數相加並回傳和。凡涉及兩個整數相加必須呼叫此工具，不要只在文字裡心算。"""
    return a + b


@tool("read_file")
def read_file(path: str, offset: int = 1, limit: int = 200) -> str:
    """讀取 workspace 內 UTF-8 文字檔，回傳帶行號內容。"""
    try:
        target = resolve_workspace_path(path)
        if not target.is_file():
            return f"Error: not a file: {path}"
        lines = target.read_text(encoding="utf-8").splitlines()
        start = max(offset - 1, 0)
        end = min(start + limit, len(lines))
        return "\n".join(f"{i + 1}| {line}" for i, line in enumerate(lines[start:end], start))
    except Exception as e:
        return f"Error: {e}"


@tool("write_file")
def write_file(path: str, content: str) -> str:
    """整檔覆寫寫入 UTF-8 文字檔（必要時建立父資料夾）。"""
    try:
        target = resolve_workspace_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error: {e}"


@tool("edit_file")
def edit_file(path: str, old_text: str, new_text: str, replace_all: bool = False) -> str:
    """在既有檔案中把 old_text 換成 new_text（預設僅單次替換）。"""
    try:
        target = resolve_workspace_path(path)
        text = target.read_text(encoding="utf-8")
        count = text.count(old_text)
        if count == 0:
            return "Error: old_text not found"
        if count > 1 and not replace_all:
            return "Error: old_text appears multiple times"
        target.write_text(
            text.replace(old_text, new_text, -1 if replace_all else 1),
            encoding="utf-8",
        )
        return f"edited {path}"
    except Exception as e:
        return f"Error: {e}"


@tool("list_dir")
def list_dir(path: str, recursive: bool = False, max_entries: int = 200) -> str:
    """列出 workspace 內資料夾內容。"""
    try:
        root = resolve_workspace_path(path)
        if not root.is_dir():
            return f"Error: not a directory: {path}"
        iterator = root.rglob("*") if recursive else root.iterdir()
        entries = [str(item.relative_to(WORKSPACE)) for item in iterator][:max_entries]
        return "\n".join(entries) if entries else "(empty)"
    except Exception as e:
        return f"Error: {e}"


@tool("exec")
def exec_workspace(command: str, timeout: int = 30) -> str:
    """在專案根目錄（workspace）執行單行 shell 指令，回傳 exit code 與輸出摘要。"""
    blocked = ("rm -rf", "del /f", "rmdir /s", "format", "shutdown")
    lowered = command.lower()
    if any(part in lowered for part in blocked):
        return "Error: blocked dangerous command (safety limit)"

    child_env = os.environ.copy()
    child_env.setdefault("PYTHONUTF8", "1")
    child_env.setdefault("PYTHONIOENCODING", "utf-8")

    run_kw: dict[str, Any] = {
        "cwd": str(WORKSPACE),
        "shell": True,
        "capture_output": True,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "timeout": timeout,
        "env": child_env,
    }
    if os.name == "nt":
        run_kw["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    try:
        result = subprocess.run(command, **run_kw)
        output = ((result.stdout or "") + (result.stderr or "")).strip()
        cap = 4000
        if len(output) > cap:
            output = output[:cap] + "\n\n[truncated]"
        if not output:
            output = "(no stdout or stderr; command finished with no captured output)"
        return f"exit_code={result.returncode}\n{output}"
    except Exception as e:
        return f"Error: {e}"


TOOLS: list[BaseTool] = [
    add_two,
    read_file,
    write_file,
    edit_file,
    list_dir,
    exec_workspace,
]
_TOOL_BY_NAME: dict[str, BaseTool] = {t.name: t for t in TOOLS}


# ---------------------------------------------------------------------------
# WG-20：工具參數 cast／validate／prepare_tool_call
# ---------------------------------------------------------------------------


def _tool_input_schema(tool_obj: BaseTool) -> dict[str, Any]:
    schema = getattr(tool_obj, "args_schema", None)
    if schema is not None and hasattr(schema, "model_json_schema"):
        return schema.model_json_schema()
    return {"type": "object", "properties": {}, "required": []}


def cast_params(params: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    props = schema.get("properties") or {}
    out = dict(params)
    for key, val in list(out.items()):
        spec = props.get(key) or {}
        t = spec.get("type")
        if t == "integer" and isinstance(val, str):
            try:
                out[key] = int(val)
            except ValueError:
                pass
        elif t == "number" and isinstance(val, str):
            try:
                out[key] = float(val)
            except ValueError:
                pass
        elif t == "boolean" and isinstance(val, str):
            if val.lower() in ("true", "1", "yes"):
                out[key] = True
            elif val.lower() in ("false", "0", "no"):
                out[key] = False
    return out


def validate_params(params: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    props = schema.get("properties") or {}
    required = schema.get("required") or []
    for r in required:
        if r not in params:
            errors.append(f"missing required field: {r}")
    for key, val in params.items():
        if key not in props:
            errors.append(f"unknown field: {key}")
            continue
        t = props[key].get("type")
        if t == "integer" and not isinstance(val, int):
            errors.append(f"{key} must be integer")
        elif t == "number" and not isinstance(val, (int, float)):
            errors.append(f"{key} must be number")
        elif t == "boolean" and not isinstance(val, bool):
            errors.append(f"{key} must be boolean")
        elif t == "string" and not isinstance(val, str):
            errors.append(f"{key} must be string")
    return errors


def prepare_tool_call(
    name: str, raw: Any
) -> tuple[BaseTool | None, dict[str, Any], str | None]:
    if not isinstance(raw, dict):
        return None, {}, f"tool args must be object, got {type(raw).__name__}"
    tool_obj = _TOOL_BY_NAME.get(name)
    if tool_obj is None:
        return None, {}, f"unknown tool: {name}"
    schema = _tool_input_schema(tool_obj)
    params = cast_params(dict(raw), schema)
    errs = validate_params(params, schema)
    if errs:
        return tool_obj, params, "; ".join(errs)
    return tool_obj, params, None


# ---------------------------------------------------------------------------
# WG-12／WG-20：system prompt
# ---------------------------------------------------------------------------


def _runtime_env_note() -> str:
    """WG-12：啟動時偵測 OS，供 Agent 選擇 shell 寫法。"""
    sys_name = platform.system()  # Windows / Darwin / Linux
    shell_hint = (
        "exec 在 PowerShell 下執行；勿用 <<、heredoc、bash -c。"
        if os.name == "nt"
        else "exec 在系統 shell 下執行；多行腳本仍請 write_file 後 uv run。"
    )
    return (
        f"\n\n【執行環境】{sys_name}（os.name={os.name}）；專案根目錄為目前工作目錄。"
        f"{shell_hint}"
    )


def get_identity() -> str:
    """WG-12：課堂人設（規則、顯示名、執行環境、exec 注意）。"""
    system_text = "你是課堂程式助教，並請使用繁體中文。"
    nick = "法鬥超人"
    exec_note = (
        "\n\n【exec 注意】"
        "\n- 請依上方【執行環境】選擇相容的 shell 指令，勿假設為 Linux Bash。"
        "\n- 若要執行 Python：先用 write_file 寫入 .py，再 exec「uv run python 相對路徑」。"
    )
    return (
        f"{system_text}\n\n【本場次顯示名稱】{nick}"
        f"{_runtime_env_note()}{exec_note}"
    )


def memory_block_for_system() -> str:
    """WG-19：讀取 MEMORY.md 組長期記憶區塊。"""
    if not MEMORY_FILE.is_file():
        return ""
    body = MEMORY_FILE.read_text(encoding="utf-8").strip()
    if not body:
        return ""
    if len(body) > MEMORY_MAX_CHARS:
        body = body[-MEMORY_MAX_CHARS:]
    return f"## Long-term Memory\n\n{body}"


@dataclass
class SkillEntry:
    name: str
    path: Path
    source: str
    description: str
    always: bool
    body: str


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text.strip()
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text.strip()
    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip()
    body = "\n".join(lines[end + 1 :]).strip()
    return meta, body


class SkillsLoader:
    def __init__(self, workspace: Path, builtin_skills_dir: Path) -> None:
        self.workspace_skills = workspace / "skills"
        self.builtin_skills = builtin_skills_dir

    def _entries_from_dir(self, root: Path, source: str, skip: set[str]) -> list[SkillEntry]:
        if not root.exists():
            return []
        entries: list[SkillEntry] = []
        for skill_dir in sorted(root.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_dir.is_dir() or not skill_file.exists():
                continue
            if skill_dir.name in skip:
                continue
            text = skill_file.read_text(encoding="utf-8")
            meta, body = split_frontmatter(text)
            name = skill_dir.name
            description = meta.get("description") or name
            always = meta.get("always", "false").lower() == "true"
            entries.append(SkillEntry(name, skill_file, source, description, always, body))
        return entries

    def list_skills(self) -> list[SkillEntry]:
        workspace_entries = self._entries_from_dir(self.workspace_skills, "workspace", set())
        workspace_names = {e.name for e in workspace_entries}
        builtin_entries = self._entries_from_dir(
            self.builtin_skills, "builtin", workspace_names
        )
        return workspace_entries + builtin_entries

    def load_skill(self, name: str) -> str | None:
        for root in (self.workspace_skills, self.builtin_skills):
            path = root / name / "SKILL.md"
            if path.exists():
                return path.read_text(encoding="utf-8")
        return None


def build_skills_summary(entries: list[SkillEntry]) -> str:
    summarized = [e for e in entries if not e.always]
    if not summarized:
        return ""
    lines = [f"- **{e.name}** — {e.description} `{e.path}`" for e in summarized]
    return "\n".join(lines)


def build_system_prompt(loader: SkillsLoader) -> str:
    """WG-12～20：人設 + 長期記憶 + Skills，組成送模用的 system 字串。"""
    parts: list[str] = [get_identity()]
    mem = memory_block_for_system()
    if mem:
        parts.append(mem)
    entries = loader.list_skills()
    active = [e for e in entries if e.always]
    if active:
        body = "\n\n---\n\n".join(f"### Skill: {e.name}\n\n{e.body}" for e in active)
        parts.append(f"# Active Skills\n\n{body}")
    summary = build_skills_summary(entries)
    if summary:
        intro = (
            "下列技能可擴充你的能力。若要使用某技能，請用 read_file 讀取清單中該技能路徑下的 SKILL.md。\n"
            "若該技能需額外套件或環境，請先依 SKILL.md 或專案說明安裝相依項目後再操作。\n\n"
        )
        parts.append("# Skills\n\n" + intro + summary)
    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------
# WG-15～16／WG-21：JSONL（含 image_path）
# ---------------------------------------------------------------------------


def _default_metadata(created_at: str | None = None) -> dict[str, Any]:
    now = datetime.now().isoformat()
    return {
        "_type": "metadata",
        "key": "session",
        "created_at": created_at or now,
        "updated_at": now,
        "metadata": {},
        "last_consolidated": 0,
    }


def _serialize_tool_calls(tc: Any) -> list[dict[str, Any]]:
    if not tc:
        return []
    out: list[dict[str, Any]] = []
    for item in tc:
        if isinstance(item, dict):
            out.append(
                {
                    "name": item.get("name", ""),
                    "args": dict(item.get("args") or {}),
                    "id": str(item.get("id", "")),
                }
            )
    return out


def _human_content_to_str(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        return "\n".join(p for p in parts if p)
    return str(content)


def load_user_row_to_history_human(row: dict[str, Any]) -> HumanMessage:
    text = str(row.get("content", ""))
    rel = row.get("image_path")
    if not rel:
        return HumanMessage(content=text)
    mt = row.get("media_type")
    extra = f"[此回合曾附圖，路徑：{rel}]"
    if mt:
        extra += f"（media_type={mt}）"
    return HumanMessage(content=f"{text}\n\n{extra}")


def _row_to_message(obj: dict[str, Any]) -> BaseMessage | None:
    role = obj.get("role")
    if role == "user":
        return load_user_row_to_history_human(obj)
    if role == "assistant":
        content = str(obj.get("content", ""))
        tc = obj.get("tool_calls")
        if tc:
            return AIMessage(content=content, tool_calls=_serialize_tool_calls(tc))
        return AIMessage(content=content)
    if role == "tool":
        tid = obj.get("tool_call_id") or ""
        nm = str(obj.get("name", "") or "").strip() or None
        return ToolMessage(
            content=str(obj.get("content", "")),
            tool_call_id=str(tid),
            name=nm,
        )
    return None


def _message_to_jsonl_row(m: BaseMessage) -> dict[str, Any] | None:
    ts = datetime.now().isoformat()
    if isinstance(m, HumanMessage):
        row: dict[str, Any] = {
            "role": "user",
            "content": _human_content_to_str(m.content),
            "timestamp": ts,
        }
        extra = getattr(m, "additional_kwargs", None) or {}
        rel = extra.get("image_path")
        if rel:
            row["image_path"] = rel
            mt = extra.get("media_type")
            if mt:
                row["media_type"] = mt
        return row
    if isinstance(m, AIMessage):
        row = {"role": "assistant", "content": m.content, "timestamp": ts}
        tc = getattr(m, "tool_calls", None)
        if tc:
            row["tool_calls"] = _serialize_tool_calls(tc)
        return row
    if isinstance(m, ToolMessage):
        row = {
            "role": "tool",
            "content": m.content,
            "tool_call_id": m.tool_call_id,
            "timestamp": ts,
        }
        tname = getattr(m, "name", None)
        if tname:
            row["name"] = tname
        return row
    return None


def load_session_jsonl(path: str) -> tuple[list[BaseMessage], dict[str, Any] | None]:
    if not os.path.exists(path):
        return [], None
    messages: list[BaseMessage] = []
    meta: dict[str, Any] | None = None
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            try:
                obj: Any = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and obj.get("_type") == "metadata":
                meta = obj
                continue
            if isinstance(obj, dict):
                msg = _row_to_message(obj)
                if msg is not None:
                    messages.append(msg)
    return messages, meta


def save_session_jsonl(
    path: str,
    messages: list[BaseMessage],
    existing_meta: dict[str, Any] | None,
    last_consolidated: int,
) -> dict[str, Any]:
    now = datetime.now().isoformat()
    if existing_meta is None:
        meta = _default_metadata(created_at=now)
    else:
        meta = dict(existing_meta)
        meta["_type"] = "metadata"
        meta["key"] = meta.get("key", "session")
        if "created_at" not in meta:
            meta["created_at"] = now
        meta["updated_at"] = now
    meta["last_consolidated"] = last_consolidated
    lines: list[str] = [json.dumps(meta, ensure_ascii=False)]
    for m in messages:
        row = _message_to_jsonl_row(m)
        if row is not None:
            lines.append(json.dumps(row, ensure_ascii=False))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")
    return meta


# ---------------------------------------------------------------------------
# WG-17／WG-19：字元預算與整併邊界
# ---------------------------------------------------------------------------


def estimate_message_tokens(message: BaseMessage) -> int:
    c = message.content
    if isinstance(c, str):
        return len(c)
    if isinstance(c, list):
        return sum(len(str(block)) for block in c)
    return len(str(c))


def pick_consolidation_boundary(
    messages: list[BaseMessage],
    last_consolidated: int,
    tokens_to_remove: int,
) -> tuple[int, int] | None:
    start = last_consolidated
    if start >= len(messages) or tokens_to_remove <= 0:
        return None
    removed_tokens = 0
    last_boundary: tuple[int, int] | None = None
    for idx in range(start, len(messages)):
        message = messages[idx]
        if idx > start and isinstance(message, HumanMessage):
            last_boundary = (idx, removed_tokens)
            if removed_tokens >= tokens_to_remove:
                return last_boundary
        removed_tokens += estimate_message_tokens(message)
    return last_boundary


def message_cost(msgs: list[BaseMessage]) -> int:
    return sum(estimate_message_tokens(m) for m in msgs)


def request_cost_chars(system_str: str, past: list[BaseMessage], human: HumanMessage) -> int:
    return len(system_str) + message_cost([*past, human])


def pick_past_for_turn(
    history: list[BaseMessage],
    last_consolidated: int,
    system_str: str,
    human_message: HumanMessage,
) -> list[BaseMessage]:
    past0 = history[last_consolidated:]
    cost = request_cost_chars(system_str, past0, human_message)
    if cost <= TOKEN_BUDGET:
        return past0
    tokens_to_remove = max(0, cost - TOKEN_BUDGET // 2)
    boundary = pick_consolidation_boundary(history, last_consolidated, tokens_to_remove)
    if boundary is not None:
        return history[boundary[0] :]
    return past0


def append_history_line(line: str) -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {line}\n")


def _messages_to_plain_text(msgs: list[BaseMessage]) -> str:
    parts: list[str] = []
    for m in msgs:
        if isinstance(m, HumanMessage):
            parts.append(f"User: {_human_content_to_str(m.content)}")
        elif isinstance(m, AIMessage):
            parts.append(f"Assistant: {_human_content_to_str(m.content)}")
        elif isinstance(m, ToolMessage):
            parts.append(f"Tool({m.tool_call_id}): {m.content}")
    return "\n".join(parts)


def run_consolidation_pass(
    consolidation_llm: ChatOpenAI,
    chunk: list[BaseMessage],
    current_memory: str,
) -> tuple[str, str] | None:
    prompt = (
        "你是長期記憶整併助手。根據下列舊對話與現有記憶，產出 JSON 物件，"
        '僅含兩個鍵："history_entry"（單行摘要）與 "memory_update"（完整 markdown 取代 MEMORY）。\n\n'
        f"現有記憶：\n{current_memory or '(空)'}\n\n"
        f"待整併對話：\n{_messages_to_plain_text(chunk)}"
    )
    response = consolidation_llm.invoke(prompt)
    text = (response.content or "").strip()
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
        entry = str(data.get("history_entry", "")).replace("\n", " ").strip()
        memory = str(data.get("memory_update", "")).strip()
        if entry and memory:
            return entry, memory
    except json.JSONDecodeError:
        return None
    return None


def maybe_consolidate_memory(
    consolidation_llm: ChatOpenAI,
    history: list[BaseMessage],
    last_consolidated: int,
    system_str: str,
    human_message: HumanMessage,
) -> int:
    """WG-19：超 TOKEN_BUDGET 時整併一段 chunk，更新 MEMORY/HISTORY 與游標。"""
    while True:
        past0 = history[last_consolidated:]
        cost = request_cost_chars(system_str, past0, human_message)
        if cost <= TOKEN_BUDGET:
            break
        tokens_to_remove = max(0, cost - TOKEN_BUDGET // 2)
        boundary = pick_consolidation_boundary(
            history, last_consolidated, tokens_to_remove
        )
        if boundary is None:
            break
        idx, _ = boundary
        chunk = history[last_consolidated:idx]
        if not chunk:
            last_consolidated = idx
            continue
        current_memory = ""
        if MEMORY_FILE.is_file():
            current_memory = MEMORY_FILE.read_text(encoding="utf-8")
        success = False
        retries = max(CONSOLIDATION_MAX_RETRIES, 0)
        for attempt in range(retries + 1):
            result = run_consolidation_pass(consolidation_llm, chunk, current_memory)
            if result:
                entry, memory_update = result
                MEMORY_DIR.mkdir(parents=True, exist_ok=True)
                MEMORY_FILE.write_text(memory_update, encoding="utf-8")
                append_history_line(entry)
                success = True
                break
        if not success:
            append_history_line("[CONSOLIDATION-FAILED] chunk consolidation failed")
        last_consolidated = idx
        past_after = history[last_consolidated:]
        if request_cost_chars(system_str, past_after, human_message) <= TOKEN_BUDGET // 2:
            break
    return last_consolidated


# ---------------------------------------------------------------------------
# WG-18：dict transcript 修復（獨立函式，不污染輸入）
# ---------------------------------------------------------------------------

COMPACTABLE = {
    "read_file",
    "exec",
    "grep",
    "glob",
    "web_search",
    "web_fetch",
    "list_dir",
}


def _collect_tool_call_ids(messages: list[dict[str, Any]]) -> set[str]:
    ids: set[str] = set()
    for m in messages:
        if m.get("role") != "assistant":
            continue
        for tc in m.get("tool_calls") or []:
            tid = tc.get("id")
            if tid:
                ids.add(str(tid))
    return ids


def build_messages_for_model(
    messages: list[dict[str, Any]],
    *,
    max_chars: int,
    max_tool_chars: int,
    keep_recent_tools: int,
) -> list[dict[str, Any]]:
    out = [dict(m) for m in messages]

    # A: 孤兒 tool
    known_ids = _collect_tool_call_ids(out)
    out = [
        m
        for m in out
        if not (
            m.get("role") == "tool"
            and str(m.get("tool_call_id", "")) not in known_ids
        )
    ]

    # B: 缺 tool 回覆補洞
    fixed: list[dict[str, Any]] = []
    i = 0
    while i < len(out):
        m = out[i]
        fixed.append(m)
        if m.get("role") == "assistant" and m.get("tool_calls"):
            existing = {
                str(t.get("tool_call_id", ""))
                for t in out[i + 1 :]
                if t.get("role") == "tool"
            }
            insert_at = i + 1
            for tc in m["tool_calls"]:
                tid = str(tc.get("id", ""))
                if tid and tid not in existing:
                    fn = tc.get("function") or {}
                    name = fn.get("name", "tool")
                    stub = {
                        "role": "tool",
                        "tool_call_id": tid,
                        "name": name,
                        "content": "[Tool result unavailable — call was interrupted or lost]",
                    }
                    fixed.insert(insert_at, stub)
                    insert_at += 1
        i += 1
    out = fixed

    # C: tool 單則上限
    for m in out:
        if m.get("role") == "tool" and isinstance(m.get("content"), str):
            c = m["content"]
            if len(c) > max_tool_chars:
                m["content"] = c[:max_tool_chars] + "\n\n[truncated]"

    # D: 小型壓縮
    compact_indices = [
        idx
        for idx, m in enumerate(out)
        if m.get("role") == "tool" and m.get("name") in COMPACTABLE
    ]
    if len(compact_indices) > keep_recent_tools:
        to_compact = compact_indices[: -keep_recent_tools]
        for idx in to_compact:
            m = out[idx]
            if isinstance(m.get("content"), str) and len(m["content"]) >= 500:
                name = m.get("name", "tool")
                m["content"] = f"[{name} result omitted from context]"

    # E: 全對話字元預算
    def row_cost(msg: dict[str, Any]) -> int:
        return len(str(msg.get("content", "")))

    def total_cost() -> int:
        return sum(row_cost(m) for m in out)

    while total_cost() > max_chars and len(out) > 2:
        removed = False
        for idx in range(len(out)):
            if out[idx].get("role") == "system":
                continue
            if idx == len(out) - 1 and out[idx].get("role") == "user":
                continue
            out.pop(idx)
            removed = True
            break
        if not removed:
            break

    if out and out[-1].get("role") != "user":
        out.append({"role": "user", "content": "(conversation continued)"})
    return out


# ---------------------------------------------------------------------------
# WG-21：多模態與送模層 messages_for_model
# ---------------------------------------------------------------------------


def guess_media_type(path: Path, fallback: str = "image/png") -> str:
    ext = path.suffix.lower()
    if ext in (".jpg", ".jpeg"):
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    return fallback


def image_bytes_to_data_url(data: bytes, media_type: str) -> str:
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{media_type};base64,{b64}"


def resolve_project_image(path_str: str) -> Path | None:
    raw = Path(path_str)
    if raw.is_absolute():
        return None
    full = (PROJECT_ROOT / path_str).resolve()
    try:
        full.relative_to(PROJECT_ROOT.resolve())
    except ValueError:
        return None
    return full


def build_human_message_for_current_turn(
    text: str,
    image_rel: str | None,
    media_type: str | None = None,
) -> HumanMessage:
    if not image_rel:
        return HumanMessage(content=text)
    full = resolve_project_image(image_rel)
    if full is None or not full.is_file():
        print(f"[warn] missing image for current turn: {image_rel}")
        return HumanMessage(content=text)
    mt = media_type or guess_media_type(full)
    url = image_bytes_to_data_url(full.read_bytes(), mt)
    msg = HumanMessage(
        content=[
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": url}},
        ]
    )
    msg.additional_kwargs["image_path"] = image_rel
    msg.additional_kwargs["media_type"] = mt
    return msg


def _human_to_text_only_placeholder(m: HumanMessage) -> HumanMessage:
    c = m.content
    if isinstance(c, str):
        return m
    if isinstance(c, list):
        parts: list[str] = []
        for block in c:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        body = "\n".join(p for p in parts if p).strip() or "[（無文字）此則曾含圖]"
        return HumanMessage(content=body + "\n\n[送模層已剝除歷史圖區塊]")
    return HumanMessage(content=str(c))


def messages_for_model(
    system_message: SystemMessage,
    past: list[BaseMessage],
    human_message: HumanMessage,
) -> list[BaseMessage]:
    out: list[BaseMessage] = [copy.deepcopy(system_message)]
    for m in past:
        mm = copy.deepcopy(m)
        if isinstance(mm, HumanMessage) and not isinstance(mm.content, str):
            mm = _human_to_text_only_placeholder(mm)
        out.append(mm)
    out.append(copy.deepcopy(human_message))
    return out


def parse_user_input(raw: str) -> tuple[str, str | None]:
    stripped = raw.strip()
    if stripped.lower().startswith("/image "):
        rest = stripped[7:].strip()
        parts = rest.split(maxsplit=1)
        if parts:
            path = parts[0]
            text = parts[1] if len(parts) > 1 else "請描述這張圖片。"
            return text, path
    return stripped, None


# ---------------------------------------------------------------------------
# WG-10／WG-13：串流 ReAct
# ---------------------------------------------------------------------------


def _flatten_ai_chunk_text(content: Any) -> str:
    if not content:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        return "".join(parts)
    return str(content)


def _print_ai_stream_content(content: Any) -> None:
    if not content:
        return
    if isinstance(content, str):
        print(content, end="", flush=True)
        return
    if isinstance(content, list):
        for block in content:
            if isinstance(block, str):
                print(block, end="", flush=True)
            elif isinstance(block, dict) and block.get("type") == "text":
                print(block.get("text", ""), end="", flush=True)


class _LeadingStripStreamPrinter:
    def __init__(self) -> None:
        self._pending = True

    def emit(self, content: Any) -> None:
        if not content:
            return
        if self._pending:
            flat = _flatten_ai_chunk_text(content)
            if not flat:
                return
            trimmed = flat.lstrip()
            if not trimmed:
                return
            print(trimmed, end="", flush=True)
            self._pending = False
            return
        _print_ai_stream_content(content)


def _run_bound_tool(name: str, args: dict[str, Any]) -> str:
    _tool_obj, params, err = prepare_tool_call(name, args)
    if err:
        return f"Error: {err}"
    if _tool_obj is None:
        return f"Error: unknown tool {name!r}"
    try:
        return str(_tool_obj.invoke(params))
    except Exception as e:
        return f"Error running tool {name}: {e}"


def run_react_turn(
    llm_tools: ChatOpenAI,
    context_messages: list[BaseMessage],
    idx_turn_start: int,
    *,
    stream_stdout: bool = True,
) -> tuple[str, list[BaseMessage]]:
    messages = list(context_messages)
    while True:
        acc: AIMessageChunk | None = None
        stream_out = _LeadingStripStreamPrinter() if stream_stdout else None
        for chunk in llm_tools.stream(messages):
            acc = chunk if acc is None else acc + chunk
            if stream_out is not None:
                stream_out.emit(getattr(chunk, "content", None))
        if acc is None:
            raise RuntimeError("模型串流未回傳任何 chunk")
        response = message_chunk_to_message(acc)

        if response.tool_calls:
            if stream_stdout:
                print()
            messages.append(response)
            for tc in response.tool_calls:
                name = str(tc["name"])
                raw_args = dict(tc.get("args") or {})
                result = _run_bound_tool(name, raw_args)
                if stream_stdout:
                    print(f"\n[工具 {name}]\n{result}\n", flush=True)
                messages.append(
                    ToolMessage(
                        content=result,
                        tool_call_id=str(tc["id"]),
                        name=name,
                    )
                )
        else:
            messages.append(response)
            break

    turn_messages = messages[idx_turn_start:]
    final_ai = next((m for m in reversed(turn_messages) if isinstance(m, AIMessage)), None)
    final_text = ((final_ai.content if final_ai else None) or "").strip()
    return final_text, turn_messages


# ---------------------------------------------------------------------------
# WG-05～07／WG-08～21：main
# ---------------------------------------------------------------------------


def main() -> None:
    # WG-05
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # WG-06～07
    if api_key:
        print(
            "已讀到 API 金鑰設定（內容不顯示）；進入對話（ReAct + 工具 + JSONL + 預算 + Skills + 附圖；"
            "輸入 quit / exit / q 結束；/image 路徑 附圖）。"
        )
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    print_wg01_to_03_banner()

    session_path = os.getenv("SESSION_JSONL_PATH", "session.jsonl")
    history, session_meta = load_session_jsonl(session_path)
    last_consolidated = int((session_meta or {}).get("last_consolidated", 0) or 0)
    if history:
        print(f"已從 {session_path!r} 載入 {len(history)} 則訊息（WG-16）。")

    loader = SkillsLoader(PROJECT_ROOT, PROJECT_ROOT / "builtin_skills")
    system_text = build_system_prompt(loader)
    system_message = SystemMessage(content=system_text)

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0.2)
    llm_tools = llm.bind_tools(TOOLS)
    consolidation_llm = ChatOpenAI(model=CHAT_MODEL, temperature=0.2)

    while True:
        user_text = input("\n你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        text, image_rel = parse_user_input(user_text)
        if not text and not image_rel:
            continue

        human_message = build_human_message_for_current_turn(text, image_rel)
        model_name = VISION_MODEL if image_rel else CHAT_MODEL
        if model_name != getattr(llm_tools, "model_name", CHAT_MODEL):
            llm_turn = ChatOpenAI(model=model_name, temperature=0.2)
            llm_tools_turn = llm_turn.bind_tools(TOOLS)
        else:
            llm_tools_turn = llm_tools

        system_text = build_system_prompt(loader)
        system_message = SystemMessage(content=system_text)

        last_consolidated = maybe_consolidate_memory(
            consolidation_llm,
            history,
            last_consolidated,
            system_text,
            human_message,
        )

        past = pick_past_for_turn(history, last_consolidated, system_text, human_message)
        context_messages = messages_for_model(system_message, past, human_message)
        idx_turn_start = 1 + len(past)

        print("\n助手：", end="", flush=True)
        _reply, turn_messages = run_react_turn(
            llm_tools_turn,
            context_messages,
            idx_turn_start,
        )
        print()

        history.extend(turn_messages)
        session_meta = save_session_jsonl(
            session_path, history, session_meta, last_consolidated
        )
        print(f"（已寫入 {session_path!r}，共 {len(history)} 則；last_consolidated={last_consolidated}）")


# WG-07：精簡進入點
if __name__ == "__main__":
    main()
