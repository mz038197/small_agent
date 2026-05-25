from __future__ import annotations

import csv
import io
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DEFAULT_CSV = BASE_DIR / "train.csv"

app = FastAPI(title="train.csv 檢視器")
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    rows, filename, message = load_default_csv()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "rows": rows,
            "filename": filename,
            "message": message,
        },
    )


@app.post("/upload")
async def upload_csv(request: Request, file: UploadFile = File(...)):
    data = await file.read()
    rows, filename, message = parse_csv_bytes(data, file.filename or "uploaded.csv")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "rows": rows,
            "filename": filename,
            "message": message,
        },
    )


def load_default_csv():
    if not DEFAULT_CSV.exists():
        return [], "train.csv", "找不到 train.csv，請先上傳檔案。"
    return parse_csv_text(DEFAULT_CSV.read_text(encoding="utf-8-sig"), DEFAULT_CSV.name)


def parse_csv_bytes(data: bytes, filename: str):
    text = data.decode("utf-8-sig", errors="replace")
    return parse_csv_text(text, filename)


def parse_csv_text(text: str, filename: str):
    reader = csv.reader(io.StringIO(text))
    rows = [row for row in reader if any(cell.strip() for cell in row)]
    if not rows:
        return [], filename, f"{filename} 內容是空的。"

    header = rows[0]
    data_rows = []
    for row in rows[1:]:
        cells = list(row)
        if len(cells) < len(header):
            cells.extend([""] * (len(header) - len(cells)))
        elif len(cells) > len(header):
            cells = cells[:len(header)]
        data_rows.append(cells)

    return [header] + data_rows, filename, f"{filename}：{len(data_rows)} 筆資料，{len(header)} 欄"
