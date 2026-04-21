const fs = require("fs");
const path = require("path");
const PptxGenJS = require("pptxgenjs");
const html2pptx = require("C:/Users/mz038/.agents/skills/document-skills/pptx/scripts/html2pptx.js");

const rootDir = __dirname;
const slidesDir = path.join(rootDir, "slides");
const outputFile = path.join(rootDir, "WG-01-17-teaching-deck.pptx");

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function writeSlideHtml(filename, body) {
  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    html { background: #F7FBFF; }
    body {
      width: 720pt;
      height: 405pt;
      margin: 0;
      padding: 0;
      display: flex;
      background: #F7FBFF;
      color: #17324D;
      font-family: Arial, Helvetica, sans-serif;
    }
    * { box-sizing: border-box; }
    .slide {
      width: 720pt;
      height: 405pt;
      padding: 26pt 30pt;
      display: flex;
      flex-direction: column;
      gap: 12pt;
    }
    .eyebrow {
      margin: 0;
      color: #1D7F8E;
      font-size: 10.5pt;
      font-weight: bold;
      letter-spacing: 1.1pt;
      text-transform: uppercase;
    }
    h1 {
      margin: 0;
      font-size: 26pt;
      line-height: 1.2;
      color: #153B6B;
    }
    h2 {
      margin: 0;
      font-size: 22pt;
      line-height: 1.25;
      color: #153B6B;
    }
    h3 {
      margin: 0;
      font-size: 15pt;
      line-height: 1.25;
      color: #153B6B;
    }
    .subtitle {
      margin: 0;
      color: #3E5E7A;
      font-size: 12.5pt;
      line-height: 1.5;
    }
    .muted {
      margin: 0;
      color: #52708A;
      font-size: 11pt;
      line-height: 1.4;
    }
    .two-col {
      display: flex;
      gap: 18pt;
      flex: 1;
      align-items: stretch;
      min-height: 0;
    }
    .left {
      width: 47%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 0;
    }
    .right {
      width: 53%;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 0;
    }
    ul {
      margin: 0;
      padding-left: 18pt;
      color: #17324D;
      font-size: 13pt;
      line-height: 1.45;
    }
    li { margin: 0 0 8pt 0; }
    .cover {
      display: flex;
      gap: 22pt;
      flex: 1;
      align-items: center;
    }
    .cover-copy {
      width: 45%;
      display: flex;
      flex-direction: column;
      gap: 12pt;
    }
    .cover-copy h1 { font-size: 30pt; }
    .cover-visual {
      width: 55%;
      height: 300pt;
      background: #EAF5FF;
      border-radius: 24pt;
      padding: 10pt;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .cards-7 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 10pt;
      margin-top: 6pt;
    }
    .cards-7 .card:nth-child(n+5) {
      grid-column: span 1;
    }
    .card {
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 18pt;
      padding: 12pt;
      min-height: 86pt;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .card p {
      margin: 0;
      font-size: 11pt;
      line-height: 1.35;
    }
    .num {
      width: 24pt;
      height: 24pt;
      border-radius: 12pt;
      background: #1FC8A5;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .num p {
      margin: 0;
      color: #FFFFFF;
      font-size: 11pt;
      font-weight: bold;
    }
    .panel {
      width: 100%;
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 18pt;
      padding: 14pt;
    }
    .flow {
      display: flex;
      gap: 10pt;
      align-items: center;
      justify-content: center;
      flex-wrap: nowrap;
      width: 100%;
    }
    .box {
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 16pt;
      padding: 10pt 12pt;
      width: 120pt;
      min-height: 70pt;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .box.teal { background: #EAF8F5; border-color: #8EE0D0; }
    .box.blue { background: #EAF2FF; border-color: #A8CCF5; }
    .box.navy { background: #163B6A; border-color: #163B6A; }
    .box p {
      margin: 0;
      text-align: center;
      font-size: 11pt;
      line-height: 1.35;
      color: #17324D;
    }
    .box.navy p { color: #FFFFFF; }
    .arrow {
      width: 24pt;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .arrow p {
      margin: 0;
      font-size: 18pt;
      color: #1FC8A5;
      font-weight: bold;
    }
    .compare {
      display: flex;
      gap: 14pt;
      flex: 1;
    }
    .compare-col {
      width: 50%;
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 18pt;
      padding: 14pt;
      display: flex;
      flex-direction: column;
      gap: 10pt;
    }
    .compare-col ul { font-size: 12pt; }
    .pill-row {
      display: flex;
      gap: 8pt;
      flex-wrap: wrap;
    }
    .pill {
      background: #EAF5FF;
      border-radius: 999pt;
      padding: 8pt 12pt;
      border: 1.5pt solid #C9DFF7;
    }
    .pill p {
      margin: 0;
      font-size: 11pt;
      color: #153B6B;
      font-weight: bold;
    }
    .three {
      display: flex;
      gap: 12pt;
      flex: 1;
    }
    .three .col {
      width: 33.33%;
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 18pt;
      padding: 14pt;
      display: flex;
      flex-direction: column;
      gap: 8pt;
    }
    .three .col ul { font-size: 11.5pt; padding-left: 16pt; }
    .stack {
      display: flex;
      flex-direction: column;
      gap: 10pt;
      width: 100%;
    }
    .stack .layer {
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 16pt;
      padding: 10pt 12pt;
    }
    .stack .layer.system { background: #EAF8F5; border-color: #8EE0D0; }
    .stack .layer.history { background: #EAF2FF; border-color: #A8CCF5; }
    .stack .layer.human { background: #FFF4E0; border-color: #FFD27A; }
    .stack .layer p {
      margin: 0;
      font-size: 11pt;
      line-height: 1.35;
      text-align: center;
    }
    .timeline {
      display: flex;
      flex-direction: column;
      gap: 10pt;
      width: 100%;
    }
    .bubble {
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 16pt;
      padding: 10pt 12pt;
      width: 86%;
    }
    .bubble.user { align-self: flex-start; }
    .bubble.ai { align-self: flex-end; background: #EAF8F5; border-color: #8EE0D0; }
    .bubble p {
      margin: 0;
      font-size: 11pt;
      line-height: 1.35;
    }
    .file {
      width: 100%;
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 18pt;
      padding: 14pt;
    }
    .line {
      background: #EAF5FF;
      border-radius: 8pt;
      padding: 8pt 10pt;
      margin-bottom: 8pt;
    }
    .line.meta { background: #EAF8F5; }
    .line.tool { background: #FFF4E0; }
    .line p {
      margin: 0;
      font-size: 10.5pt;
      line-height: 1.3;
    }
    .meter {
      width: 100%;
      background: #DCEAF8;
      border-radius: 999pt;
      height: 22pt;
      overflow: hidden;
    }
    .meter-fill {
      height: 22pt;
      width: 72%;
      background: #1FC8A5;
    }
    .meter-fill.warn { width: 94%; background: #FFB84D; }
    .ability-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12pt;
      flex: 1;
    }
    .ability {
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 18pt;
      padding: 14pt;
    }
    .ability p { margin: 0; font-size: 12pt; line-height: 1.4; }
    .footer-note {
      margin-top: auto;
      font-size: 10.5pt;
      color: #5D7891;
    }
    .visual-stack {
      width: 100%;
      display: flex;
      flex-direction: column;
      gap: 10pt;
    }
    .visual-card {
      background: #FFFFFF;
      border: 2pt solid #D5E7F7;
      border-radius: 18pt;
      padding: 12pt;
    }
    .visual-card.teal { background: #EAF8F5; border-color: #8EE0D0; }
    .visual-card.blue { background: #EAF2FF; border-color: #A8CCF5; }
    .visual-card.navy { background: #173C6C; border-color: #173C6C; }
    .visual-card p { margin: 0; font-size: 11pt; line-height: 1.35; }
    .visual-card.navy p { color: #FFFFFF; }
    .hero-shell {
      width: 100%;
      height: 100%;
      display: flex;
      gap: 12pt;
      align-items: center;
    }
    .hero-shell .screen {
      width: 58%;
      height: 210pt;
      background: #173C6C;
      border-radius: 20pt;
      padding: 16pt;
      display: flex;
      flex-direction: column;
      gap: 10pt;
    }
    .hero-shell .screen p { margin: 0; color: #FFFFFF; }
    .hero-shell .screen .visual-card p { color: #17324D; }
    .hero-shell .screen .visual-card.navy p { color: #FFFFFF; }
    .hero-shell .screen .bar {
      height: 12pt;
      border-radius: 6pt;
      background: #1FC8A5;
      width: 62%;
    }
    .hero-shell .screen .bar.small {
      width: 42%;
      background: #9EC9F6;
    }
    .hero-shell .avatar {
      width: 42%;
      height: 210pt;
      background: #FFFFFF;
      border-radius: 20pt;
      border: 2pt solid #D5E7F7;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12pt;
    }
    .hero-shell .face {
      width: 84pt;
      height: 84pt;
      border-radius: 42pt;
      background: #1FC8A5;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .hero-shell .face p { margin: 0; color: #FFFFFF; font-size: 28pt; font-weight: bold; }
    .hero-shell .avatar .bar {
      height: 12pt;
      border-radius: 6pt;
      background: #173C6C;
      width: 70%;
    }
    .hero-shell .avatar .bar.small {
      width: 50%;
      background: #8DBEF3;
    }
  </style>
</head>
<body>${body}</body>
</html>`;
  fs.writeFileSync(path.join(slidesDir, filename), html, "utf8");
}

function bullets(items) {
  return `<ul>${items.map((item) => `<li>${item}</li>`).join("")}</ul>`;
}

function sideImageSlide({ eyebrow, title, subtitle, bulletsList, visualHtml }) {
  return `
  <div class="slide">
    <p class="eyebrow">${eyebrow}</p>
    <div class="two-col">
      <div class="left">
        <h2>${title}</h2>
        <p class="subtitle">${subtitle}</p>
        ${bullets(bulletsList)}
      </div>
      <div class="right">
        ${visualHtml}
      </div>
    </div>
  </div>`;
}

function diagramTextSlide({ eyebrow, title, subtitle, bulletsList, diagram }) {
  return `
  <div class="slide">
    <p class="eyebrow">${eyebrow}</p>
    <div class="two-col">
      <div class="left">
        <h2>${title}</h2>
        <p class="subtitle">${subtitle}</p>
        ${bullets(bulletsList)}
      </div>
      <div class="right">${diagram}</div>
    </div>
  </div>`;
}

function coverSlide() {
  return `
  <div class="slide">
    <p class="eyebrow">Python × LLM × 記憶</p>
    <div class="cover">
      <div class="cover-copy">
        <h1>從 Python 基礎到會記憶的 AI Agent</h1>
        <p class="subtitle">用 17 個挑戰，把一支小程式慢慢長成像助手一樣的系統。</p>
        <div class="pill-row">
          <div class="pill"><p>輸出</p></div>
          <div class="pill"><p>互動</p></div>
          <div class="pill"><p>工具</p></div>
          <div class="pill"><p>記憶</p></div>
          <div class="pill"><p>存檔</p></div>
        </div>
        <p class="muted">目標不是背語法，而是看懂一個 Agent 的能力，怎麼一層一層被加上去。</p>
      </div>
      <div class="cover-visual">
        ${heroCoverVisual()}
      </div>
    </div>
  </div>`;
}

function roadmapSlide() {
  const items = [
    "先讓程式說第一句話",
    "替 Agent 備好套件和設定",
    "把流程收進 main()",
    "開始和大模型聊天",
    "讓它記得上一輪",
    "把對話存進檔案",
    "對話太長時學會整理記憶",
  ];
  return `
  <div class="slide">
    <p class="eyebrow">學習地圖</p>
    <h1>今天會走過哪 7 段升級路線？</h1>
    <p class="subtitle">先看全圖，再進每一題，學生比較容易知道自己現在走到哪裡。</p>
    <div class="cards-7">
      ${items
        .map(
          (item, idx) => `
        <div class="card">
          <div class="num"><p>${idx + 1}</p></div>
          <p>${item}</p>
        </div>`
        )
        .join("")}
    </div>
  </div>`;
}

function summaryMilestoneSlide() {
  return `
  <div class="slide">
    <p class="eyebrow">小結</p>
    <h1>前 10 題，我們做到了什麼？</h1>
    <p class="subtitle">從只會印一句話，到能真的和模型來回聊天。</p>
    <div class="three">
      <div class="col">
        <h3>起點</h3>
        ${bullets(["`print()` 輸出文字", "理解 `__main__` 的作用", "用變數和 f-string 組句"])}
      </div>
      <div class="col">
        <h3>備料</h3>
        ${bullets(["用 `uv add` 安裝套件", "從 `.env` 安全讀設定", "用 `main()` 把流程收乾淨"])}
      </div>
      <div class="col">
        <h3>互動</h3>
        ${bullets(["第一次 `invoke`", "用 `while` 做聊天迴圈", "改成 `stream` 做即時輸出"])}
      </div>
    </div>
  </div>`;
}

function compareRamVsFileSlide() {
  return `
  <div class="slide">
    <p class="eyebrow">對照</p>
    <h1>RAM 記憶和檔案記憶，到底差在哪？</h1>
    <p class="subtitle">兩種都重要，只是功能不一樣。</p>
    <div class="compare">
      <div class="compare-col">
        <h3>RAM 記憶</h3>
        ${bullets(["速度快", "適合本輪到下一輪的連續對話", "程式一關就忘了"])}
      </div>
      <div class="compare-col">
        <h3>檔案記憶</h3>
        ${bullets(["可以跨次執行保留", "適合 session 紀錄與載回", "讀寫較慢，但更耐久"])}
      </div>
    </div>
  </div>`;
}

function finalGrowthSlide() {
  return `
  <div class="slide">
    <p class="eyebrow">總整理</p>
    <h1>一個小 Agent 是怎麼長大的？</h1>
    <p class="subtitle">這 17 題不是 17 個零碎技巧，而是一條完整成長路線。</p>
    <div class="flow" style="margin-top: 20pt;">
      <div class="box teal"><p>先會輸出</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box blue"><p>再會互動</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box teal"><p>接著會記住</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box navy"><p>最後學會整理記憶</p></div>
    </div>
    <p class="footer-note">真正的重點：你不是在學一堆零件，而是在學怎麼把它們接成一個系統。</p>
  </div>`;
}

function abilityMapSlide() {
  const items = [
    "基礎資料與變數：幫資料命名、組句子",
    "條件判斷：有 key / 沒 key 時走不同流程",
    "迴圈：把單次問答變成持續聊天",
    "函式與模組：用 `main()`、`import` 收斂結構",
    "資料結構：`messages`、`history`、`past` 的差別",
    "檔案與例外：寫 JSONL、讀回資料、略過壞行",
  ];
  return `
  <div class="slide">
    <p class="eyebrow">Python 能力</p>
    <h1>這 17 題，其實練到哪些 Python 能力？</h1>
    <div class="ability-grid">
      ${items
        .map(
          (item) => `<div class="ability"><p>${item}</p></div>`
        )
        .join("")}
    </div>
  </div>`;
}

function lessonPlanSlide() {
  return `
  <div class="slide">
    <p class="eyebrow">課程建議</p>
    <h1>如果拿來上課，可以怎麼切三段？</h1>
    <p class="subtitle">先讓學生跑得動，再讓系統聊得起來，最後讓它記得住。</p>
    <div class="three">
      <div class="col">
        <h3>基礎段</h3>
        <p class="muted">WG-01～WG-07</p>
        ${bullets(["輸出", "變數", "f-string", "套件與設定", "`main()` 結構"])}
      </div>
      <div class="col">
        <h3>互動段</h3>
        <p class="muted">WG-08～WG-13</p>
        ${bullets(["第一次 `invoke`", "聊天迴圈", "串流", "RAM 脈絡", "System / Tool / ReAct"])}
      </div>
      <div class="col">
        <h3>記憶段</h3>
        <p class="muted">WG-14～WG-17</p>
        ${bullets(["JSONL 寫入", "JSONL 載回", "預算裁切", "長期記憶整併"])}
      </div>
    </div>
  </div>`;
}

function closingSlide() {
  return `
  <div class="slide">
    <p class="eyebrow">下一步</p>
    <div class="cover">
      <div class="cover-copy">
        <h1>下一步，讓你的 Agent 更像真的助手</h1>
        <p class="subtitle">先把對話做對，再把記憶做好，最後才是讓它變得更聰明、更穩定。</p>
        <div class="pill-row">
          <div class="pill"><p>會說</p></div>
          <div class="pill"><p>會聊</p></div>
          <div class="pill"><p>會記</p></div>
          <div class="pill"><p>會整理</p></div>
        </div>
      </div>
      <div class="cover-visual">
        ${closingVisual()}
      </div>
    </div>
  </div>`;
}

function heroCoverVisual() {
  return `
    <div class="hero-shell">
      <div class="screen">
        <p class="eyebrow" style="color:#9ED8FF;">終端機</p>
        <div class="bar"></div>
        <div class="bar small"></div>
        <div class="visual-card teal"><p>Python 程式開始輸出、互動、存記憶。</p></div>
        <div class="visual-card blue"><p>聊天、工具、JSONL、Long-term Memory 一步一步加上去。</p></div>
      </div>
      <div class="avatar">
        <div class="face"><p>AI</p></div>
        <div class="bar"></div>
        <div class="bar small"></div>
      </div>
    </div>`;
}

function closingVisual() {
  return `
    <div class="hero-shell">
      <div class="screen">
        <p class="eyebrow" style="color:#9ED8FF;">記憶</p>
        <div class="visual-card blue"><p>會說</p></div>
        <div class="visual-card teal"><p>會聊</p></div>
        <div class="visual-card navy"><p>會記、會整理</p></div>
      </div>
      <div class="avatar">
        <div class="face"><p>OK</p></div>
        <div class="bar"></div>
        <div class="bar small"></div>
      </div>
    </div>`;
}

function wg01Visual() {
  return `
    <div class="panel" style="height: 250pt; display:flex; align-items:center;">
      <div class="visual-stack">
        <div class="visual-card"><p>\`if __name__ == "__main__"\` 只在直接執行時啟動。</p></div>
        <div class="visual-card teal"><p>\`print()\` 會把文字送到終端機。</p></div>
        <div class="visual-card blue"><p>被別的檔案 import 時，這一段不會自己亂跑。</p></div>
      </div>
    </div>`;
}

function basicsVisual() {
  return `
    <div class="panel" style="height: 250pt; display:flex; align-items:center;">
      <div class="visual-stack">
        <div class="visual-card"><p>變數像幫資料貼標籤，之後可以重複使用。</p></div>
        <div class="visual-card teal"><p>先有名稱，再把名稱交給 \`print()\`。</p></div>
        <div class="visual-card blue"><p>f-string 是把變數直接縫進句子裡。</p></div>
      </div>
    </div>`;
}

function setupVisual() {
  return `
    <div class="panel" style="height: 250pt; display:flex; align-items:center;">
      <div class="flow">
        <div class="box blue"><p>專案根目錄</p></div>
        <div class="arrow"><p>→</p></div>
        <div class="box teal"><p>\`uv add\` 安裝套件</p></div>
        <div class="arrow"><p>→</p></div>
        <div class="box navy"><p>程式頂端 import</p></div>
      </div>
    </div>`;
}

function secureKeyVisual() {
  return `
    <div class="panel" style="height: 250pt; display:flex; align-items:center;">
      <div class="visual-stack">
        <div class="visual-card"><p>.env：把敏感資訊放在檔案裡，但不要交進版控。</p></div>
        <div class="visual-card teal"><p>load_dotenv()：先載入環境。</p></div>
        <div class="visual-card blue"><p>os.getenv()：只顯示有 / 無，不顯示完整 key。</p></div>
      </div>
    </div>`;
}

function chatIntroVisual() {
  return `
    <div class="panel" style="height: 250pt; display:flex; align-items:center;">
      <div class="flow">
        <div class="box blue"><p>本機 Python</p></div>
        <div class="arrow"><p>→</p></div>
        <div class="box teal"><p>ChatOpenAI</p></div>
        <div class="arrow"><p>→</p></div>
        <div class="box blue"><p>模型回應</p></div>
        <div class="arrow"><p>→</p></div>
        <div class="box navy"><p>print(content)</p></div>
      </div>
    </div>`;
}

function timelineDiagram() {
  return `
  <div class="panel" style="height: 250pt; display: flex; align-items: center;">
    <div class="timeline">
      <div class="bubble user"><p>HumanMessage：這輪使用者說了什麼</p></div>
      <div class="bubble ai"><p>AIMessage：助手回了什麼</p></div>
      <div class="bubble user"><p>再下一輪：模型要看得到上一輪</p></div>
      <div class="bubble ai"><p>所以歷史裡不能只放 user，也要放 ai</p></div>
    </div>
  </div>`;
}

function contextVsMessagesDiagram() {
  return `
  <div class="panel" style="height: 250pt; display: flex; align-items: center;">
    <div class="stack">
      <div class="layer history"><p>messages：已經完成的舊回合</p></div>
      <div class="layer human"><p>human_message：這一輪新輸入</p></div>
      <div class="layer system"><p>context_messages：送進模型的完整上下文</p></div>
      <p class="muted" style="text-align:center;">先組送模串列，串流成功後再 append 進歷史。</p>
    </div>
  </div>`;
}

function systemStackDiagram() {
  return `
  <div class="panel" style="height: 250pt; display: flex; align-items: center;">
    <div class="stack">
      <div class="layer system"><p>SystemMessage：固定規則、人設、語氣</p></div>
      <div class="layer history"><p>history：已完成的人機對話回合</p></div>
      <div class="layer human"><p>human_message：本輪使用者新輸入</p></div>
    </div>
  </div>`;
}

function reactDiagram() {
  return `
  <div class="panel" style="height: 250pt; display: flex; align-items: center;">
    <div class="flow">
      <div class="box teal"><p>模型先思考</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box blue"><p>決定呼叫工具</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box teal"><p>收到 ToolMessage</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box navy"><p>產生最後回答</p></div>
    </div>
  </div>`;
}

function jsonlDiagram() {
  return `
  <div class="file" style="height: 250pt;">
    <div class="line meta"><p>metadata：created_at / updated_at / last_consolidated</p></div>
    <div class="line"><p>user：使用者這一輪說的話</p></div>
    <div class="line"><p>assistant：助手回的話</p></div>
    <div class="line tool"><p>tool：工具執行結果（需要時才有）</p></div>
    <div class="line"><p>assistant：最後整理完的回答</p></div>
  </div>`;
}

function coldStartDiagram() {
  return `
  <div class="panel" style="height: 250pt; display: flex; align-items: center;">
    <div class="flow">
      <div class="box blue"><p>程式重新啟動</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box teal"><p>逐行讀 JSONL</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box blue"><p>還原 history</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box navy"><p>接著上次繼續聊</p></div>
    </div>
  </div>`;
}

function budgetDiagram() {
  return `
  <div class="panel" style="height: 250pt;">
    <h3>送進模型的視窗</h3>
    <p class="muted">完整的 history 很長，但真正送進模型的只有 past + 本輪 human。</p>
    <div class="meter" style="margin-top: 20pt;"><div class="meter-fill warn"></div></div>
    <p class="muted" style="margin-top: 10pt;">超過預算時，要從最舊的 user-turn 邊界開始往後裁。</p>
    <div class="flow" style="margin-top: 16pt;">
      <div class="box blue"><p>完整 history</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box teal"><p>裁成 past</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box navy"><p>再送進模型</p></div>
    </div>
  </div>`;
}

function trimBoundaryDiagram() {
  return `
  <div class="panel" style="height: 250pt;">
    <div class="flow" style="margin-top: 24pt;">
      <div class="box blue"><p>舊 user turn</p></div>
      <div class="box"><p>舊 ai turn</p></div>
      <div class="box"><p>更舊 tool turn</p></div>
      <div class="box teal"><p>最新 human_message</p></div>
    </div>
    <p class="muted" style="margin-top: 24pt; text-align:center;">只從舊資料開始裁，本輪最新輸入一定要保留。</p>
  </div>`;
}

function longMemoryDiagram() {
  return `
  <div class="panel" style="height: 250pt; display: flex; align-items: center;">
    <div class="flow">
        <div class="box blue"><p>舊對話</p></div>
      <div class="arrow"><p>→</p></div>
      <div class="box teal"><p>consolidation 摘要</p></div>
      <div class="arrow"><p>→</p></div>
        <div class="box blue"><p>寫進 MEMORY</p></div>
      <div class="arrow"><p>→</p></div>
        <div class="box navy"><p>併回 system</p></div>
    </div>
  </div>`;
}

function memoryToSystemDiagram() {
  return `
  <div class="panel" style="height: 250pt; display: flex; align-items: center;">
    <div class="stack">
      <div class="layer system"><p>課堂規則 / 人設</p></div>
      <div class="layer history"><p>## Long-term Memory</p></div>
      <div class="layer human"><p>本輪使用者輸入</p></div>
      <p class="muted" style="text-align:center;">長期記憶是背景知識，不是一般 user / assistant 對話列。</p>
    </div>
  </div>`;
}

// ─── WG Challenge Illustrations (SVG → base64 img) ────────────────────────

/** Convert raw SVG string to a PNG file (via Playwright) and return a panel <div> with an <img> pointing to that PNG. */
async function svgToPngFile(svgStr, name) {
  const { chromium } = require("playwright");
  const pngPath = path.join(rootDir, "illus", `${name}.png`);
  ensureDir(path.join(rootDir, "illus"));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 360, height: 230 });
  const html = `<!DOCTYPE html><html><body style="margin:0;padding:0;background:transparent;">${svgStr}</body></html>`;
  await page.setContent(html, { waitUntil: "networkidle" });
  await page.screenshot({ path: pngPath, clip: { x: 0, y: 0, width: 360, height: 230 }, omitBackground: true });
  await browser.close();
  return pngPath.replace(/\\/g, "/");
}

// Module-level capture map — set to an object to intercept SVG strings, null otherwise
let _svgCapture = null;
// Module-level PNG path cache populated by prerenderIllus()
const _illusPngs = {};

/** If in capture mode, record the SVG and return "". Otherwise return a panel div with the pre-rendered PNG. */
function svgToImg(svgStr, name) {
  if (_svgCapture) {
    _svgCapture[name] = svgStr;
    return "";
  }
  const pngPath = _illusPngs[name] || "";
  if (!pngPath) {
    // fallback: CSS background-image (visible in HTML preview but won't be extracted as img)
    const b64 = Buffer.from(svgStr).toString("base64");
    return `<div class="panel" style="height:250pt;padding:0;background-image:url('data:image/svg+xml;base64,${b64}');background-size:contain;background-repeat:no-repeat;background-position:center;"></div>`;
  }
  return `<div class="panel" style="height:250pt;padding:4pt;overflow:hidden;display:flex;align-items:center;justify-content:center;"><img src="${pngPath}" style="max-width:100%;max-height:100%;object-fit:contain;" alt="${name}"/></div>`;
}

function wg01Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg01a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="10" y="40" width="76" height="104" rx="6" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <path d="M60 40 L86 66 L60 66Z" fill="#B8D4F0"/>
      <rect x="18" y="80" width="40" height="6" rx="3" fill="#1FC8A5"/>
      <rect x="18" y="94" width="52" height="5" rx="3" fill="#7FB4F0"/>
      <rect x="24" y="107" width="44" height="5" rx="3" fill="#153B6B"/>
      <rect x="24" y="120" width="36" height="5" rx="3" fill="#153B6B"/>
      <text x="48" y="164" text-anchor="middle" font-size="11" fill="#52708A">basic.py</text>
      <circle cx="130" cy="92" r="20" fill="#1FC8A5"/>
      <polygon points="123,83 123,101 143,92" fill="white"/>
      <text x="130" y="128" text-anchor="middle" font-size="10" fill="#1FC8A5">uv run</text>
      <line x1="152" y1="92" x2="176" y2="92" stroke="#1FC8A5" stroke-width="3" marker-end="url(#wg01a)"/>
      <rect x="184" y="40" width="166" height="114" rx="8" fill="#0F2747"/>
      <rect x="184" y="40" width="166" height="22" rx="8" fill="#1C4D86"/>
      <circle cx="202" cy="51" r="5" fill="#FF8A65"/>
      <circle cx="218" cy="51" r="5" fill="#FFD166"/>
      <circle cx="234" cy="51" r="5" fill="#1FC8A5"/>
      <text x="194" y="82" font-size="10" fill="#9ED8FF" font-family="Courier New,monospace">if __name__==</text>
      <text x="194" y="97" font-size="10" fill="#9ED8FF" font-family="Courier New,monospace">  "__main__":</text>
      <text x="202" y="116" font-size="13" fill="#1FC8A5" font-family="Courier New,monospace">Hello, World!</text>
      <text x="267" y="174" text-anchor="middle" font-size="11" fill="#52708A">終端機輸出</text>
      <rect x="184" y="178" width="166" height="20" rx="6" fill="#153B6B"/>
      <text x="267" y="192" text-anchor="middle" font-size="9" fill="#9ED8FF">被 import 時，這段不執行</text>
    </svg>`, "wg01");
}

function wg0203Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg02a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="10" y="30" width="134" height="52" rx="8" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="20" y="50" font-size="10" fill="#52708A">agent_name =</text>
      <text x="20" y="72" font-size="14" fill="#153B6B" font-family="Courier New,monospace">"法鬥超人"</text>
      <rect x="10" y="96" width="134" height="52" rx="8" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="20" y="116" font-size="10" fill="#52708A">greeting =</text>
      <text x="20" y="138" font-size="12" fill="#153B6B" font-family="Courier New,monospace">f"Hi {name}!"</text>
      <line x1="147" y1="120" x2="174" y2="120" stroke="#1FC8A5" stroke-width="3" marker-end="url(#wg02a)"/>
      <text x="160" y="110" text-anchor="middle" font-size="9" fill="#1FC8A5">填入</text>
      <rect x="180" y="88" width="168" height="66" rx="10" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="2.5"/>
      <text x="264" y="111" text-anchor="middle" font-size="12" fill="#153B6B">Hi,</text>
      <text x="264" y="136" text-anchor="middle" font-size="18" fill="#1FC8A5" font-family="Courier New,monospace">法鬥超人</text>
      <text x="264" y="182" text-anchor="middle" font-size="10" fill="#52708A">f-string 輸出結果</text>
      <line x1="77" y1="82" x2="77" y2="96" stroke="#7FB4F0" stroke-width="1.5" stroke-dasharray="4,2"/>
      <text x="77" y="212" text-anchor="middle" font-size="10" fill="#52708A">變數貼標籤 → f-string 填進句子</text>
    </svg>`, "wg0203");
}

function wg04Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg04a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="10" y="28" width="152" height="62" rx="8" fill="#0F2747"/>
      <rect x="10" y="28" width="152" height="20" rx="8" fill="#1C4D86"/>
      <circle cx="26" cy="38" r="4" fill="#FF8A65"/>
      <circle cx="40" cy="38" r="4" fill="#FFD166"/>
      <circle cx="54" cy="38" r="4" fill="#1FC8A5"/>
      <text x="20" y="64" font-size="11" fill="#1FC8A5" font-family="Courier New,monospace">$ uv add</text>
      <text x="20" y="80" font-size="10" fill="#9ED8FF" font-family="Courier New,monospace">langchain-openai</text>
      <line x1="86" y1="94" x2="86" y2="118" stroke="#1FC8A5" stroke-width="3" marker-end="url(#wg04a)"/>
      <rect x="10" y="124" width="152" height="54" rx="6" fill="#FFF4E0" stroke="#FFD27A" stroke-width="2"/>
      <text x="18" y="144" font-size="10" fill="#52708A">pyproject.toml</text>
      <rect x="18" y="150" width="130" height="8" rx="3" fill="#153B6B"/>
      <rect x="18" y="163" width="106" height="8" rx="3" fill="#153B6B"/>
      <line x1="168" y1="150" x2="190" y2="150" stroke="#1FC8A5" stroke-width="3" marker-end="url(#wg04a)"/>
      <text x="178" y="140" text-anchor="middle" font-size="9" fill="#1FC8A5">import</text>
      <rect x="196" y="56" width="152" height="94" rx="8" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="272" y="76" text-anchor="middle" font-size="10" fill="#52708A">main.py 頂端</text>
      <rect x="204" y="84" width="136" height="14" rx="4" fill="#1FC8A5"/>
      <text x="272" y="95" text-anchor="middle" font-size="9" fill="white">from langchain_openai</text>
      <rect x="204" y="102" width="136" height="14" rx="4" fill="#1FC8A5" opacity="0.8"/>
      <text x="272" y="113" text-anchor="middle" font-size="9" fill="white">import ChatOpenAI</text>
      <rect x="204" y="120" width="136" height="14" rx="4" fill="#7FB4F0"/>
      <text x="272" y="131" text-anchor="middle" font-size="9" fill="white">from dotenv import ...</text>
      <text x="180" y="210" text-anchor="middle" font-size="11" fill="#52708A">先安裝、再 import，順序不能反</text>
    </svg>`, "wg04");
}

function wg05Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg05a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="10" y="54" width="96" height="88" rx="8" fill="#FFF4E0" stroke="#FFD27A" stroke-width="2"/>
      <text x="58" y="72" text-anchor="middle" font-size="11" fill="#52708A">.env</text>
      <text x="18" y="92" font-size="9" fill="#153B6B" font-family="Courier New,monospace">OPENAI_API_KEY=</text>
      <rect x="18" y="100" width="72" height="16" rx="8" fill="#B71C1C"/>
      <text x="54" y="112" text-anchor="middle" font-size="10" fill="white">sk-••••••••</text>
      <text x="58" y="132" text-anchor="middle" font-size="9" fill="#C62828">不進版控！</text>
      <rect x="114" y="74" width="92" height="46" rx="22" fill="#1FC8A5"/>
      <text x="160" y="93" text-anchor="middle" font-size="10" fill="white">load_dotenv()</text>
      <text x="160" y="108" text-anchor="middle" font-size="9" fill="#D9F7F1">載入環境</text>
      <line x1="106" y1="98" x2="112" y2="98" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg05a)"/>
      <line x1="206" y1="98" x2="228" y2="98" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg05a)"/>
      <rect x="234" y="54" width="114" height="90" rx="8" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="291" y="72" text-anchor="middle" font-size="9" fill="#52708A">os.getenv(key)</text>
      <rect x="244" y="82" width="94" height="22" rx="11" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="1.5"/>
      <text x="291" y="97" text-anchor="middle" font-size="11" fill="#153B6B">有設定 ✓</text>
      <rect x="244" y="112" width="94" height="22" rx="11" fill="#FEEAEA" stroke="#EF9A9A" stroke-width="1.5"/>
      <text x="291" y="127" text-anchor="middle" font-size="11" fill="#C62828">未設定 ✗</text>
      <rect x="40" y="172" width="280" height="24" rx="8" fill="#153B6B"/>
      <text x="180" y="188" text-anchor="middle" font-size="10" fill="#9ED8FF">螢幕只顯示有／無，不印完整金鑰</text>
    </svg>`, "wg05");
}

function wg0607Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg06a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="8" y="10" width="344" height="210" rx="14" fill="none" stroke="#7FB4F0" stroke-width="2.5" stroke-dasharray="7,4"/>
      <text x="22" y="28" font-size="11" fill="#7FB4F0" font-family="Courier New,monospace">def main():</text>
      <polygon points="130,52 172,78 130,104 88,78" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="130" y="74" text-anchor="middle" font-size="10" fill="#153B6B">api_key</text>
      <text x="130" y="89" text-anchor="middle" font-size="10" fill="#153B6B">存在？</text>
      <line x1="172" y1="78" x2="222" y2="78" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg06a)"/>
      <text x="196" y="69" text-anchor="middle" font-size="9" fill="#1FC8A5">有 ✓</text>
      <rect x="228" y="62" width="112" height="34" rx="8" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="2"/>
      <text x="284" y="78" text-anchor="middle" font-size="10" fill="#153B6B">繼續執行主流程</text>
      <text x="284" y="92" text-anchor="middle" font-size="9" fill="#52708A">ChatOpenAI(…)</text>
      <line x1="130" y1="104" x2="130" y2="140" stroke="#C62828" stroke-width="2.5" marker-end="url(#wg06a)"/>
      <text x="142" y="126" font-size="9" fill="#C62828">沒有 ✗</text>
      <rect x="76" y="148" width="108" height="34" rx="8" fill="#FEEAEA" stroke="#EF9A9A" stroke-width="2"/>
      <text x="130" y="163" text-anchor="middle" font-size="10" fill="#C62828">印提示訊息</text>
      <text x="130" y="177" text-anchor="middle" font-size="10" fill="#C62828">提前 return</text>
      <text x="18" y="216" font-size="10" fill="#153B6B" font-family="Courier New,monospace">if __name__=="__main__":  main()</text>
    </svg>`, "wg0607");
}

function wg08Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg08a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="10" y="64" width="72" height="58" rx="6" fill="#153B6B"/>
      <rect x="14" y="68" width="64" height="46" rx="4" fill="#0F2747"/>
      <rect x="14" y="68" width="64" height="12" rx="4" fill="#1C4D86"/>
      <text x="46" y="98" text-anchor="middle" font-size="10" fill="#1FC8A5" font-family="Courier New,monospace">invoke()</text>
      <rect x="8" y="122" width="76" height="8" rx="4" fill="#52708A"/>
      <text x="46" y="148" text-anchor="middle" font-size="10" fill="#52708A">Python 程式</text>
      <line x1="84" y1="93" x2="110" y2="93" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg08a)"/>
      <text x="96" y="83" text-anchor="middle" font-size="9" fill="#52708A">請求</text>
      <ellipse cx="138" cy="93" rx="24" ry="18" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="138" y="97" text-anchor="middle" font-size="10" fill="#153B6B">API</text>
      <line x1="162" y1="93" x2="190" y2="93" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg08a)"/>
      <circle cx="220" cy="93" r="28" fill="#1FC8A5"/>
      <text x="220" y="88" text-anchor="middle" font-size="14" fill="white">AI</text>
      <text x="220" y="106" text-anchor="middle" font-size="9" fill="#D9F7F1">模型推論</text>
      <line x1="248" y1="93" x2="276" y2="93" stroke="#7FB4F0" stroke-width="2.5" stroke-dasharray="5,3" marker-end="url(#wg08a)"/>
      <text x="263" y="83" text-anchor="middle" font-size="9" fill="#52708A">回應</text>
      <rect x="280" y="62" width="72" height="62" rx="8" fill="#FFFFFF" stroke="#D5E7F7" stroke-width="2"/>
      <text x="316" y="80" text-anchor="middle" font-size="9" fill="#52708A">AIMessage</text>
      <rect x="288" y="86" width="56" height="14" rx="4" fill="#1FC8A5"/>
      <text x="316" y="97" text-anchor="middle" font-size="9" fill="white">.content</text>
      <text x="316" y="118" text-anchor="middle" font-size="9" fill="#52708A">文字字串</text>
      <text x="180" y="172" text-anchor="middle" font-size="11" fill="#153B6B">llm = ChatOpenAI()  →  llm.invoke("問題")</text>
      <text x="180" y="190" text-anchor="middle" font-size="10" fill="#52708A">回傳的是物件，取 .content 才是文字</text>
    </svg>`, "wg08");
}

function wg09Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg09a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <circle cx="180" cy="104" r="76" fill="none" stroke="#D5E7F7" stroke-width="3" stroke-dasharray="10,5"/>
      <text x="180" y="24" text-anchor="middle" font-size="10" fill="#52708A">while True:</text>
      <rect x="56" y="74" width="76" height="40" rx="8" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="94" y="90" text-anchor="middle" font-size="11" fill="#153B6B">你輸入</text>
      <text x="94" y="106" text-anchor="middle" font-size="9" fill="#52708A">input()</text>
      <line x1="132" y1="94" x2="158" y2="94" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg09a)"/>
      <rect x="162" y="74" width="70" height="40" rx="8" fill="#1FC8A5"/>
      <text x="197" y="90" text-anchor="middle" font-size="11" fill="white">模型</text>
      <text x="197" y="106" text-anchor="middle" font-size="9" fill="#D9F7F1">invoke</text>
      <line x1="232" y1="94" x2="258" y2="94" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg09a)"/>
      <rect x="260" y="74" width="76" height="40" rx="8" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="298" y="90" text-anchor="middle" font-size="11" fill="#153B6B">印回覆</text>
      <text x="298" y="106" text-anchor="middle" font-size="9" fill="#52708A">print()</text>
      <path d="M298 114 Q298 168 180 178 Q62 168 62 114" fill="none" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg09a)"/>
      <rect x="124" y="152" width="112" height="28" rx="14" fill="#FEEAEA" stroke="#EF9A9A" stroke-width="2"/>
      <text x="180" y="170" text-anchor="middle" font-size="10" fill="#C62828">quit → break 離開</text>
      <text x="180" y="214" text-anchor="middle" font-size="10" fill="#52708A">while True 讓對話持續到你說停</text>
    </svg>`, "wg09");
}

function wg10Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <rect x="10" y="26" width="158" height="172" rx="10" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="89" y="48" text-anchor="middle" font-size="13" fill="#153B6B">invoke()</text>
      <text x="89" y="64" text-anchor="middle" font-size="9" fill="#52708A">等全部完成後一次取得</text>
      <rect x="22" y="76" width="134" height="98" rx="6" fill="#7FB4F0"/>
      <text x="89" y="118" text-anchor="middle" font-size="11" fill="white">整段文字</text>
      <text x="89" y="136" text-anchor="middle" font-size="11" fill="white">一次跳出</text>
      <text x="89" y="212" text-anchor="middle" font-size="10" fill="#52708A">⬜ 一次出現</text>
      <line x1="180" y1="20" x2="180" y2="210" stroke="#D5E7F7" stroke-width="2" stroke-dasharray="5,4"/>
      <rect x="192" y="26" width="158" height="172" rx="10" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="2"/>
      <text x="271" y="48" text-anchor="middle" font-size="13" fill="#153B6B">stream()</text>
      <text x="271" y="64" text-anchor="middle" font-size="9" fill="#52708A">邊生成邊送出 token</text>
      <rect x="202" y="76" width="30" height="22" rx="4" fill="#1FC8A5"/>
      <rect x="236" y="76" width="38" height="22" rx="4" fill="#1FC8A5"/>
      <rect x="278" y="76" width="26" height="22" rx="4" fill="#1FC8A5"/>
      <rect x="308" y="76" width="32" height="22" rx="4" fill="#1FC8A5" opacity="0.7"/>
      <rect x="202" y="104" width="44" height="22" rx="4" fill="#1FC8A5" opacity="0.9"/>
      <rect x="250" y="104" width="30" height="22" rx="4" fill="#1FC8A5" opacity="0.6"/>
      <rect x="284" y="104" width="22" height="22" rx="4" fill="#1FC8A5" opacity="0.4"/>
      <rect x="202" y="132" width="28" height="22" rx="4" fill="#1FC8A5" opacity="0.5"/>
      <rect x="234" y="132" width="36" height="22" rx="4" fill="#1FC8A5" opacity="0.3"/>
      <text x="271" y="180" text-anchor="middle" font-size="8" fill="#52708A" font-family="Courier New,monospace">end="" flush=True</text>
      <text x="271" y="212" text-anchor="middle" font-size="10" fill="#52708A">⬛ 逐塊顯示（打字機）</text>
    </svg>`, "wg10");
}

function wg11Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <line x1="44" y1="26" x2="44" y2="198" stroke="#D5E7F7" stroke-width="3"/>
      <circle cx="44" cy="46" r="9" fill="#7FB4F0"/>
      <rect x="62" y="34" width="114" height="26" rx="6" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1.5"/>
      <text x="119" y="51" text-anchor="middle" font-size="11" fill="#153B6B">HumanMessage</text>
      <circle cx="44" cy="92" r="9" fill="#1FC8A5"/>
      <rect x="62" y="80" width="114" height="26" rx="6" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="1.5"/>
      <text x="119" y="97" text-anchor="middle" font-size="11" fill="#153B6B">AIMessage</text>
      <circle cx="44" cy="138" r="9" fill="#7FB4F0"/>
      <rect x="62" y="126" width="114" height="26" rx="6" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1.5"/>
      <text x="119" y="143" text-anchor="middle" font-size="11" fill="#153B6B">HumanMessage</text>
      <circle cx="44" cy="184" r="9" fill="#1FC8A5"/>
      <rect x="62" y="172" width="114" height="26" rx="6" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="1.5"/>
      <text x="119" y="189" text-anchor="middle" font-size="11" fill="#153B6B">AIMessage</text>
      <rect x="204" y="32" width="144" height="140" rx="8" fill="#FFFFFF" stroke="#D5E7F7" stroke-width="2"/>
      <text x="276" y="52" text-anchor="middle" font-size="10" fill="#52708A">messages = [</text>
      <rect x="212" y="58" width="128" height="18" rx="4" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1"/>
      <text x="276" y="71" text-anchor="middle" font-size="9" fill="#153B6B">HumanMessage</text>
      <rect x="212" y="80" width="128" height="18" rx="4" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="1"/>
      <text x="276" y="93" text-anchor="middle" font-size="9" fill="#153B6B">AIMessage</text>
      <rect x="212" y="102" width="128" height="18" rx="4" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1"/>
      <text x="276" y="115" text-anchor="middle" font-size="9" fill="#153B6B">HumanMessage</text>
      <rect x="212" y="124" width="128" height="18" rx="4" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="1"/>
      <text x="276" y="137" text-anchor="middle" font-size="9" fill="#153B6B">AIMessage</text>
      <text x="276" y="160" text-anchor="middle" font-size="10" fill="#52708A">]</text>
      <rect x="204" y="178" width="144" height="24" rx="12" fill="#FEEAEA" stroke="#EF9A9A" stroke-width="1.5"/>
      <text x="276" y="194" text-anchor="middle" font-size="10" fill="#C62828">關程式 → 記憶消失</text>
    </svg>`, "wg11");
}

function wg12Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <rect x="36" y="26" width="288" height="52" rx="12" fill="#EAF8F5" stroke="#1FC8A5" stroke-width="2.5"/>
      <text x="180" y="46" text-anchor="middle" font-size="13" fill="#153B6B">SystemMessage</text>
      <text x="180" y="66" text-anchor="middle" font-size="10" fill="#52708A">固定角色 / 人設 / 規則 — 每輪都帶進去</text>
      <rect x="36" y="88" width="288" height="52" rx="12" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2.5"/>
      <text x="180" y="108" text-anchor="middle" font-size="13" fill="#153B6B">*history</text>
      <text x="180" y="128" text-anchor="middle" font-size="10" fill="#52708A">已完成的 Human / AI 回合（累積的對話脈絡）</text>
      <rect x="36" y="150" width="288" height="52" rx="12" fill="#FFF4E0" stroke="#FFD27A" stroke-width="2.5"/>
      <text x="180" y="170" text-anchor="middle" font-size="13" fill="#153B6B">HumanMessage（本輪）</text>
      <text x="180" y="190" text-anchor="middle" font-size="10" fill="#52708A">這一輪使用者的最新輸入 — 放最後一則</text>
      <rect x="36" y="212" width="288" height="14" rx="4" fill="#153B6B"/>
      <text x="180" y="223" text-anchor="middle" font-size="9" fill="#9ED8FF">[system, *history, human_msg]  →  llm.invoke()</text>
    </svg>`, "wg12");
}

function wg13Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg13a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="8" y="72" width="68" height="52" rx="8" fill="#1FC8A5"/>
      <text x="42" y="92" text-anchor="middle" font-size="11" fill="white">LLM</text>
      <text x="42" y="108" text-anchor="middle" font-size="9" fill="#D9F7F1">invoke</text>
      <line x1="76" y1="98" x2="100" y2="98" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg13a)"/>
      <polygon points="128,78 166,98 128,118 90,98" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="128" y="93" text-anchor="middle" font-size="9" fill="#153B6B">tool</text>
      <text x="128" y="107" text-anchor="middle" font-size="9" fill="#153B6B">calls?</text>
      <line x1="166" y1="98" x2="196" y2="98" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg13a)"/>
      <text x="180" y="88" text-anchor="middle" font-size="9" fill="#1FC8A5">有 ✓</text>
      <rect x="200" y="76" width="72" height="44" rx="8" fill="#7FB4F0"/>
      <text x="236" y="96" text-anchor="middle" font-size="10" fill="white">執行</text>
      <text x="236" y="110" text-anchor="middle" font-size="9" fill="#D4E8F8">工具函式</text>
      <line x1="272" y1="98" x2="296" y2="98" stroke="#7FB4F0" stroke-width="2.5" marker-end="url(#wg13a)"/>
      <rect x="300" y="76" width="52" height="44" rx="8" fill="#FFF4E0" stroke="#FFD27A" stroke-width="1.5"/>
      <text x="326" y="94" text-anchor="middle" font-size="9" fill="#153B6B">Tool</text>
      <text x="326" y="108" text-anchor="middle" font-size="9" fill="#153B6B">Msg</text>
      <path d="M326 120 Q326 174 42 170 Q42 158 42 124" fill="none" stroke="#7FB4F0" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#wg13a)"/>
      <text x="184" y="168" text-anchor="middle" font-size="9" fill="#52708A">loop 再送一次</text>
      <line x1="128" y1="118" x2="128" y2="156" stroke="#153B6B" stroke-width="2.5" marker-end="url(#wg13a)"/>
      <text x="140" y="142" font-size="9" fill="#153B6B">沒有 ✗</text>
      <rect x="76" y="162" width="104" height="32" rx="8" fill="#153B6B"/>
      <text x="128" y="182" text-anchor="middle" font-size="10" fill="white">最終文字回覆</text>
    </svg>`, "wg13");
}

function wg14Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg14a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="8" y="26" width="118" height="30" rx="12" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1.5"/>
      <text x="67" y="45" text-anchor="middle" font-size="11" fill="#153B6B">你說的話（Human）</text>
      <rect x="8" y="64" width="118" height="30" rx="12" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="1.5"/>
      <text x="67" y="83" text-anchor="middle" font-size="11" fill="#153B6B">助手的回覆（AI）</text>
      <rect x="8" y="102" width="118" height="30" rx="12" fill="#FFF4E0" stroke="#FFD27A" stroke-width="1.5"/>
      <text x="67" y="121" text-anchor="middle" font-size="11" fill="#153B6B">工具執行結果</text>
      <line x1="128" y1="90" x2="158" y2="90" stroke="#1FC8A5" stroke-width="3" marker-end="url(#wg14a)"/>
      <text x="143" y="80" text-anchor="middle" font-size="9" fill="#1FC8A5">寫入</text>
      <rect x="164" y="16" width="186" height="180" rx="8" fill="#FFFFFF" stroke="#D5E7F7" stroke-width="2"/>
      <text x="257" y="36" text-anchor="middle" font-size="10" fill="#52708A">session.jsonl</text>
      <rect x="172" y="44" width="170" height="20" rx="4" fill="#EAF8F5"/>
      <text x="257" y="58" text-anchor="middle" font-size="9" fill="#1D7F8E" font-family="Courier New,monospace">{_type: "metadata", …}</text>
      <rect x="172" y="68" width="170" height="20" rx="4" fill="#EAF5FF"/>
      <text x="257" y="82" text-anchor="middle" font-size="9" fill="#153B6B" font-family="Courier New,monospace">{role:"user", content:…}</text>
      <rect x="172" y="92" width="170" height="20" rx="4" fill="#EAF8F5"/>
      <text x="257" y="106" text-anchor="middle" font-size="9" fill="#153B6B" font-family="Courier New,monospace">{role:"assistant", …}</text>
      <rect x="172" y="116" width="170" height="20" rx="4" fill="#FFF4E0"/>
      <text x="257" y="130" text-anchor="middle" font-size="9" fill="#153B6B" font-family="Courier New,monospace">{role:"tool", …}</text>
      <rect x="172" y="140" width="170" height="20" rx="4" fill="#EAF8F5"/>
      <text x="257" y="154" text-anchor="middle" font-size="9" fill="#153B6B" font-family="Courier New,monospace">{role:"assistant", …}</text>
      <text x="257" y="210" text-anchor="middle" font-size="10" fill="#52708A">每行一筆 JSON，每輪整檔覆寫</text>
    </svg>`, "wg14");
}

function wg15Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg15a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="10" y="26" width="86" height="38" rx="8" fill="#153B6B"/>
      <text x="53" y="44" text-anchor="middle" font-size="10" fill="white">程式重啟</text>
      <text x="53" y="58" text-anchor="middle" font-size="9" fill="#9ED8FF">冷啟動</text>
      <line x1="53" y1="64" x2="53" y2="90" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg15a)"/>
      <rect x="10" y="96" width="86" height="74" rx="6" fill="#FFFFFF" stroke="#D5E7F7" stroke-width="2"/>
      <text x="53" y="114" text-anchor="middle" font-size="9" fill="#52708A">session.jsonl</text>
      <rect x="18" y="120" width="70" height="12" rx="3" fill="#EAF8F5"/>
      <rect x="18" y="136" width="70" height="12" rx="3" fill="#EAF5FF"/>
      <rect x="18" y="152" width="70" height="12" rx="3" fill="#EAF8F5"/>
      <line x1="98" y1="133" x2="126" y2="133" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg15a)"/>
      <text x="112" y="122" text-anchor="middle" font-size="8" fill="#1FC8A5">json.loads</text>
      <text x="112" y="146" text-anchor="middle" font-size="8" fill="#52708A">逐行讀回</text>
      <rect x="132" y="96" width="106" height="74" rx="6" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="2"/>
      <text x="185" y="114" text-anchor="middle" font-size="9" fill="#52708A">history 還原</text>
      <rect x="140" y="120" width="90" height="14" rx="4" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1"/>
      <text x="185" y="131" text-anchor="middle" font-size="8" fill="#153B6B">HumanMessage</text>
      <rect x="140" y="138" width="90" height="14" rx="4" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="1"/>
      <text x="185" y="149" text-anchor="middle" font-size="8" fill="#153B6B">AIMessage</text>
      <rect x="140" y="156" width="90" height="14" rx="4" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1"/>
      <text x="185" y="167" text-anchor="middle" font-size="8" fill="#153B6B">HumanMessage</text>
      <line x1="240" y1="133" x2="268" y2="133" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg15a)"/>
      <rect x="272" y="106" width="80" height="54" rx="8" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="2"/>
      <text x="312" y="126" text-anchor="middle" font-size="10" fill="#153B6B">接著</text>
      <text x="312" y="144" text-anchor="middle" font-size="10" fill="#1FC8A5">繼續聊</text>
      <rect x="60" y="198" width="240" height="24" rx="8" fill="#1FC8A5"/>
      <text x="180" y="214" text-anchor="middle" font-size="11" fill="white">關掉程式再開，對話不中斷</text>
    </svg>`, "wg15");
}

function wg16Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <text x="30" y="36" font-size="10" fill="#153B6B">完整 history（可能很長）</text>
      <rect x="30" y="44" width="300" height="32" rx="6" fill="#D5E7F7"/>
      <text x="180" y="64" text-anchor="middle" font-size="11" fill="#153B6B">回合 1…2…3…4…5…6…7…</text>
      <line x1="214" y1="38" x2="214" y2="118" stroke="#C62828" stroke-width="2.5" stroke-dasharray="5,3"/>
      <rect x="148" y="24" width="132" height="18" rx="6" fill="#C62828"/>
      <text x="214" y="36" text-anchor="middle" font-size="9" fill="white">TOKEN_BUDGET 上限</text>
      <text x="30" y="104" font-size="10" fill="#153B6B">送給模型的 past</text>
      <rect x="30" y="112" width="182" height="32" rx="6" fill="#1FC8A5"/>
      <text x="121" y="132" text-anchor="middle" font-size="10" fill="white">這段帶進去</text>
      <rect x="214" y="112" width="116" height="32" rx="6" fill="#FEEAEA" stroke="#EF9A9A" stroke-width="1.5" stroke-dasharray="5,3"/>
      <text x="272" y="132" text-anchor="middle" font-size="9" fill="#C62828">太舊，略過</text>
      <rect x="30" y="164" width="300" height="32" rx="6" fill="#FFF4E0" stroke="#FFD27A" stroke-width="2.5"/>
      <text x="180" y="180" text-anchor="middle" font-size="11" fill="#153B6B">human_message（本輪）</text>
      <text x="180" y="194" text-anchor="middle" font-size="9" fill="#52708A">一定保留，不受預算限制</text>
      <rect x="60" y="214" width="240" height="14" rx="4" fill="#153B6B"/>
      <text x="180" y="225" text-anchor="middle" font-size="9" fill="#9ED8FF">邊界選在 user-turn 開頭，不切斷對話</text>
    </svg>`, "wg16");
}

function wg17Illus() {
  return svgToImg(`<svg viewBox="0 0 360 230" width="360" height="230" font-family="Arial,sans-serif" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="wg17a" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="#1FC8A5"/></marker></defs>
      <rect x="8" y="36" width="64" height="16" rx="4" fill="#D5E7F7"/>
      <rect x="8" y="56" width="64" height="16" rx="4" fill="#D5E7F7" opacity="0.8"/>
      <rect x="8" y="76" width="64" height="16" rx="4" fill="#D5E7F7" opacity="0.6"/>
      <rect x="8" y="96" width="64" height="16" rx="4" fill="#D5E7F7" opacity="0.4"/>
      <text x="40" y="130" text-anchor="middle" font-size="10" fill="#52708A">舊對話</text>
      <line x1="74" y1="86" x2="96" y2="86" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg17a)"/>
      <circle cx="122" cy="86" r="24" fill="#1FC8A5"/>
      <text x="122" y="82" text-anchor="middle" font-size="10" fill="white">整併</text>
      <text x="122" y="96" text-anchor="middle" font-size="9" fill="#D9F7F1">LLM</text>
      <line x1="146" y1="86" x2="170" y2="86" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg17a)"/>
      <rect x="176" y="52" width="80" height="68" rx="8" fill="#FFFFFF" stroke="#8EE0D0" stroke-width="2"/>
      <text x="216" y="70" text-anchor="middle" font-size="9" fill="#52708A">MEMORY.md</text>
      <rect x="184" y="76" width="64" height="10" rx="3" fill="#1FC8A5"/>
      <rect x="184" y="90" width="56" height="10" rx="3" fill="#72CDBA"/>
      <rect x="184" y="104" width="48" height="10" rx="3" fill="#A8DDD4"/>
      <text x="216" y="136" text-anchor="middle" font-size="9" fill="#52708A">長期摘要</text>
      <line x1="256" y1="86" x2="278" y2="86" stroke="#1FC8A5" stroke-width="2.5" marker-end="url(#wg17a)"/>
      <rect x="282" y="52" width="72" height="68" rx="8" fill="#EAF8F5" stroke="#8EE0D0" stroke-width="2"/>
      <text x="318" y="68" text-anchor="middle" font-size="9" fill="#52708A">System</text>
      <rect x="290" y="76" width="56" height="10" rx="3" fill="#EAF5FF" stroke="#7FB4F0" stroke-width="1"/>
      <text x="318" y="85" text-anchor="middle" font-size="7" fill="#153B6B">人設 / 規則</text>
      <rect x="290" y="90" width="56" height="10" rx="3" fill="#1FC8A5"/>
      <text x="318" y="99" text-anchor="middle" font-size="7" fill="white">Long-term</text>
      <rect x="290" y="104" width="56" height="10" rx="3" fill="#1FC8A5" opacity="0.7"/>
      <text x="318" y="113" text-anchor="middle" font-size="7" fill="white">Memory</text>
      <rect x="120" y="162" width="120" height="46" rx="8" fill="#FFFFFF" stroke="#D5E7F7" stroke-width="1.5"/>
      <text x="180" y="180" text-anchor="middle" font-size="9" fill="#52708A">HISTORY.md</text>
      <rect x="128" y="186" width="104" height="10" rx="3" fill="#D5E7F7"/>
      <text x="180" y="195" text-anchor="middle" font-size="7" fill="#52708A">[2026-04-20] 整併摘要</text>
      <text x="180" y="222" text-anchor="middle" font-size="10" fill="#52708A">超預算時整併 → 寫 MEMORY → 帶回 system</text>
    </svg>`, "wg17");
}

// ─── End WG Challenge Illustrations ────────────────────────────────────────

function buildSlides() { return [
  { name: "01-cover.html", html: coverSlide() },
  { name: "02-roadmap.html", html: roadmapSlide() },
  {
    name: "03-wg01.html",
    html: sideImageSlide({
      eyebrow: "WG-01",
      title: "按下啟動鍵",
      subtitle: "先讓 Python 在正確的時機說第一句話。",
      bulletsList: [
        "`print()` 可以把文字送到終端機。",
        "`if __name__ == \"__main__\"` 代表只有直接執行這個檔案時才跑。",
        "這樣做的好處是：被別的檔案 `import` 時，不會自己亂執行。",
      ],
      visualHtml: wg01Illus(),
    }),
  },
  {
    name: "04-wg02-wg03.html",
    html: sideImageSlide({
      eyebrow: "WG-02～WG-03",
      title: "字串先有名字，再組成一句話",
      subtitle: "從單純印字，到用變數和 f-string 組句。",
      bulletsList: [
        "變數像幫資料貼標籤，之後可以重複拿來用。",
        "f-string 可以把變數直接塞進句子裡。",
        "如果先後順序寫錯，後面的句子就找不到前面的變數。",
      ],
      visualHtml: wg0203Illus(),
    }),
  },
  {
    name: "05-wg04.html",
    html: sideImageSlide({
      eyebrow: "WG-04",
      title: "把工具裝進專案",
      subtitle: "先把未來要用的套件安裝好，再在檔案頂端匯入。",
      bulletsList: [
        "`uv add` 是把套件加進這個專案。",
        "`import` / `from ... import ...` 是在程式裡把名稱拿進來。",
        "這一題先備料，還不急著真的打 API。",
      ],
      visualHtml: wg04Illus(),
    }),
  },
  {
    name: "06-wg05.html",
    html: sideImageSlide({
      eyebrow: "WG-05",
      title: "讀設定，但不把金鑰秀出來",
      subtitle: "會讀 `.env` 很重要，會保護敏感資訊更重要。",
      bulletsList: [
        "`load_dotenv()` 先把 `.env` 的資料載進環境。",
        "`os.getenv()` 再把指定變數讀出來。",
        "螢幕上只能顯示有 / 無，不要把整串金鑰印出來。",
      ],
      visualHtml: wg05Illus(),
    }),
  },
  {
    name: "07-wg06-wg07.html",
    html: diagramTextSlide({
      eyebrow: "WG-06～WG-07",
      title: "有鑰匙才往下走",
      subtitle: "用分支決定流程，再把主流程收進 `main()`。",
      bulletsList: [
        "`if / else` 讓程式能根據條件走不同路。",
        "沒有 API key 時，應該提早停下來，而不是硬往下跑。",
        "`main()` 讓入口和主要流程分開，結構更清楚。",
      ],
      diagram: wg0607Illus(),
    }),
  },
  {
    name: "08-wg08.html",
    html: sideImageSlide({
      eyebrow: "WG-08",
      title: "第一通打進大模型",
      subtitle: "第一次從本機程式把一句話送到模型，再拿回回覆。",
      bulletsList: [
        "`ChatOpenAI(...)` 是建立模型連線物件。",
        "`invoke(...)` 代表送出一次請求。",
        "回來的不是普通字串，所以通常要用 `.content` 拿文字。",
      ],
      visualHtml: wg08Illus(),
    }),
  },
  {
    name: "09-wg09.html",
    html: diagramTextSlide({
      eyebrow: "WG-09",
      title: "把一次問答變成聊天迴圈",
      subtitle: "不再只問一次，而是可以持續對話到你說停。",
      bulletsList: [
        "`while True` 可以讓聊天一直重複。",
        "`input()` 讓使用者每輪都能打新問題。",
        "`quit / exit / q` 這類指令可以安全結束聊天。",
      ],
      diagram: wg09Illus(),
    }),
  },
  {
    name: "10-wg10.html",
    html: diagramTextSlide({
      eyebrow: "WG-10",
      title: "`invoke` 和 `stream`，體感差在哪？",
      subtitle: "同樣都能拿到答案，但使用者感覺很不一樣。",
      bulletsList: [
        "`invoke` 等整段答案完成後，一次全部拿回來。",
        "`stream` 答案一小塊一小塊回來，像打字機一樣。",
        "串流輸出要搭配 `print(..., end=\"\", flush=True)` 才會看到效果。",
      ],
      diagram: wg10Illus(),
    }),
  },
  { name: "11-summary.html", html: summaryMilestoneSlide() },
  {
    name: "12-wg11.html",
    html: diagramTextSlide({
      eyebrow: "WG-11",
      title: "把上一輪也帶進下一輪",
      subtitle: "聊天之所以像聊天，是因為模型看得到前情提要。",
      bulletsList: [
        "`messages` 是放在 RAM 裡的對話時間軸。",
        "裡面不只放使用者，也要放助手，不然脈絡會斷掉。",
        "這時候記憶還沒寫進檔案，所以關程式就會消失。",
      ],
      diagram: wg11Illus(),
    }),
  },
  {
    name: "13-wg11-context.html",
    html: diagramTextSlide({
      eyebrow: "WG-11 圖解",
      title: "為什麼要先組 `context_messages`，再 append？",
      subtitle: "送模串列和真正累積的歷史，不是同一件事。",
      bulletsList: [
        "送進模型的是本輪要看的完整上下文。",
        "真正累積在 `messages` 裡的是已經完成的回合。",
        "先組、再 append，才不會把未完成的回合提早寫進歷史。",
      ],
      diagram: contextVsMessagesDiagram(),
    }),
  },
  {
    name: "14-wg12.html",
    html: diagramTextSlide({
      eyebrow: "WG-12",
      title: "把人設放進 system",
      subtitle: "有些規則不是這一輪才說，而是每一輪都要一起帶進去。",
      bulletsList: [
        "`SystemMessage` 是固定規則、人設、語氣的地方。",
        "`history` 放的是對話回合，不要把 system 混在裡面。",
        "送模時常見的組法是 `[system, *history, human]`。",
      ],
      diagram: wg12Illus(),
    }),
  },
  {
    name: "15-wg13.html",
    html: diagramTextSlide({
      eyebrow: "WG-13",
      title: "模型不只會想，還會用工具",
      subtitle: "需要計算或查資料時，模型可以自己決定要不要呼叫工具。",
      bulletsList: [
        "`@tool` 是把 Python 函式包成可被模型呼叫的工具。",
        "`bind_tools()` 讓模型知道有哪些工具可以用。",
        "`tool_calls` 和 `ToolMessage` 讓『叫工具 -> 拿結果 -> 繼續回答』串起來。",
      ],
      diagram: wg13Illus(),
    }),
  },
  {
    name: "16-wg14.html",
    html: diagramTextSlide({
      eyebrow: "WG-14",
      title: "先學會把對話寫進檔案",
      subtitle: "聊天如果只在 RAM 裡，關掉就沒了；寫進檔案才留得住。",
      bulletsList: [
        "JSONL 可以想成一行一筆資料的文字檔。",
        "第一行常放 metadata，後面每行放一則對話。",
        "這一題先練寫出去，不急著一開機就讀回來。",
      ],
      diagram: wg14Illus(),
    }),
  },
  {
    name: "17-wg15.html",
    html: diagramTextSlide({
      eyebrow: "WG-15",
      title: "重開程式，昨天的對話還在",
      subtitle: "把 JSONL 再讀回來，讓程式不是每次都從零開始。",
      bulletsList: [
        "`json.loads()` 可以把每一行 JSON 讀回 Python 資料。",
        "壞掉的行可以略過，不要讓整份檔案直接報廢。",
        "這樣一來，關掉程式再打開，也能接著聊。",
      ],
      diagram: wg15Illus(),
    }),
  },
  { name: "18-ram-vs-file.html", html: compareRamVsFileSlide() },
  {
    name: "19-wg16.html",
    html: diagramTextSlide({
      eyebrow: "WG-16",
      title: "上下文不是無限大",
      subtitle: "對話越來越長時，不能什麼都塞進模型。",
      bulletsList: [
        "`history` 是完整歷史，但送進模型的可能只是其中一段 `past`。",
        "`TOKEN_BUDGET` 是簡化版的容量上限。",
        "當容量不夠，就得從最舊的部分開始裁掉。",
      ],
      diagram: wg16Illus(),
    }),
  },
  {
    name: "20-wg16-boundary.html",
    html: diagramTextSlide({
      eyebrow: "WG-16 圖解",
      title: "裁切不是亂砍，而是有邊界的整理",
      subtitle: "只從舊資料開始裁，本輪最新輸入一定要保留。",
      bulletsList: [
        "`human_message` 一定要保留。",
        "邊界通常選在 user-turn 開頭，避免把一段對話切碎。",
        "所以 `history` 的長度，和送進模型的長度，不一定一樣。",
      ],
      diagram: trimBoundaryDiagram(),
    }),
  },
  {
    name: "21-wg17.html",
    html: diagramTextSlide({
      eyebrow: "WG-17",
      title: "把舊對話濃縮成長期記憶",
      subtitle: "短期視窗裝不下，就把舊內容整理成更短、但還有用的摘要。",
      bulletsList: [
        "`MEMORY.md` 放濃縮後的長期重點。",
        "`HISTORY.md` 記錄每次整併發生了什麼。",
        "這樣模型就算沒看到完整舊對話，還是能抓到大方向。",
      ],
      diagram: wg17Illus(),
    }),
  },
  {
    name: "22-wg17-system.html",
    html: diagramTextSlide({
      eyebrow: "WG-17 圖解",
      title: "Long-term Memory 怎麼回到模型腦中？",
      subtitle: "它不是一般聊天訊息，而是 system 背景知識的一部分。",
      bulletsList: [
        "長期記憶不是當一般 user / assistant 訊息塞回去。",
        "它會被放進 system 區塊，變成模型每輪都會看到的背景知識。",
        "這樣做比把全部舊訊息硬塞回去更省空間。",
      ],
      diagram: memoryToSystemDiagram(),
    }),
  },
  { name: "23-growth.html", html: finalGrowthSlide() },
  { name: "24-ability-map.html", html: abilityMapSlide() },
  { name: "25-lesson-plan.html", html: lessonPlanSlide() },
  { name: "26-closing.html", html: closingSlide() },
]; }

/** Panel keys used when capturing SVG from `wg*Illus()` (one combined slide may share one key). */
const ILLUS_PANEL_KEYS = ["wg01", "wg0203", "wg04", "wg05", "wg0607", "wg08", "wg09", "wg10", "wg11", "wg12", "wg13", "wg14", "wg15", "wg16", "wg17"];

/** Map WG challenge number (1–17) → panel key in `ILLUS_PANEL_KEYS`. */
const WG_NUM_TO_PANEL = {
  1: "wg01", 2: "wg0203", 3: "wg0203", 4: "wg04", 5: "wg05", 6: "wg0607", 7: "wg0607",
  8: "wg08", 9: "wg09", 10: "wg10", 11: "wg11", 12: "wg12", 13: "wg13", 14: "wg14", 15: "wg15", 16: "wg16", 17: "wg17",
};

function captureIllusSvgMap() {
  const funcs = {
    wg01: wg01Illus, wg0203: wg0203Illus, wg04: wg04Illus, wg05: wg05Illus, wg0607: wg0607Illus,
    wg08: wg08Illus, wg09: wg09Illus, wg10: wg10Illus, wg11: wg11Illus, wg12: wg12Illus, wg13: wg13Illus,
    wg14: wg14Illus, wg15: wg15Illus, wg16: wg16Illus, wg17: wg17Illus,
  };
  const svgMap = {};
  _svgCapture = svgMap;
  for (const name of ILLUS_PANEL_KEYS) funcs[name]();
  _svgCapture = null;
  return svgMap;
}

/** Write `illus/wg01.svg` … `illus/wg17.svg` (WG-02/03 and WG-06/07 duplicate the combined slide art). */
function exportIllusSvgFiles() {
  const svgMap = captureIllusSvgMap();
  const illusDir = path.join(rootDir, "illus");
  ensureDir(illusDir);
  console.log(`Exporting SVG → ${illusDir}`);
  for (let n = 1; n <= 17; n += 1) {
    const key = WG_NUM_TO_PANEL[n];
    const svg = svgMap[key];
    if (!svg) throw new Error(`Missing SVG for panel key: ${key}`);
    const fname = `wg${String(n).padStart(2, "0")}.svg`;
    fs.writeFileSync(path.join(illusDir, fname), svg, "utf8");
    console.log(`  ✓ ${fname} (from ${key})`);
  }
  console.log("Done.");
}

async function prerenderIllus() {
  const svgMap = captureIllusSvgMap();

  // Use Playwright to render each SVG to PNG, then encode as base64 data URI
  const { chromium } = require("playwright");
  const browser = await chromium.launch();
  console.log("Pre-rendering illustrations (SVG → PNG data URI)...");
  for (const name of ILLUS_PANEL_KEYS) {
    const svgStr = svgMap[name];
    if (!svgStr) { console.warn(`  No SVG for ${name}`); continue; }
    const page = await browser.newPage();
    await page.setViewportSize({ width: 720, height: 460 });
    const html = `<!DOCTYPE html><html><body style="margin:0;padding:0;width:720px;height:460px;background:white;">${svgStr}</body></html>`;
    await page.setContent(html, { waitUntil: "networkidle" });
    const pngBuf = await page.screenshot({ type: "png", clip: { x: 0, y: 0, width: 720, height: 460 } });
    await page.close();
    _illusPngs[name] = `data:image/png;base64,${pngBuf.toString("base64")}`;
    console.log(`  ✓ ${name} (${Math.round(pngBuf.length / 1024)} KB)`);
  }
  await browser.close();
  console.log("Illustrations ready.");
}

async function build() {
  await prerenderIllus();
  const slides = buildSlides();   // build after PNGs are ready
  ensureDir(slidesDir);

  for (const slide of slides) {
    writeSlideHtml(slide.name, slide.html);
  }

  const pptx = new PptxGenJS();
  pptx.layout = "LAYOUT_16x9";
  pptx.author = "Cursor";
  pptx.company = "Cursor";
  pptx.subject = "WG-01～WG-17 教學簡報";
  pptx.title = "WG-01～WG-17 教學簡報";
  pptx.lang = "zh-TW";

  for (const slide of slides) {
    await html2pptx(path.join(slidesDir, slide.name), pptx);
  }

  await pptx.writeFile({ fileName: outputFile });
  console.log(`Wrote presentation to ${outputFile}`);
}

if (process.argv.includes("--export-svg")) {
  try {
    exportIllusSvgFiles();
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
} else {
  build().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
