# 進階練習題（Challenge M2-01～）— Agent 能力演進版

完成 `example.py` 的 agent 引導學習並勾選 `example-learning-checklist.md` 後，在 **`main.py`** 上依序實作下列挑戰。本檔為**本題組**的單一規格來源（含各題驗收條件）。功能藍本為專案內之 [`memory_react_agent.py`](./memory_react_agent.py)。

**與 `challenges.md`（MR-xx）的差異**：`challenges.md` 以**語法／模組細部**為主軸細拆多題；**本檔（M2-xx）**以 **Agent 能力由簡到繁** 排序（能回話 → 多輪 → 工具 → 檔案記憶 → 預算裁切 → 完整整合），單題涵蓋範圍較大以利「每題皆可獨立驗收」。教師可擇一為課堂主線，另一作對照或自修。

**檔案角色**：`example.py` 僅供對照、勿改；作答與執行以 `main.py` 為主。

**ITS Python wiki 對照**（七份統整條目；與課程 LLM Wiki `wiki/index.md`「教材統整／Python」一致；本機路徑常見為 `G:\我的雲端硬碟\Obsidian\Agent\wiki\`）：

| 序 | 學習主軸（由簡入繁） | wiki 條目檔名（統整頁） |
|----|----------------------|-------------------------|
| 1 | 基礎資料與變數 | `Python-基礎資料與變數.md` |
| 2 | 運算與輸入輸出 | `Python-運算與輸入輸出.md` |
| 3 | 條件判斷與迴圈 | `Python-條件判斷與迴圈.md` |
| 4 | 資料結構（串列等） | `Python-資料結構-串列元組字典.md` |
| 5 | 函式與模組 | `Python-函式與模組.md` |
| 6 | 檔案與例外處理 | `Python-檔案與例外處理.md` |
| 7 | 類別與單元測試 | `Python-類別與單元測試.md` |

- **必做**：M2-01～M2-23，共 **23** 題（peas-challenge-coach 進度條 **N＝23**）。
- **選修**：M2-25、M2-26，共 **2** 題（不計入 N；完成可記「挑戰加分」）。

每題在「### 提示（選讀）」之後附有 **### 藍本對應程式**：節錄自 `memory_react_agent.py`，**行號以該檔目前版本為準**（若藍本變更請同步更新節錄）。

---

## Challenge M2-01：可執行的 agent 程式殼（主程式掛點與依賴就緒）

### 情境

工作坊要一支 **`main.py` 當唯一執行入口**：之後會在這裡接上「讀使用者輸入 → 呼叫模型 → 工具與記憶」等**行為**。本題的**使用者可感知功能**只有一件：**用 `uv run` 能從入口跑進程式並正常結束**（尚無對話、無 API、無檔案）。  
`import` 只是在宣告「接下來幾題會用到的能力」所需的符號（環境、時間、路徑型別、訊息型別、工具裝飾器、聊天客戶端），**不是題目主旨**；路徑與磁碟則留到真的要寫檔時再一起做（見 M2-16）。

### ITS 學習對照

- **5 函式與模組**：可執行腳本結構、`main` 掛點、`if __name__ == "__main__"` 與模組邊界。
- **1 基礎資料與變數**：模組文件、`__future__` 與之後 `list[BaseMessage]` 等註記的銜接。

### 規格（依「功能／行為」條列；匯入列在最後作為實作手段）

- **程式入口**：檔案末尾具 `if __name__ == "__main__":`，且會呼叫頂層 `main()`（**不要**在此題做 `OPENAI_API_KEY` 檢查，留給 M2-03）。
- **主流程掛點**：頂層 `def main() -> None:`；內容可為 `pass`，或暫印一行固定字串（例如「骨架就緒」）以證明入口有跑到 `main`。
- **模組自述**：檔案頂部有模組 `"""..."""`（一句話交代：記憶＋ReAct 助教迴圈之後會長在此檔）。
- **型別註記友善**：`from __future__ import annotations`（位置須符合 Python 官方對 `__future__` 的要求）。
- **後續行為的依賴先就緒**（本題仍不必呼叫任何 API／不建立 `_MEMORY_*`）：在模組頂層匯入 `os`、`datetime`、`Path`、`Iterable`，以及 `AIMessage`、`BaseMessage`、`HumanMessage`、`SystemMessage`、`ToolMessage`、`tool`、`ChatOpenAI`（來源與藍本一致即可）。**本題不要求**實際使用 `Path` 或定義 `_MEMORY_*`（僅先匯入，減少之後題目來回改動）。

### 驗收條件

- [ ] 從使用者角度：**執行** `main.py` 會進入 `main` 並結束、無語法錯誤（以 `uv run main.py` 驗收；不要求已呼叫 API）。
- [ ] 能說明：`from __future__ import annotations` 與之後寫 `list[BaseMessage]` 一類註記的關係？

### 提示（選讀）

> 把六欄裡的 Task 寫成「做出可跑的入口與 `main` 掛點」，匯入寫成「為後續題預留符號」的一句附帶要求即可，避免整段都在列 `import`。wiki「函式與模組」：腳本入口；wiki「基礎資料與變數」：模組文件與 `__future__`。

### 藍本對應程式（`memory_react_agent.py` 行 1–16）

（路徑常數見藍本行 18–21，於 **M2-16** 與檔案建立一併實作即可。）

```python
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
```

---

## Challenge M2-02：人設、工具規則與送模預算常數

### 情境

模型每次都要帶同一段「我是誰、怎麼回答」；算術要走工具；上下文不能無限長。把三者抽成常數，之後組 `system` 與裁切會用到。

### ITS 學習對照

- **1 基礎資料與變數**：多行字串、`int` 常數、避免魔法數字。
- **2 運算與輸入輸出**：字串拼接語意（之後與 `join` 搭配）。

### 規格

- `SYSTEM_TEXT`：繁體中文助教敘述（須含：繁中、先結論再補充、資訊不足先澄清）。
- `TOOL_INSTRUCTION`：要求算術必須呼叫四工具名稱、禁止純文字心算。
- `TOKEN_BUDGET`：`8000`（字元級近似上限，與藍本同名同義）。

### 驗收條件

- [ ] 三常數皆存在且型別正確。
- [ ] 能說明：`TOKEN_BUDGET` 預計用在程式的哪一段流程？

### 提示（選讀）

> wiki「基礎資料與變數」：字串常數與命名。

### 藍本對應程式（`memory_react_agent.py` 行 23–32）

```python
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
```

---

## Challenge M2-03：程式進入點與 API 金鑰檢查

### 情境

沒有金鑰就不應默默連線；在進入 `main()` 前先檢查環境變數。

### ITS 學習對照

- **2 運算與輸入輸出**：從環境讀取設定（`os.environ`）。
- **3 條件判斷與迴圈**：`if` 守門、不符合則中止程式。

### 規格

- **改寫** M2-01 已寫好的**單一** `if __name__ == "__main__":` 區塊（**勿**重複兩段 `if __name__`）：區塊內先檢查 `OPENAI_API_KEY`；缺則 `raise SystemExit("請設定 OPENAI_API_KEY")`（訊息可微調，須繁中友善）。
- 有值才呼叫 `main()`。

### 驗收條件

- [ ] 未設金鑰時 `uv run main.py` 以非零退出並有提示。
- [ ] 能說明：為什麼不把 key 寫死在程式裡？

### 提示（選讀）

> wiki「運算與輸入輸出」：環境變數與設定分離。

### 藍本對應程式（`memory_react_agent.py` 行 245–248）

```python
if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("請設定 OPENAI_API_KEY")
    main()
```

---

## Challenge M2-04：終端互動迴圈（REPL 骨架）

### 情境

使用者要能一直輸入、直到輸入離開指令為止。

### ITS 學習對照

- **2 運算與輸入輸出**：`print`、`input`、字串方法。
- **3 條件判斷與迴圈**：`while True`、`break` 與離開條件。

### 規格

- `main()` 內 `print` 說明如何離開（例如「輸入 quit 結束」）。
- `while True`：`user_text = input("你: ").strip()`；若 `user_text.lower() == "quit"` 則 `break`。
- 此題尚**不要求**呼叫模型。

### 驗收條件

- [ ] 輸入 `quit` 可結束程式。
- [ ] 能說明：`.strip()` 在這裡解決什麼問題？

### 提示（選讀）

> wiki「條件判斷與迴圈」：`while` 與終止條件。

### 藍本對應程式（`memory_react_agent.py` 行 225–229）

```python
    print("輸入 quit 結束。\n")
    while True:
        user_text = input("你: ").strip()
        if user_text.lower() == "quit":
            break
```

---

## Challenge M2-05：建立 `ChatOpenAI` 客戶端

### 情境

接上 OpenAI 相容聊天端點，後續才能 `invoke`。

### ITS 學習對照

- **5 函式與模組**：使用第三方類別建構子、參數語意。
- **2 運算與輸入輸出**：從環境讀取敏感設定（與 M2-03 呼應）。

### 規格

- 建立 `ChatOpenAI(model="gpt-4o-mini", temperature=0.2, ...)`。
- `api_key` 須來自 `os.environ.get("OPENAI_API_KEY")`（或與 M2-03 一致來源）；**禁止**寫死 secret。若藍本暫未帶 `api_key` 參數，作答時仍須補上以符合本題。

### 驗收條件

- [ ] 有金鑰時可建立 `llm` 物件不報錯。
- [ ] 能一句話說明：`temperature=0.2` 大致代表什麼？

### 提示（選讀）

> LangChain 文件：`ChatOpenAI` 建構子（內部自讀即可）。

### 藍本對應程式（`memory_react_agent.py` 行 217–218）

```python
def main() -> None:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
```

（作答時請補上 `api_key=os.environ.get("OPENAI_API_KEY")` 等寫法以滿足本題規格。）

---

## Challenge M2-06：單輪無工具——第一次 `invoke`

### 情境

先驗證「送得進模型、拿得到字串」，再疊歷史與工具。

### ITS 學習對照

- **3 條件判斷與迴圈**：控制每輪流程（本題僅單次呼叫）。
- **4 資料結構**：以串列表達有序訊息 `messages`。

### 規格

- 每輪建立 `messages = [SystemMessage(content=SYSTEM_TEXT), HumanMessage(content=user_text)]`（`SYSTEM_TEXT` 可來自 M2-02）。
- `reply = llm.invoke(messages)`，並 `print("助手:", reply.content)`。
- **不要求** `bind_tools`；**不要求**寫入 `history`。

### 驗收條件

- [ ] 連續兩輪皆可得到模型回覆（第二輪可不延續第一輪語境亦可）。
- [ ] 能說明：`SystemMessage` 放在串列最前面，對模型行為代表什麼？

### 提示（選讀）

> wiki「資料結構」：串列作為有序容器。

### 藍本對應程式（`memory_react_agent.py` 行 181–185）

（藍本此段在 `run_react_turn` 內；本題練習時可直接在 `main` 內組等價兩則訊息並 `llm.invoke`。）

```python
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *past,
        HumanMessage(content=user_text),
    ]
```

---

## Challenge M2-07：扁平短期記憶（多輪上下文）

### 情境

使用者希望第二輪起模型「記得」前面說過的話；先把多輪存在單層 `history`。

### ITS 學習對照

- **4 資料結構**：`list` 與 `append`、展開 `*history` 送進模型。
- **5 函式與模組**：把一輪流程收斂在迴圈內可讀。

### 規格

- `history: list[BaseMessage] = []`。
- 每輪在 `invoke` **之後**依序 `append(HumanMessage(...))`、`append(AIMessage(...))`。
- 下一輪訊息為 `[SystemMessage(SYSTEM_TEXT), *history, HumanMessage(...)]`。

### 驗收條件

- [ ] 第二輪起模型能延續第一輪話題（簡單自測）。
- [ ] 能說明：為什麼要在 `invoke` 之後才 `append`？

### 提示（選讀）

> wiki「資料結構」：串列累積狀態。

### 藍本對應程式（`memory_react_agent.py` 行 181–186）

（藍本以 `run_react_turn` 的 `*past` 表達「展開歷史」；本題用扁平 `history` 時語意相同。）

```python
    messages: list[BaseMessage] = [
        SystemMessage(content=system_text),
        *past,
        HumanMessage(content=user_text),
    ]
    past_and_user_count = 1 + len(past)
```

---

## Challenge M2-08：一輪一子串列——`turns` 與 `_flatten_turns`

### 情境

之後每輪可能含多則 `ToolMessage`，不能再假設一輪只有兩則訊息；改為「一輪＝一個子串列」，並能展開送模。

### ITS 學習對照

- **4 資料結構**：巢狀串列、`extend`、切片子範圍。
- **5 函式與模組**：純函式 `_flatten_turns` 分離展開邏輯。

### 規格

- `turns: list[list[BaseMessage]]`；每輪結束 `append` 一個子 list（至少含本輪 `HumanMessage` 與最終 `AIMessage`，若尚無工具則兩則即可）。
- 實作 `_flatten_turns(turns, start_turn) -> list[BaseMessage]`，對 `turns[start_turn:]` 內各子串列 `extend` 到同一輸出。

### 驗收條件

- [ ] `len(turns)` 等於已完成輪數；`_flatten_turns(turns, 0)` 長度等於所有訊息數之和。
- [ ] 能說明：`turns[i]` 與「一輪對話」的對應關係？

### 提示（選讀）

> wiki「資料結構」：巢狀結構與走訪。

### 藍本對應程式（`memory_react_agent.py` 行 84–88）

```python
def _flatten_turns(turns: list[list[BaseMessage]], start_turn: int) -> list[BaseMessage]:
    out: list[BaseMessage] = []
    for t in turns[start_turn:]:
        out.extend(t)
    return out
```

---

## Challenge M2-09：第一支工具與 `bind_tools`

### 情境

讓模型能「呼叫」加法；先只做一支工具與 `bind_tools`，驗證 tool schema 接上。

### ITS 學習對照

- **5 函式與模組**：`@tool` 裝飾器、可呼叫物件給模型。
- **3 條件判斷與迴圈**：之後在 ReAct 迴圈依 `tool_calls` 分支（本題可先手動測 `invoke`）。

### 規格

- `@tool` 的 `add_numbers(a: float, b: float) -> float`。
- `llm_with_tools = llm.bind_tools([add_numbers])`（或含其他工具；本題至少含加法）。
- 能在一輪對話中觸發至少一次 tool 呼叫路徑（課堂可用固定測句）。

### 驗收條件

- [ ] `add_numbers.invoke({"a": 1, "b": 2})` 數值正確。
- [ ] 能說明：`bind_tools` 與裸 `llm.invoke` 差在哪？

### 提示（選讀）

> wiki「函式與模組」：裝飾器與函式簽名。

### 藍本對應程式（`memory_react_agent.py` 行 131–134、157、219）

```python
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b
```

```python
TOOLS = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]
```

```python
    llm_with_tools = llm.bind_tools(TOOLS)
```

（本題最少需 `add_numbers` + `bind_tools`；可逐步補齊 `TOOLS` 內其他工具至 M2-10。）

---

## Challenge M2-10：四則工具、除零、註冊表

### 情境

補齊算術工具並以名稱對應到可呼叫物件，主迴圈之後才可避免巨型 `if/elif`。

### ITS 學習對照

- **3 條件判斷與迴圈**：`divide` 除零時走錯誤字串分支、不中斷程式。
- **4 資料結構**：`dict` 做名稱對應（`_TOOL_MAP`）。
- **5 函式與模組**：多個 `@tool` 與列表彙整。

### 規格

- `subtract_numbers`、`multiply_numbers`、`divide_numbers` 皆為 `@tool`；除數為 0 時回傳繁中錯誤字串。
- `TOOLS = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]`。
- `_TOOL_MAP = {t.name: t for t in TOOLS}`（或等價）。

### 驗收條件

- [ ] 四則皆可 `invoke`；除零回字串不拋例外。
- [ ] 能說明：字典 `_TOOL_MAP` 在執行 tool 時扮演什麼角色？

### 提示（選讀）

> wiki「資料結構」：字典鍵值對應。

### 藍本對應程式（`memory_react_agent.py` 行 131–159）

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


TOOLS = [add_numbers, subtract_numbers, multiply_numbers, divide_numbers]

_TOOL_MAP = {t.name: t for t in TOOLS}
```

---

## Challenge M2-11：工具參數正規化（Ollama 風格）

### 情境

部分本機後端會回傳巢狀 `{'key': {'value': ...}}`；要攤平成 `invoke` 吃得下的 `dict`。

### ITS 學習對照

- **4 資料結構**：走訪 dict、辨識巢狀結構、安全拷貝。
- **5 函式與模組**：純函式 `_normalize_tool_args` 利於測試（選修 M2-25）。

### 規格

- 實作 `_normalize_tool_args(tool_input: dict) -> dict`：若值為含 `"value"` 鍵的 `dict`，則替換為該 `value`。

### 驗收條件

- [ ] 輸入 `{"a": {"type": "number", "value": 3}}` 時輸出含扁平化後的 `a`。
- [ ] 能舉一例：不正規化時會在哪一步失敗？

### 提示（選讀）

> wiki「資料結構」：`dict` 與 `list(...items())` 避免迭代中修改問題。

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

## Challenge M2-12：`run_react_turn`——訊息串與切片基準

### 情境

把「一輪使用者輸入」封進函式：先完成訊息串開頭與「本輪從哪裡切出」的索引基準。

### ITS 學習對照

- **5 函式與模組**：函式簽名、`tuple` 回傳型別註記。
- **4 資料結構**：`*past` 展開、`len` 與索引語意。

### 規格

- 簽名與藍本一致：`run_react_turn(llm_with_tools, system_text, past, user_text) -> tuple[str, list[BaseMessage]]`。
- 建立 `messages = [SystemMessage(...), *past, HumanMessage(...)]`。
- `past_and_user_count = 1 + len(past)` 並以註解說明用途。

### 驗收條件

- [ ] `past` 為空時，`messages` 長度為 2。
- [ ] 能指出：`past_and_user_count` 對應到切片的哪個邊界？

### 提示（選讀）

> wiki「函式與模組」：參數化行為、降低 `main` 複雜度。

### 藍本對應程式（`memory_react_agent.py` 行 171–186）

```python
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
```

---

## Challenge M2-13：`run_react_turn`——工具迴圈（`tool_calls` 與 `ToolMessage`）

### 情境

模型要求工具時：把 assistant 訊息與每則工具結果接回 `messages`，再讓模型繼續推理。

### ITS 學習對照

- **3 條件判斷與迴圈**：`while True`、依 `tool_calls` 分支。
- **5 函式與模組**：查表執行工具、組裝 `ToolMessage`。

### 規格

- `while True` 內 `response = llm_with_tools.invoke(messages)`。
- 若 `response.tool_calls`：`append(response)`；對每個 `tool_call` 正規化 args、查 `_TOOL_MAP`、append `ToolMessage`（含正確 `tool_call_id`）。
- 未知工具名稱時：`ToolMessage` 內容為明確錯誤字串（與藍本一致）。

### 驗收條件

- [ ] 簡單算術可走完一輪以上工具再得到文字結論。
- [ ] 能說明：`tool_call_id` 的用途？

### 提示（選讀）

> 對照藍本 `run_react_turn` 中段；勿在迴圈外遺漏 `append`。

### 藍本對應程式（`memory_react_agent.py` 行 188–203）

```python
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
```

---

## Challenge M2-14：`run_react_turn`——收尾與回傳本輪訊息鏈

### 情境

模型不再呼叫工具時：收斂迴圈，並只把「本輪從使用者訊息起」的片段交給短期記憶結構。

### ITS 學習對照

- **3 條件判斷與迴圈**：`else` 分支離開 `while`。
- **4 資料結構**：切片、`reversed` 或從末端找最後一則 `AIMessage`。

### 規格

- 無 `tool_calls`：`messages.append(response)` 後 `break`。
- `turn_messages = messages[past_and_user_count:]`。
- 取 `turn_messages` 中**最後一則** `AIMessage` 的 `content` 為 `final_text`（去空白）；回傳 `(final_text, turn_messages)`。

### 驗收條件

- [ ] `turn_messages[0]` 為 `HumanMessage`。
- [ ] 能說明：為什麼 `final_ai` 要從 `turn_messages` 末端往前找？

### 提示（選讀）

> wiki「資料結構」：切片與「半開區間」直覺。

### 藍本對應程式（`memory_react_agent.py` 行 204–214）

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

## Challenge M2-15：`main` 接上 ReAct 與 `turns`（先不接檔案記憶與裁切）

### 情境

把 REPL 接到 `run_react_turn` 與 `turns`；此階段專注「多輪＋工具」閉環，檔案記憶與預算在後續題目再接。

### ITS 學習對照

- **5 函式與模組**：`main` 組裝呼叫、維持狀態 `turns`。
- **4 資料結構**：每輪 append 子串列。

### 規格

- `turns: list[list[BaseMessage]] = []`；`llm_with_tools` 與 M2-09／10 一致。
- 每輪：`system_prompt` 可暫用 `"\n\n".join([SYSTEM_TEXT, TOOL_INSTRUCTION])`**不**呼叫 `build_system_prompt`（檔案函式尚未接好時）；`past = _flatten_turns(turns, 0)`；呼叫 `run_react_turn` 後 `turns.append(turn_messages)`；印出助手回覆。
- M2-19 之後改為呼叫 `build_system_prompt()` 與裁切邏輯。

### 驗收條件

- [ ] 多輪對話＋算術工具路徑可跑通（不依賴 `MEMORY.md` 內容亦可）。
- [ ] 能說明：為什麼此題先不接 `build_system_prompt` 也能驗收？

### 提示（選讀）

> 漸進式整合：先固定 system 字串，再換成讀檔組字。

### 藍本對應程式（`memory_react_agent.py` 行 217–242）

（藍本已含 `build_system_prompt` 與裁切；本題作答可暫用註解區隔，至 M2-21 再與藍本對齊。）

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

## Challenge M2-16：記憶路徑常數、建立目錄與空檔

### 情境

程式即將開始讀寫「助教筆記」檔案；此時再定義 **`memory/` 與兩個檔名** 最自然：與「真的要碰磁碟」同一個交付單元，coding agent 的 Task 也較好寫成「路徑 → 建目錄 → 建空檔」，不必在第一題就預先承諾尚未用到的檔案配置。

### ITS 學習對照

- **1 基礎資料與變數**：以具名常數保存路徑；`Path` 與字串差異。
- **6 檔案與例外處理**：相對於 `__file__` 的目錄配置、`mkdir`、`touch`、存在性。
- **5 函式與模組**：小函式拆分 `_ensure_memory_dir`／`_ensure_memory_files`。

### 規格

- **路徑常數**（與藍本同語意，置於 `_ensure_memory_dir` **之上**）：
  - `_MEMORY_DIR`＝`Path(__file__).resolve().parent / "memory"`
  - `_MEMORY_FILE`＝`_MEMORY_DIR / "MEMORY.md"`
  - `_HISTORY_FILE`＝`_MEMORY_DIR / "HISTORY.md"`
- `_ensure_memory_dir`：`mkdir(parents=True, exist_ok=True)`。
- `_ensure_memory_files`：呼叫上一函式後，對 `MEMORY.md`、`HISTORY.md` 執行 `touch(exist_ok=True)`（或等價建立空檔）。

### 驗收條件

- [ ] 三個 `_MEMORY_*` 皆為 `Path`，且 `_ensure_memory_files()` 後路徑指向專案旁的 `memory/` 底下兩檔。
- [ ] 刪除本機 `memory/` 後再執行相關函式，目錄與兩檔會被建立。
- [ ] 能說明：為什麼用 `__file__` 而不是寫死絕對路徑？
- [ ] 能說明：`exist_ok=True`（`mkdir`／`touch`）避免什麼錯誤？

### 提示（選讀）

> wiki「檔案與例外處理」：`Path`、專案相對路徑、目錄與檔案建立。

### 藍本對應程式（`memory_react_agent.py`）

路徑常數（行 18–21）：

```python
# 記憶檔與專案根目錄同層的 memory/
_MEMORY_DIR = Path(__file__).resolve().parent / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"
```

`_ensure_memory_dir`／`_ensure_memory_files`（行 35–43）：

```python
def _ensure_memory_dir() -> None:
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_memory_files() -> None:
    """首次執行時建立記憶檔，避免後續流程讀不到檔案。"""
    _ensure_memory_dir()
    _MEMORY_FILE.touch(exist_ok=True)
    _HISTORY_FILE.touch(exist_ok=True)
```

---

## Challenge M2-17：讀寫長期快照檔（`MEMORY.md`）

### 情境

助教「長期筆記」要以單一檔案做快照：讀出全文、整檔覆寫更新。

### ITS 學習對照

- **6 檔案與例外處理**：`read_text`、`write_text`、`UTF-8`。
- **5 函式與模組**：讀寫分離成函式，先 `_ensure_memory_files`。

### 規格

- `read_long_term() -> str`：先確保檔案存在，再 `read_text(encoding="utf-8")`。
- `write_long_term(content: str) -> None`：先確保檔案存在，再**覆寫** UTF-8。

### 驗收條件

- [ ] 寫入後再讀取可得到相同內容（自測）。
- [ ] 能說明：為什麼用覆寫而不是追加當「快照」？

### 提示（選讀）

> wiki「檔案與例外處理」：文字檔讀寫模式概念。

### 藍本對應程式（`memory_react_agent.py` 行 46–55）

```python
def read_long_term() -> str:
    """讀取目前長期知識（檔案不存在時回傳空字串）。"""
    _ensure_memory_files()
    return _MEMORY_FILE.read_text(encoding="utf-8")


def write_long_term(content: str) -> None:
    """覆寫長期記憶檔（現狀快照）。"""
    _ensure_memory_files()
    _MEMORY_FILE.write_text(content, encoding="utf-8")
```

---

## Challenge M2-18：歷史流水檔（`HISTORY.md` 追加）

### 情境

與快照分離：把帶時間戳的一行一行摘要追加到流水檔。

### ITS 學習對照

- **6 檔案與例外處理**：以 **append** 模式開啟檔案。
- **2 運算與輸入輸出**：`datetime.strftime` 與 f-string 組行。

### 規格

- `append_history(entry: str)`：每筆 `[YYYY-MM-DD HH:MM] entry` 格式（與藍本同精神）；寫入 `_HISTORY_FILE` 採追加。

### 驗收條件

- [ ] 連續呼叫兩次後檔案至少兩行。
- [ ] 能說明：為什麼流水用追加、快照用覆寫？

### 提示（選讀）

> wiki「檔案與例外處理」：`open` 模式 `a`。

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

## Challenge M2-19：組出可注入的記憶區塊與完整 `system` 字串

### 情境

把檔案中的長期文字變成「可塞進 system 的一段」，並與人設、工具規則合併成**單一** `system_text`。

### ITS 學習對照

- **2 運算與輸入輸出**：空字串與非空分支、字串標題前綴。
- **4 資料結構**：`list` 組裝後 `insert(1, mem)` 控制順序。

### 規格

- `get_memory_context()`：若 `read_long_term().strip()` 為空則回 `""`；否則回 `"## Long-term Memory\n\n" + body`。
- `build_system_prompt()`：`parts = [SYSTEM_TEXT, TOOL_INSTRUCTION]`；若 `mem` 非空則 `parts.insert(1, mem)`；`return "\n\n".join(parts)`（順序：**人設 →（可選）記憶 → 工具規則**）。

### 驗收條件

- [ ] 無記憶檔內容時，system 仍含工具規則。
- [ ] 有記憶時三者順序正確。
- [ ] 能說明：為什麼用 `insert(1, mem)` 而不是 `append`？

### 提示（選讀）

> wiki「資料結構」：有序列表插入位置。

### 藍本對應程式（`memory_react_agent.py` 行 67–81）

```python
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
```

---

## Challenge M2-20：送模字元成本與預算裁切（以「輪」為單位）

### 情境

上下文太長時要丟棄**最舊一整輪**（含工具鏈），並用字元長度做假成本估算。

### ITS 學習對照

- **3 條件判斷與迴圈**：`while True` 直到成本落點或無輪可丟。
- **5 函式與模組**：`request_cost_chars` 與 `adjust_last_consolidated_if_over_budget` 分工。
- **4 資料結構**：巢狀 `turns` 與展開後計長度。

### 規格

- `request_cost_chars(system_text, past, current_user_content)`：`len(system_text) + sum(len(m.content or "") for m in past) + len(current_user_content)`。
- `adjust_last_consolidated_if_over_budget`：未超 `budget` 則不動；否則以 `budget // 2` 為目標，每次 `last_consolidated += 1` 丟最舊一輪，直到達標或無輪可丟。

### 驗收條件

- [ ] 人工製造長對話時，索引會前進且程式不崩潰。
- [ ] 能說明：裁切單位為何是「輪」而不是「單則訊息」？

### 提示（選讀）

> wiki「條件判斷與迴圈」：終止條件與不變式（本輪 user 內容始終計入成本）。

### 藍本對應程式（`memory_react_agent.py` 行 91–125）

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

## Challenge M2-21：`main` 完整整合（檔案記憶＋裁切＋ReAct）

### 情境

把 `build_system_prompt`、`adjust_last_consolidated_if_over_budget`、`_flatten_turns` 與 `run_react_turn` 全部接回 `main`，行為與藍本一致。

### ITS 學習對照

- **5 函式與模組**：主程式只做組裝；狀態變數語意清楚。
- **4 資料結構**：`last_consolidated` 滑動視窗與 `turns` 搭配。

### 規格

- 每輪：`system_prompt = build_system_prompt()`；更新 `last_consolidated`；`past = _flatten_turns(turns, last_consolidated)`；呼叫 `run_react_turn`；`turns.append`；列印回覆。
- `llm`／`llm_with_tools`／`TOOLS` 與先前題目一致。

### 驗收條件

- [ ] 寫入 `MEMORY.md` 後，下一輪 `system` 可反映檔案內容（簡單自測）。
- [ ] 長對話下裁切仍不崩潰。
- [ ] 能說明：`last_consolidated` 變大時，模型「看不到」什麼？

### 提示（選讀）

> 與 M2-15 對照：本題須完全對齊藍本 `main` 呼叫鏈。

### 藍本對應程式（`memory_react_agent.py` 行 217–242）

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

## Challenge M2-22：端到端自檢——工具規則在 `system`、未知工具不中斷

### 情境

確認「工具規則真的進了每次送模的 system」，且模型幻覺出不存在工具名時 agent 仍可繼續。

### ITS 學習對照

- **5 函式與模組**：錯誤以字串進 `ToolMessage` 的契約。
- **3 條件判斷與迴圈**：未知分支不中斷外層 REPL。

### 規格

- `run_react_turn` 使用的 `system_text` **必須**來自 `build_system_prompt()`（不得另用未含 `TOOL_INSTRUCTION` 的替身）。
- `_TOOL_MAP.get(name)` 為 `None` 時，`ToolMessage` 內容須為明確錯誤字串。

### 驗收條件

- [ ] 算術題會走工具（課堂固定測句）。
- [ ] 可演示未知工具名時不 traceback、迴圈可繼續。
- [ ] 能說明：為什麼錯誤要回給模型看而不是直接 `raise`？

### 提示（選讀）

> 對照藍本 `build_system_prompt` 與 `run_react_turn` 內未知工具分支。

### 藍本對應程式（`memory_react_agent.py`）

`build_system_prompt`（行 75–81）：

```python
def build_system_prompt() -> str:
    """基底 system、長期記憶區塊、與工具使用規則合併。"""
    mem = get_memory_context()
    parts = [SYSTEM_TEXT, TOOL_INSTRUCTION]
    if mem:
        parts.insert(1, mem)
    return "\n\n".join(parts)
```

未知工具（行 197–198）：

```python
                if tool_obj is None:
                    tool_result: str | float = f"Unknown tool: {name}"
```

---

## Challenge M2-23：可讀性——區塊註解與 README 自測要點

### 情境

教練／同伴要能快速定位：常數、記憶、工具、預算、ReAct、`main`。

### ITS 學習對照

- **5 函式與模組**：模組內區塊註解、可維護性。
- **2 運算與輸入輸出**：README 作為操作與自測入口。

### 規格

- 以註解分隔至少四區（名稱可微調）：記憶檔、工具、預算與展開、ReAct 單輪等。
- `README.md`（若尚無則建立極簡版）寫 **5 條以內**自測要點（每條一句）：環境變數、一輪算術工具、多輪上下文、`memory/` 兩檔、長對話裁切。

### 驗收條件

- [ ] 另一人可在約 2 分鐘內找到 `run_react_turn` 與 `adjust_last_consolidated_if_over_budget`。
- [ ] 依 README 自測條目可自行驗收主要路徑。

### 提示（選讀）

> peas-challenge-coach 驗收：程式行為先、理解題後；執行請用 `uv run main.py`。

### 藍本對應程式（`memory_react_agent.py` 行 18–21、128）

```python
# 記憶檔與專案根目錄同層的 memory/
_MEMORY_DIR = Path(__file__).resolve().parent / "memory"
_MEMORY_FILE = _MEMORY_DIR / "MEMORY.md"
_HISTORY_FILE = _MEMORY_DIR / "HISTORY.md"
```

```python
# --- 工具（react.py）---
```

---

## Challenge M2-25（選修）：`unittest` 測試 `_normalize_tool_args`

### 情境

對純函式寫最小單元測試，對照 wiki「類別與單元測試」入門。

### ITS 學習對照

- **7 類別與單元測試**：`unittest`、案例與 assert。
- **5 函式與模組**：測試與生產程式分檔。

### 規格

- 新增 `tests/test_normalize_tool_args.py`（或專案慣例路徑），至少 2 案例：一般 dict 不變、巢狀 `value` 被攤平。
- 使用 `unittest`（不要求 pytest）。

### 驗收條件

- [ ] `uv run python -m unittest`（或 README 寫明的指令）可通過。
- [ ] 能說明：為什麼先測純函式而不是整段 `invoke`？

### 提示（選讀）

> wiki「類別與單元測試」：測試模組基本結構。

### 藍本對應程式（`memory_react_agent.py` 行 162–168）

藍本僅函式本體；測試檔請自行新增。

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

## Challenge M2-26（選修）：`read_long_term` 的例外處理

### 情境

磁碟或權限異常時，讀檔不應讓整支 agent 直接 traceback。

### ITS 學習對照

- **6 檔案與例外處理**：`try`／`except`、錯誤語意與回傳值契約。
- **5 函式與模組**：集中處理 I/O 失敗策略。

### 規格

- 在 `read_long_term`（或集中讀檔處）捕捉 `OSError` 和／或 `UnicodeDecodeError`；回傳固定說明字串或空字串；**行為須在註解或 README 寫清**。

### 驗收條件

- [ ] 可演示「讀檔失敗不崩潰」路徑（教練見證即可）。
- [ ] 能說明：吞掉例外與回傳錯誤給模型兩種取捨，你選哪一種？為什麼？

### 提示（選讀）

> wiki「檔案與例外處理」：例外與使用者可見訊息。

### 藍本對應程式（`memory_react_agent.py` 行 46–49）

藍本未包 `try/except`；選修請自行擴充。

```python
def read_long_term() -> str:
    """讀取目前長期知識（檔案不存在時回傳空字串）。"""
    _ensure_memory_files()
    return _MEMORY_FILE.read_text(encoding="utf-8")
```

---

## 建議操作方式（AI coding）

1. 依序完成 **M2-01→M2-23**；選修 **M2-25、M2-26** 可視課堂時間決定是否做。
2. 使用 **peas-challenge-coach** 時：每個 `## Challenge M2-xx` 視為一題；**進度條 N＝23**（僅必做 M2-01～M2-23）。
3. 需要 AI 輔助時：先完成教練流程的對齊條列與六欄提示詞，再請 coding agent 修改 `main.py`，並附上 `@main.py` 與本檔對應 Challenge 段落。
4. 若課堂同時發 [`challenges.md`](./challenges.md)：MR 軸適合**極細步**拆解；**本檔 M2 軸**適合「能力里程碑」節奏，可擇一為主線。
5. **驗收執行**：本專案以 `uv` 管理依賴；驗收程式行為請用 `uv run main.py`（與各題驗收條件中「`uv run`」敘述一致）。選修單元測試可用 `uv run python -m unittest`（或 README 寫明的指令）。

---

## 與交付物對照（工作坊備註）

| 建議交付物 | 本專案對應 |
|------------|------------|
| README.md | 學生操作手冊、環境與 M2-23 自測要點 |
| chatbot／主程式 | `main.py` |
| 題目與驗收（本組・演進版） | 本檔 `challenges2.md` |
| 題目與驗收（本組・細拆版） | `challenges.md` |
| 功能藍本（自讀） | `memory_react_agent.py` |
