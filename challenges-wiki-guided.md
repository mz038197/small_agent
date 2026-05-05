# Wiki 挑戰題（協作教案 · WG 系列）
本檔為**獨立**的挑戰題教案：依 **LLM Wiki「教材統整／Python」七份統整頁**（見下方表格）對齊學習重點，將**逐段指定的程式**收成可引導學生動手的 Challenge。版面區塊（`### 情境`、`### 規格`、`### 驗收條件` 等）**僅在結構上**與專案內既有的挑戰題 markdown 慣例相同，題目內容以本檔為準。

**若某學習重點已在同一檔案前段某個 WG 題或「已涵蓋索引」出現且驗收涵義相同**，後續新題**不重複**同一組驗收句，只在索引表註記「已涵蓋／見 WG-xx」。

**檔案角色**：`example.py` 僅供參考、勿改；學生作答與執行以教師指定檔（常見為 `main.py`）為主。

**與專案內 `basic.py`**：各題「參考 **`basic.py`**」指**該題藍本區塊內的程式切片**；倉庫根目錄的 **`basic.py`** 為 **WG-12～WG-18** 合併示範（含 **`memory/`** 長期整併；**WG-13** 工具 **ReAct** 可參考 **`memory_react_agent.py`**；**WG-17** transcript 整備見獨立題，未必併入此合併檔）。教 **WG-01～10** 時請以藍本為準（或另存分段示範檔），避免學生直接開合併檔對不到當課進度。

**ITS Python wiki 參考**（七份統整條目；路徑依課程約定之 Agent 庫，常見為 `G:\我的雲端硬碟\Obsidian\Agent\wiki\`）：

| 序 | 學習主軸（由簡入繁） | wiki 條目檔名（統整頁） |
|----|----------------------|-------------------------|
| 1 | 基礎資料與變數 | `Python-基礎資料與變數.md` |
| 2 | 運算與輸入輸出 | `Python-運算與輸入輸出.md` |
| 3 | 條件判斷與迴圈 | `Python-條件判斷與迴圈.md` |
| 4 | 資料結構（串列等） | `Python-資料結構-串列元組字典.md` |
| 5 | 函式與模組 | `Python-函式與模組.md` |
| 6 | 檔案與例外處理 | `Python-檔案與例外處理.md` |
| 7 | 類別與單元測試 | `Python-類別與單元測試.md` |

## WG 挑戰題一覽（速查）
**Python 學習主軸**欄之編號，與上方 **ITS Python wiki 參考** 表之 **「序」**（1～7）一致：**1** 基礎資料與變數、**2** 運算與輸入輸出、**3** 條件與迴圈、**4** 資料結構、**5** 函式與模組、**6** 檔案與例外、**7** 類別與測試（多項以 **、** 分隔；為主軸複選，非課堂時數分配）。

| 編號 | 標題 | 大概內容 | Python 學習主軸（wiki 序） |
|------|------|----------|---------------------------|
| **WG-01** | 按下啟動鍵——最小進入點與第一則輸出 | `if __name__ == "__main__"`、`print()` 字面量；直接執行與被 `import` 的差異。 | 2、7 |
| **WG-02** | 給台詞一個名字——變數與再輸出 | 以變數保存字串，再交給 `print`（不接 API）。 | 1、2 |
| **WG-03** | 把身分縫進一句介紹——兩變數與 f-string | 多個 `str` 變數；`f"…{變數}…"` 組一句話輸出。 | 1、2 |
| **WG-04** | 替 Agent 備料——`uv add` 與頂層匯入 | 安裝套件；檔案頂層 `import`／`from … import`；終端輸出行為對齊 **WG-03**（仍不呼叫 API）。 | 5 |
| **WG-05** | 讀設定、不賣鑰匙——`load_dotenv` 與安全診斷 | `load_dotenv()`、`os.getenv`；印「有／無」金鑰但不洩漏內容；單行 `#` 註解。 | 1、5、6 |
| **WG-06** | 有通行證才開門——`if`／`else` 依金鑰分支 | 有金鑰與無金鑰兩種提示；仍不呼叫 `ChatOpenAI`。 | 3 |
| **WG-07** | 一行進門、其餘進房——`def main()` 與精簡進入點 | 用 `def main()` 封裝流程；進入點僅呼叫 `main()`。 | 5 |
| **WG-08** | 第一通打進大模型——`ChatOpenAI` 與 `invoke` | 建實例、`invoke`、讀回 `content` 並 `print`；無金鑰不呼叫。 | 5 |
| **WG-09** | 櫃台問答不斷線——互動迴圈與多輪 `invoke` | `while`、`input`、關鍵字結束；每輪 `invoke`（非串流）。 | 3、5 |
| **WG-10** | 回答像打字機——串流式 `stream` | 架構同 **WG-09**，改 `stream` + `print(..., end="", flush=True)`。 | 3、5 |
| **WG-11** | 短期記憶只活在當下——RAM 對話脈絡 | `HumanMessage`／`AIMessage` 串列累積；`context_messages` 先組再串流，串流後才 `append`；關閉程式即清空。 | 3、4、5 |
| **WG-12** | 人設寫進系統層——`SystemMessage` 與可變系統字串 | 課堂示範 **`build_system_prompt()`**；合併作答可拆 **`build_classroom_base_prompt()`**（課堂＋顯示名）並由 **`compose_system_string`**（**WG-20**）併入長期記憶與 Skills；`system` 與 `history` 分離；送模 **`[system_message, *history, human_message]`**；本題可僅 **RAM**、**不**寫 JSONL。 | 4、5 |
| **WG-13** | 會查表才算真 Agent——工具與 ReAct（單檔） | `@tool`、`bind_tools`、`tool_calls`、`ToolMessage`、多段 **`invoke`**；參考 **`memory_react_agent.py`**；本題不要求 JSONL／預算裁切。 | 3、4、5 |
| **WG-14** | 對話落盤、人設不留痕——JSONL 先寫檔 | 在 **WG-12** 送模結構下整檔覆寫 JSONL（首行 `metadata`；**對話列** **`user`／`assistant`／`tool`** 對齊 **WG-13**）；啟動**不**讀舊檔；**不**寫 `SystemMessage`。 | 5、6 |
| **WG-15** | 冷啟動撿回昨日脈絡——JSONL 載回 | 啟動讀檔還原 **`history`**（**`assistant`** 列可還原含 **`tool_calls`** 之 **`AIMessage`**，**`tool`** 列還原 **`ToolMessage`**，對齊 **WG-14** 完整版）；壞行略過；關閉再開可接續。 | 6 |
| **WG-16** | 視窗太窄先裁舊帳——字元預算與整併邊界 | `estimate_message_tokens`、`pick_consolidation_boundary`、`last_consolidated`；超線裁切 **`past`**；成本含 **`ToolMessage`**（與 **WG-13** 銜接）。 | 3、4、5 |
| **WG-17** | 送模前先洗對話簿——transcript 修復與工具輸出預算 | 參考 `nanobot.agent.runner`：`messages_for_model` 管線（孤兒 tool 清理、缺洞補齊、tool 截斷、舊 tool 摘要、全對話字元預算）。 | 4、5、6 |
| **WG-18** | 舊對話濃縮成長期備忘——整併與每輪讀回組裝 | `memory/MEMORY.md`、`HISTORY.md`；超線時 **consolidation** `invoke`；`## Long-term Memory` 併入 **system**；送主模型前壓至 **≤ TOKEN_BUDGET//2**。 | 5、6 |
| **WG-19** | 讓 Agent 有手有腳——`exec` 與檔案工具的最小工具箱 | 註冊並實作 `read_file`／`write_file`／`edit_file`／`list_dir` 與 `exec`；檔案操作走專用工具，shell 只做必要指令與驗證；練習 workspace 限制、唯讀工具、覆寫與局部替換邊界。 | 4、5、6、7 |
| **WG-20** | 技能卡進工具箱——最小 SkillsLoader 與 system prompt 注入 | `skills/<name>/SKILL.md`、frontmatter 摘要、workspace／builtin 合併、同名覆蓋；**`compose_system_string`** 依序：**課堂基底**（**`build_classroom_base_prompt`**）→ **長期記憶**（若有）→ **`# Active Skills`**（`always` 正文）→ **`# Skills`**（繁中引導＋摘要）；大段間 **`---`**；並**銜接 WG-19**：每個 tool 的 **JSON Schema**、`cast_params`／`validate_params`、`ToolRegistry.prepare_call`。 | 4、5、6 |

---

## 協作方式（給共同編輯者）
1. **每次**在對話中貼「一段」程式（建議附：檔名、在檔案中用途一句話）。
2. 編輯者從上表 **1～7** 參考 wiki 的「建議學習順序」小節，挑出與該段程式**直接對應**的學習重點（可複選）。
3. **去重**：查本檔 **「已涵蓋學習重點索引」** 與已寫入的 **WG-xx**；若該重點已由先前段落涵蓋，則**不**再為同一觀念新增驗收條件，只在索引註記「已涵蓋／見 WG-xx」。
4. 將新內容寫成下方 **Challenge WG-xx** 區塊：`### 情境`、`### 規格`、`### 驗收條件`、`### 提示（選讀）`、`### 藍本對應程式`（貼上指定程式或精簡版）。

---

## 已涵蓋學習重點索引（去重用 · 隨協作追加）
| wiki 序 | wiki 小節／重點（摘要） | 涵蓋來源 | 備註 |
|---------|-------------------------|----------|------|
| 2 | 用 `print()` 把字串送到終端（字面量） | **WG-01** | 最小一則輸出；與「經變數再輸出」見 **WG-02**。 |
| 7 | `if __name__ == "__main__"`：僅在直接執行此檔時跑區塊內程式 | **WG-01** | 最小進入點。 |
| 1 | 變數賦值：以名稱保存 `str`，再交給 `print` | **WG-02** | 藍本將賦值寫在 `if __name__` 區塊內；不重複 WG-01「括號內字面量」的驗收句。 |
| 1 | 多個 `str` 變數；依「是否被後續運算用到」安排賦值順序 | **WG-03**（`basic.py`） | 與 WG-02 單一 `message` 字串並列，不取代 WG-02 驗收。 |
| 2 | **f-string**（`f"..."` 與 `{變數}` 嵌入） | **WG-03** | wiki「字串格式化」一節；與 `%`、`format()` 擇一主軸時本檔以 f-string 為準。 |
| 5 | **`uv add`** 納入依賴；`import`／`from … import` 於檔案頂層宣告（可先不呼叫）；示範檔執行結果對齊 **WG-03** | **WG-04**（`basic.py`） | 合併原「僅依賴」與「僅匯入」兩題；**不**呼叫 OpenAI API、**不**強求 `load_dotenv()` 或 `.env` 內容。 |
| 6 | 搭配 **`python-dotenv`**：`load_dotenv()` 將 `.env` 載入程序環境；**`os.getenv`** 依名稱讀環境變數；終端診斷**不得**印出完整敏感字串 | **WG-05**（`basic.py`） | 以 `OPENAI_API_KEY` 為例；僅能印「有／無」或等價**不暴露金鑰本體**的描述。 |
| 1 | **單行註解**（行首 **`#`**）：讓該行**不**被 Python 執行，用於暫時關掉／保留舊程式 | **WG-05**（`basic.py`） | 藍本以 `#` 註解 **WG-04** 問候三行，與「命名與註解」wiki 小節對齊。 |
| 3 | **`if`／`else`** 依條件分支輸出（本題以金鑰是否存在為例） | **WG-06**（`basic.py`） | 在 **WG-05** 藍本上加兩支不同訊息；**仍不**呼叫 `ChatOpenAI`／`invoke`。 |
| 5 | 以 **`def main()`** 封裝主要流程；`if __name__ == "__main__":` 內**僅**呼叫 **`main()`** | **WG-07**（`basic.py`） | 終端行為與 **WG-06** 對齊（可加註解說明無行為變更）。 |
| 5 | **`ChatOpenAI`** 建實例、**`invoke`** 繁中提示、讀取回傳訊息之 **`content`** 並 `print`；無金鑰時**不**呼叫 API | **WG-08**（`basic.py`） | 需網路、可能計費；依賴安裝見 **WG-04**。 |
| 3 | **`while`** 互動迴圈、**`input()`** 讀使用者輸入；依關鍵字（如 `quit`）**中斷迴圈**；每輪 **`invoke`** 並印回覆 | **WG-09**（`basic.py`） | 延續 **WG-08** 之 `llm`；本題練「多輪對話」**不含**串流。 |
| 3 | 在迴圈內以 **`stream`** 取得增量、`print(..., end="", flush=True)` 做出**串流式**終端輸出 | **WG-10**（`basic.py`） | 架構同 **WG-09**，僅改「一輪回覆」的輸出方式；需網路、可能計費。 |
| 4 | 以**串列**累積 **`HumanMessage`／`AIMessage`**，每輪以 **`llm.stream(context_messages)`** 串流印出（藍本 **`context_messages = [*messages, human_message]`**）、再把本輪 **Human／AI** 寫回累積串列；**關閉程式即清空**（僅 **RAM**、**不**寫檔） | **WG-11**（`basic.py`） | 延續 **WG-10** 之串流體感並加上 RAM 脈絡；再 **WG-12** 將 **SystemMessage** 與 **`history`** 分離、送模 **`[system_message, *history, human_message]`**（本題可先**不**寫 JSONL）；再 **WG-13** **工具呼叫／ReAct**（單檔，參考 **`memory_react_agent.py`**）；再 **WG-14** 寫檔、**WG-15** 載回；再 **WG-16** 以字元長度模擬 **token** 與 **`pick_consolidation_boundary`**（**`history`** 可含 **WG-13** 之 **`ToolMessage`**）；再 **WG-17** 整理送模用 **transcript**；再 **WG-18** 將超預算時之舊脈絡**摘要寫入長期檔**並每輪**讀回併入 system**。 |
| 5 | 以 **`def build_system_prompt()`** 組出送進模型的**系統字串**；**`SystemMessage`** 與 **`history`（僅 Human／AI）**分離持有；每輪 **`context_messages = [system_message, *history, human_message]`** 再 **`llm.stream`**；本題**不要求** JSONL | **WG-12**（`basic.py`） | 延續 **WG-11**；示範以函式內 **`nick`** 自訂顯示名（如 **`法鬥超人`**）；**選修**可改讀 **`os.getenv("ASSISTANT_DISPLAY_NAME")`**；通過後接 **WG-13**（**ReAct**／工具），再 **WG-14**／**WG-15** 持久化。 |
| 6 | **`with open(..., "w", encoding="utf-8")`** 寫文字檔；**`json.dumps`**；**`os.getenv`** 指定路徑；與 **`datetime`** 產生時間戳欄位 | **WG-14**（`basic.py`） | **僅寫入**：在 **WG-12** 送模結構下，每輪對話回合寫回 **`history` 後**（可含 **WG-13** **`ToolMessage`** 鏈）整檔覆寫 JSONL（首行 **`metadata`**）；啟動**不**讀檔；**不**寫 **SystemMessage**。 |
| 6 | **`with open(..., encoding="utf-8")`** 讀文字檔；**`json.loads`**；**`try`／`except json.JSONDecodeError`** 略過壞行；載回後與寫檔行為閉環 | **WG-15**（`basic.py`） | 在 **WG-14** 寫檔格式上，啟動時**讀回** **`history`**（**`user`／`assistant`／`tool`** 與 **WG-14** 閉環）與 **`metadata`**；送模仍對齊 **`[system_message, *history, human_message]`**；通過後接 **WG-16**。 |
| 3 | **`for`** 自 **`last_consolidated`** 掃描 **`history`**，累加 **`estimate_message_tokens`**；在 **`HumanMessage`** 回合開頭更新 **`last_boundary`**，達 **`tokens_to_remove`** 即回傳 **`(idx, removed_tokens)`**；**`TOKEN_BUDGET`** 以常數或 **`int(os.getenv(...))`**（選修）定義 | **WG-16**（`main.py`／`basic.py`） | 延續 **WG-15**；**`history`** 與成本可含 **`ToolMessage`**（**WG-13**）；裁切邊界對齊 **`pick_consolidation_boundary`**；**完整** **`history`／JSONL**；須能說明 **`TOKEN_BUDGET`** 與 **`TOKEN_BUDGET // 2`** 如何換算成 **`tokens_to_remove`**；通過後接 **WG-17**（**transcript** 送模副本）再 **WG-18**（長期記憶整併）。 |
| 6 | **`Path`** 與專用目錄 **`memory/`**；**`MEMORY.md` 覆寫**、**`HISTORY.md` 追加**（**`[YYYY-MM-DD HH:MM]`** 前綴）；超預算時以**第二支** LLM **`invoke`** 做整併、解析結構化結果；送**主**模型前成本須 **≤ `TOKEN_BUDGET // 2`**；固定子字串 **`## Long-term Memory`** 併入 **`SystemMessage.content`**（**不得**改放成 **user／assistant／tool** 對話列） | **WG-18**（`basic.py`／`main.py`） | 規格本質參考 **`long-term-memory-template`** 之 **Challenge A**（該檔為單題完整條文）；本題疊在 **WG-16** 之上：**JSONL** 與 **metadata**（**`last_consolidated`** 等）延續 **WG-14～16**（可含 **`tool`** 列）；長期脈絡改由 **`MEMORY.md`／`HISTORY.md`** 承載。 |

---

## Challenge WG-01：按下啟動鍵——最小進入點與第一則輸出
### 情境
暖身用：讓學生確認專案環境能執行一支極短檔案，並習慣「只有直接跑這個檔時，才執行區塊裡的程式」。**不**在本題要求讀環境變數、迴圈，也不要求把邏輯拆進自訂的 `main()` 函式（留給後續單元）。通過後可銜接 **WG-02**（以變數保存問候語再輸出）。**本題驗收**以下方藍本為準；若教學檔已擴寫，驗 WG-01 時可請學生暫時只保留藍本兩行，或由教師口頭約定「整檔跑通即可，但理解題仍對準藍本兩行」。

### 規格
- 使用 `if __name__ == "__main__":` 作為程式進入點慣例。
- 進入點區塊內呼叫 `print`，引數為字串字面量（藍本為 `"Hello, World!"`；若要本土化可改繁中招呼句，但須仍為單一 `str` 字面量）。
- 檔名可維持 `basic.py` 作為課堂示範，或請學生抄入教師指定之作答檔（依班級流程擇一即可）。

### 驗收條件
- [ ] 在專案根目錄以 `uv run basic.py`（或教師指定之檔名）執行，終端機出現預期字樣。
- [ ] 能說明：`print(...)` 括號內的資料，在 Python 裡屬於哪一種基本型態？
- [ ] 能一句話說明：為什麼要把 `print` 寫在 `if __name__ == "__main__":` **底下**（與「被別的檔 `import` 時不要自動跑」有關即可）。
- [ ] 能描述一個**邊界**：若有另一支程式只寫了 `import basic`（檔名依實際為準），執行那支程式時，你預期終端會不會出現 `Hello, World!`？為什麼？

### 提示（選讀）
> 參考 wiki「**運算與輸入輸出**」：`print()` 與字串字面量。
> 參考 wiki「**類別與單元測試**」小節：`if __name__ == '__main__'` 的用途（本題只練最小形狀）。

### 藍本對應程式（`basic.py`）
```python
if __name__ == "__main__":
    print("Hello, World!")
```

---

## Challenge WG-02：給台詞一個名字——變數與再輸出
### 情境
在 **WG-01** 能跑、能說明進入點之後，在**進入點區塊裡**把「要印的字」存進**變數**再印出。終端機看到的問候句應與先前相同，避免學生以為行為改壞了。通過後可銜接 **WG-03**（名稱獨立成變數，再以 f-string 組句）。

### 規格
- 在 `if __name__ == "__main__":` **底下**（與藍本相同縮排層級）：先以賦值建立一個變數（藍本為 `message`），型別為 `str`，內容為問候字串；再呼叫 `print(message)`。
- 變數與 `print` 皆須落在進入點區塊內（不把問候字串留在「只有被 `import` 時也會執行」的模組頂層賦值）。
- **不**在本題加入 `input()`、迴圈、自訂函式或讀檔。

### 驗收條件
- [ ] `uv run basic.py` 終端機仍出現預期問候字樣。
- [ ] 能說明：`message`（或自訂的同名變數）綁到的是哪一種基本型態？
- [ ] 能連結回 **WG-01**：為什麼現在 `print` 的括號裡**不必**再寫字面量 `"Hello, World!"` 也能印出同樣結果？
- [ ] **邊界**：若把區塊內的 `message = "Hello, World!"` 改成 `message = "Hi"`，其餘行不變，你預期輸出會變成什麼？為什麼？
- [ ] **邊界**：若有另一支程式只寫了 `import basic`（檔名依實際為準）並執行，你預期此時模組裡是否一定已經有 `message` 這個名稱？為什麼？（與進入點區塊有沒有跑過有關即可。）

### 提示（選讀）
> 參考 wiki「**基礎資料與變數**」：變數是替資料命名、同一資料可透過名稱重複使用。
> 參考 wiki「**運算與輸入輸出**」：`print()` 印的是「當下的值」，引數可以是字面量也可以是變數。

### 藍本對應程式（`basic.py`）
```python
if __name__ == "__main__":
    message = "Hello, World!"
    print(message)
```

---

## Challenge WG-03：把身分縫進一句介紹——兩變數與 f-string 組句
### 情境
在 **WG-02** 已會把整句問候存進 `message` 之後，進一步把「名字／稱呼」獨立成一個變數，再用**字串模板**把名字嵌進句子裡。這樣之後只改名字變數，不必整句重抄。呼應課堂裡常見的「小助手／代理人名稱」設定。

### 規格
- 在 `if __name__ == "__main__":` 區塊內：
  - 先建立一個 `str` 變數表示名稱或稱呼（藍本為 `agent_name`；字串內容可改，但須仍為 `str`）。
  - 再建立 `message`，使用 **f-string**（字串前綴 `f`），並以 `{agent_name}`（或與你變數名一致的大括號嵌入）把名稱嵌進整句問候裡。
  - 最後 `print(message)`。
- **賦值順序**：凡在右側運算式會讀到的變數，必須**先**完成賦值（藍本為 `agent_name` 在 `message` 之上）。
- **不**在本題改用 `+` 硬串、`%` 或 `format()` 取代 f-string（避免與本題主軸混淆）；不加入 `input()`、迴圈、自訂函式。

### 驗收條件
- [ ] `uv run basic.py` 終端機出現**一整句**問候，且句中可看出你設定的名稱或稱呼（與藍本精神一致即可）。
- [ ] 能說明：`message` 這一行裡，大括號 `{...}` 在執行時會被替換成什麼？
- [ ] 能說明：為什麼 `agent_name`（或你的對應變數）那一行**必須**寫在組出 `message` 的那一行**上面**？（若反過來寫會發生什麼，用自己的話即可。）
- [ ] **邊界**：只把 `agent_name` 的字串改成另一個名字、其餘不變，你預期輸出哪裡會變、哪裡不會變？

### 提示（選讀）
> 參考 wiki「**運算與輸入輸出**」：字串格式化一節的 **f-string**（現行教材常推薦的寫法）。
> 參考 wiki「**基礎資料與變數**」：多個變數、讀程式時注意「先出現的賦值」與「後面用到誰」。
> 若本機終端機顯示中文變成亂碼，多為**主控台編碼**未用 UTF-8；檔案仍以 UTF-8 儲存為準，可換用已設 UTF-8 的終端或調整 Windows 主控台字碼頁（選讀，非本題核心）。

### 藍本對應程式（`basic.py`）
```python
if __name__ == "__main__":
    agent_name = "法鬥超人"
    message = f"Hello, 我是{agent_name}，很開心認識你!"
    print(message)
```

---

## Challenge WG-04：替 Agent 備料——`uv add` 安裝依賴與 `basic.py` 頂層匯入（終端輸出對齊 WG-03）
### 情境
後續單元會用到 **OpenAI 相關的 LangChain 整合**（套件發佈名為 `langchain-openai`）以及從 **`.env` 讀設定**（常搭配 `python-dotenv`）。本題**一次**完成兩件事，讓「套件進專案」與「程式裡怎麼引用名稱」連在一起：（1）在已用 **uv** 管理的專案**根目錄**用 **`uv add`** 把兩套件寫進 `pyproject.toml`（並由 uv 維護 lock／環境）；（2）在示範檔（藍本為 `basic.py`）**最上方**寫入兩行 `from … import`，**進入點內**仍只做與 **WG-03** 相同的問候（`agent_name`、f-string `message`、`print`）——**先不要**建立 `ChatOpenAI`、打 API、也不要求建立或提交 `.env` 內容，避免與下一階段混線。通過後可銜接 **WG-05**（在進入點呼叫 `load_dotenv`、用 `os.getenv` 讀 `OPENAI_API_KEY`，並以**不暴露完整金鑰**的方式印出診斷）。

### 規格
**依賴（專案根）**

- 工作目錄須為本專案**根目錄**（與 `pyproject.toml` 同層）。
- 以**一條指令**同時加入兩個套件（套件名以 PyPI 為準）：`uv add langchain-openai python-dotenv`
- 執行後 `pyproject.toml` 的 `[project]` → `dependencies` 中應出現上述兩個套件名（版本約束由 uv 寫入即可，不必手改）。

**示範檔結構**

- 在 `if __name__ == "__main__":` **之上**（模組頂層、無額外縮排）：
  - `from langchain_openai import ChatOpenAI`
  - `from dotenv import load_dotenv`
- `if __name__ == "__main__":` 區塊內與 **WG-03** 相同精神：先 `agent_name`（`str`），再以 **f-string** 組出 `message`，最後 `print(message)`。
- **不要求**在區塊內呼叫 `load_dotenv()`、不要求建立 `ChatOpenAI` 實例或呼叫 `invoke`（留給後續 Challenge）；頂層匯入的 `ChatOpenAI`／`load_dotenv` 執行時**可尚未被使用**。

### 驗收條件
**依賴與環境**

- [ ] 能說明：為什麼要在「專案根」執行 `uv add`，而不是在任意資料夾執行？
- [ ] 終端機曾成功跑過 `uv add langchain-openai python-dotenv`（或同等效果：兩套件已列於 `dependencies` 且 lock／環境一致）；若專案**已**含兩依賴，能說明「再跑一次 `uv add` 通常會做什麼」（例如解析／同步，而非重複亂裝）。
- [ ] 在專案根執行下列**其中一種**並成功（無 `ModuleNotFoundError`）：
  - `uv run python -c "import langchain_openai; import dotenv; print('deps-ok')"`
  - 或：`uv run python -c "import langchain_openai; from dotenv import load_dotenv; print('deps-ok')"`
- [ ] **邊界**：若只在某子資料夾執行 `uv add`、該處沒有 `pyproject.toml`，你預期會發生什麼？（用自己的話即可。）

**示範檔行為與理解**

- [ ] 在專案根執行 `uv run basic.py`（或教師指定之同結構檔名），終端機出現**一整句**問候，且句中可看出 `agent_name` 設定的名稱或稱呼（與 **WG-03** 精神一致即可）。
- [ ] 能說明：`from langchain_openai import ChatOpenAI` 這一行裡，`ChatOpenAI` 是從哪一個**已安裝套件**（PyPI 上的發佈名稱）拿出來的名稱？
- [ ] 能說明：`from dotenv import load_dotenv` 對應的是哪一個 PyPI 套件？若程式裡**沒有**呼叫 `load_dotenv()`，執行時**環境變數是否會因此自動從 `.env` 載入**？（用自己的話即可。）
- [ ] **邊界**：若把兩行頂層 `from … import` 整段刪掉、進入點內容不變，在已安裝兩依賴的專案裡，`uv run basic.py` 是否仍可能正常輸出問候？為什麼？（與「有沒有用到那些名稱」有關即可。）

### 提示（選讀）
> 參考 wiki「**函式與模組**」：`import`／`from … import` 的對象須為「目前執行環境裡已安裝」的套件；`uv add` 負責把套件納入**這個專案**的依賴宣告並裝進 uv 管理的環境。未在程式裡使用的匯入**不會**自動多做一件事（例如不會只因匯入就載入 `.env`）。
> PyPI **`langchain-openai`**（連字號）在程式裡通常對應 **`langchain_openai`**（底線）底下的名稱（如 **`ChatOpenAI`**）。
> PyPI **`python-dotenv`** 常見寫法為 **`from dotenv import load_dotenv`**；僅用 `import dotenv` 做一行驗收亦可。

### 藍本對應
**指令與快速驗收（專案根）**

```bash
uv add langchain-openai python-dotenv
```

```bash
uv run python -c "import langchain_openai; import dotenv; print('deps-ok')"
```

**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

if __name__ == "__main__":
    agent_name = "法鬥超人"
    message = f"Hello, 我是{agent_name}，很開心認識你!"
    print(message)
```

---

## Challenge WG-05：讀設定、不賣鑰匙——`load_dotenv`、讀環境變數與安全診斷輸出
### 情境
專案裡常把 **API 金鑰**放在 **`.env`**（不進版控），程式執行時要「載入 `.env` 到環境」再「依名稱讀出字串」。**請在專案根目錄**（與 `pyproject.toml` 同層）**新建一個檔案** **`.env`**，用純文字編輯器寫入至少一行 `OPENAI_API_KEY=你的金鑰`（實際金鑰由你或課堂提供；**不要**把含真金鑰的 `.env` 交進版控）。本題只練這一段：**先**在進入點呼叫 **`load_dotenv()`**，再用 **`os.getenv("OPENAI_API_KEY")`** 讀到變數（可能為 `None` 或空字串）。終端機上**只能**用「有／無」或**不會暴露金鑰本體**的短句說明狀態——**禁止**把金鑰整串 `print` 出來（螢幕錄影、截圖外洩風險）。**本題另一重點**：用 **單行註解符號 `#`**（寫在該行最前面）把 **WG-04** 的問候程式「關起來不執行」——執行時 Python 會**略過**這幾行，等於暫時從流程裡拿掉，但程式碼仍留在檔案裡方便日後取消註解再接回。通過後可銜接 **WG-06**（用 `if`／`else` 依有無金鑰印不同提示）。**本題不要求**呼叫 `ChatOpenAI` 或 `invoke`。

### 規格
- **檔案**：在**專案根目錄**建立新檔 **`.env`**（檔名開頭為點號；與示範檔 `basic.py` 同層、不在子資料夾），內容至少含 `OPENAI_API_KEY=` 與對應值；若課堂採「僅用系統環境變數、不建檔」可經教師口頭約定略過建檔步驟，但驗收時仍須能說明「有／無 `.env` 時 `getenv` 差異」。
- 在示範檔（藍本為 `basic.py`）頂層新增 **`import os`**（與既有兩行 `from … import` 並列，順序可為：`ChatOpenAI`、`load_dotenv`、`os`）。
- 在 `if __name__ == "__main__":` 區塊內，**第一行**呼叫 **`load_dotenv()`**（讓後續 `os.getenv` 能讀到 `.env` 寫入的變數）。
- 以變數（例如 `api_key`）保存 **`os.getenv("OPENAI_API_KEY")`** 的結果。
- **診斷輸出**：僅能印出「已設定／未設定」或等價語意，**不得**在 `print`／f-string 中嵌入 `{api_key}` 或任何會印出金鑰本體的寫法。
- **問候與註解**：本題藍本將 **WG-04** 的 `agent_name`／問候／`print(message)` **三行各加上行首 `#`**（**單行註解**），使這段程式**不被執行**；註解僅作用於**該行**（要停用多行就逐行加 `#`，或之後再學區塊註解）。先專心練環境讀取與一行診斷；**WG-06** 起再視藍本決定是否恢復問候（取消 `#` 或改寫）。

### 驗收條件
- [ ] 已在**專案根**建立 **`.env`** 新檔並寫入 `OPENAI_API_KEY`（或經教師同意改以系統環境變數測試，但仍能連結回說明「根目錄 `.env`」的用途）。
- [ ] 在專案根執行 `uv run basic.py`（或教師指定檔名），終端出現**一行**金鑰狀態診斷（有／無或等價），**不**出現完整 `sk-…` 或長密文本體（亦**不**在 f-string 內嵌 `{api_key}`）。
- [ ] 能說明：`load_dotenv()` 放在區塊開頭與放在 `print` 之後，對「`os.getenv` 讀不讀得到 `.env`」可能差在哪？
- [ ] **邊界**：若專案根**沒有** `.env` 檔、也沒在系統預先匯出 `OPENAI_API_KEY`，你預期 `os.getenv("OPENAI_API_KEY")` 多半是什麼？診斷行應長什麼樣？
- [ ] 能說明：藍本裡問候那幾行前面的 **`#`** 有什麼效果？若把其中一行的 `#` 刪掉、其餘仍保留註解，執行時可能發生什麼事？

### 提示（選讀）
> **`#` 單行註解**：從 `#` 起到**該行結尾**都視為註解，直譯器不會當程式執行；常用來暫停某幾行、寫給人看的說明，或像本題一樣「先關掉舊輸出、專心測新功能」。
> 布林判斷可用 `if api_key:`（`None` 與空字串多為「假」）；本題**尚未**要求寫成 `if`／`else` 兩支不同台詞，留給 **WG-06**。
> **勿**在 `print(f"...{api_key}...")` 內嵌變數值，以免終端洩漏金鑰；一行內用 `if api_key else` 或兩段字串擇一即可。
> 若誤把金鑰印出，改為只印「長度」仍可能被推測；課堂上以「只說有無」最安全。

### 藍本對應
**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"OPENAI_API_KEY：{'已設定' if api_key else '未設定'}")
    # agent_name = "法鬥超人"
    # message = f"Hello, 我是{agent_name}，很開心認識你!"
    # print(message)
```

---

## Challenge WG-06：有通行證才開門——`if`／`else` 依金鑰有無分支
### 情境
在 **WG-05** 已能讀到金鑰變數的前提下，使用者體驗上常希望：**有金鑰**與**沒金鑰**時，程式用**不同的一句話**提醒下一步（例如可呼叫模型 vs. 請先設定環境）。本題在相同檔案結構上加入 **`if api_key:`** 與 **`else:`**，兩分支各至少 **`print` 一行**且內容**不同**；**仍不**建立 `ChatOpenAI` 或呼叫 `invoke`。通過後可銜接 **WG-07**（收成 `def main()`）。

### 規格
- 延續 **WG-05**：頂層匯入、`load_dotenv()`、`api_key = os.getenv("OPENAI_API_KEY")`。
- 以 **`if api_key:`**／**`else:`** 包住（或緊接其後）**兩組不同的**狀態 `print`（分支內各至少一行；文字由教學約定，但語意須區分「有讀到可用金鑰」與「沒讀到」）。
- **診斷安全**：與 **WG-05** 相同，**任何**分支都**不得**印出完整金鑰字串（**不**在 f-string 內嵌 `{api_key}`）。
- **問候**：藍本將問候維持為**註解**（與 **WG-05** 相同）；若教師希望兩分支後都印問候，可取消註解並自行對齊驗收。

### 驗收條件
- [ ] `uv run basic.py`：無金鑰時與有金鑰時（或暫時改環境／`.env`），**狀態提示行**文字不同，且皆**不**洩漏完整金鑰。
- [ ] 能指出：`if` 的條件式為何能同時涵蓋 `None` 與空字串兩種「沒有可用金鑰」的情況？（用自己的話即可。）
- [ ] **邊界**：若誤寫成 `if api_key == True:`，與 `if api_key:` 在本題情境下可能差在哪？（提示：變數型態。）

### 提示（選讀）
> `else` 可接在 `if` 同層縮排；本題藍本在兩分支各 **`print` 一行**、**不**呼叫 API，問候維持註解。**早退 `return`** 見 **WG-07**。若取消註解問候，須想清楚要放在「兩分支後」或「僅有金鑰時」。

### 藍本對應
**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("OPENAI_API_KEY：已設定")
    else:
        print("未設定 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
    # agent_name = "法鬥超人"
    # message = f"Hello, 我是{agent_name}，很開心認識你!"
    # print(message)
```

---

## Challenge WG-07：一行進門、其餘進房——收成 `def main()` 與精簡進入點
### 情境
當進入點區塊變長，慣例會把主要流程收進 **`def main():`**，讓 `if __name__ == "__main__":` **只負責呼叫** `main()`，方便閱讀與之後擴充（例如加參數、測試）。本題把 **WG-06** 的邏輯移入 **`main()`**，並依藍本在 **無金鑰**時 **`return`**、狀態字樣可與 **WG-06** 台詞不同（**以本題藍本為準**）；頂層僅保留匯入與進入點一行呼叫。

### 規格
- 新增 **`def main() -> None:`**（`-> None` 可選，若教學未教型別註解可省略，但藍本保留示範）。
- **`main` 函式內**含：`load_dotenv()`、`api_key`、依有無金鑰之 **`if`／`else`**；**無金鑰**時在 `else` 印提示後 **`return`** 結束（**不**往下執行）。問候相關程式在藍本中**維持註解**（與 **WG-06** 相同）。
- `if __name__ == "__main__":` 區塊內**僅** `main()`（或等價單一呼叫），**不**再堆疊其他可執行述句。
- **不要求**新增其他檔案或改 `pyproject.toml`。

### 驗收條件
- [ ] `uv run basic.py` 在「有金鑰／無金鑰」兩種情境下，**分支與早退**（`return`）行為與**本題藍本**一致；狀態字樣以藍本為準（不必與 **WG-06** 逐字相同）。
- [ ] 能說明：為什麼「只把程式搬進函式」通常**不會**改變執行結果，但對維護有幫助？
- [ ] **邊界**：若誤把 `load_dotenv()` **只**放在 `if __name__` 區塊、卻放在 `main()` 呼叫**之後**，會發生什麼事？

### 提示（選讀）
> 之後若要寫測試，常會 `import` 模組而不跑 `main()`；把副作用收進 `main()` 是常見第一步。

### 藍本對應
**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("已讀到 API 金鑰設定（內容不顯示）；後續可呼叫模型。")
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return
    # agent_name = "法鬥超人"
    # message = f"Hello, 我是{agent_name}，很開心認識你!"
    # print(message)

if __name__ == "__main__":
    main()
```

---

## Challenge WG-08：第一通打進大模型——`ChatOpenAI` 與 `invoke` 最小呼叫
### 情境
依賴已在 **WG-04** 安裝、環境讀取與分支在 **WG-05～07** 演練過；本題在**有金鑰**時實際建立 **`ChatOpenAI`**、送一句**繁體中文**提示給 **`invoke`**，並把模型回覆的**文字內容**印到終端。**無金鑰**時**不得**呼叫 API：先印提示再 **`return`**（與 **WG-07** 早退寫法一致）。呼叫 API 需要**網路**，且可能**計費**；驗收前請確認課堂約定。通過後可銜接 **WG-09**（**`while`** 互動迴圈 + **`input()`**，每輪 **`invoke`**），再銜接 **WG-10**（同一迴圈骨架下改 **`stream`** 串流輸出）。

### 規格
- 延續 **WG-07** 結構：`def main()`、`load_dotenv`、`api_key`。
- **流程（藍本採「先判斷、再主流程」）**：
  - **`if api_key:`** 僅印**一行**狀態（表示讀到金鑰、可進入後續；**不**在此巢狀寫入 `ChatOpenAI`／`invoke`）。
  - **`else:`** 印「尚未讀到…」類訊息後 **`return`**，確保不會執行到 API 相關程式。
  - 上述 `if`／`else` **之後**（與 `if api_key` **同層**、且在 `return` 之後自然只會在有金鑰時執行）：建立 **`ChatOpenAI(model="gpt-4o-mini", temperature=0.2)`**，**`invoke`** 繁中提示，**`print(response.content)`**。
- **問候**：本題藍本**不含** **WG-03** 問候（前幾題若已註解問候，本題延續「最小呼叫」主軸即可）。
- **安全**：任何分支仍**不得** `print` 完整 `OPENAI_API_KEY`。

### 驗收條件
- [ ] 有設定有效 `OPENAI_API_KEY` 時，`uv run basic.py` 會印出**至少一行**模型產生的繁中文本（非空），且**不**含完整金鑰字串。
- [ ] 未設定金鑰時，程式**不**拋出未捕捉的 API 認證錯誤（應走 `else` 並 **`return`** 早退，**不**執行 `ChatOpenAI`／`invoke`），且終端仍友善提示。
- [ ] 能說明：`invoke` 的回傳值型別為何通常**不是**純 `str`，卻仍可用 `.content` 取出要給使用者看的文字？
- [ ] **邊界**：若金鑰錯誤或網路中斷，你預期程式可能在哪一行附近失敗？（不要求本題寫完整 `try`／`except`，能說出觀察點即可。）

### 提示（選讀）
> 若 `ModuleNotFoundError: langchain_core`，多半是環境未用 `uv run` 執行；請在專案根用 **`uv run basic.py`**。
> 金鑰放專案根 `.env` 時，檔案內常寫一行：`OPENAI_API_KEY=你的金鑰`（**不要**把真金鑰交進版控）。

### 藍本對應
**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print("已讀到 API 金鑰設定（內容不顯示）；後續可呼叫模型。")
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    response = llm.invoke(
        "用一句繁體中文自我介紹，並說你準備好回答使用者的問題了。"
    )
    print(response.content)

if __name__ == "__main__":
    main()
```

---

## Challenge WG-09：櫃台問答不斷線——互動迴圈與多輪 `invoke`
### 情境
**WG-08** 只呼叫模型**一次**就結束。實務上常希望終端機像「聊天程式」：**重複**讀使用者打字、送進模型、印回覆，直到使用者輸入離開指令。本題在 **WG-08** 的早退與 **`ChatOpenAI` 實例**之後，加上 **`while True`** 與 **`input()`**；每輪用 **`invoke`** 傳入使用者這一行字串，再 **`print`** 助手回覆的 **`content`**。這樣 **wiki「條件與迴圈」** 裡的 **`while`** 與 **「輸入輸出」** 裡的 **`input()`** 會在同一份小程式裡**一次串起來**。通過後可銜接 **WG-10**（同一迴圈，改為 **`stream`** 串流印出）。

### 規格
- 延續 **WG-08**：`def main()`、`load_dotenv`、無金鑰則印提示後 **`return`**（**不**呼叫 API）。
- 有金鑰時建立 **`ChatOpenAI(model="gpt-4o-mini", temperature=0.2)`**（模型名可依課程替換，驗收以藍本為準）。
- **`while True:`** 迴圈內：
  - 用 **`input()`** 讀一行使用者輸入（藍本提示字可自訂，須讓學生知道輪到誰打字）。
  - 若使用者輸入為**結束指令**（藍本：`quit`／`exit`／`q`，**不分大小寫**可比對），印一句告別並 **`break`** 離開迴圈。
  - 可選：若使用者只送**空白**，**不**呼叫 API，**`continue`** 進下一輪（藍本採此行為）。
  - 否則 **`response = llm.invoke(使用者字串)`**，再印 **`response.content`**（建議加前綴如「助手：」方便對齊終端閱讀）。
- **本題不要求** `stream`／`astream`（留給 **WG-10**）；**不要求**對話歷史串列（留給 **WG-11**）、**不要求**寫入檔案。

### 驗收條件
- [ ] 有金鑰時，`uv run basic.py` 可進入迴圈：至少手動輸入**兩輪**一般問題，助手回覆皆為可讀繁中（或課堂約定語言），且**不**洩漏金鑰。
- [ ] 輸入結束指令後程式**正常結束**（無未捕捉錯誤），且**不**再呼叫下一輪 API。
- [ ] 能說明：為什麼用 **`while True`** 搭配 **`break`**，而不是只寫一個「條件式 `while`」？
- [ ] **邊界**：若使用者第一輪就直接輸入結束指令，你預期會印幾次模型回覆？為什麼？

### 提示（選讀）
> **`input()`** 回傳的是字串；可用 **`.strip()`** 去掉頭尾空白再判斷是否空字串。
> 結束關鍵字比對可用 **`.lower()`** 做不分大小寫。
> 若終端中文顯示異常，多為主控台編碼問題，與程式邏輯無關（見 **WG-03** 提示區選讀）。

### 藍本對應
**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print("已讀到 API 金鑰設定（內容不顯示）；進入對話（輸入 quit / exit / q 結束）。")
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    while True:
        user_text = input("你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        response = llm.invoke(user_text)
        print("助手：", response.content)

if __name__ == "__main__":
    main()
```

---

## Challenge WG-10：回答像打字機——串流式回答（`stream`）
### 情境
**WG-09** 每輪要等模型**整段**生成完才一次印出；使用者體感上，改成**邊生成邊出字**會更像常見的聊天介面。本題**保留 WG-09 的迴圈與 `input`／離開指令邏輯**，只把「一輪助手回覆」從 **`invoke` + `print(整段)`** 改成對同一使用者字串呼叫 **`llm.stream(...)`**，並在 **Python 層**用 **`for chunk in ...:`** 逐塊取出文字，以 **`print(..., end="", flush=True)`** 接續印在**同一行或連續輸出**（藍本於串流結束後 **`print()` 換行**）。需**網路**，且可能**計費**。通過後可銜接 **WG-11**：在**記憶體**裡用訊息**串列**保留多輪脈絡，並維持 **`llm.stream(context_messages)`**（**`context_messages = [*messages, human_message]`**）的串流輸出（**關閉程式即消失**，仍**不**寫入檔案）。

### 規格
- 架構與 **WG-09** 相同：早退、`llm` 建立、`while True`、`input`、結束指令、`continue` 空輸入。
- **差異**：將 `llm.invoke(user_text)` 改為 **`for chunk in llm.stream(user_text):`**（或課程約定之等價寫法），僅印出有內容的 **`chunk.content`**（若某版為 `None` 則略過），並以 **`end=""`**、**`flush=True`** 串接；該輪結束後 **`print()`** 補一行換行。
- **不要求**改為 async／`astream`（除非教師另行升級）；**不要求** WebSocket 或前端。
- **不要求**跨輪 **`messages`** 脈絡串列（留給 **WG-11**）。

### 驗收條件
- [ ] 有金鑰時，連續輸入至少一輪一般問題，終端可觀察到助手回覆**分段出現**（與 **WG-09** 一次跳整段不同），且結尾換行合理。
- [ ] 結束指令行為與 **WG-09** 一致（離開迴圈、不再呼叫下一輪）。
- [ ] 能說明：**`invoke`** 與 **`stream`** 在「你什麼時候拿到完整文字」這點有什麼不同？
- [ ] **邊界**：若某一輪網路中斷，你預期錯誤比較可能發生在 **`for` 迴圈內**還是**外**？（不要求本題完整 `try`／`except`，能指認即可。）

### 提示（選讀）
> 部分教材將「串流」與 **SSE**／**Web** 綁在一起；本題僅在**終端機**用 **`print`** 模擬「逐字／逐塊」體感。
> 若 `chunk.content` 為空字串，不要印出多餘換行，避免版面碎裂。

### 藍本對應
**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print("已讀到 API 金鑰設定（內容不顯示）；進入對話（串流輸出；輸入 quit / exit / q 結束）。")
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    while True:
        user_text = input("你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        print("助手：", end="", flush=True)
        for chunk in llm.stream(user_text):
            if chunk.content:
                print(chunk.content, end="", flush=True)
        print()

if __name__ == "__main__":
    main()
```

---

## Challenge WG-11：短期記憶只活在當下——對話脈絡（記憶只在 RAM）
### 情境
**WG-09～10** 每輪只把「當下這一句使用者輸入」送進模型，模型**看不到**先前幾輪說過什麼，因此無法延續暱稱、前情提要或指代詞。實務上會在程式裡用一個**存在記憶體中的串列**（本題稱 **`messages`**）依序放入 **`HumanMessage`**（使用者）與 **`AIMessage`**（助手），**持續累積**「到目前為止」的對話時間軸。

本題**延續 WG-10 的終端體感**：仍以 **`stream`** 邊生成邊 **`print(..., end="", flush=True)`**；差別是 **`stream` 的參數改為「本輪要給模型看的那份訊息串列」**。課堂建議另用變數名 **`context_messages`** 專指**送進 **`llm.stream(...)`** 的那一個引數**：在 **WG-11** 裡，先把本輪字句建成 **`human_message = HumanMessage(...)`**，再 **`context_messages = [*messages, human_message]`**（**新開一份串列**：前半是**已結束回合**的累積 **`messages`**，最後一則是本輪使用者；**此時尚未**把 **`human_message`** **`append` 進 `messages`**）。串流結束後，再依序 **`messages.append(human_message)`**、**`messages.append(AIMessage(...))`**，下一輪脈絡才不會缺字。**WG-12** 起會改以 **`history`** 累積對話訊息，並加上 **`system_message`**，送模 **`[system_message, *history, human_message]`**（**WG-14** 起 **`history`** 可含 **WG-13** 之 **`ToolMessage`** 鏈）；到 **WG-16** 再把其中的「過去段」換成裁切後的 **`past`**，即 **`context_messages = [system_message, *past, human_message]`**，與**完整**累積的 **`history`** **脫鉤**，以練習預算裁切。

本題**刻意不做**寫檔／讀檔：關掉程式或當機後，脈絡**立刻消失**——用來參考「RAM 內短期記憶」與「寫進檔、下次載回」的差異。通過後可銜接 **WG-12**（**`SystemMessage`** 與 **`build_system_prompt()`**，送模 **`[system_message, *history, human_message]`**，可先仍**不**寫 JSONL）、再 **WG-13**（工具 **ReAct**）、再 **WG-14**（對話**寫入** JSONL）、再 **WG-15**（開機**讀回**接續）。

### 規格
- 延續 **WG-07～10**：`def main()`、`load_dotenv`、無金鑰則印提示後 **`return`**；有金鑰時建立 **`ChatOpenAI`**；**`while True`**、`input()`、結束指令（`quit`／`exit`／`q`，不分大小寫）、空白行 **`continue`**。
- 在進入迴圈前（或 `llm` 建立後）宣告 **`messages`** 為**空串列**，型別上可視為「依序儲存多則 **`langchain_core.messages`** 中的 **`HumanMessage`／`AIMessage`**」。
- 每一輪有效使用者輸入：
  1. **`human_message = HumanMessage(content=...)`** — 先把本輪使用者句建成物件（**尚未**寫入累積串列）。
  2. **`context_messages = [*messages, human_message]`**：**本輪送進 **`llm.stream`** 的引數**；為**新串列**，內容等於「**已結束的 **`messages`**」加上本則 **`human_message`**」，用來參考後續題組「累積一份、送模另一份」的拆法。
  3. **`print("助手：", end="", flush=True)`**（與 **WG-10** 對齊前綴習慣）。
  4. **`for chunk in llm.stream(context_messages):`**：將**本輪 **`context_messages`** 所代表的脈絡**送進模型；對有內容的 **`chunk.content`** 以 **`print(..., end="", flush=True)`** 串接；同時把片段累積到一字串變數（例如 **`reply_parts`** 再 **`"".join(...)`**）。
  5. **`print()`** 補換行。
  6. **`assistant_message = AIMessage(content=完整助手字串)`** 後，依序 **`messages.append(human_message)`**、**`messages.append(assistant_message)`** — 助手內容必須與終端印出的全文一致，否則下一輪模型讀到的歷史會與你實際看到的不符。
- **禁止**：把 `messages` 寫入磁碟、或從檔案載入歷史（留給 **WG-14**／**WG-15**）。
- **不要求**：自訂 **SystemMessage**／人設（留給 **WG-12**；本題可選加，非驗收重點）。

### 驗收條件
- [ ] 有金鑰時，至少一輪助手回覆在終端為**分段／逐塊出現**（與 **WG-10** 類似的串流體感），且換行合理。
- [ ] 有金鑰時，連續兩輪以上對話，**第二輪起**模型回覆能合理承接**第一輪**給過的資訊（例如先請助手記住一個自訂代號或數字，下一輪再問「剛才那個是多少」— 由教師或學生自訂台詞，**不**在教案背誦標準答案）。
- [ ] 能說明：為什麼 **`messages`** 要同時放**使用者**與**助手**的訊息，而不是只放使用者的句子？
- [ ] **邊界**：若使用者**直接關閉終端**而不輸入結束指令，重開程式後，你預期上一輪的對話還在不在？為什麼？
- [ ] **邊界**：若某一輪在 **`llm.stream(context_messages)`** 進行中程式就當掉（**尚未**執行到 **`messages.append(human_message)`**），你預期 **`messages`** 裡會不會出現本輪使用者那句？為什麼？（能描述即可，不要求 `try`／`finally`。）

### 提示（選讀）
> 參考 wiki「**資料結構**」：串列可 **`append`**，且**有順序**，適合當「對話時間軸」。
> **`HumanMessage`**／**`AIMessage`** 是框架用來標記「這句話誰說的」；模型才能區分角色。
> 若出現「模型好像沒讀到上一輪」，先檢查 **`llm.stream`** 的參數是否為 **`context_messages = [*messages, human_message]`**（或語意等價），是否把**舊回合**一併帶上，而不是只傳本輪字串。
> 串流印完後若忘記 **`messages.append(human_message)`**／**`messages.append(assistant_message)`**，下一輪會少掉本輪或助手那一側的紀錄。

### 藍本對應
**示範檔全檔（`basic.py`）**

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from dotenv import load_dotenv
import os

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        print(
            "已讀到 API 金鑰設定（內容不顯示）；進入對話（脈絡僅存於記憶體；關閉程式即消失；輸入 quit / exit / q 結束）。"
        )
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    messages: list[BaseMessage] = []

    while True:
        user_text = input("你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        human_message = HumanMessage(content=user_text)
        # 本輪送模：舊回合在 messages，本則使用者僅先進 context_messages；WG-16 起改為 [system_message, *past, human_message]
        context_messages = [*messages, human_message]
        print("助手：", end="", flush=True)
        reply_parts: list[str] = []
        for chunk in llm.stream(context_messages):
            if chunk.content:
                print(chunk.content, end="", flush=True)
                reply_parts.append(chunk.content)
        print()
        assistant_text = "".join(reply_parts)
        assistant_message = AIMessage(content=assistant_text)

        messages.append(human_message)
        messages.append(assistant_message)

if __name__ == "__main__":
    main()
```

---

## Challenge WG-12：人設寫進系統層——SystemMessage 與可變系統字串
### 情境
**WG-11** 已能以 **`HumanMessage`／`AIMessage`** 串列維持多輪脈絡，但尚未在送模串列**最前**固定放入「課堂規則、人設、安全邊界」等**系統層**文字。實務上常把這些收斂成 **`build_system_prompt()`** 回傳的一整段字串，再包成 **`SystemMessage`**，且**不**跟著 **`user`／`assistant`** 逐句寫進對話檔（若日後有 **JSONL**，仍只存人機回合）。

本題在**延續 WG-11 的串流節奏**、且**仍可不寫入磁碟**的前提下，練習 **`system_message` 與 `history` 分離**：累積側建議 **`history: list[BaseMessage]`**（僅 **Human／AI**），每輪 **`context_messages = [system_message, *history, human_message]`** 再 **`llm.stream`**。**專案示範檔 `basic.py`** 若合併多題，會再加上 **`load_session_jsonl`／`save_session_jsonl`**（見 **WG-14～15**）；本題獨立作答時**不要求** JSONL，以免與「先釐清 system／history 分工」混淆。

通過後可銜接 **WG-13**：在單檔內練習 **`bind_tools`**、**`ToolMessage`** 與 **ReAct** 式多段 **`invoke`**。再銜接 **WG-14**／**WG-15** 將 **`history`**（可含 **`ToolMessage`**）寫入／讀回 **JSONL**（送模仍維持 **`[system_message, *history, human_message]`**），之後再接 **WG-16** 預算裁切、**WG-17**（**transcript**）與 **WG-18**（長期記憶）。

### 規格
- 延續 **WG-07～11**：`def main()`、`load_dotenv`、無金鑰則印提示後 **`return`**；有金鑰時 **`ChatOpenAI`**、**`while True`**、`input()`、結束指令、空白行 **`continue`**。
- 在進入 **`while`** 之前：實作 **`def build_system_prompt() -> str`**，並建立 **`system_message = SystemMessage(content=build_system_prompt())`**；**`history: list[BaseMessage] = []`**（啟動時**不**從檔案載入）。
- **`build_system_prompt()` 回傳字串**須含（1）**一段課堂規則**（示範寫在函式內 **`system_text`**，內容須含「**繁體中文**」等可驗收關鍵字）；（2）**一段顯示名稱或人設片段**（示範為函式內 **`nick`**；**選修**：改讀 **`os.getenv("ASSISTANT_DISPLAY_NAME")`**）。
- **合併工作坊作答（如專案根 `main.py`）**：可將上兩段收斂為 **`build_classroom_base_prompt() -> str`**（僅課堂語氣與**【本場次顯示名稱】**，暱稱讀 **`ASSISTANT_DISPLAY_NAME`** 並對空白 **fallback** 與 **WG-12** 選修敘述一致）。**WG-13** 所要求「**何時必須用工具**」之文字，**不**強制寫進此函式；可改由 **`compose_system_string`** 其它段落、**ReAct** 前之組裝、或 **tool 的 description** 補足——教師驗收時須能指出**工具約束**最終出現在送模 **system** 的哪一處，且行為仍滿足 **WG-13**。
- 每一輪有效使用者輸入：送進模型處與 **WG-11** 同一精神——**先組本輪 `context_messages`、串流成功後才把本輪 Human／AI 寫回累積**。建議命名：**`human_message = HumanMessage(...)`** → **`context_messages = [system_message, *history, human_message]`** → **`llm.stream(context_messages)`** → **`history.append(human_message)`**、**`history.append(AIMessage(...))`**。**不要**把 **`system`** 與 **`history`** 硬併成「迴圈內一路 **`append`** 的單一串列」。
- **禁止**：把 **`SystemMessage`** 當成一般對話列 **`append` 進 `history`**；**本題不要求**實作 **`save_session_jsonl`**／讀檔（留給 **WG-14**／**WG-15**）。
- **不要求**：改 **metadata** 或 **JSONL** 欄位（尚無檔案格式）。

### 驗收條件
- [ ] 有金鑰時，**`llm.stream(context_messages)`**（**`context_messages = [system_message, *history, human_message]`** 或語意等價）能跑通，且終端串流行為與 **WG-11** 一致（前綴 **`助手：`** 等可保留）。
- [ ] 能指出：程式**哪一段**建立 **`system_message`**、**哪一段**初始化 **`history`**，以及迴圈內**哪一行**把兩者與 **`human_message`** 組進 **`context_messages`**。
- [ ] 能說明：**`build_system_prompt()`** 回傳字串裡，**課堂規則**與**顯示名稱**各對應函式內哪一段；修改 **`nick`** 後重開程式，模型收到的系統區塊應反映新字串。
- [ ] 能一句話說明：為何 **system** 不放在 **`history`** 裡與人機回合混在同一串列（並參考「**JSONL** 對話列通常存 **user／assistant**；併 **WG-13** 時另含 **`tool`** 列，見 **WG-14**」）。
- [ ] **邊界**：**`context_messages[0]`** 是哪一種訊息？本輪 **`human_message` 在送模串列中的位置**為何（相對於 **`history`**）？
- [ ] **邊界**（選修）：若 **`nick`** 改讀 **`os.getenv("ASSISTANT_DISPLAY_NAME")`**，環境變數**未設**與設為**空字串**時，你預期顯示名分別如何？（須與實作一致。）

### 提示（選讀）
> **`SystemMessage`** 與 **Human／AI** 一樣是 **`langchain_core.messages`** 的型別；差在角色語意是「系統規則」而非使用者或助手回合。
> 每輪 **`context_messages = [system_message, *history, human_message]`** 利用**串列展開**把「固定首則」「檔案載入且已結束的對話」「本輪使用者」接成**送模專用**的一份，**不必**與 **`history` 共用同一個 list 物件**。
> 若出現**兩則** **system**，檢查是否在迴圈內重複建立 **`SystemMessage`**，或是否誤把 **`loaded`** 裡也塞了 **system**。
> 示範檔啟動 **`print`** 可含「**可選 .env：ASSISTANT_DISPLAY_NAME**」字樣以預告擴充；**未**在 **`build_system_prompt`** 讀取時，驗收以「函式內實際字串」為準，避免口頭與程式不一致。
> 參考 wiki「**函式與模組**」：**`def`**、**`return`**，把組字收斂成單一函式較好測與改。

### 藍本對應
以下節錄對齊 **`build_system_prompt`** 與 **`system_message`／`history` 分離**（**本題可不寫 JSONL**）。**專案根目錄 `basic.py`** 合併 **WG-12～WG-18** 時會再接 **`load_session_jsonl`／`save_session_jsonl`**（**WG-14～15**）。

```python
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

def build_system_prompt() -> str:
    """建立系統提示字串。"""
    system_text = "你是課堂程式助教。請使用繁體中文；先給一句重點結論，必要時再補一句說明。"
    nick = "法鬥超人"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}"

def main() -> None:
    # load_dotenv()、api_key 檢查、建立 llm
    system_message = SystemMessage(content=build_system_prompt())
    history: list[BaseMessage] = []

    # while 內：human_message →
    # context_messages = [system_message, *history, human_message] → llm.stream →
    # history.append(human_message); history.append(AIMessage(...))
```

**選修：改接環境變數時**可於 **`.env`** 備一行（僅供教師備課，**不**強制作成驗收台詞）：

```env
# ASSISTANT_DISPLAY_NAME=Vans的助教
```

---

## Challenge WG-13：會查表才算真 Agent——工具呼叫與 ReAct 迴圈（單檔）
### 情境
**WG-12** 讓模型以 **system + history + 本輪使用者** 往來，回覆皆為**純文字**。實務上常讓模型**決定何時呼叫工具**（計算、查詢、對外 API 等），再依**工具回傳**續寫下一則模型訊息，直到不再需要工具——這種「**Reason + Act**」迴圈常稱 **ReAct**。本題在**單一 `.py` 檔**內練習 **`@tool`**、**`bind_tools`**、**`tool_calls`** 與 **`ToolMessage`**，與 **`memory_react_agent.py`** 之 **`run_react_turn`** 精神對齊；**不要求**本題接 **JSONL**／持久化／字元預算，以免與後續 **WG-16** 混淆。

通過後可銜接 **WG-14**：在 **WG-12** 送模結構下將 **`history`**（含 **ReAct** 鏈之 **`ToolMessage`**）寫入 **JSONL**（仍不寫 **system**），再 **WG-15** 載回；之後 **WG-16** 以 **`pick_consolidation_boundary`** 做短期送模裁切（成本與 **`history`** 一併納入 **`ToolMessage`**；邊界仍以 **Human 回合開頭**為主，與 **`memory_react_agent`** 類題可參考）。

### 規格
- **延續 WG-12** 之 **`build_system_prompt()`／`SystemMessage`** 概念：系統字串須含**至少一段「何時必須用工具」**的規則（範例：算術須用工具、不可純心算）。
- 以 **`langchain_core.tools.tool`** 之 **`@tool`** 定義至少**一支**可呼叫函式（課堂可四則運算擇一或全套）；集中於 **`TOOLS`** 列表，並以 **`llm.bind_tools(TOOLS)`** 取得 **`llm_with_tools`**。
- **單輪使用者輸入**的處理流程（與 **`run_react_turn`** 同構）：
  1. 組初始 **`messages = [SystemMessage(...), *past, HumanMessage(user_text)]`**（**`past`** 為本輪之前之訊息；僅 **Human／AI** 亦可，若本題已含工具鏈則可含 **ToolMessage**）。
  2. **`response = llm_with_tools.invoke(messages)`**。
  3. 若 **`response.tool_calls`** 非空：**`messages.append(response)`**，逐筆執行工具、建立 **`ToolMessage(content=..., tool_call_id=...)`** 並 **`append`**，回到步驟 2。
  4. 若無 **`tool_calls`**：將最後一則 **AI** 文字作為本輪對使用者顯示的結論（**不要求**本題 **`stream`**，避免與多段 **`invoke`** 競合）。
- **邊界**：工具名稱不在參考表時**不得**崩潰；可將錯誤說明字串放入 **`ToolMessage.content`**。
- **選修**：將本輪新訊息（含 **Tool**）**append** 進 **`history`**，供下一輪 **`past`**；**選修**：**`_normalize_tool_args`** 類相容層（因應部分後端非標準 **args** 形狀）。

### 驗收條件
- [ ] 能跑通：使用者提出須依工具才能完成的任務時，終端可觀察到程式**實際呼叫工具**（非僅模型口頭心算）。
- [ ] 能指出：**哪一行／哪一段** **`bind_tools`**，以及**哪一層迴圈**在處理 **`tool_calls`** 與 **`ToolMessage`**。
- [ ] 能說明：**`AIMessage`（含 tool_calls）** 與 **`ToolMessage`**、最終 **`AIMessage`（純文字）** 在串列中的順序與角色。
- [ ] **邊界**：口頭描述若**只做一次 `invoke`、不處理 tool_calls**，可能錯在哪裡。

### 提示（選讀）
> 參考 **`memory_react_agent.py`**：**`run_react_turn`**、**`TOOLS`**、**`_TOOL_MAP`**、**`_normalize_tool_args`**。
> **JSONL** 若日後要存工具列，需另訂 **`role`**／序列化規則；**本題可不寫檔**。
> **WG-16** 的 **`pick_consolidation_boundary`** 以 **Human 回合開頭**為邊界；一輪內若有多則 **AI／Tool**，裁切規則不同，本題不強求。

### 藍本對應
以下為**結構示意**（**非**完整可執行檔）；完整邏輯見 **`memory_react_agent.py`** 之 **`run_react_turn`** 與 **`main`** 呼叫方式。

```python
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b

TOOLS = [add_numbers]
# TOOL_MAP = {t.name: t for t in TOOLS}
# llm_with_tools = ChatOpenAI(...).bind_tools(TOOLS)
# messages = [SystemMessage(...), *past, HumanMessage(...)]
# while True:
#     r = llm_with_tools.invoke(messages)
#     if r.tool_calls:
#         messages.append(r)
#         for tc in r.tool_calls:
#             # 執行工具 → ToolMessage(..., tool_call_id=tc["id"])
#             ...
#     else:
#         messages.append(r)
#         break
```

---

## Challenge WG-14：對話落盤、人設不留痕——對話脈絡寫入 JSONL（先寫檔）
### 情境
**WG-12** 已讓 **`system_message`** 與 **`history`** 分離，且送模 **`context_messages = [system_message, *history, human_message]`**；關程式後 **RAM** 仍清空。**WG-13** 後 **`history`** 亦可含 **ReAct** 鏈上的 **`AIMessage`（含 `tool_calls`）** 與 **`ToolMessage`**。實務上把這些**可序列化**的對話訊息**寫進檔案**，留下可查紀錄，並讓下一題能**讀回**接續。

本題在**沿用 WG-12 的送模與累積節奏**的前提下，**只做寫檔**：在本輪使用者回合與助手／工具鏈**已依序 `append` 進 `history`**（串流或 **`invoke`** 流程結束後）呼叫寫檔，把 **`session_meta`** 與 **`history` 內可持久化的訊息** **整檔覆寫**到 JSONL（**第一行**為 **`metadata`**）。語法對齊 **wiki 6**：**`with open(..., "w", encoding="utf-8")`**、**`json.dumps`**、**`os.getenv`** 指定路徑。檔案長相可參考 **`session.jsonl.example`**，並**擴充** **`role: "tool"`** 等列以還原 **`ToolMessage`**（至少 **`content`**、**`tool_call_id`**）。若要做到「關閉再開仍保留完整 **ReAct** 語意」，**`assistant` 列**必須能還原**帶 `tool_calls` 的 `AIMessage`**（見下方 **規格** 之**完整版**定義）。

**刻意不做**：程式一啟動就**讀舊檔**還原 **`history`**（一律從**空串列**開始，體感仍像 **WG-12** 首次執行——再開程式不會自動接續）。讀檔接續留給 **WG-15**。

### 規格
- 延續 **WG-07～12**：`def main()`、`load_dotenv`、無金鑰則印提示後 **`return`**；有金鑰時 **`ChatOpenAI`**、**`while True`**、`input()`、結束指令、空白行 **`continue`**；**`build_system_prompt()`**、**`system_message`** 與 **`history`** 分離（同 **WG-12**）。
- **存檔路徑**：**`os.getenv("SESSION_JSONL_PATH", "session.jsonl")`**；預設 **`session.jsonl`**（**`session.jsonl.example`** 僅供參考，勿當預設寫入目標）。
- **啟動**：**`history`** 固定為**空串列**；**`session_meta`** 初值為 **`None`**。**禁止**在 **`while`** 之前呼叫任何「讀 JSONL 還原 **`history`**」的函式或等價邏輯。
- **送模（併 WG-13 之完整版）**：每輪在 **`[system_message, *history, HumanMessage(本輪)]`** 上做多段 **`llm_with_tools.invoke(...)`**（**ReAct**），迴圈內依 **`tool_calls`** **`append`** **`AIMessage`／`ToolMessage`**，直到最後一則無 **`tool_calls`** 之 **`AIMessage`**；再將**自本輪 `HumanMessage` 起**之片段整段 **`extend` 進 `history`** 並寫檔。**本檔藍本**採此路線。若課堂另做「僅 **`stream`**、無工具」之簡化版，送模仍為 **`[system_message, *history, human_message]`** 再 **`llm.stream`**，但**不**涵蓋 **JSONL** 之 **`tool`／`tool_calls`** 欄位演練。
- **寫檔時機**：本輪對話回合（含 **ReAct** 鏈若實作）**寫回 `history` 後**，呼叫寫檔邏輯；**整檔覆寫** **`"w"`** ＋ **`encoding="utf-8"`**。
- **檔案內容**：**第一行** **`metadata`**（**`_type`／`key`／`created_at`／`updated_at`／`metadata`／`last_consolidated`** 與範例檔對齊）；之後每行一則對話列，**至少**支援 **`role` 為 `user`／`assistant`／`tool`**，順序與 **`history`** 一致。
  - **`role: "tool"`** 列：須能還原 **`ToolMessage`**（至少 **`content`**、**`tool_call_id`**、**`timestamp`** 等），與 **WG-15** 載回閉環。
  - **`role: "assistant"` 列與 `tool_calls`（本教案採用之「完整版」）**：若該則 **`AIMessage` 帶有非空 `tool_calls`**（**ReAct** 中模型決定呼叫工具的那一則），JSONL **必須**在**同一列**多存一個鍵 **`tool_calls`**，其值為**可被 `json.dumps` 序列化**的陣列，且 **`WG-15` 載回時**能直接餵給建構式 **`AIMessage(content=..., tool_calls=...)`**，使還原後的物件與寫入前**語意一致**（含 **`id`／`name`／`args`** 等欄位，與你執行 **WG-13** 時 **`AIMessage.tool_calls`** 的結構對齊；不同 **LangChain** 版本若欄位名略異，以「能重建同一則 **`invoke`** 上下文」為驗收標準）。**純文字**、無工具呼叫的 **`AIMessage`**：**不**寫 **`tool_calls`** 鍵，或寫 **`"tool_calls": []`**／省略皆可，但**載回規則**須與 **WG-15** 一致。
  - **簡化版（僅純串流、無 ReAct）**：可僅有 **`user`／`assistant`**（無 **`tool_calls`**、無 **`tool`** 列）；一旦併 **WG-13** 並要持久化鏈條，即採上列**完整版**。
- **禁止**：把 **`SystemMessage`** 寫入檔案；從磁碟**載入**歷史到 **`history`**（留給 **WG-15**）。
- **不要求**：讀檔時 **`try`／`except json.JSONDecodeError`**（本題無讀檔）；合併／摘要歷史。

### 驗收條件
- [ ] 啟動後行為與 **WG-12**（無檔時）相同可對話（**不**因磁碟上已有舊檔而自動載入）。
- [ ] 至少完成一輪後，指定路徑出現 **JSONL**，**第一行**為 **`metadata`**，其後可見 **`user`／`assistant`** 列；若實作 **ReAct** 持久化，可再看到 **`tool`** 列，且**含 `tool_calls` 的 `assistant` 列**須帶 **`tool_calls`** 欄位（與上節**完整版**一致）。
- [ ] 能說明：**什麼時機**把 **`history`** 寫入檔案？為什麼在 **本輪助手也寫回 `history` 之後**，而不是 **`human_message` 一建好就寫**？
- [ ] **邊界**：若該路徑**已存在**一份舊 JSONL，新開程式後**第一輪**對話結束並存檔，你預期檔案內容與「若程式會讀舊檔」有什麼關鍵差別？（能說出「整檔覆寫、不先載入」即可。）

### 提示（選讀）
> 參考 wiki「**檔案與例外**」：**`open` 模式**（寫入用 **`"w"`**）、**`with open`**、**`encoding="utf-8"`**。
> **`json.dumps(..., ensure_ascii=False)`** 利於中文出現在檔案裡。
> **併 WG-13** 且採「完整版」時，**`assistant` 列**須寫入可序列化之 **`tool_calls`**；若 **`json.dumps` 對 `tool_calls` 報錯**，請在寫檔前轉成純 **`list[dict]`**（鍵與 **`AIMessage.tool_calls`** 一致），再與 **WG-15** 載回閉環。
> 本題先專心「**寫出去的長相**」與「**寫的時機**」，讀回與壞行略過在 **WG-15**。

### 藍本對應
主迴圈與 **`memory_react_agent.run_react_turn`** 同構（**`bind_tools`、多段 `invoke`、`ToolMessage`**）；與該檔差異僅在 **WG-14** **不**於啟動讀檔、**`history`** 恆自空開始。

**示範檔（`basic.py`）— 僅含寫入時請對齊以下結構**（完整合併版含讀檔見 **WG-15** 藍本與專案內實際 `basic.py`）

```python
"""課堂示範：WG-14 對話脈絡 JSONL 僅寫檔。

本藍本主線採 **WG-13** 風格：**`bind_tools` + 多段 `invoke` + `ToolMessage`**（非單輪 `stream`），
每輪結束後把 **`history`** 內 **Human／含 tool_calls 之 AIMessage／ToolMessage／最終 AIMessage** 整檔寫入 JSONL。
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def add_two(a: int, b: int) -> int:
    """兩個整數相加並回傳和。課堂示範用，請在需要相加時呼叫此工具。"""
    return a + b

TOOLS = [add_two]
_TOOL_BY_NAME = {t.name: t for t in TOOLS}

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

def save_session_jsonl(
    path: str,
    messages: list[BaseMessage],
    existing_meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """整檔覆寫：第一行 metadata（更新 updated_at），其餘每行一則 user／assistant／tool。"""
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
            # 完整 ReAct 鏈：有 tool_calls 時必須寫入同列，WG-15 才能還原 AIMessage(..., tool_calls=...)
            tc = getattr(m, "tool_calls", None)
            if tc:
                row["tool_calls"] = tc
        elif isinstance(m, ToolMessage):
            row = {
                "role": "tool",
                "content": m.content,
                "tool_call_id": m.tool_call_id,
                "timestamp": ts,
            }
        else:
            continue
        lines.append(json.dumps(row, ensure_ascii=False))

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")

    return meta

def build_system_prompt() -> str:
    system_text = "你是課堂程式助教。請使用繁體中文；先給一句重點結論，必要時再補一句說明。"
    nick = "法鬥超人"
    tool_rule = "凡涉及兩個整數相加，必須使用 add_two 工具完成，不要只在文字裡心算。"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}\n\n{tool_rule}"

def run_react_turn(
    llm_tools: ChatOpenAI,
    system_message: SystemMessage,
    history: list[BaseMessage],
    user_text: str,
) -> tuple[str, list[BaseMessage]]:
    """本輪自 HumanMessage 起至最終 AIMessage（可含 tool_calls／ToolMessage 鏈）。參考 memory_react_agent.run_react_turn。"""
    human_message = HumanMessage(content=user_text)
    messages: list[BaseMessage] = [system_message, *history, human_message]
    idx_turn_start = 1 + len(history)  # 本輪第一則為 human_message

    while True:
        response = llm_tools.invoke(messages)
        if response.tool_calls:
            messages.append(response)
            for tc in response.tool_calls:
                name = tc["name"]
                raw_args = dict(tc.get("args") or {})
                tool_obj = _TOOL_BY_NAME.get(name)
                if tool_obj is None:
                    result: str | int = f"未知工具: {name}"
                else:
                    try:
                        result = tool_obj.invoke(raw_args)
                    except Exception as e:
                        result = str(e)  # 課堂示範：錯誤字串化寫入 ToolMessage
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=tc["id"])
                )
        else:
            messages.append(response)
            break

    turn_messages = messages[idx_turn_start:]
    final_ai = next(
        (m for m in reversed(turn_messages) if isinstance(m, AIMessage)),
        None,
    )
    final_text = ((final_ai.content if final_ai else None) or "").strip()
    return final_text, turn_messages

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    session_path = os.getenv("SESSION_JSONL_PATH", "session.jsonl")

    system_message = SystemMessage(content=build_system_prompt())
    history: list[BaseMessage] = []
    session_meta: dict[str, Any] | None = None

    if api_key:
        print(
            "已讀到 API 金鑰設定（內容不顯示）；進入對話（ReAct + JSONL 寫檔；每次重開仍從空脈絡開始；輸入 quit / exit / q 結束）。"
        )
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    llm_tools = llm.bind_tools(TOOLS)

    while True:
        user_text = input("你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        reply_text, turn_messages = run_react_turn(
            llm_tools, system_message, history, user_text
        )
        print("助手：", reply_text)

        history.extend(turn_messages)
        session_meta = save_session_jsonl(session_path, history, session_meta)

if __name__ == "__main__":
    main()
```

---

## Challenge WG-15：冷啟動撿回昨日脈絡——從 JSONL 載回對話脈絡
### 情境
**WG-14** 已會把每輪完整 **`history`**（含 **WG-13** **ReAct** 鏈上的 **`AIMessage`（可含 **`tool_calls`**）／`ToolMessage`**，與一般 **`HumanMessage`／`AIMessage`**）寫成 JSONL，但每次開程式仍從空脈絡開始。本題在**不改寫檔格式與寫檔時機**的前提下，加上**啟動時讀檔**：若路徑上已有檔案，就把 **`metadata`** 與對話列還原成 **`langchain_core.messages`** 物件串列（**`user`／`assistant`（含 **`tool_calls` 還原**）／`tool`** 與 **WG-14**「完整版」對齊），讓**關閉程式再開**仍能延續同一場對話。

讀取時對齊 **wiki 6**：**`with open(..., encoding="utf-8")`** 逐行讀、**`json.loads`** 包在 **`try`／`except json.JSONDecodeError`** 內，壞行略過不中斷。通過後可銜接 **WG-16**：在 **WG-12** 的 **`system_message`** 與 **WG-14** 寫檔格式之上，用 **`pick_consolidation_boundary`** 做短期送模裁切（見該題）。

### 規格
- 延續 **WG-14** 之 JSONL 格式、**`SESSION_JSONL_PATH`**、每輪結束後**整檔覆寫**、**不**寫 **`SystemMessage`**；**`tool`** 列須能還原 **`ToolMessage`**（至少 **`content`**、**`tool_call_id`**，與 **WG-14** 一致）。
- **`assistant` 列與 `tool_calls`（與 WG-14「完整版」同一套）**：讀到 **`role: "assistant"`** 時，若該列含 **`tool_calls`** 鍵且為非空陣列，必須還原為 **`AIMessage(content=..., tool_calls=...)`**（參數值與檔案內 **`tool_calls`** 一致），以保留 **ReAct** 鏈上「模型發出工具呼叫」那一則的語意；若無 **`tool_calls`** 或為空陣列，則 **`AIMessage(content=...)`** 即可。
- **啟動**：若路徑**無檔**，**`history`** 為空、**`session_meta`** 為 **`None`**（與 **WG-14** 相同）。若**有檔**，以 **`"r"`** 模式逐行讀取：
  - 空行略過；**`json.loads`** 使用 **`try`／`except json.JSONDecodeError`**，壞行略過。
  - **`"_type": "metadata"`** 列：保留為 **`session_meta`**，供之後寫回時沿用 **`created_at`**、更新 **`updated_at`**。
  - **`role`** 為 **`"user"`**：轉成 **`HumanMessage`**；為 **`"assistant"`**：依上節還原 **`AIMessage`**（**含／不含 `tool_calls`**）；為 **`"tool"`**：轉成 **`ToolMessage(content=..., tool_call_id=...)`**（欄位與 **WG-14** 寫入一致）；未知 **`role`** 略過（或依教師約定記錄警告）。
- **`main()`** 開頭改為呼叫載入函式（或等價邏輯）取得 **`history`** 與 **`session_meta`**；並與 **WG-12** 相同在進入 **`while`** 前建立 **`system_message = SystemMessage(content=build_system_prompt())`**。其餘每輪與 **WG-14** 閉環：併 **WG-13** 時，以 **`bind_tools` + 多段 `invoke`** 產生本輪 **`turn_messages`**（自 **`HumanMessage`** 起，可含 **`AIMessage.tool_calls`／`ToolMessage`／最終 `AIMessage`**），**`history.extend(turn_messages)`** 後 **`save_session_jsonl`**；**本檔藍本**與 **WG-14** 藍本同採 **`run_react_turn`** 寫法（**非**單輪 **`stream`** 純文字）。
- **不要求**：變更 **WG-14** 訂好的 JSON 欄位名稱或檔案編碼。

### 驗收條件
- [ ] **關閉程式再開**（仍具金鑰）：先前對話中給過的關鍵資訊可被模型承接（自訂台詞即可），且與磁碟上 JSONL 內容一致。
- [ ] 能指出程式裡**哪一段**在啟動時讀檔，以及**哪一段**用 **`try`／`except json.JSONDecodeError`** 處理壞行。
- [ ] 能說明：**`session_meta`**（或你專案中等價變數）在「第一次寫檔」與「讀檔後再寫檔」時，**`created_at`** 與 **`updated_at`** 各自扮演什麼角色？
- [ ] **邊界**：若手動刪掉 JSONL **第一行 `metadata`** 只留下對話列，下次啟動載入後再完成一輪並存檔，你預期**第一行**會如何變化？（能描述「是否補上新的 metadata」即可。）
- [ ] （併 **WG-13** 時）**關閉再開**後，磁碟上 **`assistant` 列**若含 **`tool_calls`**，載入後 **`history`** 中對應 **`AIMessage`** 須仍帶 **`tool_calls`**（可 **`print`** 或除錯器檢查），且後續 **`ToolMessage`** 仍接在正確的 **`tool_call_id`** 之後。

### 提示（選讀）
> **`strip()`** 可避免空行或行尾空白干擾 **`json.loads`**。
> 若「讀回後模型像失憶」，先確認 **`run_react_turn`**（或等價 **ReAct**）內送 **`invoke`** 的串列含 **`[system_message, *history, HumanMessage(本輪)]`**，**`history`** 已含讀檔還原之舊訊息（含 **`tool_calls`／`tool`** 還原結果）。
> 壞行略過是為了**韌性**；課堂除錯時仍可手動打開 JSONL 檢查是否夾了非 JSON 行。
> 若 **`json.dumps` 寫檔時對 `tool_calls` 報錯**，代表該結構含不可序列化物件，須先轉成純 **`dict`／`list`／字串**再寫入（與 **WG-14**「完整版」一致）。

### 藍本對應
與 **WG-14** 藍本同一套 **`run_react_turn`**；另在 **`main()`** 開頭呼叫 **`load_session_jsonl`**，其餘寫檔時機與 **WG-14** 相同。

**示範檔全檔（`basic.py`）— 寫入＋載回合併版（對齊 WG-15）**

```python
"""課堂示範：WG-14～WG-15 對話脈絡 JSONL 寫入與載回。

啟動時 **`load_session_jsonl`** 還原含 **`tool_calls`** 之 **`AIMessage`** 與 **`ToolMessage`**；
每輪仍以 **ReAct + `invoke`** 延伸 **`history`**，再 **`save_session_jsonl`** 整檔覆寫。
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def add_two(a: int, b: int) -> int:
    """兩個整數相加並回傳和。課堂示範用，請在需要相加時呼叫此工具。"""
    return a + b

TOOLS = [add_two]
_TOOL_BY_NAME = {t.name: t for t in TOOLS}

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
    """從 JSONL 載入對話訊息串列（assistant 含 tool_calls 時還原完整 AIMessage）與 metadata；檔不存在則回傳空串列與 None。"""
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
                content = str(obj.get("content", ""))
                tc = obj.get("tool_calls")
                if tc:
                    messages.append(AIMessage(content=content, tool_calls=tc))
                else:
                    messages.append(AIMessage(content=content))
            elif role == "tool":
                tid = obj.get("tool_call_id") or ""
                messages.append(
                    ToolMessage(
                        content=str(obj.get("content", "")),
                        tool_call_id=str(tid),
                    )
                )

    return messages, meta

def save_session_jsonl(
    path: str,
    messages: list[BaseMessage],
    existing_meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """整檔覆寫：第一行 metadata（更新 updated_at），其餘每行一則 user／assistant／tool。"""
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
            tc = getattr(m, "tool_calls", None)
            if tc:
                row["tool_calls"] = tc
        elif isinstance(m, ToolMessage):
            row = {
                "role": "tool",
                "content": m.content,
                "tool_call_id": m.tool_call_id,
                "timestamp": ts,
            }
        else:
            continue
        lines.append(json.dumps(row, ensure_ascii=False))

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        if lines:
            f.write("\n")

    return meta

def build_system_prompt() -> str:
    system_text = "你是課堂程式助教。請使用繁體中文；先給一句重點結論，必要時再補一句說明。"
    nick = "法鬥超人"
    tool_rule = "凡涉及兩個整數相加，必須使用 add_two 工具完成，不要只在文字裡心算。"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}\n\n{tool_rule}"

def run_react_turn(
    llm_tools: ChatOpenAI,
    system_message: SystemMessage,
    history: list[BaseMessage],
    user_text: str,
) -> tuple[str, list[BaseMessage]]:
    human_message = HumanMessage(content=user_text)
    messages: list[BaseMessage] = [system_message, *history, human_message]
    idx_turn_start = 1 + len(history)

    while True:
        response = llm_tools.invoke(messages)
        if response.tool_calls:
            messages.append(response)
            for tc in response.tool_calls:
                name = tc["name"]
                raw_args = dict(tc.get("args") or {})
                tool_obj = _TOOL_BY_NAME.get(name)
                if tool_obj is None:
                    result: str | int = f"未知工具: {name}"
                else:
                    try:
                        result = tool_obj.invoke(raw_args)
                    except Exception as e:
                        result = str(e)  # 課堂示範：錯誤字串化寫入 ToolMessage
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=tc["id"])
                )
        else:
            messages.append(response)
            break

    turn_messages = messages[idx_turn_start:]
    final_ai = next(
        (m for m in reversed(turn_messages) if isinstance(m, AIMessage)),
        None,
    )
    final_text = ((final_ai.content if final_ai else None) or "").strip()
    return final_text, turn_messages

def main() -> None:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    session_path = os.getenv("SESSION_JSONL_PATH", "session.jsonl")

    loaded, session_meta = load_session_jsonl(session_path)
    history: list[BaseMessage] = list(loaded)
    system_message = SystemMessage(content=build_system_prompt())

    if api_key:
        print(
            "已讀到 API 金鑰設定（內容不顯示）；進入對話（ReAct + JSONL 寫入／載回可接續；輸入 quit / exit / q 結束）。"
        )
    else:
        print("尚未讀到 OPENAI_API_KEY；請檢查 .env 或系統環境變數。")
        return

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    llm_tools = llm.bind_tools(TOOLS)

    while True:
        user_text = input("你：").strip()
        if user_text.lower() in ("quit", "exit", "q"):
            print("再見！")
            break
        if not user_text:
            continue

        reply_text, turn_messages = run_react_turn(
            llm_tools, system_message, history, user_text
        )
        print("助手：", reply_text)

        history.extend(turn_messages)
        session_meta = save_session_jsonl(session_path, history, session_meta)

if __name__ == "__main__":
    main()
```

---

## Challenge WG-16：視窗太窄先裁舊帳——字元長度模擬 token 預算與整併邊界（`pick_consolidation_boundary`）
### 情境
**WG-12～15** 已讓模型讀到 **system** 加上自 **JSONL** 載回、並在記憶體中**完整累積**的對話（**WG-13** 起 **`history`** 可含 **`ToolMessage`** 與含 **`tool_calls`** 之 **`AIMessage`**，與磁碟 **JSONL** 一致）；但真實 **API** 有**上下文長度上限**，過長時必須**丟掉最舊**的一部分，只把「塞得進預算」的內容送進模型。本題用**字元數**刻意簡化模擬 **token 成本**（不呼叫 **tiktoken** 等），練習「**先判斷是否超線 → 再裁切 → 再送模（串流或 **ReAct** 多段 **`invoke`**）**」的節奏；概念上銜接 **`memory_react_agent.py`** 之 **`request_cost_chars`**／**`turns`** 預算思路。**成本**須把 **`past`** 內每一則 **`BaseMessage`**（含 **`ToolMessage`**）一併納入 **`estimate_message_tokens`**；**裁切邊界**仍以「**下一則使用者訊息**」開頭為準（**`pick_consolidation_boundary`** 對 **`HumanMessage`** 的判定），不因中間夾了 **`ToolMessage`** 而改變「從哪一則 **user** 往後保留」的語意。

> **與 WG-11～15 的用語對齊**：**WG-11** 以 **`messages`** 累積**已結束回合**（當時僅 **Human／AI**）；**WG-12** 起 **`history`** 與 **JSONL** 對齊，**WG-13** 起可含 **ReAct** 鏈；每輪無裁切時 **`context_messages = [system_message, *history, human_message]`**。**WG-16** 再把「過去段」換成裁切後的 **`past`**（**`past`** 內仍保留 **tool** 訊息之時間順序）。**`history` 的長度**與 **`context_messages` 裡「過去段」的長度**不必相同——這是本題要學生分辨的核心。

### 規格
- **延續 WG-15**：**`build_system_prompt`**、**`SystemMessage`**、**JSONL** 格式、**`load_session_jsonl`／`save_session_jsonl`**、每輪結束後整檔覆寫等**維持不變**（與 **WG-12～14** 之前題之語意銜接）。
- **資料分工**：
  - **`history`**：依時間順序完整保存**已發生**之 **`BaseMessage`**（**`HumanMessage`／`AIMessage`／`ToolMessage`** 等，與 **WG-14** **JSONL** 與 **WG-13** **ReAct** 一致；**`AIMessage`** 若含 **`tool_calls`** 仍屬同則物件）。啟動載入後 **`history`** 即為 **`load_session_jsonl` 回傳的串列**（**不**含 **system**）。
  - **`last_consolidated`**：**非負整數**，語意對齊長程式 **`Session.last_consolidated`**：從 **`history` 的該索引起**向後掃描，計算「若從某個**之後的使用者回合開頭**開始保留，已略過多少權重」。課堂可自 **`0`** 起；**選修**：每輪整併成功後把 **`last_consolidated`** 更新為本次回傳的 **`idx`**，減少重掃（須與實作一致）。
  - **本輪**使用者新輸入先建成 **`HumanMessage`**（記為 **`human_message`**），**在 append 進 `history` 之前**先參與成本計算與裁切。
  - **`past`**：由整併邊界決定。若 **`pick_consolidation_boundary`**（或等價實作）回傳 **`(idx, _)`**，則 **`past = history[idx:]`**；若回傳 **`None`**（含 **`tokens_to_remove <= 0`** 或 **`start >= len(history)`**），則 **`past = history[last_consolidated:]`**。
- **簡化成本**（本題自訂，**不**代表真實 **token**）：
  - 先定義 **`estimate_message_tokens(message: BaseMessage) -> int`**（本題即 **`len(message.content)`** 當 **`content` 為 `str`**；否則課堂自訂規則），**`cost` 與 `pick_consolidation_boundary` 必須共用**此定義。
  - **`cost = len(system_str) + sum(estimate_message_tokens(m) for m in msgs)`**。

  其中 **`system_str`** 與 **`build_system_prompt()`** 回傳字串一致；**`msgs`** 為 **`*past0`（或裁切後的 `past`）與本輪 `human_message`** 之**所有**訊息（**含** **`ToolMessage`**；本題 **`estimate_message_tokens`** 以 **`content` 字串長度**為主，**選修**：對 **`tool_calls`** 另加權）。
- **常數 `TOKEN_BUDGET`**：正整數（檔案頂部常數即可；**選修**改為 **`int(os.getenv("TOKEN_BUDGET", "8000"))`** 等，無效時需有預設）。
- **先判斷再裁切**：
  - 先令 **`past0 = history[last_consolidated:]`**，再算 **`cost`**（**`System` 字串** + **`past0`** + **本輪 `human_message`**），公式同前 **`len` 加總**。
  - 若 **`cost <= TOKEN_BUDGET`**：令 **`tokens_to_remove = 0`**（或不呼叫整併），**`past = past0`**，直接組 **`context_messages`**（見下「送模串列」）。
  - 若 **`cost > TOKEN_BUDGET`**：令 **`tokens_to_remove = max(0, cost - TOKEN_BUDGET // 2)`**（**整數**；目標是把「送模側」壓到約 **`TOKEN_BUDGET // 2`** 留給助手輸出概念）。再呼叫 **`pick_consolidation_boundary(history, last_consolidated, tokens_to_remove)`**（或等價自由函式）決定 **`past`**。
- **裁切流程**（**`pick_consolidation_boundary`**，僅在 **`cost > TOKEN_BUDGET`** 且 **`tokens_to_remove > 0`** 時必須執行；邏輯須與下列一致）：
  - **`start = last_consolidated`**。若 **`start >= len(history)`** 或 **`tokens_to_remove <= 0`**，回傳 **`None`**。
  - 自 **`start`** 以 **`for idx in range(start, len(history)):`** 走訪；維護 **`removed_tokens`** 與 **`last_boundary: tuple[int, int] | None`**。每一則迭代須與你貼的程式**同序**：先依 **`idx > start`** 且該則為**使用者**更新 **`last_boundary`** 並視情況 **`return`**，再執行 **`removed_tokens += estimate_message_tokens(message)`**（定義見上）。
  - **邊界判定**：當 **`idx > start`** 且 **`history[idx]`** 為**使用者訊息**（課堂即 **`isinstance(..., HumanMessage)`**，對齊 **`message.get("role") == "user"`**），令 **`last_boundary = (idx, removed_tokens)`**；若此時 **`removed_tokens >= tokens_to_remove`**，**立即** **`return last_boundary`**。
  - 迴圈結束若從未達標，**回傳最後一次**的 **`last_boundary`**（可為 **`None`**，表示無可用邊界）。
  - **`TOKEN_BUDGET`**：判斷「是否超線、要不要整併」；**`TOKEN_BUDGET // 2`**：換算成本輪要試著削掉的 **`tokens_to_remove`** 目標。**JSONL** 與 **`history`** 仍保存**完整**紀錄；僅送模用的 **`past`** 依 **`idx`** 切片。
- **本輪 `human_message` 必留**：送進 **`llm.stream(context_messages)`** 的 **`context_messages`** 串列**必須**含本則使用者訊息，**不可**因裁切被移除。
- **送模串列**：每輪組 **`context_messages = [system_message, *past, human_message]`**（**`past`** 依上一節），再呼叫 **`llm.stream(context_messages)`**（若本題併 **WG-13**，同一輪亦可改為 **ReAct** 多段 **`invoke`**，則 **`history`** 於該輪 **`append`** 之順序須符合工具協議）。回合結束後將本輪產生之訊息依序 **`append` 進 `history`**（純串流時為 **Human＋AI**；**ReAct** 時另含 **`ToolMessage`** 等），並呼叫 **`save_session_jsonl(session_path, history, ...)`**（**`system`** 不在 **`history`**，**不**寫進檔）。

### 驗收條件
- [ ] **預算夠**（**`cost <= TOKEN_BUDGET`**）：不進入整併、或 **`pick_consolidation_boundary`** 因 **`tokens_to_remove <= 0`** 回 **`None`** 時，**`past`** 須與 **`history[last_consolidated:]`** 一致，模型讀到的舊對話範圍與「未整併」相同。
- [ ] **預算不夠**：**`past`** 的起點索引必須落在 **`HumanMessage`**（與 **`idx > start` 且為 user** 之邊界語意一致），**不可**從 **`AIMessage`** 中間切開當作起點。
- [ ] **`removed_tokens`** 的累加順序與 **`estimate_message_tokens`** 定義，須與 **`pick_consolidation_boundary`** 行為一致；能接受「掃完仍 **`removed_tokens < tokens_to_remove`**」時回傳**最後一個** **`last_boundary`** 的設計。
- [ ] 本輪 **`HumanMessage`** 始終出現在 **`context_messages`**（**`llm.stream`** 的引數）中。
- [ ] 能說明：**`last_consolidated`**、回傳的 **`idx`**、與 **`past = history[idx:]`** 的對應；**`history` 全長**與「實際送入 **`context_messages`** 的過去段」差在哪裡（口頭、註解或白板擇一）。
- [ ] 能說明：為什麼邊界要選在「**下一則使用者訊息**」的開頭，而不是任意索引切開。

### 提示（選讀）
> 裁切發生在**組出送模串列之前**；**`history` 與 JSONL** 保存「課堂完整紀錄」，**`pick_consolidation_boundary`** 只決定「從哪一則 **Human** 開始往後算進 **`past`**」（**`past`** 內可含 **`ToolMessage`**，順序與 **`history`** 切片一致）。
> **`len(build_system_prompt())`** 與 **`SystemMessage(content=...)`** 用的字串應一致，否則 **`cost`** 與實際送進模型的 **system** 長度會脫鉤。
> 若裁切後模型行為變笨，可參考 **`TOKEN_BUDGET`**、**`tokens_to_remove`** 與邊界回傳是否過於激進。
> 下一階段可銜接 **WG-17**（送模前 **transcript** 修復／預算）再 **WG-18**（超預算時將舊脈絡整併入 **`MEMORY.md`／`HISTORY.md`** 並每輪讀回組窗）。

### 藍本對應
以下為**結構示意**（**非**完整可執行檔）；請在 **WG-12** 藍本上分離 **`history`** 與 **`last_consolidated`**，實作 **`estimate_message_tokens`** 與 **`pick_consolidation_boundary`**，並在 **`while`** 內每輪於 **`append` 進 `history` 之前**完成裁切與 **`stream`**。

```python
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage

TOKEN_BUDGET = 8000  # 或 int(os.getenv("TOKEN_BUDGET", "8000")), ...

def estimate_message_tokens(message: BaseMessage) -> int:
    c = message.content
    return len(c) if isinstance(c, str) else 0

def pick_consolidation_boundary(
    messages: list[BaseMessage],
    last_consolidated: int,
    tokens_to_remove: int,
) -> tuple[int, int] | None:
    """自 last_consolidated 掃描，挑「使用者回合開頭」idx，使略過的權重足夠。"""
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

# main 啟動：loaded, session_meta = load_session_jsonl(session_path)
history: list[BaseMessage] = list(loaded)
last_consolidated = 0
system_message = SystemMessage(content=build_system_prompt())
system_str = build_system_prompt()

# while True: 讀 user_text → human_message = HumanMessage(...)
def message_cost(msgs: list[BaseMessage]) -> int:
    return sum(estimate_message_tokens(m) for m in msgs)

past0 = history[last_consolidated:]
cost = len(system_str) + message_cost([*past0, human_message])
if cost <= TOKEN_BUDGET:
    past = past0
else:
    tokens_to_remove = max(0, cost - TOKEN_BUDGET // 2)
    boundary = pick_consolidation_boundary(history, last_consolidated, tokens_to_remove)
    past = history[boundary[0] :] if boundary is not None else past0

context_messages = [system_message, *past, human_message]
# for chunk in llm.stream(context_messages): ...
# history.append(human_message); history.append(AIMessage(...));
# save_session_jsonl(session_path, history, session_meta)
```

---

## Challenge WG-17：送模前先洗對話簿——transcript 修復與工具輸出預算
### 情境
**WG-16** 教你用 `pick_consolidation_boundary` 做「短期送模視窗」裁切；但真實 agent 還會遇到另一類問題：**對話串本身壞掉或太肥**，導致下一輪模型讀到不合法上下文、或直接被超長 `tool` 輸出塞爆。

`nanobot` 的做法很關鍵：維持一份「完整累積」的 `messages`（之後要寫 JSONL／存檔），但在每一輪呼叫模型前，另組一份 **`messages_for_model`**，允許做**修復／截斷／小型壓縮**，而且註解明確要求「**不要污染**之後要保存的新回合邊界」。

### 規格（本題用「純 dict transcript」教，避免綁死 LangChain 型別）
- 訊息格式使用 OpenAI chat 風格 `list[dict]`，至少支援：
  - `{"role": "system", "content": str}`
  - `{"role": "user" | "assistant", "content": str}`
  - `{"role": "assistant", "content": str, "tool_calls": [...]}`（每個 tool call 至少含 `id` 與 `function.name`）
  - `{"role": "tool", "tool_call_id": str, "name": str, "content": str}`
- 實作 `build_messages_for_model(messages, *, max_chars: int, max_tool_chars: int, keep_recent_tools: int) -> list[dict]`，輸入為「完整累積」的 transcript，輸出為「本輪要送進模型」的版本。
- **禁止**直接就地修改輸入 list 裡的 dict（避免不小心改到要持久化的那份）；需要改動時請複製（shallow copy dict 即可，本題不要求深拷貝整段 content）。

#### A. 孤兒 tool 清理
- 若出現 `role == "tool"`，但它的 `tool_call_id` 在更早的訊息中找不到對應的 assistant `tool_calls[].id`，則在 `messages_for_model` **移除**該 tool 訊息。

#### B. 缺 tool 回覆補洞
- 若 assistant 訊息含 `tool_calls`，但後面沒有對應的 `tool` 訊息（依 `tool_call_id` 對齊），則在 assistant 之後插入一則合成 tool 訊息：
  - `content` 可用固定字串：`"[Tool result unavailable — call was interrupted or lost]"`（本題允許自訂，但須全檔一致）。

#### C. tool 輸出單則上限
- 對 `role == "tool"` 且 `content` 為字串者：若 `len(content) > max_tool_chars`，截斷到 `max_tool_chars`，並在結尾加上提示（例如 `"\n\n[truncated]"`）。

#### D. 小型壓縮
- 針對 `name` 屬於集合 `{"read_file","exec","grep","glob","web_search","web_fetch","list_dir"}` 的 tool 訊息：
  - 若這類 tool 訊息總數 `> keep_recent_tools`，將「最舊的」幾則中、且 `len(content) >= 500` 的長輸出，替換成單行摘要：`"[{name} result omitted from context]"`。
  - **永遠保留**最後 `keep_recent_tools` 則此類 tool 訊息的原文（不做摘要）。

#### E. 全對話字元預算
- 用極簡成本：`cost(msg) = len(str(msg.get("content","")))`（`tool_calls` 可先不算進成本，本題不考精度）。
- 若總成本 `> max_chars`：從**最舊的非 system**訊息開始刪，直到 `<= max_chars` 或刪到只剩 `system + 最後一則 user` 為止。
- **硬規則**：`messages_for_model` 的第一則（若存在）必須是 `system`；且最後一則必須是 `user`（若做不到，允許插入一則極短 user：`"(conversation continued)"` 作為安全網，並在註解說明為何需要）。

### 驗收條件
- 給定含孤兒 tool 的輸入，`build_messages_for_model` 會移除孤兒，且不修改輸入 list 內容（可用 `id(old[i]) != id(out[i])` 或比對副本驗收）。
- 給定缺 tool 回覆的輸入，輸出會補上合成 tool 訊息，使每個 `tool_call_id` 都有對應 tool。
- 給定超長 tool content，輸出會被截斷到 `max_tool_chars`。
- 給定大量可壓縮 tool 輸出，最舊且夠長的會變成單行摘要，但最後 `keep_recent_tools` 則保留原文。
- 給定總成本超線輸入，輸出會刪除夠多的舊訊息使成本下降（不要求最優，但要可重現、可解釋刪到哪裡）。
- 能一句話說明：為什麼這題要分「完整累積」與「送模用副本」兩份 transcript？

### 提示（選讀）
> 參考 `nanobot/agent/runner.py`：`AgentRunner.run()` 在每一輪模型呼叫前組 `messages_for_model`，先做 orphan 清理、缺洞補齊、microcompact、tool budget、snip，再呼叫模型。
> 本題刻意不要求 async、不要求 token 估算、不要求並發工具；只把「為什麼要洗 transcript」講清楚即可。

### 藍本對應
以下為**可讀性優先**的示意骨架（不要求與專案逐字一致）：

```python
from __future__ import annotations

from typing import Any

COMPACTABLE = {"read_file", "exec", "grep", "glob", "web_search", "web_fetch", "list_dir"}

def build_messages_for_model(
    messages: list[dict[str, Any]],
    *,
    max_chars: int,
    max_tool_chars: int,
    keep_recent_tools: int,
) -> list[dict[str, Any]]:
    out = [dict(m) for m in messages]  # shallow copy rows; replace content strings as needed

    # A drop orphans, B backfill, C truncate tool, D microcompact, E snip ...
    # （請依上方規格完成；此處略）

    return out
```

---

## Challenge WG-18：舊對話濃縮成長期備忘——超預算觸發長期記憶整併與每輪讀回組裝
### 情境
**WG-16** 用 **`past`** 裁切，讓「送進主模型的字」不爆線，但舊對話仍完整留在 **`history`** 與 **JSONL**——模型**看不到**被裁掉的那段細節。實務上常把「已離開短期視窗的內容」**壓縮成可重用的長文**，下次開機或下一輪再從檔案**讀回**，塞進 **system**，讓主模型仍握有**高層次脈絡**。

本題規格與 **`long-term-memory-template`** 專案內 **`challenges.md`** 之 **Challenge A**（**必要**）**對齊**；以下為**與本專案（**`basic.py`／JSONL session**）銜接**的節錄。**細節、邊界與驗收句**若與該檔有出入，以 **`long-term-memory-template/challenges.md` Challenge A** 為準。

### 規格
#### 與 **WG-12～16** 的關係（**不**推翻既有行為）
- **延續**：**`load_session_jsonl`／`save_session_jsonl`**、**`SESSION_JSONL_PATH`**、**`history`** 仍保存**完整**對話（**`user`／`assistant`／`tool`** 與 **WG-14** 一致）與 **metadata**；**`last_consolidated`** 仍寫入 **JSONL** 第一行 **metadata**（與 **WG-16** 語意一致）。
- **新增儲層**（建議與 **`memory_react_agent.py`** 同層路徑概念）：專案根下 **`memory/`** 目錄內 **`MEMORY.md`**（**覆寫**式長期正文）、**`HISTORY.md`**（**追加**式、一行一筆摘要或失敗列）。

#### 整併與預算（與 Challenge A 同一套語意）
- **觸發與成本**：常數 **`TOKEN_BUDGET`** 名稱與語意同 **WG-16**（**字元長度**近似 token）。成本為：**system 字串**（含下節讀回之長期記憶區塊）**+** 短期 **`past`**（或與 **`history[last_consolidated:]`** 語意相同之未整併段）**+** 本輪 **`human_message`**；演算法須與 **`memory_react_agent.request_cost_chars`** **同一語意**——若改寫，請在 **`main.py`**（或作答檔）以**註解**說明對應欄位。
- **嚴格大於** **`TOKEN_BUDGET`** 時才啟動「整併流程」並**得**呼叫 **consolidation 專用** LLM（**`invoke`／`ainvoke`** 等實際呼叫，**不可**略過）；**未超線時不得**為整併而呼叫該 LLM。
- **整併後目標**：整併與 **`last_consolidated`**（游標）更新後、**呼叫主對話 `llm.stream` 之前**，以**同一套**成本公式重算，總成本**必須 ≤ `TOKEN_BUDGET // 2`**（與 template 之 **`target = budget // 2`** 語意一致）。仍高於此值**不得**送主模型，須**繼續**整併／切塊直至達成，或觸發題目已定義之**停止條件**（例如無可用 **user** 邊界——須在程式**註解**說明）。
- **分輪與邊界（整併切塊）**：以 **`last_consolidated`** 為起點，**每輪整併流程只處理一段 chunk**；切分邊界**僅能落在 user-turn 前**（**不可**拆散同一 **user** 回合後之 **assistant／`ToolMessage`** 鏈，亦**不可**把 **user** 與其後第一則 **assistant** 切半）。邊界選擇須能推進整併並朝「整併後目標」收斂；與 **WG-16** 之 **`pick_consolidation_boundary`** 可並用或等價改寫，須**自洽**。游標後若**無任何** **`HumanMessage`** 則該輪**不整併**，等下一 **user** turn。
- **整併單輪內步驟**（成功路徑摘要）：
  1. 讀取目前 **`MEMORY.md`**（不存在視為空）。
  2. 將「待整併之舊 chunk + 現有 **memory** 脈絡」送給 **consolidation 專用** LLM（可與主模型同型號或不同；須為實際 **`invoke`**）。
  3. 期望回傳**可解析的結構化結果**（擇一）：**首選**單一 **JSON** 物件字串，且**僅兩鍵**：**`history_entry`**（字串）、**`memory_update`**（字串，**完整取代** **`MEMORY.md`** 內文之 markdown）；**或** **tool call** 兩參數語意同上。解析失敗計入「重試」；若 **provider** 不支援強制 **tool**，需有 **fallback**（例如改要求純 **JSON**），仍須滿足「兩欄可從回應抽出」。
  4. 成功時：**`append_history`** 之**語意**與 **`memory_react_agent.append_history`** 一致——**`HISTORY.md`** 一行 **`[YYYY-MM-DD HH:MM] <內文>`**；**`history_entry`** 應為**單行**（內部換行改空白或截斷）。並**覆寫** **`MEMORY.md`** 為 **`memory_update`**。
  5. 更新 **`last_consolidated`** 並 **`save_session_jsonl`**（寫回 **metadata** 與完整 **`history`**）。
- **失敗策略**：同一 chunk 之 consolidation 最多重試 **`CONSOLIDATION_MAX_RETRIES`** 次（建議 **3**；**0** 表示不重試、直接 **fallback**，須**註解**）。若仍失敗：**`HISTORY.md`** 寫入**一行**，格式 **`[YYYY-MM-DD HH:MM] [CONSOLIDATION-FAILED] `** 後接**單行**（與 Challenge A 一致）；成功列**不得**使用該前綴。失敗後仍須更新 **`last_consolidated`** 使該 chunk 離開短期送入範圍；**`MEMORY.md`** 維持不變或僅註記擇一、**全專案一致**並**註解**。

#### 讀回與每輪送模組裝
- **每次**送主模型前，用於估算與實際 **`SystemMessage.content`** 的**系統字串**（**僅含 WG-12～WG-18** 時）至少包含：（1）**WG-12** 之課堂規則／顯示名等；（2）自 **`MEMORY.md`** 讀出、以固定標題 **`## Long-term Memory`** 包起來的區塊（標題字串固定）。**長期記憶須緊接在課堂規則段落之後**，且仍只出現在 **`SystemMessage.content`** 內（**不得**改放成 **user／assistant／tool** 對話列），與 **Challenge A** 語意一致。
- **併入 WG-20（Skills）時**：建議以 **`compose_system_string(loader)`**（或等價函式）一次組裝，**大段順序**為：**課堂基底**（等同 **WG-12**，可為 **`build_classroom_base_prompt()`**）→ **長期記憶**（若有內文；同 **`## Long-term Memory`** 與空檔不注入規則）→ **`# Active Skills`**（僅 **`always: true`** 之正文；多則之間可插 **`---`**；小標建議 **`### Skill: {name}`**）→ **`# Skills`**（僅非 **`always`** 之摘要＋**繁中**說明須以 **`read_file`** 讀清單中路徑之 **`SKILL.md`**，並一句帶過依賴安裝）。**課堂基底與長期記憶之間不得插入 Active／Skills**（維持 **WG-18** 與 **Challenge A** 之「規則先、記憶次之」）。各 **大段** 之間建議以 **`\n\n---\n\n`** 串接。若沒有任何非 **`always`** 技能，**不得**出現空 **`# Skills`** 標題。
- **`history`（或裁切後之 `past`）** 僅含 **`last_consolidated` 之後**、**尚未經整併移出視窗**之短期內容；**不得**把已整併走之舊段再當「新訊息」重送一遍。
- **`MEMORY.md` 為空或僅空白**：不得出現**孤立**之 **`## Long-term Memory`** 標題；與「完全不注入記憶區塊」擇一、**全專案一致**。
- **長度保護**：若 **`MEMORY.md` 純內文**（不含標題）超過 **`MEMORY_MAX_CHARS`**（建議 **6000**），先**由尾端截斷**至該長度再組進 **system**（截斷後再套區塊標題亦可）。**選修**：截斷前對 **memory** 本體再做二次摘要 **LLM**——須**註解**觸發條件；課堂**允許只做截斷**即通過長度保護項。

### 驗收條件
（與 **Challenge A** 之「整併與預算」「讀回與組裝」兩段**逐條對齊勾選**；以下為**轉寫**以利本檔自洽。）

**整併與預算**

- [ ] 觸發／不觸發與 **consolidation** 呼叫行為符合上節；送主模型前成本 **≤ `TOKEN_BUDGET // 2`**。
- [ ] 成功路徑：短期送入範圍不再含已整併內容，且 **`MEMORY.md`／`HISTORY.md`** 符合上節；失敗路徑：**`HISTORY.md`** 有 **`[CONSOLIDATION-FAILED]`** 列且短期已不含該 chunk。
- [ ] **可觀察**：整併當輪有一次 **consolidation** 用 **LLM** 呼叫（非僅調游標）；成功列與失敗列前綴區分正確。
- [ ] 能說明：為何整併邊界取在 **user-turn**，而非任意索引切訊息。

**讀回與組裝**

- [ ] 每輪讀取約定路徑之 **`memory/MEMORY.md`**；**`history`／`past`** 僅自 **`last_consolidated`** 之後，不重複送入已整併內容。
- [ ] **可觀察**：**`MEMORY.md`** 非空時，**`SystemMessage.content`** 含完整子字串 **`## Long-term Memory`**。
- [ ] 能說明：長期記憶放 **system** 與放一般對話訊息之差異。

### 提示（選讀）
> 整併後成本與裁切迴圈可參考 **`memory_react_agent.py`** 之 **`adjust_last_consolidated_if_over_budget`** 與 **`request_cost_chars`**。
> **Consolidation** 若無法強制 **tool choice**，預留 **fallback**（例如改要求純 **JSON**）。
> 先固定「**system 字串 = 規則 + 可選的 Long-term Memory 區塊**」模板，再迭代 **JSONL** 與 **`memory/`** 兩條寫入路徑，較易除錯。

### 藍本對應
**專案根目錄 `basic.py`** 已合併 **WG-12～WG-18**（**WG-13** 工具 **ReAct** 可參考 **`memory_react_agent.py`**）：含 **`memory/MEMORY.md`／`memory/HISTORY.md`**、**`system_content_for_model()`**（**`## Long-term Memory`**）、**`request_cost_chars`**、超 **`TOKEN_BUDGET`** 時 **`consolidation_llm.invoke`** 整併與 **`CONSOLIDATION_MAX_RETRIES`**／**`[CONSOLIDATION-FAILED]`** 失敗列，以及送主模型前壓至 **≤ `TOKEN_BUDGET // 2`** 之迴圈。學生作答仍可以 **`main.py`** 擴寫或參考 **`basic.py`** 分段摘抄；可並行參考 **`memory_react_agent.py`** 之 **`request_cost_chars`** 與 **`run_react_turn`** 語意。

```text
專案根/
  memory/
    MEMORY.md      # 覆寫：整併後的長期正文（markdown）
    HISTORY.md     # 追加：每行 [時間] 摘要 或 [CONSOLIDATION-FAILED] ...
  session.jsonl    # 仍：metadata + user/assistant/tool；metadata 內 last_consolidated
```

---

## Challenge WG-19：讓 Agent 有手有腳——`exec` 與檔案工具的最小工具箱
### 情境
承接 **WG-12～WG-18** 的 session／長期記憶流程；本題補上在 workspace 內真正讀寫檔與執行 shell 的 **tool** 最小工具箱：`read_file`、`write_file`、`edit_file`、`list_dir` 與 `exec`。

核心觀念只有一句：**檔案操作走檔案工具，shell 指令才走 `exec`**。也就是說，讀檔不用 `cat`、寫檔不用 `echo >`、改檔不用 `sed -i`；`exec` 留給 `python --version`、`uv run pytest`、執行示範檔這類外部指令。

本題不必接 LLM function calling；先用 `ToolRegistry` 註冊工具，再用固定流程手動驗收即可。

### 規格
- 建立 `tools_demo.py`（或教師指定檔），實作簡化版 `Tool` 與 `ToolRegistry`。
- `Tool` 至少要有 `name`、`description`、`execute`，並可用 `read_only` 標記唯讀工具。
- `ToolRegistry` 至少支援 `register()`、`get()`、`list_tools()`，並註冊五個工具：`read_file`、`write_file`、`edit_file`、`list_dir`、`exec`。
- 設定 `WORKSPACE = Path.cwd().resolve()`；檔案工具收到相對路徑時，都只能解析到 workspace 底下。像 `../outside.txt` 這種路徑要拒絕。
- `read_file(path)`：讀 UTF-8 文字檔，回傳含行號的內容；找不到檔案或目標不是檔案時回傳錯誤。此工具是唯讀。
- `write_file(path, content)`：寫入 UTF-8，必要時建立父資料夾；若檔案已存在就是整檔覆寫。
- `edit_file(path, old_text, new_text, replace_all=False)`：用 `old_text` 做局部替換；找不到就報錯；出現多次時，預設要求更多上下文，不直接全改。
- `list_dir(path)`：列出資料夾內容；目標不是資料夾時回傳錯誤。此工具是唯讀。
- `exec(command)`：用 `subprocess.run` 執行安全命令，回傳 exit code 與輸出摘要；至少阻擋 `rm -rf`、`del /f`、`rmdir /s`、`format`、`shutdown` 等危險片段。
- **`exec` 與子程序輸出編碼（跨平台必讀）**：在 **`capture_output=True` 且 `text=True`** 時，若未指定 **`encoding`**，**Python 會用系統預設編碼**去解 stdout／stderr。在 **繁中 Windows** 上常為 **cp950**；子程序若輸出 **UTF-8**（許多 CLI、日誌、**`uv`**／**`python`** 的訊息），背景讀取執行緒可能拋出 **`UnicodeDecodeError`**（終端機出現 **`Thread-* (_readerthread)`** 之類 traceback，主流程甚至仍回傳空輸出）。實作時應在 **`subprocess.run`** 明確加上 **`encoding="utf-8"`** 與 **`errors="replace"`**（或改讀 **bytes** 再以 **`errors="replace"`** 解碼），並對 **`stdout`／`stderr` 可能為 `None`** 做串接防護。教練／coding agent 檢閱 **`exec`** 時應主動核對這一段，避免只在 macOS／Linux 上測過就以為沒問題。

### 驗收條件
- `ToolRegistry.list_tools()` 可看到 `read_file`、`write_file`、`edit_file`、`list_dir`、`exec` 五個名稱。
- 手動流程能跑通：`write_file` 建立 `sandbox/hello.txt` → `list_dir` 看見它 → `read_file` 讀回含行號內容 → `edit_file` 改其中一段 → 再 `read_file` 確認 → `exec("python --version")` 回傳 exit code 與版本輸出。
- 能說明：為什麼 `write_file` 是整檔覆寫，而 `edit_file` 是局部替換；兩者各自適合什麼情境？
- 能說明：為什麼 `read_file`／`list_dir` 可標成 `read_only=True`，但 `write_file`／`edit_file`／`exec` 不應標成唯讀。
- 能說明：為什麼不建議用 `exec("cat 檔案")`、`exec("echo ... > 檔案")` 或 `exec("sed -i ...")` 取代專用檔案工具。
- **邊界**：嘗試讀取或寫入 `../outside.txt` 時，工具應拒絕或回傳清楚錯誤，不應真的改到 workspace 外。
- **邊界**：`edit_file` 的 `old_text` 若在檔案中出現兩次，預設不得兩處都改；需要求更多上下文或明確 `replace_all=True`。
- **邊界**：`exec` 收到危險命令片段時應拒絕執行，並說明是安全限制。
- **邊界（Windows）**：在會觸發大量子程序輸出的指令下，**`exec`** 不得因預設 **`cp950`** 解碼失敗而在背景執行緒崩潰；應採上節規格之 **UTF-8 + replace**（或等價作法）。

### 提示（選讀）
> 參考 `nanobot.agent.loop.AgentLoop._register_default_tools`：預設會註冊檔案工具，`exec` 則依設定是否啟用。
> 參考 `nanobot.agent.tools.filesystem`：`read_file`／`list_dir` 唯讀，`write_file` 覆寫，`edit_file` 局部替換。
> 參考 `nanobot.agent.tools.shell.ExecTool`：`exec` 很有用，但要限制工作目錄、逾時、危險命令與輸出長度。
> **教練提醒**：學生在 **Windows** 上若看到 **`UnicodeDecodeError`** 出現在 **`_readerthread`**，優先檢查 **`subprocess.run`** 是否未設 **`encoding`／`errors`**；與本節 **`exec` 與子程序輸出編碼** 規格對齊後再驗收。

### 藍本對應
以下為**可執行骨架**，重點是工具分工與安全邊界，不要求與本專案原始碼逐字一致。

```python
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

@dataclass
class Tool:
    name: str
    description: str
    execute: Callable[..., str]
    read_only: bool = False

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        return sorted(self._tools)

WORKSPACE = Path.cwd().resolve()

def resolve_workspace_path(path: str) -> Path:
    target = (WORKSPACE / path).resolve()
    try:
        target.relative_to(WORKSPACE)
    except ValueError:
        raise PermissionError(f"path is outside workspace: {path}")
    return target

def read_file(path: str, offset: int = 1, limit: int = 200) -> str:
    try:
        target = resolve_workspace_path(path)
        if not target.is_file():
            return f"Error: not a file: {path}"
        lines = target.read_text(encoding="utf-8").splitlines()
        start = max(offset - 1, 0)
        end = min(start + limit, len(lines))
        return "\n".join(f"{i + 1}| {line}" for i, line in enumerate(lines[start:end], start))
    except Exception as e:
        return f"Error: {e}"

def write_file(path: str, content: str) -> str:
    try:
        target = resolve_workspace_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"wrote {len(content)} characters to {path}"
    except Exception as e:
        return f"Error: {e}"

def edit_file(path: str, old_text: str, new_text: str, replace_all: bool = False) -> str:
    try:
        target = resolve_workspace_path(path)
        text = target.read_text(encoding="utf-8")
        count = text.count(old_text)
        if count == 0:
            return "Error: old_text not found"
        if count > 1 and not replace_all:
            return "Error: old_text appears multiple times"
        target.write_text(text.replace(old_text, new_text, -1 if replace_all else 1), encoding="utf-8")
        return f"edited {path}"
    except Exception as e:
        return f"Error: {e}"

def list_dir(path: str, recursive: bool = False, max_entries: int = 200) -> str:
    try:
        root = resolve_workspace_path(path)
        if not root.is_dir():
            return f"Error: not a directory: {path}"
        iterator = root.rglob("*") if recursive else root.iterdir()
        entries = [str(item.relative_to(WORKSPACE)) for item in iterator][:max_entries]
        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}"

def exec_command(command: str, timeout: int = 30) -> str:
    blocked = ("rm -rf", "del /f", "rmdir /s", "format", "shutdown")
    lowered = command.lower()
    if any(part in lowered for part in blocked):
        return "Error: blocked dangerous command"

    result = subprocess.run(
        command,
        cwd=WORKSPACE,
        shell=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    return f"exit_code={result.returncode}\n{output[:4000]}"

def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(Tool("read_file", "Read a UTF-8 text file with line numbers.", read_file, read_only=True))
    registry.register(Tool("write_file", "Write UTF-8 text, overwriting existing content.", write_file))
    registry.register(Tool("edit_file", "Replace old_text with new_text in an existing file.", edit_file))
    registry.register(Tool("list_dir", "List files under a directory.", list_dir, read_only=True))
    registry.register(Tool("exec", "Execute a safe shell command inside the workspace.", exec_command))
    return registry

if __name__ == "__main__":
    tools = build_registry()
    print("tools:", ", ".join(tools.list_tools()))
    print(tools.get("write_file").execute("sandbox/hello.txt", "第一行\n第二行\n"))
    print(tools.get("list_dir").execute("sandbox"))
    print(tools.get("read_file").execute("sandbox/hello.txt"))
    print(tools.get("edit_file").execute("sandbox/hello.txt", "第二行", "第二行（已修改）"))
    print(tools.get("read_file").execute("sandbox/hello.txt"))
    print(tools.get("exec").execute("python --version"))
```

---

## Challenge WG-20：技能卡進工具箱——最小 SkillsLoader 與 system prompt 注入
### 情境
前面 **WG-12～WG-19** 已建立 session、JSONL、`past` 裁切、長期記憶整併與 workspace 檔案／shell 工具；本題補上如何把「程序知識」以 **skill** 形式寫成 `SKILL.md`，並在啟動時穩定注入 **system prompt**（摘要＋必要時全文）。

本專案 `nanobot` 的做法很適合拆給學生：**skill 不是 Python tool，也不是模型直接可呼叫的函式**；它是一份 markdown 程序知識。runtime 先掃描 `skills/<name>/SKILL.md`，讀 frontmatter 的 `description` 做摘要；若該 skill 標成 `always`，才把正文去掉 frontmatter 後完整注入 system prompt。其他 skill 只出現在摘要清單中，提醒模型：「需要時請讀這個 `SKILL.md`。」

本題只做「最小可理解架構」：掃目錄、讀檔、取 frontmatter、合併 workspace／builtin、組出 system prompt。**不要求**真的讓 LLM 自動選 skill，也不要求實作 MCP、tool registry、sandbox 權限或背景 Dream agent。

### 規格
#### 檔案結構
- 在專案根建立兩個 skill 根目錄（可依教師指定簡化為只做一個）：
  - `**skills/`**：使用者或學生自訂 skill。
  - `**builtin_skills/**`：教師提供的內建 skill 範例。
- 每個 skill 是一個資料夾，底下必須有 `**SKILL.md**`：

```text
專案根/
  main.py
  skills/
    class-helper/
      SKILL.md
  builtin_skills/
    summarize/
      SKILL.md
```

- `**SKILL.md**` 最小格式須含 YAML-like frontmatter 與正文：

```markdown
---
name: class-helper
description: 協助學生把問題拆成步驟，適合卡關時使用。
always: false
---

# Class Helper
先問學生目前做到哪一步，再給一個最小提示，不直接給完整答案。
```

#### `SkillEntry` 與讀取函式
- 建議定義一個小資料結構（`dataclass` 或 dict 皆可）保存：
  - `name`
  - `path`
  - `source`（`"workspace"` 或 `"builtin"`）
  - `description`
  - `always`
  - `body`
- 實作 `**split_frontmatter(text: str) -> tuple[dict[str, str], str]**` 或等價函式：
  - 若檔案開頭是 `---`，讀到下一個單獨一行 `---` 為止。
  - 至少能解析 `name: ...`、`description: ...`、`always: true/false` 三種簡單鍵值。
  - 回傳 metadata 與去掉 frontmatter 後的 markdown body。
  - 不要求支援巢狀 YAML、陣列、多行字串；本題以課堂簡化格式為準。
- skill 的識別名稱以**資料夾名稱**為準（對齊本專案 loader）；frontmatter 內的 `name` 可要求與資料夾同名，或只當作顯示資訊。若 `description` 不存在，使用資料夾名稱作為 fallback。

#### `SkillsLoader`
- 實作一個 `**SkillsLoader`** 類別或同等函式群：
  - 初始化接收 `workspace: Path` 與 `builtin_skills_dir: Path`。
  - `workspace_skills = workspace / "skills"`。
  - `list_skills()` 掃描兩個根目錄底下的第一層資料夾，只收有 `**SKILL.md**` 的項目。
  - 先列 workspace skills，再列 builtin skills。
  - 若 workspace 與 builtin 有同名 skill，**workspace 版本優先**，builtin 同名版本不列入。
  - 略過一般檔案、沒有 `SKILL.md` 的資料夾、空目錄。
- 實作 `**load_skill(name: str)`**：
  - 先找 `skills/<name>/SKILL.md`，再找 `builtin_skills/<name>/SKILL.md`。
  - 找不到則回傳 `None` 或拋出清楚錯誤（擇一，但驗收時須能說明）。

#### system prompt 組裝
- 實作 `**build_skills_summary(entries)**`：
  - 對每個非 `always` skill 產生一行摘要，格式可自訂，但須含 **skill 名稱、description、SKILL.md 路徑**。
  - 範例（一行）：**`class-helper`**、description、以及反引號內 **`skills/class-helper/SKILL.md`** 路徑皆須可從該行讀出。
- 實作 **`compose_system_string(loader: SkillsLoader) -> str`**（或等價名稱），將 **WG-12** 課堂基底、**WG-18** 長期記憶（若有）、與本題 **Skills** 併成**單一**送模用字串（亦供 **WG-16** 成本估算與 **`SystemMessage.content`** 使用）。**建議大段順序**（與合併示範 **`main.py`** 一致）：
  1. **課堂基底**：等同 **WG-12** 之 **`system_text`＋顯示名**；函式名可為 **`build_classroom_base_prompt()`**。
  2. **長期記憶**：同 **WG-18** **`memory_block_for_system()`** 語意（有內文才 append）。
  3. **Active Skills**：`always: true` 的 skill，放入 **去掉 frontmatter 後的正文**；區塊標題 **`# Active Skills`**。
  4. **Skills**：`build_skills_summary` 產生之清單；區塊標題 **`# Skills`**；其前附**繁體中文**短引導（須明示以 **`read_file`** 讀取清單中路徑之 **`SKILL.md`**，並一句帶過「若需套件／環境請先依該檔或專案說明安裝」）。
- **大段之間**建議以 **`\n\n---\n\n`** 串接（可讀性）；**不得**在「課堂基底」與「**`## Long-term Memory`**」之間插入 **Active／Skills**（與 **WG-18** 讀回小節一致）。
- 若沒有任何非 **`always`** skill，**不得**出現空的 **`# Skills`** 標題；若完全沒有 skill，亦**不**出現空 **Active** 標題。

#### Tool schema 驗證與參數 cast（銜接 **WG-19**）

延續 **WG-19** 的 **`Tool`／`ToolRegistry`**：模型經 **function calling** 回傳的參數常是**字串或寬鬆 JSON**，進 **`execute`** 前須先**依 schema 做安全 cast**，再**驗證型別與必填欄位**，避免把髒資料餵進檔案工具或 **`exec`**。

- **JSON Schema 形狀**：每個 **`Tool`** 帶一份 **`parameters: dict`**，至少支援 **`{"type": "object", "properties": {...}, "required": [...]}`**。
  - **`properties`** 內各欄的 **`type`** 至少支援 **`string`／`integer`／`number`／`boolean`**。
  - **選修**：**`array`**（僅一層元素）、**`object`**（巢狀一層）。
- **`cast_params(params: dict) -> dict`**：在驗證**之前**呼叫；參考本專案 **`Tool.cast_params`**——例如 **`"42"`** 在 **`type: "integer"`** 時轉成 **`int`**；**`"true"`／`"false"`**（大小寫不敏感）在 **`boolean`** 轉成 **`bool`**；已符合目標型別則保留；無法轉換時可保留原值交給驗證階段報錯（**全專案一致**即可）。
- **`validate_params(params: dict) -> list[str]`**：回傳**錯誤訊息串列**（**空**表示通過）；須檢查 **`required`** 缺欄、各欄 **`type`** 與 **`properties`** 鍵是否多出未定義欄位（擇一策略，**註解**說明）。**課堂可自寫檢查器**，不必實作完整 **JSON Schema** 草案。
- **`ToolRegistry.prepare_call(name, params) -> tuple[Tool | None, dict, str | None]`** 或等價流程：工具名不存在、或 **params** 不是 **dict**（**JSON object**）時回傳 **`error` 字串**；否則 **`cast_params` → `validate_params`**，若有錯誤則組成單一 **`error`**（例如分號串接多條訊息），**不**呼叫 **`execute`**。

#### 與本專案 `nanobot` 的參考重點
- 參考 `**nanobot.agent.skills.SkillsLoader`**：
  - `skills/<name>/SKILL.md` 是被發現的最小單位。
  - workspace skill 會覆蓋同名 builtin skill。
  - `build_skills_summary` 只把摘要放進 prompt，避免一次塞入所有 skill 正文。
- 參考 `**nanobot.agent.context.ContextBuilder**`：
  - `always` skill 的正文可直接進 system prompt。
  - 一般 skill 只進摘要，等模型需要時再讀全文。
- 本題不實作 `requires.bins`／`requires.env`、`disabled_skills`、`metadata.nanobot`、sandbox `extra_allowed_dirs`；這些可列為選修或下一題。
- 參考 **`nanobot.agent.tools.base.Tool`** 之 **`cast_params`／`validate_params`**，以及 **`nanobot.agent.tools.registry.ToolRegistry.prepare_call`**：先 cast、再驗證、最後才 **`execute`**；本題規格與該順序一致即可，不要求 **async** 或與執行緒並發細節逐字相同。

### 驗收條件
- 建立至少兩個 skill：一個在 `skills/`、一個在 `builtin_skills/`，且皆有 `SKILL.md`。
- `list_skills()` 只列出有 `SKILL.md` 的資料夾，並略過一般檔案與缺少 `SKILL.md` 的資料夾。
- 當 `skills/demo/SKILL.md` 與 `builtin_skills/demo/SKILL.md` 同名時，清單與載入結果使用 workspace 版本。
- `split_frontmatter` 能取出 `description`，且組出的摘要列含 skill 名稱、description、路徑。
- `always: true` 的 skill 正文會出現在 **Active Skills** 區塊，且不再重複出現在一般摘要清單。
- 一般 skill 不把全文塞進 system prompt，只出現在摘要清單。
- 能說明：為什麼 skill 不等於 tool？若模型需要使用某個一般 skill，為什麼應該先讀 `SKILL.md`？
- **邊界**：若 `SKILL.md` 沒有 frontmatter，程式仍不崩潰，且至少能用資料夾名稱作為 skill 名稱。
- **`prepare_call`**：對 **`read_file`**（或自訂一個 **`integer`** 參數的示範工具）傳入**字串形式的數字**，**`cast_params`** 後 **`validate_params`** 為空；缺 **`required`** 欄位時 **`validate_params`** 非空且 **`prepare_call`** 不進 **`execute`**。
- 能一句話說明：為什麼要先 **`cast_params`** 再 **`validate_params`**（而不是只驗證原始字串）？

### 提示（選讀）
> 本專案完整版本使用 `yaml.safe_load` 解析 frontmatter；本題為了讓學生專心在架構，可先用「逐行切 `key: value`」的簡化解析器。若課堂已加入 `pyyaml`，也可以改用 `yaml.safe_load`，但仍須保留「缺 frontmatter 不崩潰」的行為。

> `Path.iterdir()` 只掃第一層即可；本題不需要遞迴搜尋巢狀資料夾。

> 「漸進載入」的目的，是不要一開始把所有 skill 正文塞進 prompt。摘要讓模型知道有哪些技能；真正要用時，再讀指定 `SKILL.md`。

> **Tool schema**：參考 **`nanobot/agent/tools/base.py`**（**`_cast_value`**、**`validate_params`**）與 **`nanobot/agent/tools/registry.py`**（**`prepare_call`**）；**`Schema.validate_json_schema_value`** 在 **`nanobot/agent/tools/schema.py`**，本題可只取子集行為。

### 藍本對應
以下為**結構示意**（可直接放入 `main.py` 或 `skills_demo.py` 擴寫）；重點是函式邊界與資料流，不要求與本專案原始碼逐字一致。

```python
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SkillEntry:
    name: str
    path: Path
    source: str
    description: str
    always: bool
    body: str

def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text

    lines = text.splitlines()
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text

    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip()

    body = "\n".join(lines[end + 1 :]).strip()
    return meta, body

class SkillsLoader:
    def __init__(self, workspace: Path, builtin_skills_dir: Path) -> None:
        self.workspace_skills = workspace / "skills"
        self.builtin_skills = builtin_skills_dir

    def _entries_from_dir(self, root: Path, source: str, skip: set[str]) -> list[SkillEntry]:
        if not root.exists():
            return []

        entries: list[SkillEntry] = []
        for skill_dir in root.iterdir():
            skill_file = skill_dir / "SKILL.md"
            if not skill_dir.is_dir() or not skill_file.exists():
                continue
            if skill_dir.name in skip:
                continue

            text = skill_file.read_text(encoding="utf-8")
            meta, body = split_frontmatter(text)
            name = skill_dir.name
            description = meta.get("description") or name
            always = meta.get("always", "false").lower() == "true"
            entries.append(SkillEntry(name, skill_file, source, description, always, body))
        return entries

    def list_skills(self) -> list[SkillEntry]:
        workspace_entries = self._entries_from_dir(self.workspace_skills, "workspace", set())
        workspace_names = {entry.name for entry in workspace_entries}
        builtin_entries = self._entries_from_dir(self.builtin_skills, "builtin", workspace_names)
        return workspace_entries + builtin_entries

    def load_skill(self, name: str) -> str | None:
        for root in (self.workspace_skills, self.builtin_skills):
            path = root / name / "SKILL.md"
            if path.exists():
                return path.read_text(encoding="utf-8")
        return None

def build_skills_summary(entries: list[SkillEntry]) -> str:
    summarized = [e for e in entries if not e.always]
    if not summarized:
        return ""
    lines = [f"- **{e.name}** — {e.description} `{e.path}`" for e in summarized]
    return "\n".join(lines)


def build_classroom_base_prompt() -> str:
    """WG-12 基底：課堂規則＋顯示名（合併示範可不塞 WG-13 工具細則於此）。"""
    system_text = (
        "你是課堂程式助教。請使用繁體中文；先給一句重點結論，必要時再補一句說明。"
    )
    nick = os.getenv("ASSISTANT_DISPLAY_NAME") or "法鬥超人"
    if isinstance(nick, str) and not nick.strip():
        nick = "法鬥超人"
    return f"{system_text}\n\n【本場次顯示名稱】{nick}"


def memory_block_for_system() -> str:
    """WG-18：有 MEMORY.md 內文才回傳 ## Long-term Memory 區塊；此藍本略讀檔，實作請接真檔案。"""
    return ""


def compose_system_string(loader: SkillsLoader) -> str:
    """課堂基底 → 長期記憶（若有）→ Active Skills → Skills 摘要（若有）。"""
    parts: list[str] = [build_classroom_base_prompt()]
    mem = memory_block_for_system()
    if mem:
        parts.append(mem)

    entries = loader.list_skills()
    active = [e for e in entries if e.always]
    if active:
        body = "\n\n---\n\n".join(f"### Skill: {e.name}\n\n{e.body}" for e in active)
        parts.append(f"# Active Skills\n\n{body}")

    summary = build_skills_summary(entries)
    if summary:
        intro = (
            "下列技能可擴充你的能力。若要使用某技能，請用 read_file 讀取清單中該技能路徑下的 SKILL.md。\n"
            "若該技能需額外套件或環境，請先依 SKILL.md 或專案說明安裝相依項目後再操作。\n\n"
        )
        parts.append("# Skills\n\n" + intro + summary)
    return "\n\n---\n\n".join(parts)
```

---

## 附錄：七份 wiki 內可參考的「學習順序」標題（編輯速查）
以下僅供**編輯教案**時參考用，不必整段給學生；學生端仍以本檔各 Challenge 的情境與驗收為主。

- **1 基礎資料與變數**：資料有型態 → 型態轉換 → 變數與賦值 → 命名與註解 → 作用範圍。
- **2 運算與輸入輸出**：運算式與運算子 → 型態下的運算效果 → `print()` → `input()` 與轉型 → 字串格式化。
- **3 條件與迴圈**：布林邏輯 → `if` → `if-else`／`elif` → `while` → `for`／`range()` → 條件與迴圈組合。
- **4 資料結構**：串列基礎 → 批次操作 → 迴圈讀串列 → 切片與串接 → 元組 → 字典與 `get()`／`in`。
- **5 函式與模組**：為何要有函式 → `def`／參數／`return` → 預設參數 → 作用範圍 → 內建與字串函式 → `import` 三型 → `random`／`time`。
- **6 檔案與例外**：`open()` 模式 → `with open` → 指標與寫入 → `os`／`os.path` → `try`／`except` → 檔案＋例外整合。
- **7 類別與測試**：類別作模組化 → 基本結構 → 類別與物件 → 屬性與方法 → `unittest` 最小結構 → `if __name__ == '__main__'`。
