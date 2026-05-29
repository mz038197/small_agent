from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from dataset_streamlit_shell.data_ui import (
    ANALYSIS_READY_PATH,
    CLEANING_LOG_PATH,
    FILTERED_DATASET_PATH,
    _display_path,
    append_cleaning_log,
    create_analysis_dataset,
    load_analysis_dataset,
    load_cleaning_log,
    load_working_dataset,
    refresh_working_dataset_cache,
    render_chat_panel,
    render_dataset_metrics,
    reset_working_dataset_from_source,
)


PromptList = list[str]


def _page_shell(title: str, caption: str, render_main: Callable[[pd.DataFrame], None]) -> None:
    main, side = st.columns([5, 3], gap="large")
    with main:
        st.title(title)
        st.caption(caption)
        st.info(
            f"目前整理基準：`{_display_path(FILTERED_DATASET_PATH)}`。"
            "左側負責診斷與驗證；需要修改資料時，請在右側請 Agent 協作。"
        )
        df = load_working_dataset()
        if df is None:
            st.warning("尚未建立工作資料。請先到「資料上傳與預覽」上傳 CSV。")
            return
        _render_refresh_controls()
        render_main(df)
        _render_recent_log()
    with side:
        render_chat_panel()


def _render_refresh_controls() -> None:
    refresh_col, reset_col = st.columns(2)
    if refresh_col.button("重新讀取工作資料", use_container_width=True):
        refresh_working_dataset_cache()
        st.rerun()
    if reset_col.button("回到原始資料", use_container_width=True):
        if reset_working_dataset_from_source():
            st.success("已用原始資料重建工作資料。")
            st.rerun()
        else:
            st.error("找不到原始資料，無法重置。")


def _render_prompts(prompts: PromptList) -> None:
    st.markdown("##### 建議問 Agent")
    st.caption("學生可以自然提問；系統規則會讓 Agent 預設修改工作資料並保護原始資料。")
    for prompt in prompts:
        st.code(prompt, language="text")


def _render_recent_log() -> None:
    with st.expander("最近整理紀錄", expanded=False):
        entries = load_cleaning_log()
        if not entries:
            st.caption(f"尚無紀錄。Agent 修改資料後可寫入 `{_display_path(CLEANING_LOG_PATH)}`。")
            return
        for entry in entries:
            created_at = _format_log_time(str(entry.get("created_at", "")))
            actor = _actor_label(str(entry.get("actor", "")))
            note = str(entry.get("note", ""))
            action = _action_label(str(entry.get("action", "")), note)
            columns = _summarize_columns(entry.get("columns", []))
            rows = entry.get("rows")
            st.markdown(f"**{created_at} · {actor} · {action}**")
            detail = []
            if columns:
                detail.append(f"欄位：{', '.join(str(c) for c in columns)}")
            if rows is not None:
                detail.append(f"筆數：{rows}")
            if note:
                detail.append(note)
            if detail:
                st.caption("；".join(detail))


def _format_log_time(value: str) -> str:
    if not value:
        return "時間不明"
    try:
        return datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return value


def _actor_label(value: str) -> str:
    labels = {"agent": "Agent", "ui": "UI"}
    return labels.get(value.lower(), value or "來源不明")


def _action_label(value: str, note: str = "") -> str:
    labels = {
        "rename_columns_traditional_chinese": "欄位改成繁體中文",
        "rename_columns_to_traditional_chinese": "欄位改成繁體中文",
        "reset_working_dataset": "重置工作資料",
        "create_analysis_dataset": "建立分析資料集",
        "remove_duplicate_rows": "刪除重複資料列",
        "drop_duplicate_rows": "刪除重複資料列",
        "fill_missing_values": "處理缺失值",
        "fill_missing_age": "補齊年齡空值",
        "handle_outliers": "處理離群值",
        "drop_columns": "刪除欄位",
        "encode_categorical_columns": "類別欄位編碼",
    }
    normalized = value.strip().lower()
    if normalized in labels:
        return labels[normalized]
    if note:
        return "整理工作資料"
    return "未命名整理"


def _summarize_columns(value: object, *, max_items: int = 4) -> list[str]:
    if not isinstance(value, list):
        return []
    columns = [str(column) for column in value]
    if len(columns) <= max_items:
        return columns
    remaining = len(columns) - max_items
    return columns[:max_items] + [f"+ {remaining} 個"]


def render_quality_page() -> None:
    def body(df: pd.DataFrame) -> None:
        render_dataset_metrics(df)
        st.markdown("##### 診斷：欄位與資料概覽")
        c1, c2, c3 = st.columns(3)
        c1.metric("重複列", f"{int(df.duplicated().sum()):,}")
        c2.metric("缺失儲存格", f"{int(df.isna().sum().sum()):,}")
        c3.metric("物件/文字欄位", f"{len(df.select_dtypes(include=['object', 'string']).columns):,}")
        overview = pd.DataFrame(
            {
                "資料型態": [str(df[column].dtype) for column in df.columns],
                "非空值筆數": df.notna().sum(),
                "空值筆數": df.isna().sum(),
                "不同值數量": df.nunique(dropna=True),
            },
            index=df.columns,
        )
        st.dataframe(overview, use_container_width=True)
        with st.expander("資料預覽", expanded=False):
            st.dataframe(df.head(20), use_container_width=True, hide_index=True)
        _render_prompts(
            [
                "請檢查目前工作資料的欄位名稱，並建議哪些欄位需要重新命名。",
                "請檢查目前工作資料的欄位型態是否合理，先不要修改資料。",
                "請把不清楚的欄位名稱改成適合資料分析的名稱，並回報修改前後對照。",
            ]
        )

    _page_shell("欄位與資料概覽", "先看欄位名稱、型態、列數欄數與基本結構。", body)


def render_missing_page() -> None:
    def body(df: pd.DataFrame) -> None:
        missing = df.isna().sum().sort_values(ascending=False)
        missing_frame = pd.DataFrame(
            {
                "空值筆數": missing,
                "空值比例": (missing / max(len(df), 1)).round(4),
                "欄位類型": [_column_kind(df[column]) for column in missing.index],
                "資料型態": [str(df[column].dtype) for column in missing.index],
            }
        )
        st.markdown("##### 診斷：缺失值")
        missing_total = int(df.isna().sum().sum())
        st.metric("缺失儲存格", f"{missing_total:,}")
        if missing_total:
            st.error(
                f"紅燈：目前還有 {missing_total:,} 個缺失儲存格，"
                "建議先請 Agent 處理後再建立分析資料集。"
            )
        else:
            st.success("綠燈：目前沒有缺失儲存格，可以進入下一個整理步驟。")
        st.dataframe(missing_frame, use_container_width=True)
        _render_prompts(
            [
                "請依缺失比例整理目前工作資料的缺失值問題，先不要修改資料。",
                "請建議各欄位缺失值適合刪除、補平均數、中位數、眾數，或另外建立 Unknown 類別。",
                "請依你的建議處理目前工作資料的缺失值，並回報每個欄位修改了幾筆。",
            ]
        )

    _page_shell("缺失值處理", "專心判斷缺失值，不混入離群值或分布探索。", body)


def _column_kind(series: pd.Series) -> str:
    if pd.api.types.is_numeric_dtype(series):
        return "數值"
    return "類別"


def render_duplicates_page() -> None:
    def body(df: pd.DataFrame) -> None:
        st.markdown("##### 診斷：刪除重複資料列")
        st.caption(
            "先定義什麼算重複。未選欄位時，預設每個欄位都相同才算同一筆；"
            "選多個欄位時，必須所有選取欄位都相同，才會歸在同一個重複組別。"
        )
        all_columns = [str(column) for column in df.columns]
        selected_columns = st.multiselect(
            "用哪些欄位判斷重複",
            all_columns,
            default=[],
            placeholder="不選欄位時，使用整列完全相同判斷",
            key="duplicate_rule_columns",
        )
        rule_columns = selected_columns or all_columns
        rule_label = "整列完全相同" if not selected_columns else " + ".join(selected_columns)

        duplicated_mask = df.duplicated(subset=rule_columns, keep=False)
        duplicate_candidates = df.loc[duplicated_mask].copy()
        duplicate_groups = 0
        estimated_delete = 0

        if not duplicate_candidates.empty:
            grouped = duplicate_candidates.groupby(rule_columns, dropna=False, sort=False)
            duplicate_candidates.insert(0, "重複組別", grouped.ngroup() + 1)
            duplicate_candidates.insert(1, "組內序號", grouped.cumcount() + 1)
            duplicate_candidates.insert(
                2,
                "建議處理",
                duplicate_candidates["組內序號"].map(
                    lambda index: "保留第一筆" if index == 1 else "可請 Agent 判斷刪除"
                ),
            )
            duplicate_groups = int(duplicate_candidates["重複組別"].nunique())
            estimated_delete = len(duplicate_candidates) - duplicate_groups

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("總資料列數", f"{len(df):,}")
        c2.metric("重複候選列數", f"{len(duplicate_candidates):,}")
        c3.metric("重複組別數", f"{duplicate_groups:,}")
        c4.metric("預估可刪除筆數", f"{estimated_delete:,}")

        st.markdown("##### 目前重複定義")
        st.write(rule_label)

        if duplicate_candidates.empty:
            st.success("依照目前定義，沒有找到重複資料列。")
        else:
            st.markdown("##### 重複候選預覽")
            st.caption(
                "`重複組別` 相同，代表這些資料依照目前規則被判定為同一組疑似重複資料。"
                "這裡只預覽前 50 筆，真正刪除仍請右側 Agent 執行。"
            )
            st.dataframe(
                duplicate_candidates.head(50),
                use_container_width=True,
                hide_index=True,
            )

        rule_for_prompt = (
            "整列完全相同"
            if not selected_columns
            else "、".join(f"`{column}`" for column in selected_columns)
        )
        _render_prompts(
            [
                f"請依「{rule_for_prompt}」檢查目前工作資料的重複資料列，先不要修改資料，請說明重複候選列數與可能影響。",
                f"請依「{rule_for_prompt}」刪除目前工作資料中的重複資料列，每個重複組別保留第一筆，並回報刪除了幾筆。",
                "請刪除重複資料後，在 cleaning_log.jsonl 追加一筆紀錄，actor 是 agent，action 是 remove_duplicate_rows。",
            ]
        )

    _page_shell("刪除重複資料列", "讓學生先定義重複規則，再請 Agent 刪除重複列。", body)


def render_outliers_page() -> None:
    def body(df: pd.DataFrame) -> None:
        numeric = df.select_dtypes(include="number")
        st.markdown("##### 診斷：離群值")
        if numeric.empty:
            st.warning("目前沒有數值欄位。")
            return

        st.caption(
            "離群值不是固定答案。請先選擇判斷方法，系統才會依照該方法列出可能有離群值的欄位。"
        )
        method = st.selectbox(
            "離群值判斷方法",
            ["請選擇方法", "IQR 法", "Z-score 法"],
            key="outlier_method",
        )
        if method == "請選擇方法":
            st.info("你還沒有定義什麼算離群值，因此系統不會先判斷。")
            return

        if method == "IQR 法":
            outlier_frame = _iqr_outlier_summary(df, numeric)
        else:
            threshold = st.slider("Z-score 閾值", min_value=2.0, max_value=4.0, value=3.0, step=0.1)
            outlier_frame = _zscore_outlier_summary(df, numeric, threshold)

        if outlier_frame.empty:
            st.warning("目前數值欄位沒有足夠資料可檢查離群值。")
            return

        st.markdown("##### 有離群值的欄位")
        st.dataframe(outlier_frame, use_container_width=True, hide_index=True)
        outlier_columns = outlier_frame[outlier_frame["離群值筆數"] > 0]["欄位名稱"].tolist()
        if not outlier_columns:
            st.success("依照目前方法，沒有偵測到離群值欄位。")
            return

        selected = st.selectbox(
            "選擇欄位查看細節",
            ["請選擇欄位"] + outlier_columns,
            key="outlier_detail_column",
        )
        if selected == "請選擇欄位":
            st.info("請選擇一個欄位，查看圖形與離群值資料列。")
            return

        selected_rule = outlier_frame[outlier_frame["欄位名稱"] == selected].iloc[0]
        selected_values = pd.to_numeric(df[selected], errors="coerce")
        if method == "IQR 法":
            outlier_mask = (selected_values < selected_rule["離群值下界"]) | (
                selected_values > selected_rule["離群值上界"]
            )
            _render_iqr_outlier_chart(selected_values, selected)
        else:
            mean = float(selected_rule["平均數"])
            std = float(selected_rule["標準差"])
            threshold_value = float(selected_rule["Z-score 閾值"])
            zscores = (selected_values - mean) / std if std else selected_values * 0
            outlier_mask = zscores.abs() > threshold_value
            _render_zscore_outlier_chart(selected_values, selected, mean, std, threshold_value)

        outlier_rows = df[outlier_mask.fillna(False)]
        st.markdown("##### 離群值資料列預覽")
        st.dataframe(outlier_rows.head(30), use_container_width=True, hide_index=True)
        _render_prompts(
            [
                f"請使用 {method} 檢查目前工作資料的 `{selected}` 欄位離群值，先不要修改資料。",
                f"請針對 `{selected}` 欄位說明這些離群值可能是錯誤資料，還是真實但極端的觀察。",
                f"請依你的判斷處理 `{selected}` 欄位的離群值，並回報修改前後摘要，最後寫入 cleaning_log.jsonl。",
            ]
        )

    _page_shell("離群值檢查", "專心檢查極端數值，避免和缺失值、分布探索混在一起。", body)


def _iqr_outlier_summary(df: pd.DataFrame, numeric: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for column in numeric.columns:
        values = numeric[column].dropna()
        if values.empty:
            continue
        q1 = values.quantile(0.25)
        q3 = values.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = int(((values < lower) | (values > upper)).sum())
        rows.append(
            {
                "欄位名稱": str(column),
                "離群值筆數": outlier_count,
                "離群值比例": round(outlier_count / max(len(df), 1), 4),
                "第一四分位數": q1,
                "第三四分位數": q3,
                "四分位距": iqr,
                "離群值下界": lower,
                "離群值上界": upper,
            }
        )
    return pd.DataFrame(rows).sort_values("離群值筆數", ascending=False)


def _zscore_outlier_summary(
    df: pd.DataFrame,
    numeric: pd.DataFrame,
    threshold: float,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for column in numeric.columns:
        values = numeric[column].dropna()
        if len(values) < 2:
            continue
        mean = float(values.mean())
        std = float(values.std(ddof=0))
        if std == 0:
            outlier_count = 0
        else:
            zscores = (values - mean) / std
            outlier_count = int((zscores.abs() > threshold).sum())
        rows.append(
            {
                "欄位名稱": str(column),
                "離群值筆數": outlier_count,
                "離群值比例": round(outlier_count / max(len(df), 1), 4),
                "平均數": mean,
                "標準差": std,
                "Z-score 閾值": threshold,
            }
        )
    return pd.DataFrame(rows).sort_values("離群值筆數", ascending=False)


def _render_iqr_outlier_chart(values: pd.Series, column: str) -> None:
    fig, ax = plt.subplots(figsize=(8, 2.8), constrained_layout=True)
    ax.boxplot(values.dropna(), vert=False, patch_artist=True)
    ax.set_title(f"{column} 的箱形圖")
    ax.set_xlabel(column)
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)


def _render_zscore_outlier_chart(
    values: pd.Series,
    column: str,
    mean: float,
    std: float,
    threshold: float,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.6), constrained_layout=True)
    clean_values = values.dropna()
    ax.hist(clean_values, bins=24, alpha=0.75)
    lower = mean - threshold * std
    upper = mean + threshold * std
    ax.axvline(lower, color="red", linestyle="--", label="離群值下界")
    ax.axvline(upper, color="red", linestyle="--", label="離群值上界")
    ax.set_title(f"{column} 的 Z-score 分布")
    ax.set_xlabel(column)
    ax.set_ylabel("筆數")
    ax.legend()
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)


def render_numeric_page() -> None:
    render_outliers_page()


def render_categorical_page() -> None:
    def body(df: pd.DataFrame) -> None:
        categorical = df.select_dtypes(include=["object", "string", "category"])
        st.markdown("##### 診斷：類別欄位")
        if categorical.empty:
            st.warning("目前沒有類別欄位。")
            return
        overview = pd.DataFrame(
            {
                "missing_count": categorical.isna().sum(),
                "unique_count": categorical.nunique(dropna=True),
                "top_value": [
                    categorical[column].mode(dropna=True).iloc[0]
                    if not categorical[column].mode(dropna=True).empty
                    else ""
                    for column in categorical.columns
                ],
            }
        )
        st.dataframe(overview, use_container_width=True)
        selected = st.selectbox("查看類別分布", [str(c) for c in categorical.columns])
        counts = df[selected].fillna("Missing").astype(str).value_counts().head(30)
        st.bar_chart(counts)
        _render_prompts(
            [
                "請檢查目前工作資料的類別欄位，列出缺失值與類別數量最多的欄位。",
                f"請分析 `{selected}` 欄位的類別分布，建議是否需要合併稀有類別。",
                f"請把 `{selected}` 欄位的缺失值填成 Other，並回報修改了幾筆。",
            ]
        )

    _page_shell("類別欄位診斷", "檢查類別欄位缺失值、類別分布與稀有類別。", body)


def render_encoding_page() -> None:
    def body(df: pd.DataFrame) -> None:
        st.markdown("##### 診斷：類別欄位編碼")
        categorical = [str(c) for c in df.select_dtypes(include=["object", "string", "category"]).columns]
        if categorical:
            st.markdown("###### 類別欄位")
            overview = pd.DataFrame(
                {
                    "unique_count": df[categorical].nunique(dropna=True),
                    "missing_count": df[categorical].isna().sum(),
                }
            )
            st.dataframe(overview, use_container_width=True)
        else:
            st.caption("目前沒有需要編碼的文字/類別欄位。")
        _render_prompts(
            [
                "請檢查目前工作資料有哪些類別欄位需要編碼，並建議 Label Encoding 或 One-Hot Encoding。",
                "請先不要修改資料，說明哪些欄位適合做 One-Hot Encoding，哪些不適合。",
                "請針對適合的類別欄位新增 One-Hot Encoding 欄位，保留原欄位，並回報新增了哪些欄位。",
            ]
        )

    _page_shell("類別欄位編碼", "把類別欄位轉成後續分析可用的數值表示。", body)


def render_correlation_page() -> None:
    def body(df: pd.DataFrame) -> None:
        st.markdown("##### 診斷：數值相關性")
        numeric = df.select_dtypes(include="number")
        if len(numeric.columns) < 2:
            st.warning("數值欄位少於 2 個，無法計算相關矩陣。")
            return
        corr = numeric.corr(numeric_only=True)
        st.dataframe(corr.style.format("{:.2f}"), use_container_width=True)
        strong_pairs: list[dict[str, object]] = []
        columns = list(corr.columns)
        for left_index, left in enumerate(columns):
            for right in columns[left_index + 1 :]:
                value = corr.loc[left, right]
                if pd.notna(value):
                    strong_pairs.append(
                        {
                            "left": str(left),
                            "right": str(right),
                            "correlation": float(value),
                            "abs_correlation": abs(float(value)),
                        }
                    )
        st.markdown("###### 相關性最高的欄位組")
        if strong_pairs:
            strong_frame = pd.DataFrame(strong_pairs).sort_values("abs_correlation", ascending=False)
            st.dataframe(strong_frame.head(12), use_container_width=True, hide_index=True)
        else:
            st.caption("目前沒有可排序的數值欄位組。")
        _render_prompts(
            [
                "請解讀目前數值欄位的相關性，指出最值得注意的正相關與負相關。",
                "請根據相關矩陣，判斷這份資料是否適合建立分析資料集，先不要修改資料。",
                "請指出哪些欄位可能帶有重複資訊，後續做 PCA 時應該注意什麼。",
            ]
        )

    _page_shell("數值相關性", "在建立分析資料集之前，檢查數值欄位之間的關係。", body)


def render_encoding_correlation_page() -> None:
    render_encoding_page()


def render_analysis_ready_page() -> None:
    def body(df: pd.DataFrame) -> None:
        st.markdown("##### 建立分析資料集")
        st.caption("將目前工作資料另存為穩定的 `analysis_ready.csv`，供 Wald / PCA 使用。")
        missing_total = int(df.isna().sum().sum())
        object_cols = len(df.select_dtypes(include=["object", "string", "category"]).columns)
        duplicate_rows = int(df.duplicated().sum())
        numeric_cols = len(df.select_dtypes(include="number").columns)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("列數", f"{len(df):,}")
        c2.metric("數值欄位", f"{numeric_cols:,}")
        c3.metric("缺失儲存格", f"{missing_total:,}")
        c4.metric("重複列", f"{duplicate_rows:,}")
        if object_cols:
            st.warning(f"仍有 {object_cols} 個文字/類別欄位。PCA 可能需要先做編碼或只選數值欄位。")
        if missing_total:
            st.warning("仍有缺失值。Wald / PCA 前建議先完成缺失值處理。")
        if st.button("建立 analysis_ready.csv", type="primary", use_container_width=True):
            create_analysis_dataset(df)
            append_cleaning_log(
                action="建立分析資料集",
                columns=df.columns,
                rows=len(df),
                note="由 current_filtered.csv 匯出 analysis_ready.csv。",
                actor="ui",
            )
            st.success(f"已建立 `{_display_path(ANALYSIS_READY_PATH)}`。")
        analysis = load_analysis_dataset()
        if analysis is not None:
            st.markdown("###### 目前分析資料集")
            render_dataset_metrics(analysis)
            st.download_button(
                "下載 analysis_ready.csv",
                data=analysis.to_csv(index=False).encode("utf-8-sig"),
                file_name="analysis_ready.csv",
                mime="text/csv",
                use_container_width=True,
            )
        _render_prompts(
            [
                "請檢查目前工作資料是否適合建立分析資料集，列出還需要整理的問題。",
                "請確認目前工作資料是否還有缺失值、重複列或未編碼欄位，先不要修改資料。",
                "請建議建立分析資料集前還需要完成哪些整理步驟。",
            ]
        )

    _page_shell("建立分析資料集", "把整理工作資料轉成後續分析使用的穩定資料表。", body)


def wald_status(df: pd.DataFrame) -> dict[str, object]:
    numeric = df.select_dtypes(include="number")
    binary_columns = [
        str(column)
        for column in df.columns
        if df[column].dropna().nunique() == 2
    ]
    return {
        "rows": len(df),
        "numeric_columns": len(numeric.columns),
        "missing_cells": int(df.isna().sum().sum()),
        "binary_columns": binary_columns,
    }


def pca_status(df: pd.DataFrame) -> dict[str, object]:
    numeric = df.select_dtypes(include="number")
    return {
        "rows": len(df),
        "numeric_columns": len(numeric.columns),
        "missing_cells": int(numeric.isna().sum().sum()) if not numeric.empty else 0,
        "enough_columns": len(numeric.columns) >= 2,
        "enough_rows": len(df) >= 3,
    }


def render_analysis_shell(title: str, caption: str, render_main: Callable[[pd.DataFrame], None]) -> None:
    main, side = st.columns([5, 3], gap="large")
    with main:
        st.title(title)
        st.caption(caption)
        st.info(f"目前分析基準：`{_display_path(ANALYSIS_READY_PATH)}`。")
        df = load_analysis_dataset()
        if df is None:
            st.warning("尚未建立分析資料集。請先到「建立分析資料集」頁完成匯出。")
            return
        render_main(df)
    with side:
        render_chat_panel()

