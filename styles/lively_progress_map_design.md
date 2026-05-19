# 活潑關卡地圖設計規範 (Design.md)

## 1. 視覺概覽

本風格用於**工作坊進度地圖、學習路徑、關卡流程圖**等教學視覺，核心為**活潑關卡感 (Playful Game Map)**：比一般簡報更有生命力，適合國高中／大學生技術課程。

視覺氣質參考：Notion 的清爽、手遊關卡地圖的節奏、兒童科普插畫的友善——**不要**暗沉科技風、**不要** cyberpunk／霓虹夜店感。

**參考成品：** `assets/generated/challenges/wg-basic-progress-map-lively.png`

---

## 2. 色彩系統 (Color Palette)

以明亮淺底為主，節點採糖果色交替，終點單點高亮。

| 角色 | 色碼 | 用途 |
|------|------|------|
| **Background** | `#FFFDF7` | 主背景（純白 `#FFFFFF` 可接受） |
| **Title** | `#1E3A5F` | 主標題（深藍） |
| **Body** | `#374151` | 節點內文、次要說明 |
| **Mint** | `#6EE7B7` | 關卡卡面交替色之一 |
| **Coral** | `#FB923C` | 關卡卡面交替色之一 |
| **Lavender** | `#C4B5FD` | 關卡卡面交替色之一 |
| **Sky** | `#7DD3FC` | 關卡卡面交替色之一 |
| **Path** | `#38BDF8` | 虛線路徑、圓頭箭頭 |
| **Rainbow Line** | 漸層細線 | 標題下方裝飾線 |
| **Finish** | `#FBBF24` | 終點關卡高亮（可加皇冠） |

**禁止：** 深靛青漸層底、isometric 暗色網格、星空粒子、高對比霓虹描邊。

---

## 3. 字體規範 (Typography)

- **Primary Font:** 圓潤無襯線繁中（如 Microsoft JhengHei、Noto Sans TC）
- **Fallback:** System Sans-serif
- **特徵：**
  - 主標題：粗體、置頂置中，字數少
  - 關卡標題：每卡一行短中文，字級大於編號
  - 關卡編號：小字灰色（如 `WG-01`），置於標題下方
  - 避免長段落；節點多時寧可精簡文字也不擠壓

---

## 4. 視覺特徵 (Visual Language)

### 4.1 角色與裝飾

- 角落放置**可愛小機器人吉祥物**（圓潤、揮手、友善）
- 少量**星星、sparkles** 點綴，不搶主體
- 可選起點：**「START!」** 木牌或標籤
- 可選終點：**「完成！」** 對話框、小皇冠

### 4.2 關卡卡面 (Level Cards)

- 形狀：圓角矩形（手遊關卡感）
- 陰影：柔和 drop shadow，輕微浮起
- 結構：**小圖示 → 大字標題 → 小字編號**
- 配色：Mint / Coral / Lavender / Sky **交替**使用
- 終點卡：Finish 色高亮，可強調完成感

### 4.3 路徑與箭頭 (Path)

- 連接方式：彩色**虛線**或**圓點**路徑
- 箭頭：圓頭、略粗、可愛
- 常見版型：
  - **S 形蛇形：** 由下而上，每列左右往返（適合 12～16 關）
  - **分區網格：** 上中下區塊 + pill 區塊標題（適合投影片分章）

### 4.4 標題區 (Hero)

- 主標題置頂、深藍色
- 標題下方一條**細彩虹裝飾線**
- 可選副標（小字、灰色），如 `WG-01 → WG-16`

### 4.5 構圖比例

- 建議：**16:9** 橫幅（投影片、教材圖）
- 留白充足，節點對齊整齊，路徑節奏清楚

---

## 5. Codex 產圖指引

產圖時將本 Design.md 的風格錨點併入 prompt，**情境內容**另填。

```powershell
$gen = Join-Path $env:USERPROFILE '.cursor\skills\codex-imagegen\scripts\generate-image.ps1'
& $gen `
  -PromptFile ".cursor/tmp/codex-prompt-<主題>.txt" `
  -OutputPath "assets/generated/<路徑>.png" `
  -AspectRatio "16:9" `
  -Style "playful colorful game map illustration white background"
```

- **Prompt 範本：** `styles/codex-prompt-progress-map-lively.txt`（僅含情境填空）
- **已填範例：** `styles/examples/codex-prompt-wg01-16-basic-progress.txt`

對 Cursor 可說：「依 `styles/lively_progress_map_design.md` 產圖，情境為 …」

---

## 6. 反模式 (Anti-patterns)

| 避免 | 原因 |
|------|------|
| 深色漸層 + 發光玻璃節點 | 偏 cyberpunk，與本風格不符 |
| 過多英文長句 | 降低學生閱讀友善度 |
| 節點超過 20 且字很小 | Codex 易漏字、重複編號 |
| 寫實照片、複雜透視 | 破壞扁平插畫一致性 |

---

*此文件由工作坊活潑關卡地圖視覺整理產生；參考 `wg-basic-progress-map-lively.png`。*
