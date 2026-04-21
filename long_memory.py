import os
from datetime import datetime
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# 記憶檔與專案根目錄同層的 memory/（工作坊範例儲層；整併與組窗題見 challenges.md）
_MEMORY_DIR = Path(__file__).resolve().parent / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"

SYSTEM_TEXT = "你是耐心的程式助教，使用繁體中文。先給重點結論，再補 1-2 句必要說明；若資訊不足，先問 1 個澄清問題。"
# 送進模型前可負擔的內容長度上限（字元數近似 token）；與 challenges.md Challenge A（整併與讀回組窗）的 TOKEN_BUDGET 同名同義。
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
    """基底 system 與長期記憶區塊合併。"""
    mem = get_memory_context()
    if mem:
        return f"{SYSTEM_TEXT}\n\n{mem}"
    return SYSTEM_TEXT


def request_cost_chars(
    system_text: str, past: list, current_user_content: str
) -> int:
    """
    Challenge A（整併與送模成本估算）用的假成本：系統字串長度 + 所有要送進模型的 Human/AI 的 content 長度。
    本輪使用者內容一定計入（不可刪）。
    """
    system_len = len(system_text)
    past_len = sum(len(m.content) for m in past)
    return system_len + past_len + len(current_user_content)


def adjust_last_consolidated_if_over_budget(
    history: list,
    last_consolidated: int,
    current_user_content: str,
    budget: int,
    system_text: str,
) -> int:
    """
    last_consolidated 語意：完整對話在 history；past = history[last_consolidated:] 為「要送進模型的過去」。
    索引永遠落在某一輪開頭（偶數）。僅在 cost > budget 時才前進，每次 +2 丟最舊一輪，
    直到 cost <= budget // 2（預留輸出側概念）或 past 已無法再刪一整輪。
    """
    past = history[last_consolidated:]
    if request_cost_chars(system_text, past, current_user_content) <= budget:
        return last_consolidated

    target = budget // 2
    while True:
        past = history[last_consolidated:]
        cost = request_cost_chars(system_text, past, current_user_content)
        if cost <= target or len(past) < 2:
            return last_consolidated
        last_consolidated += 2


def main() -> None:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    history: list = []  # 只存「已結束回合」的 HumanMessage / AIMessage（成對 append）
    # 從哪一則起算「過去」；僅在超線裁切時 +=2，不縮短 history 本體
    last_consolidated = 0

    print("輸入 quit 結束。\n")
    while True:
        user_text = input("你: ").strip()
        if user_text.lower() == "quit":
            break

        system_prompt = build_system_prompt()
        last_consolidated = adjust_last_consolidated_if_over_budget(
            history, last_consolidated, user_text, TOKEN_BUDGET, system_prompt
        )
        past = history[last_consolidated:]

        messages_to_send = [
            SystemMessage(content=system_prompt),
            *past,
            HumanMessage(content=user_text),
        ]

        reply = llm.invoke(messages_to_send)

        history.append(HumanMessage(content=user_text))
        history.append(AIMessage(content=reply.content))

        print("助手:", reply.content, "\n")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("請設定 OPENAI_API_KEY")
    main()
