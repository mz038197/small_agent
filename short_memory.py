import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


SYSTEM_TEXT = """
你是耐心的程式助教，使用繁體中文。
先給重點結論，再補 1-2 句必要說明；
若資訊不足，先問 1 個澄清問題。
"""

def main() -> None:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    history: list = []  # 只存「已結束回合」的 HumanMessage / AIMessage

    print("輸入 quit 結束。\n")
    while True:
        user_text = input("你: ").strip()
        if user_text.lower() == "quit":
            break

        messages_to_send = [
            # 組訊息串列，順序須為 system → 歷史回合 → 本輪 user

        ]

        reply = llm.invoke(messages_to_send)

        # 回應結束後才寫入短期記憶（history）
        history.append(HumanMessage(content=user_text))
        history.append(AIMessage(content=reply.content))

        print("助手:", reply.content, "\n")


if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("請設定 OPENAI_API_KEY")
    main()