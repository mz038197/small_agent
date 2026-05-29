from pathlib import Path
import tempfile
import unittest

import pandas as pd

from dataset_streamlit_shell import data_ui
from dataset_streamlit_shell import workflow_ui


class DatasetLifecycleTests(unittest.TestCase):
    def test_dataset_lifecycle_paths_use_original_working_ready_names(self) -> None:
        self.assertEqual(data_ui.ORIGINAL_DATASET_PATH.name, "original.csv")
        self.assertEqual(data_ui.WORKING_DATASET_PATH.name, "working.csv")
        self.assertEqual(data_ui.READY_DATASET_PATH.name, "ready.csv")

    def test_dataset_lifecycle_paths_stay_under_data_directory(self) -> None:
        data_dir = Path(data_ui.DATA_DIR)

        self.assertEqual(data_ui.ORIGINAL_DATASET_PATH.parent, data_dir)
        self.assertEqual(data_ui.WORKING_DATASET_PATH.parent, data_dir)
        self.assertEqual(data_ui.READY_DATASET_PATH.parent, data_dir)

    def test_text_or_category_columns_lists_columns_students_need_to_fix(self) -> None:
        df = pd.DataFrame(
            {
                "Age": [22, 38],
                "Fare": [7.25, 71.28],
                "Name": ["Braund", "Cumings"],
                "Embarked": pd.Series(["S", "C"], dtype="category"),
            }
        )

        self.assertEqual(
            workflow_ui.text_or_category_columns(df),
            ["Name", "Embarked"],
        )

    def test_prepare_dataframe_for_display_stringifies_mixed_object_columns(self) -> None:
        df = pd.DataFrame({"top": ["S", pd.Series([True], dtype="bool").iloc[0]], "count": [2, 3]})

        display_df = data_ui.prepare_dataframe_for_display(df)

        self.assertEqual(display_df["top"].tolist(), ["S", "True"])
        self.assertEqual(display_df["count"].tolist(), [2, 3])

    def test_dataset_context_restricts_agent_script_location(self) -> None:
        df = pd.DataFrame({"Age": [22, 38]})

        context = data_ui.dataset_context(df)

        self.assertIn("dataset_streamlit_shell/scripts/", context)
        self.assertIn("不要在專案根目錄建立臨時 Python 腳本", context)

    def test_load_agent_class_reports_missing_agent_core(self) -> None:
        agent_class, error = data_ui.load_agent_class(Path("missing-project"))

        self.assertIsNone(agent_class)
        self.assertIn("agent_core.py", error or "")

    def test_load_agent_class_requires_agent_symbol(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "agent_core.py").write_text("class NotAgent: ...\n", encoding="utf-8")

            agent_class, error = data_ui.load_agent_class(tmp_path)

        self.assertIsNone(agent_class)
        self.assertIn("Agent", error or "")

    def test_load_agent_class_loads_agent_symbol(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "agent_core.py").write_text("class Agent: ...\n", encoding="utf-8")

            agent_class, error = data_ui.load_agent_class(tmp_path)

        self.assertIsNone(error)
        self.assertIsNotNone(agent_class)
        self.assertEqual(agent_class.__name__, "Agent")

    def test_load_agent_class_supports_dataclass_agent_core(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            (tmp_path / "agent_core.py").write_text(
                "from __future__ import annotations\n"
                "from dataclasses import dataclass\n\n"
                "@dataclass\n"
                "class Config:\n"
                "    name: str\n\n"
                "class Agent:\n"
                "    config: Config | None = None\n",
                encoding="utf-8",
            )

            agent_class, error = data_ui.load_agent_class(tmp_path)

        self.assertIsNone(error)
        self.assertIsNotNone(agent_class)
        self.assertEqual(agent_class.__name__, "Agent")


if __name__ == "__main__":
    unittest.main()
