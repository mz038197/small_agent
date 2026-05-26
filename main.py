"""
Agent Workshop CLI（main.py）— WG-22 進入點。

執行：`uv run main.py`
WG-12～21 執行邏輯在 **`agent_core.py`**；本檔僅 **`input`／`print`**、離開指令與 **WG-21 `/image`** 解析。
"""

from __future__ import annotations

from agent_core import Agent, get_token_budget


def main() -> None:
    try:
        agent = Agent.from_env()
    except RuntimeError as e:
        print(e)
        return

    print(
        "已讀到 API 金鑰設定（內容不顯示）；進入對話"
        "（串流 + 工具 + JSONL + 預算裁切 + WG-21 附圖）。"
    )
    print(
        "（WG-21 附圖：先輸入 `/image 相對路徑`，再輸入本輪文字；"
        "或單行 `/image 路徑 問題`。）"
    )

    if agent.history:
        print(
            f"已從 {agent.session_path!r} 載入 {len(agent.history)} 則訊息（WG-16）；"
            f" last_consolidated={agent.last_consolidated}（WG-17）。"
        )
    else:
        print("尚無可載入歷史或檔不存在；自空 history 開始（WG-15 寫入）。")

    print(
        f"（WG-17 TOKEN_BUDGET={get_token_budget()}，"
        f"WG-19 整併目標 ≤ {get_token_budget() // 2} 字元；以字元長度模擬 token。）"
    )

    pending_image: str | None = None

    while True:
        user_line = input("\n你：").strip()
        if user_line.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_line:
            continue

        image_rel: str | None = None
        user_text = user_line

        if user_line.startswith("/image "):
            rest = user_line[len("/image ") :].strip()
            if not rest:
                print(
                    "（用法：`/image 相對路徑`，下一行輸入文字；"
                    "或 `/image 路徑 問題`）"
                )
                continue
            parts = rest.split(maxsplit=1)
            image_rel = parts[0]
            if len(parts) > 1:
                user_text = parts[1].strip()
            else:
                pending_image = image_rel
                print(f"（已選附圖 {image_rel!r}，請輸入本輪文字）")
                continue
        elif pending_image is not None:
            image_rel = pending_image
            pending_image = None
            user_text = user_line

        if not user_text and not image_rel:
            continue

        print("\n助手：", end="", flush=True)
        agent.chat(user_text, image_path=image_rel)
        print()


if __name__ == "__main__":
    main()
