"""
合併 long_memory.py、short_memory.py、react.py：
- 長期記憶（檔案）與歷史摘要、送模前字元成本與預算裁切
- 短期記憶（多輪對話，含工具呼叫鏈）
- ReAct 風格：四則運算工具與 Ollama 非標準 tool args 修正
"""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Iterable

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 記憶檔與專案根目錄同層的 memory/
_MEMORY_DIR = Path(__file__).resolve().parent / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"

SYSTEM_TEXT = (
    "你是耐心的程式助教，使用繁體中文。先給重點結論，再補 1-2 句必要說明；"
    "若資訊不足，先問 1 個澄清問題。"
)
TOOL_INSTRUCTION = (
    "凡涉及算術運算，必須使用 add_numbers、subtract_numbers、multiply_numbers、"
    "divide_numbers 這四項工具完成計算，不要只在回覆文字裡心算。"
)
# 送進模型前可負擔的內容長度上限（字元數近似 token）
TOKEN_BUDGET = 8000


def _ensure_memory_dir() -> None:
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_memory_files() -> None:
    """首次執行時建立記憶檔，避免後續流程讀不到檔案。"""
    _ensure_memory_dir()
    _MEMORY_FILE.touch(exist_ok=True)
    _HISTORY_FILE.touch(exist_ok=True)


def read_long_term() -> str:
    """讀取目前長期知識（檔案不存在時回傳空字串）。"""
    _ensure_memory_files()
    return _MEMORY_FILE.read_text(encoding="utf-8")


def write_long_term(content: str) -> None:
    """覆寫長期記憶檔（現狀快照）。"""
    _ensure_memory_files()
    _MEMORY_FILE.write_text(content, encoding="utf-8")


def append_history(entry: str) -> None:
    """追加一筆歷史摘要；每筆自動加上 [YYYY-MM-DD HH:MM] 前綴。"""
    _ensure_memory_files()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"[{ts}] {entry.strip()}\n"
    with _HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(line)


def get_memory_context() -> str:
    """供 system prompt 注入；無內容時回傳空字串（呼叫端可不退化區塊）。"""
    body = read_long_term().strip()
    if not body:
        return ""
    return "## Long-term Memory\n\n" + body


def build_system_prompt() -> str:
    """基底 system、長期記憶區塊、與工具使用規則合併。"""
    mem = get_memory_context()
    parts = [SYSTEM_TEXT, TOOL_INSTRUCTION]
    if mem:
        parts.insert(1, mem)
    return "\n\n".join(parts)


def _flatten_turns(turns: list[list[BaseMessage]], start_turn: int) -> list[BaseMessage]:
    out: list[BaseMessage] = []
    for t in turns[start_turn:]:
        out.extend(t)
    return out


def request_cost_chars(
    system_text: str, past: Iterable[BaseMessage], current_user_content: str
) -> int:
    """
    假成本：系統字串長度 + 所有要送進模型的過去訊息 content 長度 + 本輪使用者內容。
    本輪使用者內容一定計入（不可刪）。
    """
    system_len = len(system_text)
    past_len = sum(len(m.content or "") for m in past)
    return system_len + past_len + len(current_user_content)


def adjust_last_consolidated_if_over_budget(
    turns: list[list[BaseMessage]],
    last_consolidated: int,
    current_user_content: str,
    budget: int,
    system_text: str,
) -> int:
    """
    last_consolidated 語意：從第幾「輪」開始保留在送模的 past 裡；
    僅在 cost > budget 時才前進，每次刪掉最舊一輪（一整段含工具鏈），
    直到 cost <= budget // 2（預留輸出側概念）或已無法再刪。
    """
    past = _flatten_turns(turns, last_consolidated)
    if request_cost_chars(system_text, past, current_user_content) <= budget:
        return last_consolidated

    target = budget // 2
    while True:
        past = _flatten_turns(turns, last_consolidated)
        cost = request_cost_chars(system_text, past, current_user_content)
        if cost <= target or last_consolidated >= len(turns):
            return last_consolidated
        last_consolidated += 1


# --- 工具（react.py）---


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b


@tool
def subtract_numbers(a: float, b: float) -> float:
    """Subtract b from a and return the difference (a - b)."""
    return a - b


@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b


@tool
def divide_numbers(a: float, b: float) -> float | str:
    """Divide a by b and return the quotient. If b is zero, returns an error message instead."""
    if b == 0:
        return "錯誤：除數不可為零"
    return a / b


TOOLS = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

_TOOL_MAP = {t.name: t for t in TOOLS}


def _normalize_tool_args(tool_input: dict) -> dict:
    """修正 Ollama 等後端可能回傳的巢狀 {'key': {'type': '...', 'value': ...}} 格式。"""
    normalized = dict(tool_input)
    for key, value in list(normalized.items()):
        if isinstance(value, dict) and "value" in value:
            normalized[key] = value["value"]
    return normalized


def run_react_turn(
    llm_with_tools: ChatOpenAI,
    system_text: str,
    past: list[BaseMessage],
    user_text: str,
) -> tuple[str, list[BaseMessage]]:
    """
    執行一輪使用者輸入：可能含多段 tool call，直到得到最終 AI 文字回覆。
    回傳 (最終內容, 本輪應寫入短期記憶的訊息序列，自 HumanMessage 起)。
    """
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *past,
        HumanMessage(content=user_text),
    ]
    past_and_user_count = 1 + len(past)

    while True:
        response = llm_with_tools.invoke(messages)
        if response.tool_calls:
            messages.append(response)
            for tool_call in response.tool_calls:
                name = tool_call["name"]
                raw_args = tool_call.get("args") or {}
                tool_input = _normalize_tool_args(dict(raw_args))
                tool_obj = _TOOL_MAP.get(name)
                if tool_obj is None:
                    tool_result: str | float = f"Unknown tool: {name}"
                else:
                    tool_result = tool_obj.invoke(tool_input)
                messages.append(
                    ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])
                )
        else:
            messages.append(response)
            break

    turn_messages = messages[past_and_user_count:]
    final_ai = next(
        (m for m in reversed(turn_messages) if isinstance(m, AIMessage)),
        None,
    )
    final_text = ((final_ai.content if final_ai else None) or "").strip()
    return final_text, turn_messages


def main() -> None:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    llm_with_tools = llm.bind_tools(TOOLS)

    # 每輪為一個 list：自本輪 HumanMessage 起，到含工具在內的完整鏈
    turns: list[list[BaseMessage]] = []
    last_consolidated = 0

    print("輸入 quit 結束。\n")
    while True:
        user_text = input("你: ").strip()
        if user_text.lower() == "quit":
            break

        system_prompt = build_system_prompt()
        last_consolidated = adjust_last_consolidated_if_over_budget(
            turns, last_consolidated, user_text, TOKEN_BUDGET, system_prompt
        )
        past = _flatten_turns(turns, last_consolidated)

        reply_text, turn_messages = run_react_turn(
            llm_with_tools, system_prompt, past, user_text
        )
        turns.append(turn_messages)

        print("助手:", reply_text, "\n")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("請設定 OPENAI_API_KEY")
    main()
