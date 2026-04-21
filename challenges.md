# 進階練習題（Challenge MR-01～）

完成 `example.py` 的 agent 引導學習並勾選 `example-learning-checklist.md` 後，在 `**main.py**` 上依序實作下列挑戰。本檔為**本組題目的單一規格來源**（含各題驗收條件）。功能藍本為專案內之 `memory_react_agent.py`（含檔案長期記憶、歷史摘要、送模字元預算、短期多輪含工具鏈、四則工具與 Ollama 風格參數正規化）；學生透過小步驟**漸進拼回**同一行為，而非一次複製整檔。

**檔案角色**：`example.py` 僅供對照、勿改；作答與執行以 `main.py` 為主。需要對照完整行為時可並讀 `memory_react_agent.py`（教練／學生自用，題目不強制逐行一致，但**驗收條件**須滿足）。

**ITS Python wiki 對照**（七份統整條目見 LLM Wiki 之 `wiki/index.md`「教材統整／Python」；本機若使用課程約定之 Agent 庫，條目目錄為 `G:\我的雲端硬碟\Obsidian\Agent\wiki\`。教練口頭可說「我們現在在練檔案那一軌」而不唸檔名。）


| 序   | 學習主軸（由簡入繁） | wiki 條目檔名（統整頁）          |
| --- | ---------- | ----------------------- |
| 1   | 基礎資料與變數    | `Python-基礎資料與變數.md`     |
| 2   | 運算與輸入輸出    | `Python-運算與輸入輸出.md`     |
| 3   | 條件判斷與迴圈    | `Python-條件判斷與迴圈.md`     |
| 4   | 資料結構（串列等）  | `Python-資料結構-串列元組字典.md` |
| 5   | 函式與模組      | `Python-函式與模組.md`       |
| 6   | 檔案與例外處理    | `Python-檔案與例外處理.md`     |
| 7   | 類別與單元測試    | `Python-類別與單元測試.md`     |


**Challenge 編號與 ITS 軌對照**（實作順序由淺入深；一題可跨多軌，下表為「主要練習點」）：


| MR 範圍           | 主要對照 ITS wiki 序      |
| --------------- | -------------------- |
| MR-01～MR-05     | 1 基礎資料與變數            |
| MR-06～MR-08     | 2 運算與輸入輸出            |
| MR-09～MR-13     | 3 條件判斷與迴圈；4 資料結構     |
| MR-14～MR-23     | 5 函式與模組（工具、查表、ReAct） |
| MR-24～MR-29     | 6 檔案與例外處理            |
| MR-30～MR-36     | 4～5 預算裁切、主程式整合、驗收    |
| MR-37～MR-38（選修） | 7 單元測試；6 例外處理加深      |


- **必做**：MR-01～MR-36，共 **36** 題（peas-challenge-coach 進度條 **N＝36**）。
- **選修**：MR-37、MR-38，共 **2** 題（不計入 N；完成可記「挑戰加分」）。

---

## Challenge MR-01：模組文件字串與 `from __future__ import annotations`

### 情境

先讓 `main.py` 成為「可維護的模組」：有說明這支程式做什麼的文件字串，並啟用延後評估的型別註記，後續函式簽名才能寫 `list[BaseMessage]` 等而不報錯。

### 規格

- 檔案最上方為模組層 `"""..."""`（一句話交代：記憶＋ReAct 助教迴圈即可）。
- 第二行起為 `from __future__ import annotations`（須在一般 `import` 之前以外的規則依 Python 官方；若你採「文件字串後第一行」亦可，但**不得**破壞執行）。

### 驗收條件

- 開啟 `main.py` 可看到模組 docstring 與 `__future__` 行。
- 能說明：**為什麼**要加 `from __future__ import annotations`？（與前向參考、可讀註記有關即可。）

### 提示（選讀）

> 對照 wiki「基礎資料與變數」中關於註解、模組與程式結構的說明。

### 藍本對應程式（`memory_react_agent.py` 行 1–7）

模組文件字串與 `__future__`；一般 `import` 在下一題。

```python
"""
合併 long_memory.py、short_memory.py、react.py：
- 長期記憶（檔案）與歷史摘要、送模前字元成本與預算裁切
- 短期記憶（多輪對話，含工具呼叫鏈）
- ReAct 風格：四則運算工具與 Ollama 非標準 tool args 修正
"""
from __future__ import annotations
```

---

## Challenge MR-02：匯入區（依賴一次到位）

### 情境

後續每一步都會用到訊息型別與 LLM；先把 import 寫齊，避免之後每題補洞分心。

### 規格

- 至少包含：`os`、`datetime`、`Pathlib.Path`、`typing.Iterable`。
- LangChain：`AIMessage`、`BaseMessage`、`HumanMessage`、`SystemMessage`、`ToolMessage`、`tool`、`ChatOpenAI`（來自 `langchain_core`／`langchain_openai`，與 `memory_react_agent.py` 一致即可）。

### 驗收條件

- `main.py` 可 `uv run` 通過語法階段（尚不需呼叫 API 也可先註解 `main` 內容，但 import 須存在）。
- 能指出：**哪幾個**名稱是「訊息物件」、**哪個**是「可呼叫的模型客戶端」？

### 提示（選讀）

> 對照 wiki「函式與模組」：第三方套件 import 習慣。

### 藍本對應程式（`memory_react_agent.py` 行 9–16）

```python
import os
from datetime import datetime
from pathlib import Path
from typing import Iterable

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
```

---

## Challenge MR-03：記憶目錄與檔案路徑常數（`Path`）

### 情境

長期記憶要落在專案旁的 `memory/`。用 `Path` 表達路徑，避免手拼字串斜線。

### 規格

- 定義 `_MEMORY_DIR`＝`Path(__file__).resolve().parent / "memory"`。
- `_MEMORY_FILE`＝`_MEMORY_DIR / "MEMORY.md"`。
- `_HISTORY_FILE`＝`_MEMORY_DIR / "HISTORY.md"`。

### 驗收條件

- 三個常數皆存在且型別為 `Path`（或與之一致的可執行寫法）。
- 能說明：為什麼用 `__file__` 而不是寫死絕對路徑？

### 提示（選讀）

> wiki「基礎資料與變數」＋「檔案與例外」：`Path` 與相對路徑概念。

### 藍本對應程式（`memory_react_agent.py` 行 18–21）

```python
# 記憶檔與專案根目錄同層的 memory/
_MEMORY_DIR = Path(__file__).resolve().parent / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"
```

---

## Challenge MR-04：`SYSTEM_TEXT` 常數（助教角色）

### 情境

模型每次都要帶同一段「我是誰、怎麼回答」；先抽成模組層字串常數。

### 規格

- 定義 `SYSTEM_TEXT`（繁體中文助教敘述；文意與 `memory_react_agent.py` 可同義，不必逐字相同，但須包含：**繁體中文**、**先結論再補充**、**資訊不足時先問澄清** 三點精神）。

### 驗收條件

- `SYSTEM_TEXT` 為單一 `str`（可用括號多行字串）。
- 能唸出其中一句，說明它如何影響使用者體驗。

### 提示（選讀）

> wiki「基礎資料與變數」：字串常數與多行字串。

### 藍本對應程式（`memory_react_agent.py` 行 23–26）

```python
SYSTEM_TEXT = (
    "你是耐心的程式助教，使用繁體中文。先給重點結論，再補 1-2 句必要說明；"
    "若資訊不足，先問 1 個澄清問題。"
)
```

---

## Challenge MR-05：`TOOL_INSTRUCTION` 與 `TOKEN_BUDGET`

### 情境

算術題要走工具；送進模型的上下文不能無限長。把兩段「規則／上限」變成常數，之後組 prompt 與裁切會用到。

### 規格

- `TOOL_INSTRUCTION`：`str`，明確要求算術必須呼叫 `add_numbers`、`subtract_numbers`、`multiply_numbers`、`divide_numbers`，禁止純文字心算。
- `TOKEN_BUDGET`：`int`，語意為「字元級近似上限」，預設 **8000**（與藍本同名同義即可）。

### 驗收條件

- 兩常數皆存在且型別正確。
- 能說明：`TOKEN_BUDGET` 在程式裡預計用在**哪一段流程**？（送模前成本／裁切。）

### 提示（選讀）

> wiki「基礎資料與變數」：`int` 與「魔法數字抽常數」。

### 藍本對應程式（`memory_react_agent.py` 行 27–32）

```python
TOOL_INSTRUCTION = (
    "凡涉及算術運算，必須使用 add_numbers、subtract_numbers、multiply_numbers、"
    "divide_numbers 這四項工具完成計算，不要只在回覆文字裡心算。"
)
# 送進模型前可負擔的內容長度上限（字元數近似 token）
TOKEN_BUDGET = 8000
```

---

## Challenge MR-06：`if __name__ == "__main__"` 與 `OPENAI_API_KEY` 檢查

### 情境

沒有金鑰就不應默默連線；在進入 `main()` 前先檢查環境變數。

### 規格

- 使用 `os.environ.get("OPENAI_API_KEY")`（或等價讀法）；若缺值則 `raise SystemExit("請設定 OPENAI_API_KEY")`（訊息可微調，須為繁中友善句）。
- 有值才呼叫 `main()`（`main` 可先為 `pass` 或 `print`，下一題再填）。

### 驗收條件

- 未設金鑰時執行 `uv run main.py` 會以非零退出並印出／顯示提示。
- 能說明：為什麼不直接在程式裡寫死 API key？

### 提示（選讀）

> wiki「運算與輸入輸出」＋「條件判斷」：環境讀取與程式進入點。

### 藍本對應程式（`memory_react_agent.py` 行 245–248）

進入點；`main()` 定義於行 217 起。

```python
if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("請設定 OPENAI_API_KEY")
    main()
```

---

## Challenge MR-07：終端機開場 `print` 與 `quit` 提示

### 情境

使用者要知道怎麼離開迴圈。

### 規格

- 在 `main()` 開頭 `print` 一行以上說明（例如「輸入 quit 結束」）。

### 驗收條件

- 執行後第一眼能看到離開方式。
- 能說明：為什麼不直接把說明寫在 `input()` 的提示字串裡就好？（開放題，能自圓其說即可。）

### 提示（選讀）

> wiki「運算與輸入輸出」：`print` 與使用者引導。

### 藍本對應程式（`memory_react_agent.py` 行 225–225）

僅 `print` 開場一行；完整 `main` 見 MR-36 節錄。

```python
    print("輸入 quit 結束。\n")
```

---

## Challenge MR-08：`while True` 與 `input` 讀取使用者

### 情境

建立 REPL 骨架：一直讀一行使用者輸入。

### 規格

- `while True:` 內 `user_text = input("你: ").strip()`（提示字可微調，須有「你」或等同語意）。
- 若 `user_text.lower() == "quit"`：`break`。

### 驗收條件

- 輸入 `quit` 可結束程式（此時尚未要求呼叫模型也可）。
- 能說明：`.strip()` 避免什麼問題？

### 提示（選讀）

> wiki「條件判斷與迴圈」：`while` 與字串方法。

### 藍本對應程式（`memory_react_agent.py` 行 226–229）

REPL 讀入與 `quit`。

```python
    while True:
        user_text = input("你: ").strip()
        if user_text.lower() == "quit":
            break
```

---

## Challenge MR-09：`ChatOpenAI` 實例（模型與溫度）

### 情境

接上 OpenAI 相容聊天模型；參數與藍本對齊即可。

### 規格

- 在 `main()`（或你集中初始化處）建立 `ChatOpenAI(model="gpt-4o-mini", temperature=0.2, ...)`。
- `api_key` 須來自 `os.environ.get("OPENAI_API_KEY")`（或與 MR-06 一致之來源），**禁止**在程式碼內寫死 secret。

### 驗收條件

- 有金鑰時可建立 `llm` 物件不報錯（不要求此題已 `invoke`）。
- 能說明：`temperature=0.2` 大致代表什麼？

### 提示（選讀）

> wiki「函式與模組」：使用第三方類別建構子。

### 藍本對應程式（`memory_react_agent.py` 行 218–218）

`ChatOpenAI` 建立（藍本未帶 `api_key` 時可再加；題目 MR-09 要求從環境讀取）。

```python
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
```

---

## Challenge MR-10：單輪無歷史、無工具——`invoke` 一次

### 情境

先驗證「送得進模型、拿得到字串」，再疊歷史與工具。

### 規格

- 每輪建立 `messages = [SystemMessage(content=SYSTEM_TEXT), HumanMessage(content=user_text)]`。
- `reply = llm.invoke(messages)`，並 `print("助手:", reply.content)`（格式可微調）。
- 此題**不要求** `bind_tools`；**不要求**寫入 `history`。

### 驗收條件

- 連續兩輪對話皆可得到模型回覆（不依賴上一輪上下文亦可）。
- 能說明：`SystemMessage` 與 `HumanMessage` 在串列中的順序為何重要？

### 提示（選讀）

> wiki「資料結構」：用串列當有序訊息序列。

### 藍本對應程式（`memory_react_agent.py` 行 181–186）

藍本在 `run_react_turn` 內組 `messages`；本題練習時可無 `bind_tools`，僅 `llm.invoke([System, Human])` 等價精神即可。

```python
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *past,
        HumanMessage(content=user_text),
    ]
    past_and_user_count = 1 + len(past)
```

---

## Challenge MR-11：`history` 與成對 append（仍無工具）

### 情境

短期記憶：只保留「已結束回合」的 user／assistant 成對訊息。

### 規格

- `history: list[BaseMessage] = []`（型別註記與藍本一致即可）。
- 每輪在取得 `reply` 後：`history.append(HumanMessage(...))` 再 `history.append(AIMessage(...))`。
- 下一輪送進模型時須為 `[SystemMessage(SYSTEM_TEXT), *history, HumanMessage(...)]`。

### 驗收條件

- 第二輪開始模型能「延續」第一輪話題（簡單自測即可）。
- 能說明：為什麼要在 `invoke`**之後**才 append？（避免送進未完成的 assistant。）

### 提示（選讀）

> wiki「資料結構」：`list` 與展開 `*history`。

### 藍本對應程式（`memory_react_agent.py` 行 237–240）

藍本以 `turns`／`run_react_turn` 為主軸；此節錄示範主迴圈內「呼叫後 append」位置。

```python
        reply_text, turn_messages = run_react_turn(
            llm_with_tools, system_prompt, past, user_text
        )
        turns.append(turn_messages)
```

---

## Challenge MR-12：`turns: list[list[BaseMessage]]` 與「一輪一個子串列」語意

### 情境

之後每輪可能含多則 `ToolMessage`，不能再假設一輪只有兩則訊息；改為「一輪＝一個子串列」。

### 規格

- 以 `turns: list[list[BaseMessage]] = []` 取代（或並存後再切換）單層 `history`；**本題驗收**以 `turns` 為準。
- 每輪結束後 `turns.append([HumanMessage(...), AIMessage(...)])`（僅兩則亦可，須成為**一個子 list**）。

### 驗收條件

- `len(turns)` 等於已完成對話輪數。
- 能說明：`turns[i]` 代表什麼？（第 i 輪從使用者訊息起的一小段鏈。）

### 提示（選讀）

> wiki「資料結構」：巢狀串列。

### 藍本對應程式（`memory_react_agent.py` 行 221–223）

`turns` 與註解。

```python
    # 每輪為一個 list：自本輪 HumanMessage 起，到含工具在內的完整鏈
    turns: list[list[BaseMessage]] = []
    last_consolidated = 0
```

---

## Challenge MR-13：`_flatten_turns`（展開多輪）

### 情境

送模型時要把「從某一輪起」的子串列展平成單層訊息串列。

### 規格

- 函式簽名與藍本一致：`_flatten_turns(turns: list[list[BaseMessage]], start_turn: int) -> list[BaseMessage]`。
- 行為：對 `turns[start_turn:]` 內每個子串列 `extend` 到同一輸出串列。

### 驗收條件

- `start_turn == 0` 且有三輪時，展開後訊息數等於各輪長度之和。
- `start_turn` 增加時，展開結果變短（口頭或簡單 assert 均可）。

### 提示（選讀）

> wiki「函式與模組」：純函式與迴圈累積。

### 藍本對應程式（`memory_react_agent.py` 行 84–88）

```python
def _flatten_turns(turns: list[list[BaseMessage]], start_turn: int) -> list[BaseMessage]:
    out: list[BaseMessage] = []
    for t in turns[start_turn:]:
        out.extend(t)
    return out
```

---

## Challenge MR-14：`add_numbers` 與 `@tool` 裝飾器

### 情境

讓模型能「呼叫」加法；先只做一支工具。

### 規格

- `@tool` 裝飾的 `add_numbers(a: float, b: float) -> float`，回傳 `a + b`。
- docstring 可維持英文（與 LangChain tool 慣例相容）或中英並列。

### 驗收條件

- `add_numbers.invoke({"a": 1, "b": 2})` 回傳 `3.0`（或數值相等）。
- 能說明：`@tool` 做了什麼事（大意：註冊 schema 給模型）？

### 提示（選讀）

> wiki「函式與模組」：裝飾器與函式簽名。

### 藍本對應程式（`memory_react_agent.py` 行 131–134）

```python
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b
```

---

## Challenge MR-15：其餘三則運算工具與除零

### 情境

補齊減乘除；除法在除數為 0 時不可崩潰。

### 規格

- `subtract_numbers`、`multiply_numbers`、`divide_numbers` 皆為 `@tool`。
- `divide_numbers`：若 `b == 0`，回傳**繁中錯誤字串**（例如「錯誤：除數不可為零」），型別可為 `float | str`。

### 驗收條件

- 四則皆可 `invoke` 測試通過；除零回傳字串而非例外中斷整支程式。
- 能說明：為什麼除零不直接丟 `ZeroDivisionError` 給整個 agent？

### 提示（選讀）

> wiki「條件判斷與迴圈」：`if` 邊界。

### 藍本對應程式（`memory_react_agent.py` 行 131–154）

四則工具可一併節錄對照。

```python
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
```

---

## Challenge MR-16：`TOOLS` 與 `_TOOL_MAP`

### 情境

主迴圈之後要以名稱查表派發，避免巨型 `if/elif`。

### 規格

- `TOOLS = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]`。
- `_TOOL_MAP = {t.name: t for t in TOOLS}`（或等價、鍵為模型回傳的 `name` 字串）。

### 驗收條件

- `_TOOL_MAP["add_numbers"]` 可取回可 `invoke` 的物件。
- 能說明：字典在此的用途？（名稱→可呼叫物件。）

### 提示（選讀）

> wiki「資料結構」：字典與鍵值對應。

### 藍本對應程式（`memory_react_agent.py` 行 157–159）

```python
TOOLS = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

_TOOL_MAP = {t.name: t for t in TOOLS}
```

---

## Challenge MR-17：`bind_tools` 與 `llm_with_tools`

### 情境

讓 `invoke` 回傳的 assistant 訊息可帶 `tool_calls`。

### 規格

- `llm_with_tools = llm.bind_tools(TOOLS)`。
- 後續單輪測試須改為對 `llm_with_tools.invoke(...)` 呼叫（可仍無 `past`）。

### 驗收條件

- 使用者問簡單算術時，回傳物件**有機會**出現 `tool_calls`（依模型而定；至少程式路徑正確）。
- 能說明：`bind_tools` 與裸 `llm.invoke` 差在哪？

### 提示（選讀）

> LangChain 文件：tool binding 概念（內部自讀即可，題目不考背文件）。

### 藍本對應程式（`memory_react_agent.py` 行 217–219）

含 `main` 內 `llm` 與 `bind_tools`。

```python
def main() -> None:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    llm_with_tools = llm.bind_tools(TOOLS)
```

---

## Challenge MR-18：`_normalize_tool_args`

### 情境

部分本機後端（如 Ollama）可能回傳巢狀 `{'key': {'value': ...}}`；要攤平成工具 `invoke` 吃得下的 `dict`。

### 規格

- 實作 `_normalize_tool_args(tool_input: dict) -> dict`：對每個值，若為 `dict` 且含鍵 `"value"`，則替換為該 `value`。

### 驗收條件

- 輸入 `{"a": {"type": "number", "value": 3}}` 時輸出 `{"a": 3}`（型別可為 int/float，須一致且可 invoke）。
- 能舉一例：**不**正規化時會在哪一步壞掉？

### 提示（選讀）

> wiki「資料結構」：巢狀 dict 與拷貝（注意是否要先 `dict(tool_input)`）。

### 藍本對應程式（`memory_react_agent.py` 行 162–168）

```python
def _normalize_tool_args(tool_input: dict) -> dict:
    """修正 Ollama 等後端可能回傳的巢狀 {'key': {'type': '...', 'value': ...}} 格式。"""
    normalized = dict(tool_input)
    for key, value in list(normalized.items()):
        if isinstance(value, dict) and "value" in value:
            normalized[key] = value["value"]
    return normalized
```

---

## Challenge MR-19：`run_react_turn`——訊息串初始與 `past_and_user_count`

### 情境

把「一輪對話＋可能多段工具」封裝成函式；先完成訊息串開頭與切片基準。

### 規格

- 簽名：`run_react_turn(llm_with_tools, system_text: str, past: list[BaseMessage], user_text: str) -> tuple[str, list[BaseMessage]]`（型別註記可與藍本一致）。
- 建立 `messages = [SystemMessage(content=system_text), *past, HumanMessage(content=user_text)]`。
- `past_and_user_count = 1 + len(past)`（註解說明：前面有 1 個 system + len(past) 則 past，下一則起為本輪）。

### 驗收條件

- `past` 為空時，`messages` 長度為 2（system + human）。
- 能指出：`past_and_user_count` 對應到 `messages` 的哪一個索引意義？

### 提示（選讀）

> wiki「函式與模組」：參數化 system 與 past。

### 藍本對應程式（`memory_react_agent.py` 行 181–186）

訊息串初始與 `past_and_user_count`。

```python
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *past,
        HumanMessage(content=user_text),
    ]
    past_and_user_count = 1 + len(past)
```

---

## Challenge MR-20：`run_react_turn`——`while True` 與第一次 `invoke`

### 情境

進入可能多輪「模型→工具→模型」的迴圈。

### 規格

- 在 `while True` 內：`response = llm_with_tools.invoke(messages)`。
- 尚**不必**完成 tool 分支（可暫以「若無 tool_calls 則 break」占位），但本題完成後須能對**純文字回覆**正常結束並回傳字串。

### 驗收條件

- 不觸發工具的一般閒聊可結束迴圈並得到 `final_text`（可先寫死從 `response.content` 取）。
- 能說明：為什麼外層用 `while True` 而不是 `for` 固定次數？（與「模型可能多輪 tool」有關；若日後要加「最大迭代次數」也常在這層擴充。）

### 提示（選讀）

> wiki「條件判斷與迴圈」：`while` 與終止條件。

### 藍本對應程式（`memory_react_agent.py` 行 188–189）

`while` 內第一次 `invoke`。

```python
    while True:
        response = llm_with_tools.invoke(messages)
```

---

## Challenge MR-21：`run_react_turn`——`tool_calls` 分支與 `ToolMessage`

### 情境

模型要求工具時：把 assistant 訊息與每則工具結果接回 `messages`。

### 規格

- 若 `response.tool_calls` 為真：`messages.append(response)`。
- 對每個 `tool_call`：讀 `name`、`id`、`args`；`args` 經 `_normalize_tool_args`；用 `_TOOL_MAP.get` 找不到時結果為明確錯誤字串；找到則 `invoke`。
- 每個結果 `messages.append(ToolMessage(content=str(tool_result), tool_call_id=...))`。

### 驗收條件

- 使用者請模型用工具做簡單加法時，終端可看到一輪以上 `invoke`（或你 log）且最後有文字回覆。
- 能說明：`tool_call_id` 做什麼用？

### 提示（選讀）

> 對照藍本 `memory_react_agent.py` 的 `run_react_turn` 中段。

### 藍本對應程式（`memory_react_agent.py` 行 190–203）

含 `tool_calls` 與 `ToolMessage`。

```python
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
```

---

## Challenge MR-22：`run_react_turn`——無工具分支與 `turn_messages` 切片

### 情境

模型不再呼叫工具時：append 最後一則 AI，離開迴圈，並只把「本輪從使用者訊息起」的片段交給短期記憶。

### 規格

- `else`（無 `tool_calls`）：`messages.append(response)` 後 `break`。
- `turn_messages = messages[past_and_user_count:]`。
- `final_ai` 為 `turn_messages` 中**最後一則** `AIMessage`；`final_text` 為其 `content` 去空白；回傳 `(final_text, turn_messages)`。

### 驗收條件

- `turn_messages[0]` 型別為 `HumanMessage`。
- 能說明：為什麼 `final_ai` 要從 `turn_messages` 末端往前找？

### 提示（選讀）

> wiki「資料結構」：切片與索引。

### 藍本對應程式（`memory_react_agent.py` 行 204–214）

無工具分支與回傳切片。

```python
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
```

---

## Challenge MR-23：`main` 改呼叫 `run_react_turn`（先不啟用預算裁切）

### 情境

把 REPL 主迴圈接到 `run_react_turn`；此時 `past` 可先固定為 `_flatten_turns(turns, 0)` 或等價於「全部展開」，**尚未**要求實作 `last_consolidated`。

### 規格

- 每輪：`system_prompt = build_system_prompt()`（若尚未實作 `build_system_prompt`，可暫用 `SYSTEM_TEXT` 串 `TOOL_INSTRUCTION` 的替身函式，但 MR-27 須改回正式版）。
- `reply_text, turn_messages = run_react_turn(llm_with_tools, system_prompt, past, user_text)`。
- `turns.append(turn_messages)`。

### 驗收條件

- 多輪對話 + 算術工具路徑可跑通。
- 能說明：`turn_messages` 與 `turns` 的關係？

### 提示（選讀）

> wiki「函式與模組」：把複雜迴圈收進函式後 `main` 變薄。

### 藍本對應程式（`memory_react_agent.py` 行 217–242）

完整 `main` 迴圈（含 `run_react_turn`）。

```python
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
```

---

## Challenge MR-24：`_ensure_memory_dir`

### 情境

第一次寫入前確保資料夾存在。

### 規格

- `_ensure_memory_dir() -> None`：`_MEMORY_DIR.mkdir(parents=True, exist_ok=True)`。

### 驗收條件

- 刪除本機 `memory/` 後再跑相關函式，目錄會被建立。
- 能說明：`exist_ok=True` 避免什麼錯誤？

### 提示（選讀）

> wiki「檔案與例外處理」：目錄建立。

### 藍本對應程式（`memory_react_agent.py` 行 35–36）

```python
def _ensure_memory_dir() -> None:
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
```

---

## Challenge MR-25：`_ensure_memory_files`

### 情境

確保兩個檔案存在（可為空檔）。

### 規格

- 呼叫 `_ensure_memory_dir()`，再對 `_MEMORY_FILE`、`_HISTORY_FILE` 執行 `touch(exist_ok=True)`（或等價「不存在則建立空檔」）。

### 驗收條件

- 首次執行後兩檔皆存在。
- 能說明：`MEMORY.md` 與 `HISTORY.md` 分工差異？（快照 vs 追加流水。）

### 提示（選讀）

> wiki「檔案與例外處理」：檔案存在性。

### 藍本對應程式（`memory_react_agent.py` 行 39–43）

```python
def _ensure_memory_files() -> None:
    """首次執行時建立記憶檔，避免後續流程讀不到檔案。"""
    _ensure_memory_dir()
    _MEMORY_FILE.touch(exist_ok=True)
    _HISTORY_FILE.touch(exist_ok=True)
```

---

## Challenge MR-26：`read_long_term`

### 情境

讀取助教「長期知識」快照。

### 規格

- 先 `_ensure_memory_files()`，再 `read_text(encoding="utf-8")` 回傳 `str`。

### 驗收條件

- 空檔時回傳空字串或僅空白（與藍本「讀取後 `.strip()` 在下一題處理」可二選一，但**行為需自洽**並在 README 或註解寫清）。
- 能說明：為什麼用 UTF-8？

### 提示（選讀）

> wiki「檔案與例外處理」：讀取文字檔。

### 藍本對應程式（`memory_react_agent.py` 行 46–49）

```python
def read_long_term() -> str:
    """讀取目前長期知識（檔案不存在時回傳空字串）。"""
    _ensure_memory_files()
    return _MEMORY_FILE.read_text(encoding="utf-8")
```

---

## Challenge MR-27：`write_long_term` 與 `get_memory_context`

### 情境

覆寫快照；並把快照轉成「可塞進 system」的一段標題區塊。

### 規格

- `write_long_term(content: str)`：確保檔案存在後**整檔覆寫** UTF-8。
- `get_memory_context()`：若 `read_long_term().strip()` 為空則回 `""`；否則回 `"## Long-term Memory\n\n" + body`（`body` 為去掉首尾空白後內文）。

### 驗收條件

- 寫入一段文字後，`get_memory_context()` 非空且含標題列。
- 能說明：為什麼空記憶時回空字串而不是固定寫「無」？

### 提示（選讀）

> wiki「運算與輸入輸出」：字串拼接與空字串語意。

### 藍本對應程式（`memory_react_agent.py`）

`write_long_term`（行 52–55）：

```python
def write_long_term(content: str) -> None:
    """覆寫長期記憶檔（現狀快照）。"""
    _ensure_memory_files()
    _MEMORY_FILE.write_text(content, encoding="utf-8")
```

`get_memory_context`（行 67–72）：

```python
def get_memory_context() -> str:
    """供 system prompt 注入；無內容時回傳空字串（呼叫端可不退化區塊）。"""
    body = read_long_term().strip()
    if not body:
        return ""
    return "## Long-term Memory\n\n" + body
```

---

## Challenge MR-28：`append_history`

### 情境

把時間戳摘要寫入流水檔，與快照檔分離。

### 規格

- 每筆格式：`[{YYYY-MM-DD HH:MM}] {entry}\n`（與藍本同精神；時間格式可微調但須可讀）。
- 以 **append** 模式開啟 `_HISTORY_FILE`。

### 驗收條件

- 連續呼叫兩次後檔案至少兩行。
- 能說明：為什麼用追加而不是覆寫？

### 提示（選讀）

> wiki「檔案與例外處理」：開啟模式 `a`。

### 藍本對應程式（`memory_react_agent.py` 行 58–64）

```python
def append_history(entry: str) -> None:
    """追加一筆歷史摘要；每筆自動加上 [YYYY-MM-DD HH:MM] 前綴。"""
    _ensure_memory_files()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    line = f"[{ts}] {entry.strip()}\n"
    with _HISTORY_FILE.open("a", encoding="utf-8") as f:
        f.write(line)
```

---

## Challenge MR-29：`build_system_prompt`（順序與藍本一致）

### 情境

把「人設、長期記憶區塊、工具規則」合成單一字串送進 `SystemMessage`。

### 規格

- `mem = get_memory_context()`。
- `parts = [SYSTEM_TEXT, TOOL_INSTRUCTION]`；若 `mem` 非空則 `parts.insert(1, mem)`（順序為 **SYSTEM →（可選）MEM → TOOL**）。
- `return "\n\n".join(parts)`。

### 驗收條件

- 無記憶檔內容時，system 仍含工具規則。
- 有記憶時，三者順序正確（可用 `print` 或檔案目測）。
- 能說明：`insert(1, mem)` 而不是 `append` 的理由？

### 提示（選讀）

> wiki「資料結構」：`list` 插入位置。

### 藍本對應程式（`memory_react_agent.py` 行 75–81）

```python
def build_system_prompt() -> str:
    """基底 system、長期記憶區塊、與工具使用規則合併。"""
    mem = get_memory_context()
    parts = [SYSTEM_TEXT, TOOL_INSTRUCTION]
    if mem:
        parts.insert(1, mem)
    return "\n\n".join(parts)
```

---

## Challenge MR-30：`request_cost_chars`

### 情境

在送模前用字元長度做**假成本**（近似 token 預算題）。

### 規格

- 簽名：`request_cost_chars(system_text: str, past: Iterable[BaseMessage], current_user_content: str) -> int`。
- 回傳 `len(system_text) + sum(len(m.content or "") for m in past) + len(current_user_content)`。

### 驗收條件

- `past` 為空時，成本僅 system + 本輪 user。
- 能說明：為什麼 `m.content` 可能是 `None` 要用 `or ""`？

### 提示（選讀）

> wiki「運算與輸入輸出」：累加與空值處理。

### 藍本對應程式（`memory_react_agent.py` 行 91–100）

```python
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
```

---

## Challenge MR-31：`adjust_last_consolidated_if_over_budget`

### 情境

超過 `TOKEN_BUDGET` 時，丟棄**最舊一整輪**（含工具鏈），直到成本落在 `budget // 2` 以下或無輪可丟。

### 規格

- 參數：`turns, last_consolidated, current_user_content, budget, system_text`（與藍本一致）。
- 先用 `_flatten_turns` 取得 `past`，計算 `request_cost_chars`；未超 `budget` 則直接回傳 `last_consolidated`。
- 超標時以 `target = budget // 2`，迴圈中每次 `last_consolidated += 1`，直到成本達標或 `last_consolidated >= len(turns)`。

### 驗收條件

- 人工塞長字串或 mock 大量 `turns` 時，索引會前進且程式不崩潰。
- 能說明：為什麼裁切單位是「輪」而不是「單則訊息」？（與工具鏈完整性。）

### 提示（選讀）

> wiki「條件判斷與迴圈」：`while True` 與終止條件。

### 藍本對應程式（`memory_react_agent.py` 行 103–125）

```python
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
```

---

## Challenge MR-32：`main` 接上預算裁切與 `past`

### 情境

每輪在呼叫 `run_react_turn` 前更新 `last_consolidated` 與 `past`。

### 規格

- 維持 `turns: list[list[BaseMessage]]` 與 `last_consolidated = 0`。
- 每輪：`system_prompt = build_system_prompt()`；`last_consolidated = adjust_last_consolidated_if_over_budget(...)`；`past = _flatten_turns(turns, last_consolidated)`。

### 驗收條件

- 在長對話下（可人工製造）仍不會無限增長送模內容至明顯超線（以你的成本函式為準）。
- 能說明：`last_consolidated` 變大時，模型「看不到」什麼？

### 提示（選讀）

> wiki「資料結構」：滑動視窗在巢狀 `turns` 上的實作。

### 藍本對應程式（`memory_react_agent.py` 行 231–235）

預算裁切與 `_flatten_turns` 取 `past`。

```python
        system_prompt = build_system_prompt()
        last_consolidated = adjust_last_consolidated_if_over_budget(
            turns, last_consolidated, user_text, TOKEN_BUDGET, system_prompt
        )
        past = _flatten_turns(turns, last_consolidated)
```

---

## Challenge MR-33：`TOOL_INSTRUCTION` 已進 `build_system_prompt` 的端到端自檢

### 情境

確認模型收到的 system **一定**含工具規則（避免只在別處字串拼接而漏接）。

### 規格

- 在程式或 README 註明：最終送進 `run_react_turn` 的 `system_text` 必須來自 `build_system_prompt()`（不得另用未含 `TOOL_INSTRUCTION` 的替身）。

### 驗收條件

- 實際一輪對話中，請模型做加法時會走工具（課堂固定測句即可）。
- 能說明：若把工具規則只寫在註解而不進 system，會發生什麼事？

### 提示（選讀）

> 對照藍本 `build_system_prompt` 與 `run_react_turn` 呼叫點。

### 藍本對應程式（`memory_react_agent.py` 行 75–81）

`build_system_prompt`；與主程式 `system_prompt = build_system_prompt()` 併讀。

```python
def build_system_prompt() -> str:
    """基底 system、長期記憶區塊、與工具使用規則合併。"""
    mem = get_memory_context()
    parts = [SYSTEM_TEXT, TOOL_INSTRUCTION]
    if mem:
        parts.insert(1, mem)
    return "\n\n".join(parts)
```

---

## Challenge MR-34：未知工具名稱時的行為

### 情境

模型若幻覺出不存在工具名，agent 不可崩潰。

### 規格

- `_TOOL_MAP.get(name)` 為 `None` 時，`ToolMessage` 內容為明確錯誤字串（例如 `Unknown tool: ...`）。

### 驗收條件

- 可透過暫時改名／mock 等方式演示錯誤字串進 `ToolMessage` 後迴圈可繼續。
- 能說明：為什麼錯誤要回給模型看而不是直接 `raise`？

### 提示（選讀）

> wiki「檔案與例外」精神遷移：錯誤資料亦為「可處理訊息」。

### 藍本對應程式（`memory_react_agent.py` 行 197–198）

未知工具名稱分支。

```python
                if tool_obj is None:
                    tool_result: str | float = f"Unknown tool: {name}"
```

---

## Challenge MR-35：程式結構整理（區塊註解與可讀順序）

### 情境

教練／同伴讀 code 時能快速定位：常數、記憶、工具、預算、react、main。

### 規格

- 以註解分隔至少四區：`# --- 記憶檔 ---`、`# --- 工具 ---`、`# --- 預算與展開 ---`、`# --- ReAct 單輪 ---`（名稱可微調，須一眼可辨）。

### 驗收條件

- 另一人可在 2 分鐘內找到 `run_react_turn` 與 `adjust_last_consolidated_if_over_budget`。
- 能說明：你為何把某函式放在該區塊？

### 提示（選讀）

> wiki「函式與模組」：模組內編排與可維護性。

### 藍本對應程式（`memory_react_agent.py` 行 18–21）

路徑常數區；另見行 128 `# --- 工具（react.py）---`。

```python
# 記憶檔與專案根目錄同層的 memory/
_MEMORY_DIR = Path(__file__).resolve().parent / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"
```

---

## Challenge MR-36：行為對照藍本的手動驗收清單（整合）

### 情境

最後一圈確認與 `memory_react_agent.py` 功能對齊：REPL、quit、工具、長期記憶檔、預算裁切。

### 規格

- 在 `README.md`（若尚無則建立極簡版）寫 5 條以內「自測要點」（不需長劇本；每條一句行為描述即可），涵蓋：環境變數、一輪算術工具、多輪上下文、`memory/` 兩檔存在、長對話下裁切仍可回覆。

### 驗收條件

- 依你自己寫的 5 條逐條操作皆可通過。
- 能用自己的話說明：**本輪**訊息從 `input` 到 `print("助手:…")` 中間經過哪些主要步驟（至少 4 步，順序正確）。

### 提示（選讀）

> peas-challenge-coach 驗收時：程式行為先、理解題後；執行請用 `uv run main.py`。

### 藍本對應程式（`memory_react_agent.py` 行 217–248）

完整 `main` 與 `if __name__`。

```python
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
```

---

## Challenge MR-37（選修）：`_normalize_tool_args` 的 `unittest`

### 情境

對「純函式」寫最小單元測試，對照 wiki「類別與單元測試」。

### 規格

- 新增 `tests/test_normalize_tool_args.py`（或專案慣例路徑），至少 2 個案例：一般 dict 不變、巢狀 `value` 被攤平。
- 使用 `unittest`（與課程 wiki 一致）；**不要求** pytest。

### 驗收條件

- `uv run python -m unittest`（或你在 README 寫明的單一檔測試指令）可通過。
- 能說明：為什麼先測「純函式」而不是整段 `invoke`？

### 提示（選讀）

> wiki「類別與單元測試」：`unittest` 基本結構。

### 藍本對應程式（`memory_react_agent.py` 行 162–168）

藍本僅函式本體；`unittest` 檔請於作答專案自行新增。

```python
def _normalize_tool_args(tool_input: dict) -> dict:
    """修正 Ollama 等後端可能回傳的巢狀 {'key': {'type': '...', 'value': ...}} 格式。"""
    normalized = dict(tool_input)
    for key, value in list(normalized.items()):
        if isinstance(value, dict) and "value" in value:
            normalized[key] = value["value"]
    return normalized
```

---

## Challenge MR-38（選修）：`try`／`except` 包住讀檔失敗（仍不崩潰）

### 情境

磁碟滿權限等極端狀況下，讀檔不應讓整支 agent 直接 traceback（選修加深）。

### 規格

- 在 `read_long_term`（或集中讀檔處）對 `OSError`／`UnicodeDecodeError` 之一或兩者做捕捉，回傳**固定說明字串**或記錄到 stderr 後回空字串；**行為须在註解或 README 寫清**。

### 驗收條件

- 可透過暫時改壞路徑等方式演示「不崩潰」路徑（教練見證即可）。
- 能說明：**吞掉例外**與**回傳錯誤字串給模型**的取捨你選哪一邊？為什麼？

### 提示（選讀）

> wiki「檔案與例外處理」：`try-except` 與錯誤語意。

### 藍本對應程式（`memory_react_agent.py` 行 46–49）

藍本未包 `try/except`；選修請在 `read_long_term` 自行擴充。

```python
def read_long_term() -> str:
    """讀取目前長期知識（檔案不存在時回傳空字串）。"""
    _ensure_memory_files()
    return _MEMORY_FILE.read_text(encoding="utf-8")
```

---

## 建議操作方式（AI coding）

1. 依序完成 **MR-01→MR-36**；選修 **MR-37、MR-38** 可視課堂時間決定是否做。
2. 使用 **peas-challenge-coach** 時：每個 `## Challenge MR-xx` 視為一題；**進度條 N＝36**（僅必做 MR-01～MR-36）。
3. 需要 AI 輔助時：先完成教練流程的對齊條列與六欄提示詞，再請 coding agent 修改 `main.py`，並附上 `@main.py` 與本檔對應 Challenge 段落。

---

## 與交付物對照（工作坊備註）


| 建議交付物       | 本專案對應                   |
| ----------- | ----------------------- |
| README.md   | 學生操作手冊、環境與 MR-36 自測要點   |
| chatbot／主程式 | `main.py`               |
| 題目與驗收（本組）   | 本檔 `challenges.md`      |
| 功能藍本（自讀）    | `memory_react_agent.py` |


