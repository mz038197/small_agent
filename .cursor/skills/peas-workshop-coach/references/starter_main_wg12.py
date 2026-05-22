"""
WG-12 起點範本（starter_main_wg12.py）— peas-workshop-coach skill 內唯讀。

blank `main.py` 時由教練複製**全文**至此檔內容；**僅含 WG-12**，不含 WG-13～16（無 @tool、無 ReAct、無 JSONL）。
完整標準（WG-13～16）對照 `reference_agent.py`。
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI


def build_system_prompt() -> str:
    system_text = "你是課堂程式助教，並請使用繁體中文。"
    nick = "法鬥超人"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}"


def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print(
            "已讀到 API 金鑰設定（內容不顯示）；進入對話（串流 + 人設在 system 層；"
            "輸入 quit / exit / q 結束）。"
        )
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    llm = ChatOpenAI(model="gpt-5.4-mini", temperature=0.2)
    system_text = build_system_prompt()
    history: list[BaseMessage] = []

    while True:
        user_text = input("\n你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        human_message = HumanMessage(content=user_text)
        context_messages: list[BaseMessage] = [
            SystemMessage(content=system_text),
            *history,
            human_message,
        ]
        print("\n助手：", end="", flush=True)
        reply_parts: list[str] = []
        for chunk in llm.stream(context_messages):
            content = chunk.content
            if isinstance(content, str) and content:
                print(content, end="", flush=True)
                reply_parts.append(content)
        print()
        assistant_message = AIMessage(content="".join(reply_parts))

        history.append(human_message)
        history.append(assistant_message)


if __name__ == "__main__":
    main()
