const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "Codex";
pptx.subject = "決策樹建構流程";
pptx.title = "決策樹的建立流程";
pptx.company = "Generated from transcript";
pptx.lang = "zh-TW";
pptx.theme = {
  headFontFace: "Arial",
  bodyFontFace: "Arial",
  lang: "zh-TW"
};

const C = {
  ink: "1E293B",
  muted: "64748B",
  bg: "F8FAFC",
  panel: "FFFFFF",
  teal: "0F766E",
  coral: "F97316",
  amber: "F59E0B",
  blue: "2563EB",
  line: "CBD5E1",
  paleTeal: "CCFBF1",
  paleCoral: "FFEDD5",
  paleBlue: "DBEAFE",
  dark: "0F172A",
  white: "FFFFFF"
};

function addBg(slide) {
  slide.background = { color: C.bg };
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 13.333, h: 0.16, fill: { color: C.teal }, line: { color: C.teal } });
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 7.32, w: 13.333, h: 0.18, fill: { color: C.dark }, line: { color: C.dark } });
}

function title(slide, text, kicker = "") {
  if (kicker) {
    slide.addText(kicker, { x: 0.55, y: 0.34, w: 5, h: 0.24, fontFace: "Arial", fontSize: 8.5, bold: true, color: C.teal, breakLine: false });
  }
  slide.addText(text, { x: 0.55, y: 0.63, w: 8.3, h: 0.42, fontFace: "Arial", fontSize: 22, bold: true, color: C.ink, margin: 0 });
}

function footer(slide, n) {
  slide.addText(String(n).padStart(2, "0"), { x: 12.33, y: 7.08, w: 0.45, h: 0.2, fontSize: 8, bold: true, color: C.white, align: "right", margin: 0 });
}

function bulletList(slide, items, x, y, w, h, fontSize = 16) {
  slide.addText(items.map(t => ({ text: t, options: { bullet: { type: "ul" } } })), {
    x, y, w, h, fontFace: "Arial", fontSize, color: C.ink,
    fit: "shrink", breakLine: false,
    paraSpaceAfterPt: 10, margin: 0.06
  });
}

function pill(slide, text, x, y, w, color) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.38, rectRadius: 0.08, fill: { color }, line: { color } });
  slide.addText(text, { x, y: y + 0.08, w, h: 0.14, fontSize: 8.5, bold: true, color: C.dark, align: "center", margin: 0 });
}

function card(slide, heading, body, x, y, w, h, accent = C.teal) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.04, fill: { color: C.panel }, line: { color: C.line, width: 0.8 } });
  slide.addShape(pptx.ShapeType.rect, { x, y, w: 0.08, h, fill: { color: accent }, line: { color: accent } });
  slide.addText(heading, { x: x + 0.25, y: y + 0.22, w: w - 0.45, h: 0.3, fontSize: 13.5, bold: true, color: C.ink, margin: 0 });
  slide.addText(body, { x: x + 0.25, y: y + 0.63, w: w - 0.45, h: h - 0.8, fontSize: 11.8, color: C.muted, fit: "shrink", margin: 0, breakLine: false });
}

function node(slide, text, x, y, w, h, fill, stroke = C.teal) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { color: stroke, width: 1.2 } });
  slide.addText(text, { x, y: y + h / 2 - 0.09, w, h: 0.2, fontSize: 10.5, bold: true, color: C.dark, align: "center", margin: 0, fit: "shrink" });
}

function conn(slide, x1, y1, x2, y2) {
  slide.addShape(pptx.ShapeType.line, { x: x1, y: y1, w: x2 - x1, h: y2 - y1, line: { color: C.line, width: 1.2, beginArrowType: "none", endArrowType: "triangle" } });
}

function slide1() {
  const s = pptx.addSlide(); addBg(s);
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 4.1, h: 7.5, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText("決策樹的\n建立流程", { x: 0.75, y: 1.34, w: 3.05, h: 1.55, fontSize: 31, bold: true, color: C.white, fit: "shrink", margin: 0, breakLine: false });
  s.addText("從訓練資料到分類葉節點", { x: 0.78, y: 3.17, w: 2.8, h: 0.32, fontSize: 12.5, color: "D1D5DB", margin: 0 });
  pill(s, "根節點", 5.08, 1.34, 1.28, C.paleTeal);
  pill(s, "特徵切分", 6.78, 1.34, 1.28, C.paleBlue);
  pill(s, "純度提升", 8.48, 1.34, 1.28, C.paleCoral);
  pill(s, "停止條件", 10.18, 1.34, 1.28, "FEF3C7");
  s.addText("核心問題：每一步要選哪個特徵切分，並在什麼時候停止？", { x: 5.05, y: 2.34, w: 6.4, h: 0.72, fontSize: 23, bold: true, color: C.ink, fit: "shrink", margin: 0 });
  bulletList(s, ["以貓狗分類為例，從 10 筆訓練樣本開始。", "每個節點嘗試把資料分成更純的子集合。", "當節點已足夠純，或繼續切分不划算時，就形成葉節點。"], 5.1, 3.42, 6.5, 1.5, 15);
  footer(s, 1);
}

function slide2() {
  const s = pptx.addSlide(); addBg(s); title(s, "建構決策樹的三個動作", "流程總覽");
  card(s, "1. 選擇根節點特徵", "先決定最上層用哪個特徵切分，例如耳朵形狀。", 0.75, 1.55, 3.7, 1.35, C.teal);
  card(s, "2. 依特徵值分成子集合", "把訓練樣本分到左右分支，例如尖耳朵與垂耳朵。", 4.85, 1.55, 3.7, 1.35, C.blue);
  card(s, "3. 對各分支重複", "若子集合仍混有不同類別，就繼續選特徵並切分。", 8.95, 1.55, 3.7, 1.35, C.coral);
  node(s, "訓練資料", 1.2, 4.05, 1.55, 0.55, C.white, C.line);
  node(s, "選特徵", 3.25, 4.05, 1.55, 0.55, C.paleTeal);
  node(s, "切分資料", 5.3, 4.05, 1.55, 0.55, C.paleBlue);
  node(s, "檢查純度", 7.35, 4.05, 1.55, 0.55, C.paleCoral);
  node(s, "葉節點或再切分", 9.4, 4.05, 2.1, 0.55, "FEF3C7", C.amber);
  conn(s, 2.75, 4.32, 3.25, 4.32); conn(s, 4.8, 4.32, 5.3, 4.32); conn(s, 6.85, 4.32, 7.35, 4.32); conn(s, 8.9, 4.32, 9.4, 4.32);
  s.addText("決策樹不是一次完成，而是在每個節點反覆回答同一組問題。", { x: 1.35, y: 5.62, w: 10.7, h: 0.42, fontSize: 17, bold: true, color: C.ink, align: "center", margin: 0 });
  footer(s, 2);
}

function slide3() {
  const s = pptx.addSlide(); addBg(s); title(s, "範例：用耳朵形狀作為根節點", "貓狗分類");
  node(s, "根節點\n耳朵形狀？", 5.4, 1.35, 2.3, 0.85, C.paleTeal);
  node(s, "尖耳朵\n5 筆樣本", 2.05, 3.0, 2.15, 0.72, C.white, C.teal);
  node(s, "垂耳朵\n5 筆樣本", 8.9, 3.0, 2.15, 0.72, C.white, C.teal);
  conn(s, 6.1, 2.2, 3.15, 3.0); conn(s, 7.0, 2.2, 10.0, 3.0);
  s.addText("左分支：接著用臉部形狀切分", { x: 1.35, y: 4.42, w: 4.1, h: 0.28, fontSize: 13.5, bold: true, color: C.ink, margin: 0 });
  bulletList(s, ["圓臉：4/4 是貓，形成「預測貓」葉節點。", "非圓臉：0/1 是貓，形成「預測不是貓」葉節點。"], 1.35, 4.85, 4.55, 1.0, 12.5);
  s.addText("右分支：接著用鬍鬚有無切分", { x: 7.4, y: 4.42, w: 4.1, h: 0.28, fontSize: 13.5, bold: true, color: C.ink, margin: 0 });
  bulletList(s, ["有鬍鬚：1/1 是貓，形成「預測貓」葉節點。", "無鬍鬚：0/4 是貓，形成「預測不是貓」葉節點。"], 7.4, 4.85, 4.55, 1.0, 12.5);
  footer(s, 3);
}

function slide4() {
  const s = pptx.addSlide(); addBg(s); title(s, "關鍵決策一：每個節點要選哪個特徵？", "切分標準");
  s.addText("好的特徵能讓左右子集合更接近「全是同一類」。", { x: 0.75, y: 1.3, w: 7.6, h: 0.32, fontSize: 16, bold: true, color: C.ink, margin: 0 });
  card(s, "耳朵形狀", "尖耳朵與垂耳朵切開後，兩側純度有改善。", 0.85, 2.12, 3.35, 1.35, C.teal);
  card(s, "臉部形狀", "可在左分支進一步把貓與狗分得更清楚。", 4.95, 2.12, 3.35, 1.35, C.blue);
  card(s, "鬍鬚有無", "可在右分支取得純度很高的子節點。", 9.05, 2.12, 3.35, 1.35, C.coral);
  s.addShape(pptx.ShapeType.roundRect, { x: 1.35, y: 4.5, w: 10.65, h: 1.2, rectRadius: 0.04, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText("選特徵的目標：最大化純度提升，也就是讓分類預測更容易做對。", { x: 1.75, y: 4.9, w: 9.85, h: 0.36, fontSize: 18, bold: true, color: C.white, align: "center", margin: 0, fit: "shrink" });
  footer(s, 4);
}

function slide5() {
  const s = pptx.addSlide(); addBg(s); title(s, "純度與雜質：決策樹的核心直覺", "概念理解");
  s.addText("純度高", { x: 1.1, y: 1.55, w: 2.2, h: 0.28, fontSize: 15, bold: true, color: C.teal, align: "center", margin: 0 });
  s.addText("純度低", { x: 5.55, y: 1.55, w: 2.2, h: 0.28, fontSize: 15, bold: true, color: C.coral, align: "center", margin: 0 });
  s.addText("理想切分", { x: 9.9, y: 1.55, w: 2.2, h: 0.28, fontSize: 15, bold: true, color: C.blue, align: "center", margin: 0 });
  card(s, "單一類別", "節點中幾乎全是貓，或幾乎全是狗。可以很自然地建立葉節點。", 0.85, 2.0, 3.3, 2.0, C.teal);
  card(s, "類別混雜", "節點中貓狗比例接近，預測不確定性高，需要繼續找特徵切分。", 5.0, 2.0, 3.3, 2.0, C.coral);
  card(s, "降低雜質", "下一步會用熵等指標衡量雜質，並選出能讓雜質下降最多的切分。", 9.15, 2.0, 3.3, 2.0, C.blue);
  s.addText("如果有「是否具備貓的 DNA」這種完美特徵，根節點就能一次把貓與非貓分乾淨；現實中通常只能在可用特徵中找最佳近似。", { x: 1.0, y: 5.25, w: 11.3, h: 0.55, fontSize: 14.2, color: C.ink, align: "center", fit: "shrink", margin: 0 });
  footer(s, 5);
}

function slide6() {
  const s = pptx.addSlide(); addBg(s); title(s, "關鍵決策二：什麼時候停止切分？", "停止條件");
  card(s, "節點已經純淨", "若樣本 100% 屬於同一類，就直接建立葉節點。", 0.75, 1.45, 3.8, 1.2, C.teal);
  card(s, "達到最大深度", "限制樹的層數，避免模型過大、規則過碎。", 4.78, 1.45, 3.8, 1.2, C.blue);
  card(s, "純度提升太小", "若切分帶來的改善低於門檻，就不值得繼續拆。", 8.82, 1.45, 3.8, 1.2, C.coral);
  card(s, "樣本數太少", "若節點樣本低於設定門檻，繼續切分容易只記住個別案例。", 2.35, 3.45, 3.8, 1.2, C.amber);
  card(s, "形成葉節點", "停止後以該節點中的多數類別作為預測結果。", 7.25, 3.45, 3.8, 1.2, C.teal);
  s.addText("停止切分的設計，是在準確度、模型大小與泛化能力之間取得平衡。", { x: 1.2, y: 5.8, w: 10.9, h: 0.35, fontSize: 17, bold: true, color: C.ink, align: "center", margin: 0 });
  footer(s, 6);
}

function slide7() {
  const s = pptx.addSlide(); addBg(s); title(s, "為什麼要限制樹的大小？", "避免過度擬合");
  s.addShape(pptx.ShapeType.rect, { x: 0.85, y: 1.45, w: 5.5, h: 4.8, fill: { color: C.panel }, line: { color: C.line } });
  s.addText("樹太深", { x: 1.2, y: 1.85, w: 1.8, h: 0.28, fontSize: 17, bold: true, color: C.coral, margin: 0 });
  bulletList(s, ["規則變得龐大而難懂。", "可能把訓練資料中的偶然細節也學進去。", "在新資料上的表現反而下降。"], 1.25, 2.45, 4.35, 1.7, 14);
  s.addShape(pptx.ShapeType.rect, { x: 6.95, y: 1.45, w: 5.5, h: 4.8, fill: { color: C.panel }, line: { color: C.line } });
  s.addText("控制方式", { x: 7.3, y: 1.85, w: 1.8, h: 0.28, fontSize: 17, bold: true, color: C.teal, margin: 0 });
  bulletList(s, ["設定最大深度。", "設定最小樣本數。", "要求切分必須帶來足夠的純度提升。"], 7.35, 2.45, 4.45, 1.7, 14);
  s.addText("小一點的樹通常更穩定，也更容易解釋。", { x: 3.2, y: 6.55, w: 7.0, h: 0.28, fontSize: 15.5, bold: true, color: C.ink, align: "center", margin: 0 });
  footer(s, 7);
}

function slide8() {
  const s = pptx.addSlide(); addBg(s); title(s, "重點回顧", "Takeaways");
  bulletList(s, [
    "決策樹從根節點開始，逐步用特徵把資料切成子集合。",
    "每次切分都希望提高純度，讓節點更接近單一類別。",
    "純度與雜質可用熵等指標衡量，並用來選擇最佳特徵。",
    "停止切分的條件包含：節點純淨、達最大深度、提升太小、樣本太少。",
    "限制樹的大小能降低過度擬合，讓模型更容易泛化。"
  ], 1.05, 1.45, 8.3, 3.75, 15);
  s.addShape(pptx.ShapeType.roundRect, { x: 9.75, y: 1.55, w: 2.55, h: 3.95, rectRadius: 0.04, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText("下一步", { x: 10.2, y: 2.0, w: 1.65, h: 0.3, fontSize: 17, bold: true, color: C.white, align: "center", margin: 0 });
  s.addText("理解「熵」如何量化雜質，並計算哪個特徵最值得切分。", { x: 10.08, y: 2.65, w: 1.95, h: 1.45, fontSize: 14, color: "E5E7EB", align: "center", fit: "shrink", margin: 0.05 });
  footer(s, 8);
}

[slide1, slide2, slide3, slide4, slide5, slide6, slide7, slide8].forEach(fn => fn());

pptx.writeFile({ fileName: "generated/decision-tree-transcript-summary.pptx" });
