# Long-term Memory

## User Information
- 使用者目前在處理 Streamlit 畫面的 Titanic 通用 CSV 資料集。

## Preferences
- 回答資料問題時，需先用 read_file 或 exec 工具實際讀取 CSV 後再回答。
- 若使用者要求補值、計算欄位或新增欄位，應讀取並更新 `dataset_streamlit_shell/data/current_filtered.csv`。
- 不要覆蓋 `dataset_streamlit_shell/data/current.csv`。

## Project Context
- 完整資料路徑：`dataset_streamlit_shell/data/current.csv`
- Agent 工作資料路徑：`dataset_streamlit_shell/data/current_filtered.csv`
- 上傳資料時系統會先建立一份和完整資料相同的工作副本。
- 資料共有 891 筆、12 欄。
- 欄位：`PassengerId`, `Survived`, `Pclass`, `Name`, `Sex`, `Age`, `SibSp`, `Parch`, `Ticket`, `Fare`, `Cabin`, `Embarked`
- 已以實際資料計算：女生存活率為 233 / 314 = 0.7420，約 74.2%。
- 已以實際資料計算：男生存活率為 109 / 577 = 0.1889，約 18.9%。

## Important Notes
- 需要以實際讀檔結果作答，不能只憑記憶推測資料內容。
- `current_filtered.csv` 是可更新的工作檔，`current.csv` 為原始完整資料，不應直接覆寫。