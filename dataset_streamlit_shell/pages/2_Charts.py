from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataset_streamlit_shell.data_ui import (
    inject_style,
    load_dataset,
    render_chat_panel,
    render_dataset_metrics,
)


st.set_page_config(page_title="CSV Charts", page_icon="CH", layout="wide")
inject_style()


def _numeric_columns(df: pd.DataFrame) -> list[str]:
    return [str(column) for column in df.select_dtypes(include="number").columns]


def _categorical_columns(df: pd.DataFrame) -> list[str]:
    columns: list[str] = []
    for column in df.columns:
        series = df[column]
        if pd.api.types.is_numeric_dtype(series):
            continue
        if series.nunique(dropna=True) <= 50:
            columns.append(str(column))
    return columns


main, side = st.columns([5, 3], gap="large")

with main:
    st.title("Charts")
    st.caption("用泛用圖表快速建立資料直覺，再請右側 Agent 幫你驗證觀察。")

    df = load_dataset()
    if df is None:
        st.info("請先到 Database 頁上傳 CSV。")
    else:
        render_dataset_metrics(df)

        numeric_cols = _numeric_columns(df)
        categorical_cols = _categorical_columns(df)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("##### Numeric Distribution")
            if numeric_cols:
                selected_numeric = st.selectbox("numeric column", numeric_cols)
                values = pd.to_numeric(df[selected_numeric], errors="coerce").dropna()
                if values.empty:
                    st.info("這個欄位沒有可繪製的數值。")
                else:
                    st.bar_chart(values.value_counts(bins=20).sort_index())
            else:
                st.info("目前資料沒有數值欄位。")

        with c2:
            st.markdown("##### Category Counts")
            if categorical_cols:
                selected_category = st.selectbox("category column", categorical_cols)
                counts = (
                    df[selected_category]
                    .fillna("Unknown")
                    .astype(str)
                    .value_counts()
                    .head(20)
                )
                st.bar_chart(counts)
            else:
                st.info("目前資料沒有適合直接統計的類別欄位。")

        st.markdown("##### Suggested Questions")
        st.markdown(
            """
- 這份資料有哪些欄位缺失值最多？
- 哪些數值欄位看起來有離群值？
- 幫我根據目前篩選結果新增一個計算欄位，並寫回 filtered CSV。
"""
        )

with side:
    render_chat_panel()
