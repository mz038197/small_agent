# Agent Workshop — 基礎 Agent 段（WG-13～WG-16）

本檔為 **peas-workshop-coach** skill 專用教案（僅含 WG-13～WG-16）。**前置**：學生須**已完成 WG-12**；作答在專案根 **`main.py`**（空白時教練複製 **`starter_main_wg12.py`**，僅 WG-12 骨架）。WG-13～16 程式對照 **`reference_agent.py`**。

- **串流要求（WG-10 起）**：除工具判斷、工具執行、JSONL 載入等**內部步驟**外，凡是「最後要顯示給使用者看的 assistant 文字回覆」都必須使用 `stream` 串流輸出；不得只以 `print(response.content)` 一次印出最終回答。

---

## Challenge WG-13：會查表才算真 Agent——工具呼叫與 ReAct 迴圈（單檔）

### 情境

**WG-12** 讓模型以 **system + history + 本輪使用者** 往來。本題在**單一 `.py` 檔**內練習 `add_numbers`、`@tool`、`bind_tools`、`tool_calls` 與 `ToolMessage`，並實作與示範檔一致的 **ReAct** 流程（`run_react_turn`、`_stream_model_response`）；**不要求** JSONL／持久化／字元預算。

通過後可銜接 **WG-14**（追加檔案／`exec` 工具至 `TOOLS`），再 **WG-15**／**WG-16**（JSONL 寫入／載回）。

### 規格

- **延續 WG-12** 之 `build_system_prompt()` 與 `history` 分離；`run_react_turn(llm_tools, system_text, history, user_text)` 在內部建立 `SystemMessage(content=system_text)`。
- 以 `@tool` 定義 `add_numbers(a: float, b: float) -> float`；**docstring** 須說明算術須呼叫工具、不可心算（對齊示範檔繁中文案）。
- `TOOLS = [add_numbers]`；`_TOOL_BY_NAME = {t.name: t for t in TOOLS}`；`llm.bind_tools(TOOLS)` 取得 `llm_tools`。
- **串流輔助 `_stream_model_response`**：`llm_tools.stream(messages)` 累積 chunk（`acc + chunk`），邊收邊 `print` 文字；以 `message_chunk_to_message(acc)` 轉成 `AIMessage`（保留 `tool_calls`）。
- **單輪 ReAct（`run_react_turn`）**：
  1. `messages = [SystemMessage(system_text), *history, HumanMessage(user_text)]`；記 `idx_turn_start = 1 + len(history)`。
  2. 呼叫 `_stream_model_response` → `response`；`messages.append(response)`。
  3. 若 `response.tool_calls` 非空：逐筆 `_run_bound_tool(name, args)`，`print(f"\n[工具 {name}]\n{result}\n")`，`append ToolMessage(..., name=name)`，回到步驟 2。
  4. 若無 `tool_calls`：`break`；`turn_messages = messages[idx_turn_start:]`；`final_text = response.content.strip()`；回傳 `(final_text, turn_messages)`。
- **邊界**：未知工具名回傳錯誤字串於 `ToolMessage.content`，不得崩潰。
- **選修**：每輪 `history.extend(turn_messages)` 供下一輪使用。

### 驗收條件

- 使用者提出須用工具完成的算術時，終端可觀察到 `[工具 add_numbers]` 與實際工具執行。
- 能指出：`bind_tools`、`_stream_model_response`、`run_react_turn` 內處理 `tool_calls` 的迴圈。
- 能說明：含 `tool_calls` 的 `AIMessage`、`ToolMessage`、最終純文字 `AIMessage` 在串列中的順序。
- **邊界**：只做一次 `invoke`、不處理 `tool_calls` 時可能錯在哪裡。

### 藍本對應

對齊 **`reference_agent.py`** 之 **WG-13** 段落（`add_numbers`、`_stream_model_response`、`_run_bound_tool`、`run_react_turn`）。

```python
@tool
def add_numbers(a: float, b: float) -> float:
    """兩個數字相加並回傳和。純算術必須呼叫此工具，不可心算後直接回答。"""
    return float(a) + float(b)

TOOLS = [add_numbers]
_TOOL_BY_NAME = {t.name: t for t in TOOLS}

def _stream_model_response(llm_tools, messages) -> AIMessage:
    acc = None
    for chunk in llm_tools.stream(messages):
        acc = chunk if acc is None else acc + chunk
        if isinstance(chunk.content, str) and chunk.content:
            print(chunk.content, end="", flush=True)
    return message_chunk_to_message(acc)

def run_react_turn(llm_tools, system_text, history, user_text):
    # 見 reference_agent.py 完整實作
    ...
```


---

## Challenge WG-14：讓 Agent 有手有腳——`exec` 與檔案的 LangChain **`@tool` 最小組**

### 情境

緊接 **WG-13**，你已用 `@tool`、`bind_tools`、多段 `stream` 與 `ToolMessage` 跑通 **ReAct**。本題在 `TOOLS` 上**追加** workspace 內**讀／寫／列目錄／局部替換**與 **`exec`**（shell）；仍**不要求** JSONL——從 **WG-15** 起再接上。

核心觀念：**檔案操作走檔案工具，shell 指令才走 `exec`**。讀檔不用 `cat`、寫檔不用 `echo >`、改檔不用 `sed -i`。

**Agent 使用 `exec` 時**：多行 Python 須 **write_file → `uv run python …`**；Windows PowerShell 勿用 `<<`／heredoc。工具 **docstring** 說明用途即可；跨平台編碼細節見下方 **`exec`** 規格。

本題**不要求**自訂 `ToolRegistry`；`_TOOL_BY_NAME` 對照表供 `_run_bound_tool` 使用（與 **WG-13** 相同）。

### 規格

- 在 **`main.py`** 實作，依賴 `langchain_core`（與 **WG-13** 一致）。
- **保留 WG-13 之 `add_numbers`**；`TOOLS` 順序對齊示範檔：`add_numbers`、`read_file`、`write_file`、`edit_file`、`list_dir`、`exec`（共六支；對外名稱 **`exec`** 由 `@tool("exec")` 裝飾 `exec_workspace` 等實作函式）。
- 設定 `WORKSPACE = Path.cwd().resolve()`；`resolve_workspace_path`：拒絕**絕對路徑**；`../outside.txt` 等須拒絕。
- **`read_file(path, offset=1, limit=200)`**：UTF-8、帶行號；非檔案回傳錯誤。
- **`write_file(path, content)`**：UTF-8 整檔覆寫；必要時 `mkdir(parents=True)`。
- **`edit_file(path, old_text, new_text, replace_all=False)`**：局部替換；`old_text` 多次出現且未 `replace_all` 時報錯。
- **`list_dir(path, recursive=False, max_entries=200)`**：列出相對 workspace 之路徑；可 `rglob`。
- **`exec`（`exec_workspace`）**：`subprocess.run`、`cwd=WORKSPACE`、`shell=True`、`encoding="utf-8"`、`errors="replace"`、`timeout`（預設 30）；子程序 env 設 `PYTHONUTF8=1`；Windows 可設 `CREATE_NO_WINDOW`；輸出合併 stdout／stderr，超過約 4000 字元截斷；阻擋 `rm -rf`／`del /f` 等危險片段。
- **`exec` 與子程序輸出編碼（跨平台必讀）**：繁中 Windows 預設 cp950 解碼可能導致 `UnicodeDecodeError`；須明確 `encoding="utf-8"` 與 `errors="replace"`（對齊示範檔）。

### 驗收條件

- `sorted(t.name for t in TOOLS)` 含 `add_numbers` 與五支檔案／shell 工具名。
- 手動流程：`write_file` → `list_dir` → `read_file` → `edit_file` → 再 `read_file` → `exec("python --version")`（以 `BaseTool.invoke` 或 ReAct 皆可）。
- 能說明：**write_file** 整檔覆寫 vs **edit_file** 局部替換；為何不用 `exec("cat …")` 讀檔。
- **邊界**：`../outside.txt` 拒絕；`edit_file` 重複 `old_text` 預設不改兩處；危險 `exec` 拒絕；Windows 大量子程序輸出不崩潰。

### 藍本對應

對齊 **`reference_agent.py`** 之 **WG-13／WG-14** 段落（`WORKSPACE` 至 `_TOOL_BY_NAME`）。`TOOLS` 須含 `add_numbers`：

```python
TOOLS = [
    add_numbers,
    read_file,
    write_file,
    edit_file,
    list_dir,
    exec_workspace,
]
_TOOL_BY_NAME = {t.name: t for t in TOOLS}
```

其餘五支 `@tool` 實作見示範檔 **`reference_agent.py`**（約第 45～169 行）。


---

## Challenge WG-15：對話落盤、人設不留痕——對話脈絡寫入 JSONL（先寫檔）

### 情境

**WG-12～14** 已以 `build_system_prompt()` 與 `run_react_turn` 維持 **ReAct** 對話；關程式後 **RAM** 仍清空。本題在**沿用相同主迴圈**的前提下**只做寫檔**：每輪 `history.extend(turn_messages)` 後呼叫 `save_session_jsonl`，把 `session_meta` 與完整 `history`（含 `tool_calls`／`ToolMessage`）**整檔覆寫**到 JSONL（**第一行** `metadata`）。檔案長相可參考 **`references/session.jsonl.example`**（含一般對話與 **ReAct** 一輪完整鏈）。

規格與函式簽名以 **`reference_agent.py`**（**WG-15～16** 段落）為準。

**刻意不做**：啟動時讀舊檔（留 **WG-16**）。**WG-15 獨立驗收**時 `main()` 仍從空 `history` 開始；合併示範檔已含 **WG-16** 載入邏輯，教師可指定「本題只驗寫檔、暫不驗載回」。

### 規格

- 延續 **WG-07～14**：`load_dotenv`、金鑰早退、`build_system_prompt()`、`run_react_turn(llm_tools, system_text, history, user_text)`、`llm.bind_tools(TOOLS)`（`TOOLS` 含 **WG-13** `add_numbers` 與 **WG-14** 五支工具，對齊示範檔）。
- **存檔路徑**：`os.getenv("SESSION_JSONL_PATH", "session_wiki_wg.jsonl")`（示範檔預設；可覆寫）。`session.jsonl.example` 僅供對照格式，**勿**當預設寫入目標。
- **啟動（WG-15 獨立）**：`history = []`、`session_meta = None`；**禁止**呼叫 `load_session_jsonl`。
- **寫檔時機**：每輪 `run_react_turn` 結束、`history.extend(turn_messages)` 之後。
- **輔助函式**（對齊示範檔）：
  - `_default_metadata(created_at=None)`：第一行 metadata（與 `session.jsonl.example` 欄位對齊）；含 `last_consolidated: 0`（供進階段預留）。
  - `_serialize_tool_calls(tc)`：將 `tool_calls` 正規化為 `{name, args, id}` 陣列再寫入 JSONL。
  - `_message_to_jsonl_line(m)`：`HumanMessage`／`AIMessage`（含 tool_calls）／`ToolMessage` → 一行 JSON；`ToolMessage` 可選寫 `name`。
  - `save_session_jsonl(path, messages, existing_meta, last_consolidated) -> dict`：整檔覆寫；更新 `updated_at`；保留 `created_at`（若 `existing_meta` 有）。
- **JSONL 列**：`user`／`assistant`／`tool`；`assistant` 含非空 `tool_calls` 時同列寫入 `tool_calls`（經 `_serialize_tool_calls`）；每列建議 `timestamp`。
- **禁止**：寫入 `SystemMessage`／system 字串。

### 驗收條件

- 至少一輪對話後，指定路徑出現 JSONL；第一行 `metadata`；其後有 `user`／`assistant`；若走 ReAct 則另有 `tool` 與含 `tool_calls` 的 `assistant` 列。
- 能說明：為何在 `extend(turn_messages)` **之後**才 `save_session_jsonl`。
- **邊界**：舊 JSONL 存在時，**WG-15 獨立版**重開仍從空 `history` 開始，第一輪存檔為**整檔覆寫**（不 merge 舊列）。

### 藍本對應

對齊 **`reference_agent.py`**：`_default_metadata`、`_serialize_tool_calls`、`_message_to_jsonl_line`、**`save_session_jsonl`**（約第 190～321 行）；**`main()`** 寫檔段落（約第 441～446 行）。**WG-15 獨立**時省略啟動的 **`load_session_jsonl`** 呼叫。


---

## Challenge WG-16：冷啟動撿回昨日脈絡——從 JSONL 載回對話脈絡

### 情境

**WG-15** 已會寫入完整 **ReAct** 鏈。本題加上**啟動讀檔**：`load_session_jsonl` 還原 `history` 與 `session_meta`，使**關閉再開**可接續。讀取時壞行略過（`json.JSONDecodeError`）。載入後須能還原 **`session.jsonl.example`** 同構之 `tool_calls`／`tool` 鏈。

合併示範檔 **`reference_agent.py`** 已實作 **WG-12～16** 完整閉環。

### 規格

- 延續 **WG-15** JSONL 格式與 `save_session_jsonl` 時機；**不**改欄位名。
- **新增 `load_session_jsonl(path) -> tuple[list[BaseMessage], dict | None]`**（對齊示範檔）：
  - 無檔 → `([], None)`。
  - 有檔 → 逐行 `json.loads`；`_type == "metadata"` → `session_meta`；其餘經 `_row_to_message` 還原（`_serialize_tool_calls` 還原 `AIMessage.tool_calls`；`ToolMessage` 含 `tool_call_id`、可選 `name`）。
- **`main()` 啟動**：`history, session_meta = load_session_jsonl(session_path)`；`system_text = build_system_prompt()`；有載入則印出訊息則數（示範檔行為）。
- 每輪：`run_react_turn` → `history.extend(turn_messages)` → `save_session_jsonl(..., last_consolidated=int(session_meta.get("last_consolidated", 0)))`。

### 驗收條件

- **關閉再開**：先前對話關鍵資訊可被模型承接；與 JSONL 一致。
- 能指出 `load_session_jsonl` 位置與 bad-line 處理。
- 能說明 `created_at`／`updated_at` 在首次寫檔 vs 讀檔後再寫檔的差異。
- **ReAct**：載入後 `AIMessage.tool_calls` 與後續 `ToolMessage.tool_call_id` 仍對齊。

### 藍本對應

完整可執行示範：**`reference_agent.py`**。

關鍵入口：

```python
session_path = os.getenv("SESSION_JSONL_PATH", "session_wiki_wg.jsonl")
history, session_meta = load_session_jsonl(session_path)
system_text = build_system_prompt()
# ...
history.extend(turn_messages)
last_consolidated = int(session_meta.get("last_consolidated", 0) or 0)
session_meta = save_session_jsonl(session_path, history, session_meta, last_consolidated)
```

JSONL 輔助函式見示範檔第 190～321 行；ReAct 見第 324～393 行；**`main()`** 見第 408～446 行。
