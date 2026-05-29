from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataset_streamlit_shell.data_ui import (
    ANALYSIS_READY_PATH,
    DATASET_PATH,
    FILTERED_DATASET_PATH,
    SHELL_ROOT,
    _display_path,
    inject_style,
    load_analysis_dataset,
    load_dataset,
    load_working_dataset,
    render_chat_panel,
    render_column_pills,
    render_dataset_metrics,
)


st.set_page_config(page_title="CSV Data Agent Shell", page_icon="CSV", layout="wide")
inject_style()


def overview() -> None:
    main, side = st.columns([5, 3], gap="large")

    with main:
        st.title("Dataset Learning Lab")
        st.caption(
            "上傳 CSV，透過 Agent 協作整理工作資料，建立可進入 Wald / PCA 的分析資料集。"
        )

        source_df = load_dataset()
        working_df = load_working_dataset()
        analysis_df = load_analysis_dataset()
        df = working_df if working_df is not None else source_df
        if df is None:
            st.info("請到「資料上傳與預覽」頁上傳 CSV。上傳後會建立原始資料與整理工作資料。")
            return

        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        render_dataset_metrics(df)
        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("##### 資料生命週期")
        st.write("原始資料：上傳後保留，不直接修改。")
        st.write("整理工作資料：Agent 協作整理與診斷的主要工作區。")
        st.write("分析資料集：整理完成後建立，供 Wald / PCA 使用。")
        with st.expander("技術資訊", expanded=False):
            st.caption(f"原始資料檔：`{_display_path(DATASET_PATH)}`")
            st.caption(f"整理工作資料檔：`{_display_path(FILTERED_DATASET_PATH)}`")
            st.caption(f"分析資料集檔：`{_display_path(ANALYSIS_READY_PATH)}`")
        render_column_pills(df.columns)

        if analysis_df is None:
            st.warning("尚未建立分析資料集。完成資料整理後，請到「建立分析資料集」頁產生 `analysis_ready.csv`。")
        else:
            st.success(f"分析資料集已建立：{len(analysis_df):,} 筆、{len(analysis_df.columns):,} 欄。")

        st.markdown("##### 快速預覽")
        st.dataframe(df.head(12), use_container_width=True, hide_index=True)

        st.markdown("##### 課程流程")
        st.markdown(
            """
1. 在「資料上傳與預覽」上傳或更換 CSV。
2. 到「AI 協作整理流程」診斷 `current_filtered.csv`，請右側 Agent 一步一步整理資料。
3. 在「建立分析資料集」產生 `analysis_ready.csv`。
4. Wald / PCA 頁面預設讀取 `analysis_ready.csv`。
"""
        )

    with side:
        render_chat_panel()


pages = {
    "資料工作區": [
        st.Page(overview, title="總覽", default=True),
        st.Page(str(SHELL_ROOT / "pages" / "1_Database.py"), title="資料上傳與預覽"),
        st.Page(str(SHELL_ROOT / "pages" / "2_Charts.py"), title="通用圖表"),
    ],
    "AI 協作整理流程": [
        st.Page(str(SHELL_ROOT / "pages" / "3_Field_Quality.py"), title="欄位與資料概覽"),
        st.Page(str(SHELL_ROOT / "pages" / "4_Duplicates.py"), title="刪除重複資料列"),
        st.Page(str(SHELL_ROOT / "pages" / "5_Numeric_Diagnostics.py"), title="缺失值處理"),
        st.Page(str(SHELL_ROOT / "pages" / "6_Outliers.py"), title="離群值檢查"),
        st.Page(str(SHELL_ROOT / "pages" / "7_Categorical.py"), title="類別欄位整理"),
        st.Page(str(SHELL_ROOT / "pages" / "8_Encoding.py"), title="類別欄位編碼"),
        st.Page(str(SHELL_ROOT / "pages" / "9_Correlation.py"), title="數值相關性"),
        st.Page(str(SHELL_ROOT / "pages" / "8_Analysis_Ready.py"), title="建立分析資料集"),
    ],
    "統計推論": [
        st.Page(str(SHELL_ROOT / "pages" / "9_Wald.py"), title="Wald 法"),
    ],
    "降維分析": [
        st.Page(str(SHELL_ROOT / "pages" / "10_PCA.py"), title="PCA 主成分分析"),
    ],
}

st.navigation(pages).run()
