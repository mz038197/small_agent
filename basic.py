"""課堂示範：WG-12～WG-18 對話脈絡 JSONL、SystemMessage、字元預算裁切（WG-16）、長期記憶整併（WG-17）；WG-13 ReAct 見 memory_react_agent.py；WG-19 檔案／exec 工具見 wiki_wg_workshop.py（對照 challenges-wiki-guided.md，教學順序為 WG-13 後接 WG-19 再進 JSONL）。"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# WG-17：與專案根同層的 memory/（對照 long-term-memory-template Challenge A）
_MEMORY_DIR = Path(__file__).resolve().parent / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"

# 長期記憶正文長度上限（字元）；超過則由尾端截斷再組進 system
MEMORY_MAX_CHARS = 6000
# 整併失敗時，同一 chunk 最多重試次數（0 表示不重試，直接 fallback）
CONSOLIDATION_MAX_RETRIES = 3

# 整併專用 LLM 溫度（與主對話可分開）
CONSOLIDATION_TEMPERATURE = 0.1


def build_system_prompt() -> str:
    """WG-12：建立系統提示字串（不含長期記憶區塊；WG-17 另併入）。"""
    system_text = "你是課堂程式助教。請使用繁體中文；先給一句重點結論，必要時再補一句說明。"
    nick = "法鬥超人"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}"


def _ensure_memory_dir() -> None:
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_memory_files() -> None:
    _ensure_memory_dir()
    _MEMORY_FILE.touch(exist_ok=True)
    _HISTORY_FILE.touch(exist_ok=True)


def read_long_term() -> str:
    """讀取 MEMORY.md（不存在時視為空）。"""
    if not _MEMORY_FILE.exists():
        return ""
    return _MEMORY_FILE.read_text(encoding="utf-8")


def write_long_term(content: str) -> None:
    """覆寫 MEMORY.md。"""
    _ensure_memory_files()
    _MEMORY_FILE.write_text(content, encoding="utf-8")


def append_history(entry: str, *, failed: bool = False) -> None:
    """
    追加 HISTORY.md 一行；與 memory_react_agent 語意對齊。
    failed=True 時使用 [CONSOLIDATION-FAILED] 前綴（單行摘錄）。
    """
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
    """
    WG-17：供拼入 SystemMessage；若無內容則不回傳孤立標題。
    內文超過 MEMORY_MAX_CHARS 時由尾端截斷。
    """
    body = read_long_term().strip()
    if not body:
        return ""
    if len(body) > MEMORY_MAX_CHARS:
        body = body[-MEMORY_MAX_CHARS:]
    return f"## Long-term Memory\n\n{body}"


def system_content_for_model() -> str:
    """送主模型用的完整 system 字串：課堂規則 + 可選長期記憶區塊。"""
    base = build_system_prompt()
    mem = memory_block_for_system()
    if not mem:
        return base
    return f"{base}\n\n{mem}"


def _token_budget() -> int:
    """讀取 TOKEN_BUDGET（預設 8000）；無效字串時回退預設。"""
    raw = os.getenv("TOKEN_BUDGET", "8000")
    try:
        return max(1, int(raw))
    except ValueError:
        return 8000


def estimate_message_tokens(message: BaseMessage) -> int:
    """WG-16：以字元長度模擬 token（與 pick_consolidation_boundary 共用）。"""
    c = message.content
    return len(c) if isinstance(c, str) else 0


def request_cost_chars(
    system_text: str, past: list[BaseMessage], human_message: HumanMessage
) -> int:
    """
    與 memory_react_agent.request_cost_chars 同一語意：
    len(system) + 過去訊息 content 長度 + 本輪使用者內容（本輪必留）。
    """
    return (
        len(system_text)
        + sum(estimate_message_tokens(m) for m in past)
        + estimate_message_tokens(human_message)
    )


def pick_consolidation_boundary(
    messages: list[BaseMessage],
    last_consolidated: int,
    tokens_to_remove: int,
) -> tuple[int, int] | None:
    """自 last_consolidated 掃描，挑 HumanMessage 開頭邊界，使略過的權重足夠。"""
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


def _messages_to_chunk_text(msgs: list[BaseMessage]) -> str:
    """供整併 LLM 閱讀的純文字。"""
    lines: list[str] = []
    for m in msgs:
        if isinstance(m, HumanMessage):
            lines.append(f"user: {m.content}")
        elif isinstance(m, AIMessage):
            lines.append(f"assistant: {m.content}")
        else:
            lines.append(f"other: {m.content}")
    return "\n".join(lines)


def _parse_consolidation_json(text: str) -> tuple[str, str] | None:
    """自模型回覆抽出 history_entry、memory_update；失敗回傳 None。"""
    text = text.strip()
    try:
        # 允許 ```json 包圍
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
    """
    呼叫整併專用 LLM；成功回傳 (history_entry, memory_update)，失敗 None。
    """
    chunk_text = _messages_to_chunk_text(chunk_msgs)
    instruction = (
        "你是整併助手。請閱讀「現有長期記憶（markdown）」與「待整併對話片段」，"
        "僅輸出一個 JSON 物件（不要其他說明），兩個鍵：\n"
        '- "history_entry": 字串，單行可讀摘要（繁體中文）\n'
        '- "memory_update": 字串，將完整取代 MEMORY.md 的正文（markdown）\n'
    )
    user_body = f"{instruction}\n\n【現有 MEMORY】\n{current_memory}\n\n【待整併片段】\n{chunk_text}"
    messages = [
        SystemMessage(content="你僅輸出合法 JSON 物件，鍵名必為 history_entry 與 memory_update。"),
        HumanMessage(content=user_body),
    ]
    r = llm.invoke(messages)
    raw = r.content if isinstance(r.content, str) else str(r.content)
    parsed = _parse_consolidation_json(raw)
    return parsed


def consolidate_one_chunk(
    consolidation_llm: ChatOpenAI,
    history: list[BaseMessage],
    last_consolidated: int,
    boundary_idx: int,
) -> int:
    """
    將 history[last_consolidated:boundary_idx] 整併進長期記憶；成功寫入 MEMORY／HISTORY，失敗則 [CONSOLIDATION-FAILED]。
    chunk 為空時不呼叫 LLM，僅回傳 boundary_idx（游標由呼叫端決定是否更新）。
    """
    chunk = history[last_consolidated:boundary_idx]
    if not chunk:
        return boundary_idx

    current_mem = read_long_term()
    # MAX_RETRIES=0：只試 1 次即 fallback；>0：首試 + 重試次數
    attempts = 1 if CONSOLIDATION_MAX_RETRIES == 0 else (1 + CONSOLIDATION_MAX_RETRIES)
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


def load_session_jsonl(path: str) -> tuple[list[BaseMessage], dict[str, Any] | None]:
    """從 JSONL 載入 messages 與 metadata；檔不存在則回傳空串列與 None。"""
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
                messages.append(AIMessage(content=str(obj.get("content", ""))))
            # role == "tool" 或其他未知列：略過

    return messages, meta


def save_session_jsonl(
    path: str,
    messages: list[BaseMessage],
    existing_meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """整檔覆寫：第一行 metadata（更新 updated_at），其餘每行一則 user／assistant（略過 SystemMessage）。"""
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

    lines: list[str] = [json.dumps(meta, ensure_ascii=False)]

    for m in messages:
        ts = datetime.now().isoformat()
        if isinstance(m, HumanMessage):
            row = {"role": "user", "content": m.content, "timestamp": ts}
        elif isinstance(m, AIMessage):
            row = {"role": "assistant", "content": m.content, "timestamp": ts}
        else:
            continue
        lines.append(json.dumps(row, ensure_ascii=False))

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")

    return meta


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print(
            "已讀到 API 金鑰設定（內容不顯示）；進入對話（脈絡寫入 JSONL、關閉後可接續；"
            "WG-17：memory/MEMORY.md、HISTORY.md；超預算時整併後送主模型前成本 ≤ TOKEN_BUDGET//2；"
            "可選 .env：ASSISTANT_DISPLAY_NAME、TOKEN_BUDGET；輸入 quit / exit / q 結束）。"
        )
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    session_path = os.getenv("SESSION_JSONL_PATH", "session.jsonl")
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
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    consolidation_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=CONSOLIDATION_TEMPERATURE,
    )

    while True:
        user_text = input("你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        human_message = HumanMessage(content=user_text)

        # --- 送模前：system 含 WG-17 長期記憶；成本與 request_cost_chars、WG-16 邊界語意一致 ---
        system_str = system_content_for_model()
        past0 = history[last_consolidated:]
        cost = request_cost_chars(system_str, past0, human_message)

        if cost <= token_budget:
            past = past0
        else:
            # 嚴格超過 TOKEN_BUDGET：整併（含 consolidation LLM）直到送主模型前成本 ≤ TOKEN_BUDGET//2
            target = token_budget // 2
            while request_cost_chars(
                system_content_for_model(),
                history[last_consolidated:],
                human_message,
            ) > target:
                sys_s = system_content_for_model()
                past_live = history[last_consolidated:]
                cost_now = request_cost_chars(sys_s, past_live, human_message)
                tokens_to_remove = max(0, cost_now - target)
                boundary = pick_consolidation_boundary(
                    history, last_consolidated, max(1, tokens_to_remove)
                )
                if boundary is None:
                    # 無可用 user 邊界或無法再推進：避免無限迴圈（見 pick_consolidation_boundary／WG-16 停止條件註解）
                    break
                b_idx = boundary[0]
                consolidate_one_chunk(
                    consolidation_llm, history, last_consolidated, b_idx
                )
                last_consolidated = b_idx
                if session_meta is None:
                    session_meta = _default_metadata()
                session_meta["last_consolidated"] = last_consolidated
                session_meta = save_session_jsonl(session_path, history, session_meta)

            past = history[last_consolidated:]
            system_str = system_content_for_model()

        system_message = SystemMessage(content=system_str)
        context_messages: list[BaseMessage] = [system_message, *past, human_message]

        print("助手：", end="", flush=True)
        reply_parts: list[str] = []
        for chunk in llm.stream(context_messages):
            if chunk.content:
                print(chunk.content, end="", flush=True)
                reply_parts.append(chunk.content)
        print()
        assistant_text = "".join(reply_parts)

        history.append(human_message)
        history.append(AIMessage(content=assistant_text))

        if session_meta is None:
            session_meta = _default_metadata()
        session_meta["last_consolidated"] = last_consolidated
        session_meta = save_session_jsonl(session_path, history, session_meta)


if __name__ == "__main__":
    main()
