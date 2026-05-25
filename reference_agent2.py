"""
Agent Workshop 標準程式（reference_agent2.py）— WG-12～20 合併示範。

對齊 `challenges-agent-workshop.md`（**WG-12～20**）；教練驗收與 Spec 以本檔為準。
學生實作請改專案根 **`main.py`**，勿直接修改本檔。

- WG-12：`build_system_prompt`、`SystemMessage` 與 `history` 分離（system 不進 JSONL）
- WG-13：抽出 `get_identity`（【解題方式】【依賴管理】）、`@tool`、`bind_tools`、ReAct 內層迴圈、`ToolMessage`
- WG-14：workspace 路徑解析、五支檔案／shell 工具 + `add_numbers`
- WG-15：每輪後 `save_session_jsonl`（先寫檔；啟動不讀舊檔）
- WG-16：啟動時 `load_session_jsonl`（略過壞行；關閉再開可接續）
- WG-17：`get_token_budget`、`estimate_message_tokens`、`pick_consolidation_boundary`；送模用 `past` 裁切
- WG-18：`messages_for_model`（孤兒 tool 清理、缺 tool 回覆補洞；送模副本不污染 JSONL）
- WG-19：`memory_block_for_system`、ReAct 前 consolidation 整併、`memory/MEMORY.md`（nanobot 四節結構）、`prompts/memory_merge.md`
- WG-20：`SkillsLoader`、`SKILLS_LOADER`、Active／Skills 併入 `build_system_prompt()`

預設對話檔：`session_wiki_wg.jsonl`（可用環境變數 `SESSION_JSONL_PATH` 覆寫）
"""

from __future__ import annotations

import json
import os
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
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


# ---------------------------------------------------------------------------
# WG-12：人設（system 與 history 分離；完整 build_system_prompt 見 WG-20）
# WG-13：自 build_system_prompt 抽出 get_identity（【解題方式】【依賴管理】）
# ---------------------------------------------------------------------------


def get_identity() -> str:
    """WG-13 自 build_system_prompt 抽出；含【解題方式】【依賴管理】。"""
    system_text = (
        "你是課堂程式助教，並請使用繁體中文。\n\n"
        "【解題方式】可重複驗證的任務，優先 write_file 寫成腳本，再 exec 執行"
        "（例如 uv run python 相對路徑）；避免只在對話中口算或貼無法重跑的一次性指令。\n\n"
        "【依賴管理】本專案用 uv 管理套件；新增 Python 依賴請在專案根 exec "
        "uv add <套件名>，不要用 pip install。"
    )
    nick = "法鬥超人"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}"


# ---------------------------------------------------------------------------
# WG-13：工具與 ReAct（`add_numbers`、`bind_tools`、串流、ToolMessage）
# ---------------------------------------------------------------------------


@tool
def add_numbers(a: float, b: float) -> float:
    """兩個數字相加並回傳和。純算術必須呼叫此工具，不可心算後直接回答。"""
    return float(a) + float(b)


def _stream_model_response(
    llm_tools: ChatOpenAI,
    messages: list[BaseMessage],
) -> AIMessage:
    """串流累積為 AIMessage；僅印模型文字，工具執行由呼叫端處理。"""
    acc: AIMessageChunk | None = None
    for chunk in llm_tools.stream(messages):
        acc = chunk if acc is None else acc + chunk
        content = chunk.content
        if isinstance(content, str) and content:
            print(content, end="", flush=True)
    if acc is None:
        raise RuntimeError("模型串流未回傳任何 chunk")
    return message_chunk_to_message(acc)


def _run_bound_tool(name: str, args: dict[str, Any]) -> str:
    tool_obj = _TOOL_BY_NAME.get(name)
    if tool_obj is None:
        return f"Error: unknown tool {name!r}"
    try:
        out = tool_obj.invoke(dict(args or {}))
        return str(out)
    except Exception as e:
        return f"Error running tool {name}: {e}"


def run_react_turn(
    llm_tools: ChatOpenAI,
    system_text: str,
    past: list[BaseMessage],
    user_text: str,
) -> tuple[str, list[BaseMessage]]:
    """單輪 ReAct：stream → tool_calls → ToolMessage 迴圈，直到純文字回覆。

    WG-17：`past` 為裁切後送模切片；完整 `history` 由 `main()` 另行累積。
    WG-18：每段 stream 前以 `messages_for_model` 修復 transcript。
    """
    human_message = HumanMessage(content=user_text)
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *past,
        human_message,
    ]
    idx_turn_start = 1 + len(past)

    while True:
        messages = messages_for_model(messages)
        response = _stream_model_response(llm_tools, messages)
        messages.append(response)
        print()

        if response.tool_calls:
            for tc in response.tool_calls:
                name = str(tc["name"])
                raw_args = dict(tc.get("args") or {})
                result = _run_bound_tool(name, raw_args)
                print(f"\n[工具 {name}]\n{result}\n", flush=True)
                messages.append(
                    ToolMessage(
                        content=result,
                        tool_call_id=str(tc["id"]),
                        name=name,
                    )
                )
        else:
            break

    turn_messages = messages[idx_turn_start:]
    final_text = response.content.strip()
    return final_text, turn_messages


# ---------------------------------------------------------------------------
# WG-14：workspace 檔案／shell `@tool`（追加至 WG-13 之 TOOLS）
# ---------------------------------------------------------------------------

WORKSPACE = Path.cwd().resolve()


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
    """在 workspace 目錄下執行 shell 指令（已阻擋常見危險片段）。"""
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


TOOLS = [
    add_numbers,
    read_file,
    write_file,
    edit_file,
    list_dir,
    exec_workspace,
]

_TOOL_BY_NAME: dict[str, Any] = {t.name: t for t in TOOLS}


# ---------------------------------------------------------------------------
# WG-15：JSONL 寫入（每輪 extend 後 save；第一行 metadata；不寫 SystemMessage）
# ---------------------------------------------------------------------------


def _default_metadata(created_at: str | None = None) -> dict[str, Any]:
    """建立第一行 metadata 物件（與 session.jsonl.example 欄位對齊）。"""
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


def _message_to_jsonl_line(m: BaseMessage) -> str | None:
    ts = datetime.now().isoformat()
    if isinstance(m, HumanMessage):
        row: dict[str, Any] = {"role": "user", "content": m.content, "timestamp": ts}
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
        return None
    return json.dumps(row, ensure_ascii=False)


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
        line = _message_to_jsonl_line(m)
        if line is not None:
            lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")

    return meta


# ---------------------------------------------------------------------------
# WG-16：JSONL 載入（啟動還原 history／session_meta；壞行略過）
# ---------------------------------------------------------------------------


def _row_to_message(obj: dict[str, Any]) -> BaseMessage | None:
    role = obj.get("role")
    if role == "user":
        return HumanMessage(content=str(obj.get("content", "")))
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


# ---------------------------------------------------------------------------
# WG-17：字元預算與送模裁切（history 全量保留，past 為送模切片）
# ---------------------------------------------------------------------------


def get_token_budget() -> int:
    raw = os.getenv("TOKEN_BUDGET", "100000")
    try:
        n = int(raw)
        return n if n > 0 else 100000
    except ValueError:
        return 100000


def estimate_message_tokens(message: BaseMessage) -> int:
    content = message.content
    return len(content) if isinstance(content, str) else 0


def message_cost(msgs: list[BaseMessage]) -> int:
    return sum(estimate_message_tokens(m) for m in msgs)


def pick_consolidation_boundary(
    messages: list[BaseMessage],
    last_consolidated: int,
    tokens_to_remove: int,
) -> tuple[int, int] | None:
    """自 last_consolidated 掃描，挑「使用者回合開頭」idx，使略過的權重足夠。"""
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
    system_text: str,
    past: list[BaseMessage],
    human_message: HumanMessage,
) -> int:
    """WG-17／WG-19 共用成本公式。"""
    return len(system_text) + message_cost([*past, human_message])


# ---------------------------------------------------------------------------
# WG-18：送模 transcript 修復（完整 history 與 messages_for_model 副本分離）
# ---------------------------------------------------------------------------


def _known_tool_call_ids(messages: list[BaseMessage], before_index: int) -> set[str]:
    ids: set[str] = set()
    for msg in messages[:before_index]:
        if not isinstance(msg, AIMessage):
            continue
        for tc in msg.tool_calls or []:
            if isinstance(tc, dict):
                tid = tc.get("id")
                if tid:
                    ids.add(str(tid))
    return ids


def messages_for_model(messages: list[BaseMessage]) -> list[BaseMessage]:
    """WG-18：自完整 transcript 產出送模副本（A 孤兒 tool、B 缺 tool 補洞）。

    回傳新 list，不就地修改輸入（避免污染將寫入 JSONL 的 history）。
    """
    out: list[BaseMessage] = list(messages)

    # A: drop orphan ToolMessage rows
    kept: list[BaseMessage] = []
    for msg in out:
        if isinstance(msg, ToolMessage):
            tid = str(msg.tool_call_id or "")
            if tid and tid in _known_tool_call_ids(kept, len(kept)):
                kept.append(msg)
        else:
            kept.append(msg)
    out = kept

    # B: backfill missing ToolMessage after AIMessage tool_calls
    unavailable_tool_text = "[Tool result unavailable — call was interrupted or lost]"
    i = 0
    while i < len(out):
        msg = out[i]
        if not isinstance(msg, AIMessage):
            i += 1
            continue
        tool_calls = msg.tool_calls or []
        if not tool_calls:
            i += 1
            continue

        j = i + 1
        responded: set[str] = set()
        while j < len(out) and isinstance(out[j], ToolMessage):
            responded.add(str(out[j].tool_call_id or ""))
            j += 1

        insert_at = j
        for tc in tool_calls:
            if not isinstance(tc, dict):
                continue
            tid = str(tc.get("id", "") or "")
            if not tid or tid in responded:
                continue
            name = str(tc.get("name", "") or "").strip() or None
            out.insert(
                insert_at,
                ToolMessage(
                    content=unavailable_tool_text,
                    tool_call_id=tid,
                    name=name,
                ),
            )
            insert_at += 1
        i += 1

    return out


# ---------------------------------------------------------------------------
# WG-19：長期記憶整併（ReAct 前；memory/MEMORY.md、memory/HISTORY.md）
# ---------------------------------------------------------------------------

REFERENCE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = REFERENCE_DIR / "memory"
MEMORY_PATH = MEMORY_DIR / "MEMORY.md"
HISTORY_PATH = MEMORY_DIR / "HISTORY.md"
MEMORY_TEMPLATE_PATH = REFERENCE_DIR / "templates" / "memory" / "MEMORY.md"
MEMORY_MERGE_PROMPT_PATH = REFERENCE_DIR / "prompts" / "memory_merge.md"
LONG_TERM_MEMORY_HEADING = "## Long-term Memory"
CONSOLIDATION_MAX_RETRIES = 3


def read_memory_md() -> str:
    if not MEMORY_PATH.is_file():
        return ""
    return MEMORY_PATH.read_text(encoding="utf-8").strip()


def load_memory_merge_prompt() -> str:
    return MEMORY_MERGE_PROMPT_PATH.read_text(encoding="utf-8")


def is_default_memory_template(content: str) -> bool:
    """True when MEMORY.md is still the bundled nanobot starter template."""
    if not content.strip():
        return True
    if not MEMORY_TEMPLATE_PATH.is_file():
        return False
    return content.strip() == MEMORY_TEMPLATE_PATH.read_text(encoding="utf-8").strip()


def memory_block_for_system() -> str:
    """有 MEMORY.md 內文且非預設模板時，回傳 ## Long-term Memory 區塊（全文讀入，不截斷）。"""
    body = read_memory_md()
    if not body or is_default_memory_template(body):
        return ""
    return f"{LONG_TERM_MEMORY_HEADING}\n\n{body}"


def append_history_log(line: str) -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    single = " ".join(line.split())
    with open(HISTORY_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {single}\n")


def write_memory_md(content: str) -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    MEMORY_PATH.write_text(content, encoding="utf-8")


def _message_plaintext(message: BaseMessage) -> str:
    if isinstance(message, HumanMessage):
        role = "user"
    elif isinstance(message, AIMessage):
        role = "assistant"
    elif isinstance(message, ToolMessage):
        role = "tool"
    else:
        role = "other"
    content = message.content if isinstance(message.content, str) else str(message.content)
    extra = ""
    if isinstance(message, AIMessage) and message.tool_calls:
        names = [
            str(tc.get("name", ""))
            for tc in message.tool_calls
            if isinstance(tc, dict)
        ]
        extra = f" [tool_calls: {', '.join(names)}]"
    if len(content) > 2000:
        content = content[:2000] + "…"
    return f"{role}{extra}: {content}"


def _chunk_to_text(chunk: list[BaseMessage]) -> str:
    return "\n".join(_message_plaintext(m) for m in chunk)


def _parse_consolidation_json(text: str) -> dict[str, str] | None:
    text = text.strip()
    try:
        obj = json.loads(text)
        if isinstance(obj, dict) and "history_entry" in obj and "memory_update" in obj:
            return {
                "history_entry": str(obj["history_entry"]),
                "memory_update": str(obj["memory_update"]),
            }
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            obj = json.loads(text[start : end + 1])
            if isinstance(obj, dict) and "history_entry" in obj and "memory_update" in obj:
                return {
                    "history_entry": str(obj["history_entry"]),
                    "memory_update": str(obj["memory_update"]),
                }
        except json.JSONDecodeError:
            pass
    return None


def _invoke_consolidation(
    consolidation_llm: ChatOpenAI,
    chunk_text: str,
    existing_memory: str,
) -> dict[str, str] | None:
    consolidation_system = load_memory_merge_prompt()
    user_prompt = (
        f"## CURRENT MEMORY\n{existing_memory or '（空）'}\n\n"
        f"## CONVERSATION CHUNK\n{chunk_text}\n\n"
        "僅回傳 JSON，不要其他文字。"
    )
    response = consolidation_llm.invoke(
        [
            SystemMessage(content=consolidation_system),
            HumanMessage(content=user_prompt),
        ]
    )
    content = response.content if isinstance(response.content, str) else str(response.content)
    return _parse_consolidation_json(content)


def _consolidate_pack(
    consolidation_llm: ChatOpenAI,
    chunk: list[BaseMessage],
    existing_memory: str,
) -> None:
    """Phase B：整包 chunk + 既有 MEMORY 一次 consolidation；寫 MEMORY／HISTORY。"""
    if not chunk:
        return

    chunk_text = _chunk_to_text(chunk)
    max_retries = CONSOLIDATION_MAX_RETRIES

    if max_retries <= 0:
        fail_note = " ".join(chunk_text.split())[:200]
        append_history_log(f"[CONSOLIDATION-FAILED] {fail_note}")
        return

    for _ in range(max_retries):
        parsed = _invoke_consolidation(consolidation_llm, chunk_text, existing_memory)
        if parsed is None:
            continue
        entry = " ".join(parsed["history_entry"].split())
        write_memory_md(parsed["memory_update"].strip())
        append_history_log(entry)
        return

    fail_note = " ".join(chunk_text.split())[:200]
    append_history_log(f"[CONSOLIDATION-FAILED] {fail_note}")


def ensure_budget_before_react(
    consolidation_llm: ChatOpenAI,
    history: list[BaseMessage],
    last_consolidated: int,
    human_message: HumanMessage,
) -> int:
    """WG-19：ReAct 前外層迴圈 — Phase A 規劃 final_idx，Phase B 整包整併 + 推游標。

    僅在 cost <= TOKEN_BUDGET // 2 時 return；呼叫端可直接進入 ReAct，無需再驗證。
    """
    target = get_token_budget() // 2

    while True:
        # Phase A — 規劃（不呼叫 consolidation LLM）
        system_text = build_system_prompt()
        past0 = history[last_consolidated:]
        cost = request_cost_chars(system_text, past0, human_message)
        if cost <= target:
            return last_consolidated

        tokens_to_remove = max(0, cost - target)
        boundary = pick_consolidation_boundary(
            history, last_consolidated, tokens_to_remove
        )
        if boundary is None or boundary[0] <= last_consolidated:
            # 無可用 user 邊界時，整併剩餘全部 history 尾段
            if last_consolidated >= len(history):
                raise RuntimeError(
                    f"WG-19：past 已空仍無法壓至 target（cost={cost}，target={target}）。"
                    " 請縮短 MEMORY 或調高 TOKEN_BUDGET。"
                )
            final_idx = len(history)
        else:
            final_idx = boundary[0]

        pack = history[last_consolidated:final_idx]
        if not pack:
            raise RuntimeError(
                f"WG-19：整併包為空無法推進（cost={cost}，target={target}）。"
            )

        print(
            f"（WG-19 規劃：final_idx={final_idx}，"
            f"待整併 {len(pack)} 則；cost={cost}，target={target}。）"
        )

        # Phase B — 整包整併 + 推游標（一次 invoke）
        existing = read_memory_md()
        print(
            f"（WG-19 整併：history[{last_consolidated}:{final_idx}]"
            f" + MEMORY → memory/MEMORY.md。）"
        )
        _consolidate_pack(consolidation_llm, pack, existing)
        last_consolidated = final_idx
        # 回到 Phase A 重算（MEMORY 更新後 system 可能變長）


# ---------------------------------------------------------------------------
# WG-20：SkillsLoader 與 system prompt 注入（模組級 SKILLS_LOADER）
# ---------------------------------------------------------------------------


@dataclass
class SkillEntry:
    name: str
    path: str
    source: str
    description: str
    always: bool
    body: str


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
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
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.workspace_skills = self.workspace / "skills"
        self.builtin_skills = self.workspace / "builtin_skills"
        self.workspace_skills.mkdir(parents=True, exist_ok=True)
        self.builtin_skills.mkdir(parents=True, exist_ok=True)

    def _skill_path_for_read(self, skill_file: Path) -> str:
        return skill_file.resolve().relative_to(self.workspace).as_posix()

    def _entries_from_dir(
        self, root: Path, source: str, skip: set[str]
    ) -> list[SkillEntry]:
        if not root.exists():
            return []

        entries: list[SkillEntry] = []
        for skill_dir in sorted(root.iterdir(), key=lambda p: p.name):
            skill_file = skill_dir / "SKILL.md"
            if not skill_dir.is_dir() or not skill_file.is_file():
                continue
            if skill_dir.name in skip:
                continue

            text = skill_file.read_text(encoding="utf-8")
            meta, body = split_frontmatter(text)
            name = skill_dir.name
            description = meta.get("description") or name
            always = meta.get("always", "false").lower() == "true"
            rel_path = self._skill_path_for_read(skill_file)
            entries.append(
                SkillEntry(name, rel_path, source, description, always, body)
            )
        return entries

    def list_skills(self) -> list[SkillEntry]:
        workspace_entries = self._entries_from_dir(
            self.workspace_skills, "workspace", set()
        )
        workspace_names = {entry.name for entry in workspace_entries}
        builtin_entries = self._entries_from_dir(
            self.builtin_skills, "builtin", workspace_names
        )
        return workspace_entries + builtin_entries

    def load_skill(self, name: str) -> str | None:
        for root in (self.workspace_skills, self.builtin_skills):
            path = root / name / "SKILL.md"
            if path.is_file():
                return path.read_text(encoding="utf-8")
        return None


def build_skills_summary(entries: list[SkillEntry]) -> str:
    summarized = [e for e in entries if not e.always]
    if not summarized:
        return ""
    lines = [f"- **{e.name}** — {e.description} `{e.path}`" for e in summarized]
    return "\n".join(lines)


SKILLS_LOADER = SkillsLoader(WORKSPACE)


def build_system_prompt() -> str:
    """WG-12～20 送模 system 唯一入口（人設 + 長期記憶 + Skills）。"""
    parts: list[str] = [get_identity()]
    mem = memory_block_for_system()
    if mem:
        parts.append(mem)

    entries = SKILLS_LOADER.list_skills()
    active = [e for e in entries if e.always]
    if active:
        body = "\n\n---\n\n".join(
            f"### Skill: {e.name}\n\n{e.body}" for e in active
        )
        parts.append(f"# Active Skills\n\n{body}")

    summary = build_skills_summary(entries)
    if summary:
        intro = (
            "下列技能可擴充你的能力。若要使用某技能，請用 read_file 讀取清單中"
            "該技能路徑下的 SKILL.md。\n"
            "若該技能需額外套件或環境，請先依 SKILL.md 或專案說明安裝相依項目後再操作。\n\n"
        )
        parts.append("# Skills\n\n" + intro + summary)

    return "\n\n---\n\n".join(parts) if len(parts) > 1 else parts[0]


# ---------------------------------------------------------------------------
# 進入點（WG-12～20 合併主迴圈）
# ---------------------------------------------------------------------------


def print_wg01_to_03_banner() -> None:
    """WG-01～03 最小示範（不呼叫 API）。"""
    agent_name = "法鬥超人"
    tip = f"（WG-02/03 示範）Hello，我是 {agent_name}，準備進入課堂對話。"
    print(tip)


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print("已讀到 API 金鑰設定（內容不顯示）；進入對話（串流 + 工具 + JSONL + 預算裁切）。")
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    # WG-16：啟動載入
    session_path = os.getenv("SESSION_JSONL_PATH", "session_wiki_wg.jsonl")
    history, session_meta = load_session_jsonl(session_path)
    last_consolidated = (
        int(session_meta.get("last_consolidated", 0) or 0) if session_meta else 0
    )
    if history:
        print(
            f"已從 {session_path!r} 載入 {len(history)} 則訊息（WG-16）；"
            f" last_consolidated={last_consolidated}（WG-17）。"
        )
    else:
        print(f"尚無可載入歷史或檔不存在；自空 history 開始（WG-15 寫入）。")

    # WG-12～14：模型、system、工具
    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.2)
    llm_tools = llm.bind_tools(TOOLS)
    consolidation_llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.2)
    print(
        f"（WG-17 TOKEN_BUDGET={get_token_budget()}，"
        f"WG-19 整併目標 ≤ {get_token_budget() // 2} 字元；以字元長度模擬 token。）"
    )

    while True:
        user_text = input("\n你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        human_message = HumanMessage(content=user_text)

        # WG-19：完成後 cost 已 <= target；直接組 system + past 進 ReAct
        prev_consolidated = last_consolidated
        last_consolidated = ensure_budget_before_react(
            consolidation_llm, history, last_consolidated, human_message
        )
        if last_consolidated != prev_consolidated:
            if session_meta is None:
                session_meta = _default_metadata()
            session_meta = save_session_jsonl(
                session_path, history, session_meta, last_consolidated
            )
        system_text = build_system_prompt()
        past = history[last_consolidated:]

        # WG-13：ReAct 一輪（送模含 system + past + 本輪 user）
        print("\n助手：", end="", flush=True)
        _reply_text, turn_messages = run_react_turn(
            llm_tools, system_text, past, user_text
        )
        print()

        history.extend(turn_messages)

        # WG-15：整檔覆寫 JSONL（含 last_consolidated）
        if session_meta is None:
            session_meta = _default_metadata()
        session_meta = save_session_jsonl(
            session_path, history, session_meta, last_consolidated
        )
        print(
            f"（已寫入 {session_path!r}，共 {len(history)} 則累積訊息；"
            f" last_consolidated={last_consolidated}。）"
        )


if __name__ == "__main__":
    main()
