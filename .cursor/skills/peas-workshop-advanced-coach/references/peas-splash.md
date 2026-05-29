# PEAS 開場品牌畫面（Workshop Bridge Coach）

供 `peas-workshop-advanced-coach` 在新工作階段第一則學生可見訊息頂端使用。

輸出順序：

1. 一行純文字字標：`PEAS · Workshop 進階教練`
2. 空一行
3. 下方「對話用版面」作為單一 `text` fenced code block
4. 同一則訊息最後加一個準備確認問句

首則訊息不得包含進度列、題目、掃描結果或實作內容。

## 對話用版面

```text
┌─────────────────────────────────────────────────────────────┬──────────────────────────┐
│                                                             │                          │
│      /|     PEAS Workshop Bridge · WG-13～22                │Tips for getting started  │
│     / |     Session: 本輪教練剛開始                         │先掃描目前進度，          │
│    /  |     Mode: Scan → Route → Card → Verify              │每次只處理一題。          │
│   /   |                                                     │                          │
│    \  |                                                     │Recent activity           │
│     \ |                                                     │等待你說準備好了          │
│      \|                                                     │                          │
│                                                             │                          │
│  ~/your/project/root/path…                                  │                          │
│                                                             │                          │
└─────────────────────────────────────────────────────────────┴──────────────────────────┘
```

## 缺檔 fallback

若本檔無法讀取，仍輸出簡化版：

```text
PEAS · Workshop 進階教練

┌──────────────────────────────┐
│  PEAS Workshop Bridge        │
│  Scan → Route → Card         │
└──────────────────────────────┘
```
