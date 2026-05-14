"""One-off script: main.py -> main_colab.ipynb for Google Colab."""
from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    repo = Path(__file__).resolve().parent
    src_text = (repo / "main.py").read_text(encoding="utf-8")

    old = "ROOT = Path(__file__).resolve().parent\nWORKSPACE = ROOT"
    new = (
        "# Colab：notebook 中通常無 __file__；可設環境變數 SMALL_AGENT_ROOT 指向專案根目錄\n"
        "try:\n"
        "    _ROOT_BASE = Path(__file__).resolve().parent\n"
        "except NameError:\n"
        "    import os as _os\n"
        "    _ROOT_BASE = Path(_os.environ.get(\"SMALL_AGENT_ROOT\", \"/content/small_agent\")).resolve()\n"
        "ROOT = _ROOT_BASE\n"
        "WORKSPACE = ROOT"
    )
    if old not in src_text:
        raise SystemExit("expected ROOT block not found in main.py")
    src_text = src_text.replace(old, new, 1)

    marker = '\n\nif __name__ == "__main__":\n    main()\n'
    if marker not in src_text:
        raise SystemExit("expected __main__ block not found in main.py")
    src_text = src_text.replace(marker, "\n", 1)

    nb: dict = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": [],
    }

    def add_md(s: str) -> None:
        nb["cells"].append(
            {"cell_type": "markdown", "metadata": {}, "source": s.splitlines(keepends=True)}
        )

    def add_code(s: str) -> None:
        nb["cells"].append(
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": s.splitlines(keepends=True),
            }
        )

    add_md(
        """# small_agent：`main.py`（Colab）

本筆記本由倉庫 `main.py` 轉出，行為與本機執行 `python main.py` 對齊（ReAct、JSONL、`memory/`、Skills 等）。

## 使用前準備

1. **專案目錄**：將整個 `small_agent` 專案上傳到 Colab 的 `/content/small_agent`（左側檔案面板上傳 zip 後解壓並改名），或自行 clone；必要時在「環境」儲存格設定 `os.environ["SMALL_AGENT_ROOT"] = "/你的/路徑"`。
2. **API 金鑰**：在 Colab「祕鑰」新增 `OPENAI_API_KEY`，或於「環境」儲存格 `os.environ["OPENAI_API_KEY"] = "sk-..."`。
3. **Python 版本**：本倉 `pyproject.toml` 標 `>=3.12`；Colab 若為 3.10/3.11 多數仍可執行，若套件不相容請改用支援 3.12 的執行階段。

## 執行順序

由上而下執行；**互動**：最後一格啟動後，在輸出框依提示輸入，輸入 `quit` / `exit` / `q` 結束。
"""
    )

    add_code(
        """# 安裝相依（Colab 每次新執行階段建議重跑）
%pip install -q "python-dotenv>=1.2.2" "langchain-openai>=1.1.13"
"""
    )

    add_code(
        """# 可選：從 Colab「祕鑰」讀取 OPENAI_API_KEY（若已在 UI 建立同名祕鑰）
try:
    from google.colab import userdata
    import os

    k = userdata.get("OPENAI_API_KEY")
    if k and not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = k
        print("已從 Colab userdata 設定 OPENAI_API_KEY")
except Exception as e:
    print("略過 userdata（非 Colab 或未設定祕鑰）：", type(e).__name__)
"""
    )

    add_code(
        """# 可選：指定專案根（預設 /content/small_agent）
import os
from pathlib import Path

# 若專案不在預設路徑，取消註解並改成你的路徑：
# os.environ["SMALL_AGENT_ROOT"] = "/content/small_agent"

p = Path(os.environ.get("SMALL_AGENT_ROOT", "/content/small_agent"))
print("SMALL_AGENT_ROOT ->", p.resolve())
print("存在：", p.is_dir())
if p.is_dir():
    print("內容預覽：", [x.name for x in list(p.iterdir())[:15]])
"""
    )

    add_code(src_text + "\n# 啟動互動迴圈\nmain()\n")

    out = repo / "main_colab.ipynb"
    out.write_text(json.dumps(nb, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Wrote", out, "chars:", len(src_text))


if __name__ == "__main__":
    main()
