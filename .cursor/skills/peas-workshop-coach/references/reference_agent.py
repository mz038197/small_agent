"""
Agent Workshop 標準程式（reference_agent.py）— peas-workshop-coach skill 內唯讀對照。

對齊 `references/challenges-agent.md`（WG-13～16）；教練驗收與 Spec 以本檔為準。
學生實作請改專案根 **`main.py`**，勿直接修改本檔。

- WG-12：`build_system_prompt`、`SystemMessage` 與 `history` 分離（system 不進 JSONL）
- WG-13：`@tool`、`bind_tools`、ReAct 內層迴圈、`ToolMessage`
- WG-14：workspace 路徑解析、五支檔案／shell 工具 + `add_numbers`
- WG-15～16：每輪後 `save_session_jsonl`；啟動時 `load_session_jsonl`（略過壞行）

預設對話檔：`session_wiki_wg.jsonl`（可用環境變數 `SESSION_JSONL_PATH` 覆寫）
"""

from __future__ import annotations

import json
import os
import subprocess
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
# WG-13／WG-14：LangChain `@tool`（workspace 檔案／shell + 算術）
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


@tool
def add_numbers(a: float, b: float) -> float:
    """兩個數字相加並回傳和。純算術必須呼叫此工具，不可心算後直接回答。"""
    return float(a) + float(b)


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
# WG-12：system prompt
# ---------------------------------------------------------------------------


def build_system_prompt() -> str:
    system_text = "你是課堂程式助教，並請使用繁體中文。"
    nick = "法鬥超人"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}"


# ---------------------------------------------------------------------------
# WG-15～16：JSONL（第一行 metadata；不寫入 SystemMessage）
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
        line = _message_to_jsonl_line(m)
        if line is not None:
            lines.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")

    return meta


# ---------------------------------------------------------------------------
# WG-10：串流輔助（chunk 累積為 AIMessage，邊收邊印文字）
# ---------------------------------------------------------------------------

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
    history: list[BaseMessage],
    user_text: str,
) -> tuple[str, list[BaseMessage]]:
    """WG-13 ReAct：每輪模型皆 stream；工具同步執行並印結果。"""
    human_message = HumanMessage(content=user_text)
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *history,
        human_message,
    ]
    idx_turn_start = 1 + len(history)

    while True:
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
# WG-01～03：最小示範（不呼叫 API）
# ---------------------------------------------------------------------------


def print_wg01_to_03_banner() -> None:
    """WG-01：`if __name__ == "__main__"` 在檔案末端。\nWG-02/03：變數 + f-string。"""
    agent_name = "法鬥超人"
    tip = f"（WG-02/03 示範）Hello，我是 {agent_name}，準備進入課堂對話。"
    print(tip)


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print("已讀到 API 金鑰設定（內容不顯示）；進入對話（串流 + 工具 + JSONL）。")
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    session_path = os.getenv("SESSION_JSONL_PATH", "session_wiki_wg.jsonl")
    history, session_meta = load_session_jsonl(session_path)
    if history:
        print(f"已從 {session_path!r} 載入 {len(history)} 則訊息（WG-16）。")
    else:
        print(f"尚無可載入歷史或檔不存在；自空 history 開始（可接 WG-15 寫入）。")

    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.2)
    llm_tools = llm.bind_tools(TOOLS)
    system_text = build_system_prompt()

    while True:
        user_text = input("\n你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        print("\n助手：", end="", flush=True)
        _reply_text, turn_messages = run_react_turn(llm_tools, system_text, history, user_text)
        print()

        history.extend(turn_messages)
        if session_meta is None:
            session_meta = _default_metadata()
        last_consolidated = int(session_meta.get("last_consolidated", 0) or 0)
        session_meta = save_session_jsonl(session_path, history, session_meta, last_consolidated)
        print(f"（已寫入 {session_path!r}，共 {len(history)} 則累積訊息。）")


if __name__ == "__main__":
    main()
