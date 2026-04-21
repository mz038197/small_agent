# `example.py` 學習重點 Checklist

學完本範例後，可用下列項目自評是否掌握。勾選表示「能用自己的話說清楚，必要時能指到程式對應位置」。

---

## 環境與執行

- [ ] 知道為何要設定 `OPENAI_API_KEY`，以及 `ChatOpenAI` 在缺少金鑰時大致會如何失敗；也知道自訂 OpenAI 相容端點時應使用 `OPENAI_BASE_URL`（見 `example.py` 約第 40 行與 `load_dotenv` 用法）。

- [ ] 請在 example.py **實作／確認** : 在專案根目錄建立 `.env`，在裡面設定 `OPENAI_API_KEY`（`sk-12345678`）和 `OPENAI_BASE_URL`（`http://203.71.78.31:8000/v1`），並知道為何需要此檔案、不要將金鑰提交到版控。

- [ ] 請在 `example.py` **實作／確認**：使用 `python-dotenv` 的 `load_dotenv()` 從專案根目錄載入環境變數，並以 `os.getenv("OPENAI_API_KEY")`、`os.getenv("OPENAI_BASE_URL")` 讀取，使程式能拿到正確設定（無需每次在終端機手動 `export`）（約第 2、8 行）。

## 模型與工具綁定

- [ ] 能解釋 `llm.bind_tools(arithmetic_tools)`：為何要把工具清單綁到模型上、綁定後模型回傳可能長什麼樣子（約第 42–48 行）。

## 工具定義（`@tool`）

- [ ] 能說明 **`@tool()` 本質上做了什麼**：把一般 Python 函式包成 LangChain 的 **Tool**（例如內部是 `StructuredTool`），讓程式同時擁有「實際可呼叫的函式」與「要交給模型看的工具宣告」（名稱、參數 schema、描述等 metadata）。

- [ ] 能對照 **`example.py` 第 11–34 行**，把「原始碼上的東西」連到「模型端看到的工具」：**函式名** → 工具名稱；**參數型別標註**（如 `a: float, b: float`）→ 參數 schema；**docstring**（三引號字串）→ 工具的 **description**（給模型讀的自然語言說明，不是給 Python 執行時用的註解而已）。

- [ ] 能解釋 **docstring／description 為何會影響「選不選、何時選」**：在 `bind_tools` 之後，模型在決定是否發出 `tool_calls`、要呼叫哪一個工具時，主要依據就是每個工具對外暴露的 **名稱 + description + 參數定義**；description 寫得越符合使用情境、邊界寫得越清楚，模型越不容易選錯工具或誤判何時該呼叫。

- [ ] 能對照四個工具：`add_numbers`、`subtract_numbers`、`multiply_numbers`、`divide_numbers` 的參數與回傳；並說明 `divide_numbers` 在除數為零時為何回傳字串而非數字（約第 29–34 行）。

## 訊息型別與角色

- [ ] 分得清 `SystemMessage`、`HumanMessage`、`AIMessage` 各代表誰說的話；並知道本範例中 system 內容要求模型對算術**一律用工具**、不可只心算（約第 3–4、52–58 行）。

- [ ] 能解釋 `ToolMessage` 的用途：在模型發出 `tool_calls` 之後，如何把每個工具的執行結果塞回對話，以及為何需要 `tool_call_id`（約第 107–108 行）。

## Tool calling 迴圈

- [ ] 能描述 `while True` 迴圈：何時把 `response` 加進 `messages`、何時走「執行工具」分支、何時結束迴圈（約第 65–111 行）。

- [ ] 能依序說出處理單次 `tool_call` 的步驟：讀 `name` / `args`、執行對應工具、用 `ToolMessage` 把字串化結果接回去（約第 78–108 行）。

## 本範例的題目語意

- [ ] 能用自己的話說明使用者問題要求的是哪種運算順序（先加再乘再除），以及模型應透過哪些工具呼叫來完成（約第 60–62 行）。

- [ ] 能舉一例：若不在 system 裡強制「必須用工具」，模型可能用純文字心算，會帶來什麼風險或與本範例設計目標的差異。

- [ ] 能說出若要把「多輪對話」接在本範例後面，`messages` 清單應如何延續（不必改碼，概念即可）。

---

## 使用方式建議

1. 先通讀 `example.py` 一輪，再依本清單逐項自問自答。
2. 卡關時可搭配 AI 助教，但請用**自己的話**寫兩句總結，確認不是只貼上答案。
