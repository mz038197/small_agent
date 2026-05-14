#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 4 simulated activity photos (illustration style, no identifiable faces)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 900  # long edge 1200 <= 1600
OUT = Path(__file__).parent


def load_font(size: int):
    for p in (
        r"C:\Windows\Fonts\msjh.ttc",
        r"C:\Windows\Fonts\msjhbd.ttc",
        r"C:\Windows\Fonts\mingliu.ttc",
    ):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_person_back(d, x, y, scale=1.0, shirt="#2d6a4f"):
    s = scale
    # body
    d.rounded_rectangle(
        [x - 25 * s, y, x + 25 * s, y + 85 * s],
        radius=8,
        fill=shirt,
        outline="#1b4332",
        width=2,
    )
    # head from back (no face)
    d.ellipse([x - 22 * s, y - 45 * s, x + 22 * s, y + 5 * s], fill="#c9ada7", outline="#6c757d", width=2)
    # hair blob
    d.arc([x - 24 * s, y - 48 * s, x + 24 * s, y + 8 * s], 200, 340, fill="#4a3728", width=int(14 * s))


def draw_bin(d, cx, cy, label_color, icon="recycle"):
    w, h = 70, 95
    d.rounded_rectangle(
        [cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2],
        radius=10,
        fill=label_color,
        outline="#222",
        width=2,
    )
    if icon == "recycle":
        d.polygon(
            [(cx, cy - 25), (cx + 18, cy + 8), (cx - 18, cy + 8)],
            outline="white",
            width=3,
        )


def photo_01_sorting():
    img = Image.new("RGB", (W, H), "#f4f1e8")
    d = ImageDraw.Draw(img)
    # table
    d.rounded_rectangle([80, 420, W - 80, 520], radius=12, fill="#d8d4c8", outline="#9a9590", width=2)
    # boxes
    for i, col in enumerate(["#8fbc8f", "#dda15e", "#bc6c25"]):
        bx = 200 + i * 280
        d.rounded_rectangle([bx, 280, bx + 160, 400], radius=8, fill=col, outline="#333", width=2)
    draw_person_back(d, 420, 350, 1.1, "#2d6a4f")
    draw_person_back(d, 720, 360, 0.95, "#1d3557")
    # hands area - second hand clothes pile
    d.ellipse([350, 440, 480, 500], fill="#e76f51", outline="#333", width=2)
    d.text((100, 60), "綠生活循環市集｜模擬過程照 01", fill="#264653", font=load_font(36))
    d.text((100, 120), "整理二手物資（背影示意，無可辨識臉孔）", fill="#333", font=load_font(24))
    return img


def photo_02_guiding():
    img = Image.new("RGB", (W, H), "#eef6f0")
    d = ImageDraw.Draw(img)
    # floor
    d.rectangle([0, 550, W, H], fill="#c5d4c0")
    # booth sign
    d.rounded_rectangle([400, 120, 800, 280], radius=16, fill="#2a9d8f", outline="#264653", width=3)
    d.text((480, 180), "分類挑戰", fill="white", font=load_font(42))
    # rope line
    for x in range(150, 1050, 80):
        d.ellipse([x, 480, x + 20, 510], fill="#e9c46a", outline="#333", width=2)
    draw_person_back(d, 600, 400, 1.0, "#264653")
    # abstract "crowd" as shapes from back
    for i, ox in enumerate([-120, 120, 200]):
        draw_person_back(d, 600 + ox, 420 + i * 15, 0.75 - i * 0.05, "#457b9d")
    d.text((100, 60), "綠生活循環市集｜模擬過程照 02", fill="#264653", font=load_font(36))
    d.text((100, 120), "攤位動線引導（僅背影與剪影，無正面肖像）", fill="#333", font=load_font(24))
    return img


def photo_03_recycling():
    img = Image.new("RGB", (W, H), "#faf8f3")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 500, W, H], fill="#adb5bd")
    draw_bin(d, 280, 620, "#2d6a4f")
    draw_bin(d, 480, 620, "#457b9d")
    draw_bin(d, 680, 620, "#bc6c25")
    draw_bin(d, 880, 620, "#6c757d")
    draw_person_back(d, 520, 480, 1.05, "#1b4332")
    # bag
    d.rounded_rectangle([470, 520, 540, 580], radius=6, fill="#dda15e", outline="#333", width=2)
    d.text((100, 60), "綠生活循環市集｜模擬過程照 03", fill="#264653", font=load_font(36))
    d.text((100, 120), "場復後分類回收（示意，無學生證或姓名）", fill="#333", font=load_font(24))
    return img


def photo_04_booth_result():
    img = Image.new("RGB", (W, H), "#fff8e7")
    d = ImageDraw.Draw(img)
    # booth backdrop
    d.rounded_rectangle([100, 180, W - 100, 520], radius=20, fill="#95d5b2", outline="#2d6a4f", width=4)
    d.rounded_rectangle([150, 220, W - 150, 320], radius=12, fill="#1b4332")
    d.text((W // 2 - 180, 250), "二手交換 × 減塑", fill="#fefae0", font=load_font(38))
    # table with items
    d.rounded_rectangle([200, 540, 1000, 680], radius=10, fill="#d4a373", outline="#6f4518", width=2)
    for i in range(5):
        d.ellipse([260 + i * 130, 560, 330 + i * 130, 630], fill="#e63946" if i % 2 else "#457b9d", outline="#333")
    draw_person_back(d, 1050, 420, 0.9, "#588157")
    d.text((100, 60), "綠生活循環市集｜模擬成果照 04", fill="#264653", font=load_font(36))
    d.text((100, 120), "完成後的攤位布置（全景示意）", fill="#333", font=load_font(24))
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pairs = [
        ("01_整理二手物資.png", photo_01_sorting),
        ("02_攤位動線引導.png", photo_02_guiding),
        ("03_場復分類回收.png", photo_03_recycling),
        ("04_攤位布置成果.png", photo_04_booth_result),
    ]
    for name, fn in pairs:
        img = fn()
        path = OUT / name
        img.save(path, "PNG", optimize=True)
        print(path, img.size)


if __name__ == "__main__":
    main()
