<!-- Slide number: 1 -->
PYTHON × LLM × 記憶

從 Python 基礎到會記憶的 AI Agent

終端機

AI
Python 程式開始輸出、互動、存記憶。
用 17 個挑戰，把一支小程式慢慢長成像助手一樣的系統。

聊天、工具、JSONL、Long-term Memory 一步一步加上去。
輸出
互動
工具
記憶
存檔

目標不是背語法，而是看懂一個 Agent 的能力，怎麼一層一層被加上去。

### Notes:

<!-- Slide number: 2 -->
學習地圖
今天會走過哪 7 段升級路線？
先看全圖，再進每一題，學生比較容易知道自己現在走到哪裡。

1
2
3
4
先讓程式說第一句話
替 Agent 備好套件和設定
把流程收進 main()
開始和大模型聊天

5
6
7
讓它記得上一輪
把對話存進檔案
對話太長時學會整理記憶

### Notes:

<!-- Slide number: 3 -->
WG-01

按下啟動鍵

`if __name__ == "__main__"` 只在直接執行時啟動。
先讓 Python 在正確的時機說第一句話。
`print()` 可以把文字送到終端機。
`if __name__ == "__main__"` 代表只有直接執行這個檔案時才跑。
這樣做的好處是：被別的檔案 `import` 時，不會自己亂執行。

變數像幫資料貼標籤，之後可以重複使用。

f-string 是把變數直接縫進句子裡。

### Notes:

<!-- Slide number: 4 -->
WG-02～WG-03

字串先有名字，再組成一句話

`if __name__ == "__main__"` 只在直接執行時啟動。
從單純印字，到用變數和 f-string 組句。
變數像幫資料貼標籤，之後可以重複拿來用。
f-string 可以把變數直接塞進句子裡。
如果先後順序寫錯，後面的句子就找不到前面的變數。

變數像幫資料貼標籤，之後可以重複使用。

f-string 是把變數直接縫進句子裡。

### Notes:

<!-- Slide number: 5 -->
WG-04

把工具裝進專案
先把未來要用的套件安裝好，再在檔案頂端匯入。

`uv add` 是把套件加進這個專案。
`import` / `from ... import ...` 是在程式裡把名稱拿進來。
這一題先備料，還不急著真的打 API。
專案根目錄
`uv add` 安裝套件
程式頂端 import
→
→

### Notes:

<!-- Slide number: 6 -->
WG-05

讀設定，但不把金鑰秀出來

.env：把敏感資訊放在檔案裡，但不要交進版控。
會讀 `.env` 很重要，會保護敏感資訊更重要。
`load_dotenv()` 先把 `.env` 的資料載進環境。
`os.getenv()` 再把指定變數讀出來。
螢幕上只能顯示有 / 無，不要把整串金鑰印出來。

load_dotenv()：先載入環境。

os.getenv()：只顯示有 / 無，不顯示完整 key。

### Notes:

<!-- Slide number: 7 -->
WG-06～WG-07

有鑰匙才往下走
用分支決定流程，再把主流程收進 `main()`。

`if / else` 讓程式能根據條件走不同路。
沒有 API key 時，應該提早停下來，而不是硬往下跑。
`main()` 讓入口和主要流程分開，結構更清楚。
有：往下跑
沒有：return
讀設定
有 key？
→
→

### Notes:

<!-- Slide number: 8 -->
WG-08

第一通打進大模型
第一次從本機程式把一句話送到模型，再拿回回覆。

模型回應
`ChatOpenAI(...)` 是建立模型連線物件。
`invoke(...)` 代表送出一次請求。
回來的不是普通字串，所以通常要用 `.content` 拿文字。
本機 Python
→
→
→
ChatOpenAI
print(content)

### Notes:

<!-- Slide number: 9 -->
WG-09

把一次問答變成聊天迴圈
不再只問一次，而是可以持續對話到你說停。

`while True` 可以讓聊天一直重複。
`input()` 讓使用者每輪都能打新問題。
`quit / exit / q` 這類指令可以安全結束聊天。
你輸入
送給模型
印出回答
下一輪
→
→
→

### Notes:

<!-- Slide number: 10 -->
對照
`invoke` 和 `stream`，體感差在哪？
同樣都能拿到答案，但使用者感覺很不一樣。

`invoke`
`stream`
等整段答案完成後一次拿到
程式寫法通常比較直觀
畫面上像突然整段跳出
答案會一小塊一小塊回來
更像真實聊天或打字機效果
常搭配 `print(..., end="", flush=True)`

### Notes:

<!-- Slide number: 11 -->
小結
前 10 題，我們做到了什麼？
從只會印一句話，到能真的和模型來回聊天。

起點
備料
互動
`print()` 輸出文字
理解 `__main__` 的作用
用變數和 f-string 組句
用 `uv add` 安裝套件
從 `.env` 安全讀設定
用 `main()` 把流程收乾淨
第一次 `invoke`
用 `while` 做聊天迴圈
改成 `stream` 做即時輸出

### Notes:

<!-- Slide number: 12 -->
WG-11

把上一輪也帶進下一輪
HumanMessage：這輪使用者說了什麼
聊天之所以像聊天，是因為模型看得到前情提要。

`messages` 是放在 RAM 裡的對話時間軸。
裡面不只放使用者，也要放助手，不然脈絡會斷掉。
這時候記憶還沒寫進檔案，所以關程式就會消失。
AIMessage：助手回了什麼

再下一輪：模型要看得到上一輪

所以歷史裡不能只放 user，也要放 ai

### Notes:

<!-- Slide number: 13 -->
WG-11 圖解

為什麼要先組 `context_messages`，再 append？

messages：已經完成的舊回合

human_message：這一輪新輸入
送模串列和真正累積的歷史，不是同一件事。
送進模型的是本輪要看的完整上下文。
真正累積在 `messages` 裡的是已經完成的回合。
先組、再 append，才不會把未完成的回合提早寫進歷史。

context_messages：送進模型的完整上下文
先組送模串列，串流成功後再 append 進歷史。

### Notes:

<!-- Slide number: 14 -->
WG-12

把人設放進 system
有些規則不是這一輪才說，而是每一輪都要一起帶進去。

SystemMessage：固定規則、人設、語氣
`SystemMessage` 是固定規則、人設、語氣的地方。
`history` 放的是對話回合，不要把 system 混在裡面。
送模時常見的組法是 `[system, *history, human]`。

history：已完成的人機對話回合

human_message：本輪使用者新輸入

### Notes:

<!-- Slide number: 15 -->
WG-13

模型不只會想，還會用工具
需要計算或查資料時，模型可以自己決定要不要呼叫工具。

決定呼叫工具
產生最後回答
模型先思考

`@tool` 是把 Python 函式包成可被模型呼叫的工具。
`bind_tools()` 讓模型知道有哪些工具可以用。
`tool_calls` 和 `ToolMessage` 讓『叫工具 -> 拿結果 -> 繼續回答』串起來。
收到 ToolMessage
→
→
→

### Notes:

<!-- Slide number: 16 -->
WG-14

metadata：created_at / updated_at / last_consolidated
先學會把對話寫進檔案

user：使用者這一輪說的話
聊天如果只在 RAM 裡，關掉就沒了；寫進檔案才留得住。

assistant：助手回的話
JSONL 可以想成一行一筆資料的文字檔。
第一行常放 metadata，後面每行放一則對話。
這一題先練寫出去，不急著一開機就讀回來。

tool：工具執行結果（需要時才有）

assistant：最後整理完的回答

### Notes:

<!-- Slide number: 17 -->
WG-15

重開程式，昨天的對話還在

接著上次繼續聊
把 JSONL 再讀回來，讓程式不是每次都從零開始。
程式重新啟動

`json.loads()` 可以把每一行 JSON 讀回 Python 資料。
壞掉的行可以略過，不要讓整份檔案直接報廢。
這樣一來，關掉程式再打開，也能接著聊。
逐行讀 JSONL
還原 history
→
→
→

### Notes:

<!-- Slide number: 18 -->
對照
RAM 記憶和檔案記憶，到底差在哪？
兩種都重要，只是功能不一樣。

RAM 記憶
檔案記憶
速度快
適合本輪到下一輪的連續對話
程式一關就忘了
可以跨次執行保留
適合 session 紀錄與載回
讀寫較慢，但更耐久

### Notes:

<!-- Slide number: 19 -->
WG-16

送進模型的視窗
完整的 history 很長，但真正送進模型的只有 past + 本輪 human。
上下文不是無限大
對話越來越長時，不能什麼都塞進模型。

`history` 是完整歷史，但送進模型的可能只是其中一段 `past`。
`TOKEN_BUDGET` 是簡化版的容量上限。
當容量不夠，就得從最舊的部分開始裁掉。
超過預算時，要從最舊的 user-turn 邊界開始往後裁。

完整 history
再送進模型
→
→
裁成 past

### Notes:

<!-- Slide number: 20 -->
WG-16 圖解

裁切不是亂砍，而是有邊界的整理

舊 user turn
更舊 tool turn
舊 ai turn
最新 human_message
只從舊資料開始裁，本輪最新輸入一定要保留。
`human_message` 一定要保留。
邊界通常選在 user-turn 開頭，避免把一段對話切碎。
所以 `history` 的長度，和送進模型的長度，不一定一樣。
只從舊資料開始裁，本輪最新輸入一定要保留。

### Notes:

<!-- Slide number: 21 -->
WG-17

把舊對話濃縮成長期記憶
短期視窗裝不下，就把舊內容整理成更短、但還有用的摘要。

舊對話
`MEMORY.md` 放濃縮後的長期重點。
`HISTORY.md` 記錄每次整併發生了什麼。
這樣模型就算沒看到完整舊對話，還是能抓到大方向。
consolidation 摘要
寫進 MEMORY
併回 system
→
→
→

### Notes:

<!-- Slide number: 22 -->
WG-17 圖解

Long-term Memory 怎麼回到模型腦中？

課堂規則 / 人設
它不是一般聊天訊息，而是 system 背景知識的一部分。

## Long-term Memory
長期記憶不是當一般 user / assistant 訊息塞回去。
它會被放進 system 區塊，變成模型每輪都會看到的背景知識。
這樣做比把全部舊訊息硬塞回去更省空間。

本輪使用者輸入
長期記憶是背景知識，不是一般 user / assistant 對話列。

### Notes:

<!-- Slide number: 23 -->
總整理
一個小 Agent 是怎麼長大的？
這 17 題不是 17 個零碎技巧，而是一條完整成長路線。

→
→
→
先會輸出
再會互動
接著會記住
最後學會整理記憶
真正的重點：你不是在學一堆零件，而是在學怎麼把它們接成一個系統。

### Notes:

<!-- Slide number: 24 -->
PYTHON 能力
這 17 題，其實練到哪些 Python 能力？

基礎資料與變數：幫資料命名、組句子
條件判斷：有 key / 沒 key 時走不同流程
迴圈：把單次問答變成持續聊天

函式與模組：用 `main()`、`import` 收斂結構
資料結構：`messages`、`history`、`past` 的差別
檔案與例外：寫 JSONL、讀回資料、略過壞行

### Notes:

<!-- Slide number: 25 -->
課程建議
如果拿來上課，可以怎麼切三段？
先讓學生跑得動，再讓系統聊得起來，最後讓它記得住。

基礎段
互動段
記憶段
WG-01～WG-07
WG-08～WG-13
WG-14～WG-17
輸出
變數
f-string
套件與設定
`main()` 結構
第一次 `invoke`
聊天迴圈
串流
RAM 脈絡
System / Tool / ReAct
JSONL 寫入
JSONL 載回
預算裁切
長期記憶整併

### Notes:

<!-- Slide number: 26 -->
下一步

記憶
下一步，讓你的 Agent 更像真的助手

會說
OK

先把對話做對，再把記憶做好，最後才是讓它變得更聰明、更穩定。
會聊

會記、會整理

會說
會聊
會記
會整理

### Notes:
