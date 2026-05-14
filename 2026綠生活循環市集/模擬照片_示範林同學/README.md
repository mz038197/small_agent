# 模擬活動照片（示範：林同學）

本資料夾為 **課程／工作坊示範用**，模擬某位學生在「2026 綠生活循環市集」中的 **過程與成果** 影像素材。**目前四張 PNG 為 Codex CLI `imagegen` 產出**（透過 Cursor 同捆腳本 `codex-imagegen`／`generate-image.ps1`），**非真實校園攝影**；課堂上請再說明：真實繳交須使用本人拍攝且已檢查個資之照片。

## 如何以 `/codex-imagegen` 重產（教師或進階學生）

1. 確認已安裝並登入 Codex CLI：`npm i -g @openai/codex`、`codex login`。
2. 中文 prompt 已放在專案 `.cursor/tmp/`：
  - `codex-img-01-secondhand.txt` → `01_整理二手物資.png`
  - `codex-img-02-line.txt` → `02_攤位動線引導.png`
  - `codex-img-03-recycle.txt` → `03_場復分類回收.png`
  - `codex-img-04-booth.txt` → `04_攤位布置成果.png`
3. 在專案根目錄於 PowerShell 執行（範例為第一張；其餘請改 `-PromptFile` 與 `-OutputPath`）：

```powershell
$gen = Join-Path $env:USERPROFILE '.cursor/skills/codex-imagegen/scripts/generate-image.ps1'
& $gen `
  -PromptFile ".cursor/tmp/codex-img-01-secondhand.txt" `
  -OutputPath "2026綠生活循環市集/模擬照片_示範林同學/01_整理二手物資.png" `
  -Cwd (Get-Location) `
  -AspectRatio "4:3" `
  -Style "自然光、校園活動紀實、無可辨識臉孔、無個資"
```

重產前若目標檔已存在，Codex 端有時會另存 `-v2`；若要腳本一定回傳成功，可先刪除或改名舊檔再執行。

**檔案大小**：單張約 2MB 上下，若四張同時嵌入一份心得 PDF，請依 `03_圖片素材與個資規範.md` 自行壓縮長邊（建議 ≤1600px）以控制總檔案在 4MB 內。

## 檔案一覽


| 檔名              | 類型    | 說明        |
| --------------- | ----- | --------- |
| `01_整理二手物資.png` | 過程    | 物資整理、背影示意 |
| `02_攤位動線引導.png` | 過程    | 攤位前動線與引導  |
| `03_場復分類回收.png` | 過程    | 回收分類與場復   |
| `04_攤位布置成果.png` | 成果／證明 | 完成後的攤位布置  |


圖說範例（每則 25～40 字）見 `圖說範例_林同學.md`。

## 與 `03_圖片素材與個資規範.md` 的對應

- **張數**：4 張，介於規定的 3～5 張之間。
- **過程／成果**：過程至少 2 張（01～03 皆為過程情境）、成果至少 1 張（04）。
- **個資與肖像**：畫面為 **插畫式示意**，人物為 **背影／無可辨識臉孔**，無學生證、姓名貼、QR Code、聊天截圖等。
- **解析度**：1200×900，長邊 **未超過 1600px**，便於壓入 PDF 並控制檔案大小。

## 備用：程式示意圖（非 Codex）

若環境無 Codex，可用本資料夾內 `generate_simulated_photos.py`（Pillow 插畫風）產生占位圖；**與目前 Codex 產出的寫實風格不同**。

```powershell
py .\generate_simulated_photos.py
```

