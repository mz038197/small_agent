"""
Wiki 挑戰題合併實作（challenges-wiki-guided.md WG-04～WG-20）：
ReAct 每輪以 `stream` 串流印出、JSONL 持久化、字元預算裁切、長期記憶整併、送模前 transcript 管線（WG-17）、
workspace 檔案／exec 工具（WG-19）、SkillsLoader 與 prepare_call／cast（WG-20）。
無 OPENAI_API_KEY 時早退不呼叫 API（WG-05～07）。
"""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from collections.abc import Callable
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
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# --- 專案根路徑（WG-19/20：workspace、skills / builtin_skills）---
ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT

# --- memory/ 與長度、重試（WG-18 長期記憶）---
_MEMORY_DIR = ROOT / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"
MEMORY_MAX_CHARS = 6000
CONSOLIDATION_MAX_RETRIES = 3
CONSOLIDATION_TEMPERATURE = 0.1

# --- WG-17：送模用 OpenAI dict transcript 管線（環境變數可調）---
COMPACTABLE_TOOL_NAMES = frozenset(
    {"read_file", "exec", "grep", "glob", "web_search", "web_fetch", "list_dir"}
)


def _env_int(name: str, default: int) -> int:
    try:
        return max(0, int(os.getenv(name, str(default))))
    except ValueError:
        return default


MODEL_TRANSCRIPT_MAX_CHARS = _env_int("MODEL_TRANSCRIPT_MAX_CHARS", 120_000)
MODEL_MAX_TOOL_RESULT_CHARS = _env_int("MODEL_MAX_TOOL_RESULT_CHARS", 8000)
MODEL_KEEP_RECENT_TOOLS = _env_int("MODEL_KEEP_RECENT_TOOLS", 8)


def _token_budget() -> int:
    raw = os.getenv("TOKEN_BUDGET", "8000")
    try:
        return max(1, int(raw))
    except ValueError:
        return 8000


# --- WG-20：資料結構與 frontmatter ---


@dataclass
class SkillEntry:
    name: str
    path: Path
    source: str
    description: str
    always: bool
    body: str


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """簡化 frontmatter：--- ... ---；無則回傳 ({}, 全文)。"""
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    end: int | None = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text

    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip()

    body = "\n".join(lines[end + 1 :]).strip()
    return meta, body


class SkillsLoader:
    """掃描 workspace/skills 與 builtin_skills；同名時 workspace 優先。"""

    def __init__(self, workspace: Path, builtin_skills_dir: Path) -> None:
        self.workspace_skills = workspace / "skills"
        self.builtin_skills = builtin_skills_dir

    def _entries_from_dir(
        self, root: Path, source: str, skip: set[str]
    ) -> list[SkillEntry]:
        if not root.exists():
            return []

        entries: list[SkillEntry] = []
        for skill_dir in sorted(root.iterdir(), key=lambda p: p.name):
            if not skill_dir.is_dir():
                continue
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
            name = skill_dir.name
            if name in skip:
                continue

            text = skill_file.read_text(encoding="utf-8")
            meta, body = split_frontmatter(text)
            description = meta.get("description") or name
            always = meta.get("always", "false").lower() == "true"
            entries.append(
                SkillEntry(
                    name=name,
                    path=skill_file.resolve(),
                    source=source,
                    description=description,
                    always=always,
                    body=body,
                )
            )
        return entries

    def list_skills(self) -> list[SkillEntry]:
        workspace_entries = self._entries_from_dir(
            self.workspace_skills, "workspace", set()
        )
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
    """僅非 always 的 skill 各一行摘要（名稱、description、路徑）。"""
    summarized = [e for e in entries if not e.always]
    if not summarized:
        return ""
    lines = [
        f"- **{e.name}** — {e.description} `{e.path}`"
        for e in summarized
    ]
    return "\n".join(lines)


def build_classroom_base_prompt() -> str:
    """WG-12 基底：課堂規則與顯示名（工具約束可另段組入 compose_system_string 或依 tool 描述）。"""
    system_text = (
        "你是課堂程式助教。請使用繁體中文。"
    )
    nick = os.getenv("ASSISTANT_DISPLAY_NAME") or "法鬥超人"
    if isinstance(nick, str) and not nick.strip():
        nick = "法鬥超人"

    return f"{system_text}\n\n【本場次顯示名稱】{nick}"


def _ensure_memory_dir() -> None:
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_memory_files() -> None:
    _ensure_memory_dir()
    _MEMORY_FILE.touch(exist_ok=True)
    _HISTORY_FILE.touch(exist_ok=True)


def read_long_term() -> str:
    if not _MEMORY_FILE.exists():
        return ""
    return _MEMORY_FILE.read_text(encoding="utf-8")


def write_long_term(content: str) -> None:
    _ensure_memory_files()
    _MEMORY_FILE.write_text(content, encoding="utf-8")


def append_history(entry: str, *, failed: bool = False) -> None:
    _ensure_memory_files()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    one_line = re.sub(r"\s+", " ", entry.strip())
    if failed:
        raw = one_line[:500] if len(one_line) > 500 else one_line
        line = f"[{ts}] [CONSOLIDATION-FAILED] raw:{raw}\n"
    else:
        line = f"[{ts}] {one_line}\n"
    with _HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(line)


def memory_block_for_system() -> str:
    """WG-18：有內文才加 ## Long-term Memory；超長由尾端截斷。"""
    body = read_long_term().strip()
    if not body:
        return ""
    if len(body) > MEMORY_MAX_CHARS:
        body = body[-MEMORY_MAX_CHARS:]
    return f"## Long-term Memory\n\n{body}"


def compose_system_string(loader: SkillsLoader) -> str:
    """
    送主模型／成本估算用完整 system 字串：
    課堂基底 → 長期記憶（若有）→ Active Skills（always 正文）→ Skills 摘要與 read_file 規則（若有）。
    """
    parts: list[str] = [build_classroom_base_prompt()]

    mem = memory_block_for_system()
    if mem:
        parts.append(mem)

    entries = loader.list_skills()
    active = [e for e in entries if e.always]
    if active:
        body = "\n\n---\n\n".join(
            f"### Skill: {e.name}\n\n{e.body}" for e in active
        )
        parts.append(f"# Active Skills\n\n{body}")

    summary = build_skills_summary(entries)
    if summary:
        parts.append(
            "# Skills\n\n"
            """下列技能可擴充你的能力。若要使用某技能，請用 read_file 讀取清單中該技能路徑下的 SKILL.md。
若該技能需額外套件或環境，請先依 SKILL.md 或專案說明安裝相依項目後再操作。\n\n"""
            f"{summary}"
        )
    return "\n\n---\n\n".join(parts)


# --- WG-19：workspace 檔案工具 + exec；WG-20：JSON Schema 子集 + cast／validate／prepare_call ---


def resolve_workspace_path(rel: str) -> Path:
    """相對路徑解析到 WORKSPACE 下；禁止跳出根目錄。"""
    raw = (rel or ".").strip() or "."
    target = (WORKSPACE / raw).resolve()
    try:
        target.relative_to(WORKSPACE.resolve())
    except ValueError as e:
        raise PermissionError(f"path is outside workspace: {rel}") from e
    return target


def _read_file_impl(params: dict[str, Any]) -> str:
    path = str(params.get("path", ""))
    offset = int(params.get("offset", 1))
    limit = int(params.get("limit", 200))
    try:
        target = resolve_workspace_path(path)
        if not target.is_file():
            return f"Error: not a file: {path}"
        lines = target.read_text(encoding="utf-8").splitlines()
        start = max(offset - 1, 0)
        end = min(start + limit, len(lines))
        return "\n".join(f"{i + 1}| {line}" for i, line in enumerate(lines[start:end], start=start))
    except Exception as e:
        return f"Error: {e}"


def _write_file_impl(params: dict[str, Any]) -> str:
    path = str(params.get("path", ""))
    content = str(params.get("content", ""))
    try:
        target = resolve_workspace_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error: {e}"


def _edit_file_impl(params: dict[str, Any]) -> str:
    path = str(params.get("path", ""))
    old_text = str(params.get("old_text", ""))
    new_text = str(params.get("new_text", ""))
    replace_all = bool(params.get("replace_all", False))
    try:
        target = resolve_workspace_path(path)
        text = target.read_text(encoding="utf-8")
        count = text.count(old_text)
        if count == 0:
            return "Error: old_text not found"
        if count > 1 and not replace_all:
            return "Error: old_text appears multiple times; set replace_all=true or add context"
        new_body = text.replace(old_text, new_text, -1 if replace_all else 1)
        target.write_text(new_body, encoding="utf-8")
        return f"edited {path}"
    except Exception as e:
        return f"Error: {e}"


def _list_dir_impl(params: dict[str, Any]) -> str:
    path = str(params.get("path", "."))
    recursive = bool(params.get("recursive", False))
    max_entries = int(params.get("max_entries", 200))
    try:
        root = resolve_workspace_path(path)
        if not root.is_dir():
            return f"Error: not a directory: {path}"
        iterator = root.rglob("*") if recursive else root.iterdir()
        entries = [str(p.relative_to(WORKSPACE.resolve())) for p in iterator][:max_entries]
        return "\n".join(entries) if entries else "(empty)"
    except Exception as e:
        return f"Error: {e}"


def _exec_impl(params: dict[str, Any]) -> str:
    command = str(params.get("command", ""))
    timeout = int(params.get("timeout", 30))
    blocked = ("rm -rf", "del /f", "rmdir /s", "format", "shutdown")
    lowered = command.lower()
    if any(b in lowered for b in blocked):
        return "Error: blocked dangerous command"
    try:
        child_env = os.environ.copy()
        # Windows 子程序常見：主控台 UTF-8 與 Python 預設編碼不一致，PIPE 解碼失敗或變空。
        child_env.setdefault("PYTHONUTF8", "1")
        child_env.setdefault("PYTHONIOENCODING", "utf-8")

        run_kw: dict[str, Any] = {
            "cwd": str(WORKSPACE.resolve()),
            "shell": True,
            "capture_output": True,
            "text": True,
            "encoding": "utf-8",
            "errors": "replace",
            "timeout": timeout,
            "env": child_env,
        }

        if os.name == "nt":
            # 隱藏子程序控制台視窗；仍透過 PIPE 擷取 stdout/stderr。
            run_kw["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        result = subprocess.run(command, **run_kw)
        raw_out = (result.stdout or "") + (result.stderr or "")
        out = raw_out.strip()
        cap = 4000
        if len(out) > cap:
            out = out[:cap] + "\n\n[truncated]"
        if not out:
            out = "(no stdout or stderr; command finished with no captured output)"
        return f"exit_code={result.returncode}\n{out}"
    except Exception as e:
        return f"Error: {e}"


def _add_two_impl(params: dict[str, Any]) -> str:
    a = int(params["a"])
    b = int(params["b"])
    return str(a + b)


def _cast_scalar(value: Any, typ: str) -> Any:
    if typ == "string":
        if value is None:
            return ""
        return str(value)
    if typ == "integer":
        if isinstance(value, bool):
            raise ValueError("boolean is not integer")
        if isinstance(value, int) and not isinstance(value, bool):
            return int(value)
        if isinstance(value, float) and value.is_integer():
            return int(value)
        s = str(value).strip()
        return int(s)
    if typ == "number":
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return float(value)
        return float(str(value).strip())
    if typ == "boolean":
        if isinstance(value, bool):
            return value
        s = str(value).strip().lower()
        if s in ("true", "1", "yes"):
            return True
        if s in ("false", "0", "no"):
            return False
        raise ValueError(f"cannot cast to boolean: {value!r}")
    return value


def cast_params(params: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    """WG-20：依簡化 JSON Schema 將字串等寬鬆輸入 cast 成 Python 型別。"""
    props = (schema.get("properties") or {}) if isinstance(schema, dict) else {}
    out: dict[str, Any] = dict(params)
    for key, spec in props.items():
        if key not in out:
            continue
        if not isinstance(spec, dict):
            continue
        typ = spec.get("type", "string")
        try:
            out[key] = _cast_scalar(out[key], typ)
        except (ValueError, TypeError):
            # 無法轉換時保留原值，交給 validate 報錯（與教案一致）
            pass
    return out


def validate_params(params: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """WG-20：檢查 required 與型別；額外鍵：拒絕未定義欄位。"""
    errs: list[str] = []
    if not isinstance(schema, dict):
        return ["invalid tool schema"]
    props = schema.get("properties") or {}
    required = list(schema.get("required") or [])
    for key in required:
        if key not in params:
            errs.append(f"missing required field: {key}")
    for key in params:
        if key not in props:
            errs.append(f"unexpected field: {key}")
    for key, spec in props.items():
        if key not in params:
            continue
        if not isinstance(spec, dict):
            continue
        typ = spec.get("type", "string")
        val = params[key]
        if typ == "string" and not isinstance(val, str):
            errs.append(f"{key} must be string")
        elif typ == "integer" and not isinstance(val, int):
            errs.append(f"{key} must be integer")
        elif typ == "number" and not isinstance(val, (int, float)):
            errs.append(f"{key} must be number")
        elif typ == "boolean" and not isinstance(val, bool):
            errs.append(f"{key} must be boolean")
    return errs


@dataclass
class LessonToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    read_only: bool
    execute: Callable[[dict[str, Any]], str]


class LessonToolRegistry:
    """WG-19／20：註冊、prepare_call（cast→validate）、execute。"""

    def __init__(self) -> None:
        self._tools: dict[str, LessonToolSpec] = {}

    def register(self, spec: LessonToolSpec) -> None:
        self._tools[spec.name] = spec

    def get(self, name: str) -> LessonToolSpec | None:
        return self._tools.get(name)

    def list_tool_names(self) -> list[str]:
        return sorted(self._tools)

    def prepare_call(
        self, name: str, params: Any
    ) -> tuple[LessonToolSpec | None, dict[str, Any], str | None]:
        if not isinstance(params, dict):
            return None, {}, "params must be a JSON object"
        tool = self.get(name)
        if tool is None:
            return None, {}, f"unknown tool: {name}"
        casted = cast_params(params, tool.parameters)
        errs = validate_params(casted, tool.parameters)
        if errs:
            return tool, casted, "; ".join(errs)
        return tool, casted, None

    def run_tool(self, name: str, raw: dict[str, Any]) -> str:
        tool, casted, err = self.prepare_call(name, raw)
        if err:
            return f"Error: {err}"
        assert tool is not None
        try:
            return tool.execute(casted)
        except Exception as e:
            return f"Error: {e}"


_LESSON_REGISTRY: LessonToolRegistry | None = None


def get_lesson_registry() -> LessonToolRegistry:
    global _LESSON_REGISTRY
    if _LESSON_REGISTRY is None:
        _LESSON_REGISTRY = build_default_lesson_registry()
    return _LESSON_REGISTRY


def build_default_lesson_registry() -> LessonToolRegistry:
    reg = LessonToolRegistry()
    reg.register(
        LessonToolSpec(
            name="add_two",
            description="兩個整數相加並回傳和。課堂示範用。",
            parameters={
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"},
                },
                "required": ["a", "b"],
            },
            read_only=True,
            execute=_add_two_impl,
        )
    )
    reg.register(
        LessonToolSpec(
            name="read_file",
            description="讀 UTF-8 文字檔並回傳含行號片段（workspace 內相對路徑）。",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "offset": {"type": "integer"},
                    "limit": {"type": "integer"},
                },
                "required": ["path"],
            },
            read_only=True,
            execute=_read_file_impl,
        )
    )
    reg.register(
        LessonToolSpec(
            name="write_file",
            description="寫入 UTF-8 文字檔（整檔覆寫）；必要時建立父資料夾。",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
            read_only=False,
            execute=_write_file_impl,
        )
    )
    reg.register(
        LessonToolSpec(
            name="edit_file",
            description="在既有檔案以 old_text 替換為 new_text；多次命中需 replace_all。",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_text": {"type": "string"},
                    "new_text": {"type": "string"},
                    "replace_all": {"type": "boolean"},
                },
                "required": ["path", "old_text", "new_text"],
            },
            read_only=False,
            execute=_edit_file_impl,
        )
    )
    reg.register(
        LessonToolSpec(
            name="list_dir",
            description="列出 workspace 內目錄內容（相對路徑）。",
            parameters={
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "recursive": {"type": "boolean"},
                    "max_entries": {"type": "integer"},
                },
                "required": [],
            },
            read_only=True,
            execute=_list_dir_impl,
        )
    )
    reg.register(
        LessonToolSpec(
            name="exec",
            description="在 workspace 目錄下執行 shell 指令（有安全阻擋與逾時）。",
            parameters={
                "type": "object",
                "properties": {
                    "command": {"type": "string"},
                    "timeout": {"type": "integer"},
                },
                "required": ["command"],
            },
            read_only=False,
            execute=_exec_impl,
        )
    )
    return reg


# --- WG-17：OpenAI 風格 dict transcript 管線 ---


def _assistant_has_tool_call_id(msg: dict[str, Any], tool_call_id: str) -> bool:
    for tc in msg.get("tool_calls") or []:
        if isinstance(tc, dict) and str(tc.get("id")) == str(tool_call_id):
            return True
    return False


def _drop_orphan_tools(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for i, m in enumerate(messages):
        if m.get("role") == "tool":
            tid = m.get("tool_call_id")
            ok = any(
                _assistant_has_tool_call_id(messages[j], str(tid))
                for j in range(i)
                if messages[j].get("role") == "assistant"
            )
            if not ok:
                continue
        out.append(m)
    return out


def _backfill_missing_tools(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """在缺 tool 回覆處插入合成 tool 訊息。"""
    out = list(messages)
    i = 0
    while i < len(out):
        m = out[i]
        if m.get("role") != "assistant" or not m.get("tool_calls"):
            i += 1
            continue
        ids = [str(tc.get("id")) for tc in m["tool_calls"] if isinstance(tc, dict)]
        j = i + 1
        found: set[str] = set()
        while j < len(out) and out[j].get("role") == "tool":
            found.add(str(out[j].get("tool_call_id")))
            j += 1
        insert_at = j
        for tid in ids:
            if tid in found:
                continue
            fn = next(
                (
                    tc.get("function", {}).get("name", "unknown")
                    for tc in m["tool_calls"]
                    if isinstance(tc, dict) and str(tc.get("id")) == tid
                ),
                "unknown",
            )
            synthetic = {
                "role": "tool",
                "tool_call_id": tid,
                "name": fn,
                "content": "[Tool result unavailable — call was interrupted or lost]",
            }
            out.insert(insert_at, synthetic)
            insert_at += 1
        i += 1
    return out


def _truncate_tool_contents(
    messages: list[dict[str, Any]], max_tool_chars: int
) -> None:
    suffix = "\n\n[truncated]"
    for m in messages:
        if m.get("role") != "tool":
            continue
        c = str(m.get("content", ""))
        if len(c) > max_tool_chars:
            m["content"] = c[: max_tool_chars - len(suffix)] + suffix


def _microcompact_tools(messages: list[dict[str, Any]], keep_recent: int) -> None:
    indices = [
        i
        for i, m in enumerate(messages)
        if m.get("role") == "tool"
        and str(m.get("name", "")) in COMPACTABLE_TOOL_NAMES
    ]
    if len(indices) <= keep_recent:
        return
    protected = set(indices[-keep_recent:])
    for i in indices:
        if i in protected:
            continue
        m = messages[i]
        c = str(m.get("content", ""))
        if len(c) >= 500:
            nm = str(m.get("name", "tool"))
            messages[i] = dict(m)
            messages[i]["content"] = f"[{nm} result omitted from context]"


def _msg_dict_cost(m: dict[str, Any]) -> int:
    return len(str(m.get("content", "")))


def _total_dict_cost(messages: list[dict[str, Any]]) -> int:
    return sum(_msg_dict_cost(m) for m in messages)


def _snip_transcript(messages: list[dict[str, Any]], max_chars: int) -> None:
    while _total_dict_cost(messages) > max_chars:
        if len(messages) <= 1:
            break
        first_role = messages[0].get("role")
        if first_role == "system" and len(messages) == 2 and messages[1].get("role") == "user":
            break
        del_idx = 1 if first_role == "system" else 0
        if del_idx >= len(messages):
            break
        if del_idx == len(messages) - 1 and messages[del_idx].get("role") == "user":
            break
        del messages[del_idx]


def _ensure_system_user_guardrails(messages: list[dict[str, Any]]) -> None:
    if not messages:
        return
    if messages[-1].get("role") != "user":
        messages.append({"role": "user", "content": "(conversation continued)"})
    sys_idxs = [i for i, m in enumerate(messages) if m.get("role") == "system"]
    if sys_idxs and sys_idxs[0] != 0:
        si = sys_idxs[0]
        s = messages.pop(si)
        messages.insert(0, s)


def build_messages_for_model(
    messages: list[dict[str, Any]],
    *,
    max_chars: int,
    max_tool_chars: int,
    keep_recent_tools: int,
) -> list[dict[str, Any]]:
    """WG-17：孤兒清理 → 補洞 → tool 截斷 → microcompact → 全對話字元預算。"""
    out: list[dict[str, Any]] = []
    for m in messages:
        row = dict(m)
        if row.get("tool_calls"):
            row["tool_calls"] = copy.deepcopy(row["tool_calls"])
        out.append(row)

    out = _drop_orphan_tools(out)
    out = _backfill_missing_tools(out)
    _truncate_tool_contents(out, max_tool_chars)
    _microcompact_tools(out, keep_recent_tools)
    _snip_transcript(out, max_chars)
    _ensure_system_user_guardrails(out)
    return out


def _lc_tool_calls_to_openai(tool_calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    oai: list[dict[str, Any]] = []
    for tc in tool_calls:
        if not isinstance(tc, dict):
            continue
        name = str(tc.get("name", ""))
        args = tc.get("args") or {}
        tid = str(tc.get("id", ""))
        oai.append(
            {
                "id": tid,
                "type": "function",
                "function": {
                    "name": name,
                    "arguments": json.dumps(args, ensure_ascii=False),
                },
            }
        )
    return oai


def lc_messages_to_openai_dicts(messages: list[BaseMessage]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for m in messages:
        if isinstance(m, SystemMessage):
            out.append({"role": "system", "content": str(m.content)})
        elif isinstance(m, HumanMessage):
            out.append({"role": "user", "content": str(m.content)})
        elif isinstance(m, AIMessage):
            d: dict[str, Any] = {
                "role": "assistant",
                "content": str(m.content or ""),
            }
            tc = getattr(m, "tool_calls", None) or []
            if tc:
                d["tool_calls"] = _lc_tool_calls_to_openai(
                    [t if isinstance(t, dict) else dict(t) for t in tc]
                )
            out.append(d)
        elif isinstance(m, ToolMessage):
            name = getattr(m, "name", None) or ""
            out.append(
                {
                    "role": "tool",
                    "tool_call_id": m.tool_call_id,
                    "name": str(name) if name else "unknown",
                    "content": str(m.content),
                }
            )
    return out


def _openai_tool_calls_to_lc(tool_calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lc: list[dict[str, Any]] = []
    for tc in tool_calls:
        if not isinstance(tc, dict):
            continue
        fn = tc.get("function") or {}
        if isinstance(fn, dict):
            name = str(fn.get("name", ""))
            raw_args = fn.get("arguments", "{}")
            if isinstance(raw_args, str):
                try:
                    args = json.loads(raw_args) if raw_args.strip() else {}
                except json.JSONDecodeError:
                    args = {}
            else:
                args = dict(raw_args) if isinstance(raw_args, dict) else {}
        else:
            name = ""
            args = {}
        lc.append({"name": name, "args": args, "id": str(tc.get("id", ""))})
    return lc


def openai_dicts_to_lc_messages(rows: list[dict[str, Any]]) -> list[BaseMessage]:
    out: list[BaseMessage] = []
    for m in rows:
        role = m.get("role")
        if role == "system":
            out.append(SystemMessage(content=str(m.get("content", ""))))
        elif role == "user":
            out.append(HumanMessage(content=str(m.get("content", ""))))
        elif role == "assistant":
            tc = m.get("tool_calls")
            if tc:
                out.append(
                    AIMessage(
                        content=str(m.get("content", "")),
                        tool_calls=_openai_tool_calls_to_lc(
                            tc if isinstance(tc, list) else []
                        ),
                    )
                )
            else:
                out.append(AIMessage(content=str(m.get("content", ""))))
        elif role == "tool":
            out.append(
                ToolMessage(
                    content=str(m.get("content", "")),
                    tool_call_id=str(m.get("tool_call_id", "")),
                    name=str(m.get("name", "") or "unknown"),
                )
            )
    return out


# --- WG-13：LangChain bind_tools 介面（實際執行經 LessonToolRegistry）---


@tool
def add_two(a: int, b: int) -> int:
    """兩個整數相加並回傳和。課堂示範用，請在需要相加時呼叫此工具。"""
    return int(get_lesson_registry().run_tool("add_two", {"a": a, "b": b}))


@tool
def read_file(path: str, offset: int = 1, limit: int = 200) -> str:
    """讀取 workspace 內 UTF-8 文字檔，回傳含行號內容。"""
    return get_lesson_registry().run_tool(
        "read_file", {"path": path, "offset": offset, "limit": limit}
    )


@tool
def write_file(path: str, content: str) -> str:
    """整檔覆寫寫入 UTF-8 文字檔。"""
    return get_lesson_registry().run_tool("write_file", {"path": path, "content": content})


@tool
def edit_file(path: str, old_text: str, new_text: str, replace_all: bool = False) -> str:
    """局部替換檔案內容。"""
    return get_lesson_registry().run_tool(
        "edit_file",
        {
            "path": path,
            "old_text": old_text,
            "new_text": new_text,
            "replace_all": replace_all,
        },
    )


@tool
def list_dir(path: str = ".", recursive: bool = False, max_entries: int = 200) -> str:
    """列出目錄內容（相對於專案根）。"""
    return get_lesson_registry().run_tool(
        "list_dir",
        {"path": path, "recursive": recursive, "max_entries": max_entries},
    )


@tool("exec")
def exec_command(command: str, timeout: int = 30) -> str:
    """在 workspace 下執行 shell 指令（有安全阻擋）。"""
    return get_lesson_registry().run_tool(
        "exec", {"command": command, "timeout": timeout}
    )


def all_lesson_tools() -> list[Any]:
    return [add_two, read_file, write_file, edit_file, list_dir, exec_command]


TOOLS = all_lesson_tools()


def _serialize_tool_calls(tc: Any) -> list[dict[str, Any]]:
    """寫入 JSONL 前轉成可 json.dumps 的結構。"""
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


def estimate_message_tokens(message: BaseMessage) -> int:
    """WG-16：字元長度近似 token；AIMessage 含 tool_calls 時加權。"""
    c = message.content
    n = len(c) if isinstance(c, str) else 0
    if isinstance(message, AIMessage):
        tc = getattr(message, "tool_calls", None) or []
        if tc:
            n += len(json.dumps(_serialize_tool_calls(tc), ensure_ascii=False))
    return n


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


def request_cost_chars(
    system_text: str, past: list[BaseMessage], human_message: HumanMessage
) -> int:
    """與 memory_react_agent.request_cost_chars 同語意（含 ToolMessage 之 content）。"""
    return (
        len(system_text)
        + sum(estimate_message_tokens(m) for m in past)
        + estimate_message_tokens(human_message)
    )


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

            if not isinstance(obj, dict):
                continue

            role = obj.get("role")
            if role == "user":
                messages.append(HumanMessage(content=str(obj.get("content", ""))))
            elif role == "assistant":
                content = str(obj.get("content", ""))
                tc = obj.get("tool_calls")
                if tc:
                    messages.append(
                        AIMessage(content=content, tool_calls=_serialize_tool_calls(tc))
                    )
                else:
                    messages.append(AIMessage(content=content))
            elif role == "tool":
                tid = obj.get("tool_call_id") or ""
                nm = str(obj.get("name", "") or "").strip() or None
                messages.append(
                    ToolMessage(
                        content=str(obj.get("content", "")),
                        tool_call_id=str(tid),
                        name=nm,
                    )
                )

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
        ts = datetime.now().isoformat()
        if isinstance(m, HumanMessage):
            row = {"role": "user", "content": m.content, "timestamp": ts}
        elif isinstance(m, AIMessage):
            row = {"role": "assistant", "content": m.content, "timestamp": ts}
            tc = getattr(m, "tool_calls", None)
            if tc:
                row["tool_calls"] = _serialize_tool_calls(tc)
        elif isinstance(m, ToolMessage):
            row = {
                "role": "tool",
                "content": m.content,
                "tool_call_id": m.tool_call_id,
                "timestamp": ts,
            }
            tname = getattr(m, "name", None)
            if tname:
                row["name"] = tname
        else:
            continue
        lines.append(json.dumps(row, ensure_ascii=False))

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")

    return meta


def _flatten_ai_chunk_text(content: Any) -> str:
    """從單一 AIMessageChunk.content 抽出可當成純文字串流處理的字串（供略過開頭空白）。"""
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
    """將單一 chunk 的可讀文字印到 stdout（WG-10：end=''、flush）。"""
    if not content:
        return
    if isinstance(content, str):
        print(content, end="", flush=True)
        return
    if isinstance(content, list):
        for block in content:
            if isinstance(block, str):
                print(block, end="", flush=True)
            elif isinstance(block, dict):
                if block.get("type") == "text":
                    print(block.get("text", ""), end="", flush=True)


class _LeadingStripStreamPrinter:
    """略過模型在訊息開頭常送的連續換行，避免「助手：」下方空白過多。"""

    __slots__ = ("_pending",)

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


def run_react_turn(
    llm_tools: ChatOpenAI,
    system_text: str,
    history: list[BaseMessage],
    user_text: str,
    *,
    stream_stdout: bool = True,
) -> tuple[str, list[BaseMessage]]:
    """WG-13：ReAct 多段呼叫；最後一則與含 tool_calls 之中間步皆用 stream 累積為 AIMessage。"""
    human_message = HumanMessage(content=user_text)
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *history,
        human_message,
    ]
    idx_turn_start = 1 + len(history)

    while True:
        dict_rows = lc_messages_to_openai_dicts(messages)
        pruned = build_messages_for_model(
            dict_rows,
            max_chars=MODEL_TRANSCRIPT_MAX_CHARS,
            max_tool_chars=MODEL_MAX_TOOL_RESULT_CHARS,
            keep_recent_tools=MODEL_KEEP_RECENT_TOOLS,
        )
        messages_for_invoke = openai_dicts_to_lc_messages(pruned)
        acc: AIMessageChunk | None = None
        stream_out = _LeadingStripStreamPrinter() if stream_stdout else None
        for chunk in llm_tools.stream(messages_for_invoke):
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
            reg = get_lesson_registry()
            for tc in response.tool_calls:
                name = str(tc["name"])
                raw_args = dict(tc.get("args") or {})
                result = reg.run_tool(name, raw_args)
                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=str(tc["id"]),
                        name=name,
                    )
                )
        else:
            messages.append(response)
            break

    turn_messages = messages[idx_turn_start:]
    final_ai = next(
        (m for m in reversed(turn_messages) if isinstance(m, AIMessage)),
        None,
    )
    final_text = ((final_ai.content if final_ai else None) or "").strip()
    return final_text, turn_messages


def _messages_to_chunk_text(msgs: list[BaseMessage]) -> str:
    lines: list[str] = []
    for m in msgs:
        if isinstance(m, HumanMessage):
            lines.append(f"user: {m.content}")
        elif isinstance(m, AIMessage):
            lines.append(f"assistant: {m.content}")
        elif isinstance(m, ToolMessage):
            lines.append(f"tool[{m.tool_call_id}]: {m.content}")
    return "\n".join(lines)


def _parse_consolidation_json(text: str) -> tuple[str, str] | None:
    text = text.strip()
    try:
        fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if fence:
            text = fence.group(1).strip()
        obj = json.loads(text)
        if not isinstance(obj, dict):
            return None
        he = obj.get("history_entry")
        mu = obj.get("memory_update")
        if not isinstance(he, str) or not isinstance(mu, str):
            return None
        return he, mu
    except (json.JSONDecodeError, TypeError):
        return None


def run_consolidation_llm(
    llm: ChatOpenAI, chunk_msgs: list[BaseMessage], current_memory: str
) -> tuple[str, str] | None:
    chunk_text = _messages_to_chunk_text(chunk_msgs)
    instruction = (
        "你是整併助手。請閱讀「現有長期記憶（markdown）」與「待整併對話片段」，"
        "僅輸出一個 JSON 物件（不要其他說明），兩個鍵：\n"
        '- "history_entry": 字串，單行可讀摘要（繁體中文）\n'
        '- "memory_update": 字串，將完整取代 MEMORY.md 的正文（markdown）\n'
    )
    user_body = f"{instruction}\n\n【現有 MEMORY】\n{current_memory}\n\n【待整併片段】\n{chunk_text}"
    msgs = [
        SystemMessage(
            content="你僅輸出合法 JSON 物件，鍵名必為 history_entry 與 memory_update。"
        ),
        HumanMessage(content=user_body),
    ]
    r = llm.invoke(msgs)
    raw = r.content if isinstance(r.content, str) else str(r.content)
    return _parse_consolidation_json(raw)


def consolidate_one_chunk(
    consolidation_llm: ChatOpenAI,
    history: list[BaseMessage],
    last_consolidated: int,
    boundary_idx: int,
) -> int:
    """整併 history[last_consolidated:boundary_idx]；回傳 boundary_idx。"""
    chunk = history[last_consolidated:boundary_idx]
    if not chunk:
        return boundary_idx

    current_mem = read_long_term()
    attempts = (
        1 if CONSOLIDATION_MAX_RETRIES == 0 else (1 + CONSOLIDATION_MAX_RETRIES)
    )
    for _ in range(attempts):
        parsed = run_consolidation_llm(consolidation_llm, chunk, current_mem)
        if parsed is not None:
            he, mu = parsed
            append_history(he, failed=False)
            write_long_term(mu)
            return boundary_idx

    fail_note = _messages_to_chunk_text(chunk)[:500]
    append_history(fail_note, failed=True)
    return boundary_idx


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    loader = SkillsLoader(ROOT, ROOT / "builtin_skills")
    session_path = os.getenv("SESSION_JSONL_PATH", str(ROOT / "session.jsonl"))

    if api_key:
        print(
            "已讀到 API 金鑰設定（內容不顯示）；進入對話（ReAct + 串流輸出 + JSONL、"
            "WG-16/17 預算與長期記憶、WG-18 Skills；輸入 quit / exit / q 結束）。"
        )
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    loaded, session_meta = load_session_jsonl(session_path)
    history: list[BaseMessage] = list(loaded)
    last_consolidated = 0
    if session_meta is not None:
        try:
            last_consolidated = int(session_meta.get("last_consolidated", 0))
        except (TypeError, ValueError):
            last_consolidated = 0
    last_consolidated = max(0, min(last_consolidated, len(history)))

    token_budget = _token_budget()
    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.2)
    llm_tools = llm.bind_tools(TOOLS)
    consolidation_llm = ChatOpenAI(
        model="gpt-4o-mini", temperature=CONSOLIDATION_TEMPERATURE
    )

    while True:
        user_text = input("\n\n你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        human_message = HumanMessage(content=user_text)
        system_str = compose_system_string(loader)
        
        past0 = history[last_consolidated:]
        cost = request_cost_chars(system_str, past0, human_message)

        # WG-17：嚴格大於 TOKEN_BUDGET 才整併；送模前壓至 ≤ TOKEN_BUDGET//2
        if cost > token_budget:
            target = token_budget // 2
            while (
                request_cost_chars(
                    compose_system_string(loader),
                    history[last_consolidated:],
                    human_message,
                )
                > target
            ):
                sys_s = compose_system_string(loader)
                past_live = history[last_consolidated:]
                cost_now = request_cost_chars(sys_s, past_live, human_message)
                tokens_to_remove = max(1, cost_now - target)
                boundary = pick_consolidation_boundary(
                    history, last_consolidated, tokens_to_remove
                )
                if boundary is None:
                    break
                b_idx = boundary[0]
                consolidate_one_chunk(
                    consolidation_llm, history, last_consolidated, b_idx
                )
                last_consolidated = b_idx
                if session_meta is None:
                    session_meta = _default_metadata()
                session_meta["last_consolidated"] = last_consolidated
                session_meta = save_session_jsonl(
                    session_path, history, session_meta, last_consolidated
                )

        system_str = compose_system_string(loader)
        past = history[last_consolidated:]

        print("\n\n助手：", end="", flush=True)
        reply_text, turn_messages = run_react_turn(
            llm_tools, system_str, past, user_text
        )
        print()

        history.extend(turn_messages)
        if session_meta is None:
            session_meta = _default_metadata()
        session_meta["last_consolidated"] = last_consolidated
        session_meta = save_session_jsonl(
            session_path, history, session_meta, last_consolidated
        )


if __name__ == "__main__":
    main()
