#!/usr/bin/env python3
"""Render entry.png for make.fun news-image-20261118.

Infographic: Wednesday 18 November 2026 world news, five verified stories.
Deterministic PIL render (fixed fonts, fixed layout, no clock, no random).
Run: python3 draw.py [output_path]  (default: entry.png next to this file)
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (11, 20, 36)
CARD_BG = (20, 33, 58)
CARD_BORDER = (34, 52, 90)
WHITE = (245, 247, 250)
MUTED = (168, 182, 205)
FOOTER = (138, 154, 181)
TITLE = (255, 255, 255)
SUBHEAD = (150, 196, 255)

FONT_DIR = "/usr/share/fonts/truetype/noto"
BOLD = os.path.join(FONT_DIR, "NotoSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "NotoSans-Regular.ttf")

STORIES = [
    ("IRAN STRIKES KUWAIT AND BAHRAIN",
     "Iran struck Ali Al Salem Air Base in Kuwait, home to US forces, and "
     "targets in Bahrain — a day after US warplanes hit an Iranian missile "
     "site on Qeshm Island.",
     (229, 72, 77)),
    ("XI AND PUTIN MEET IN SHENZHEN",
     "Xi Jinping and Vladimir Putin met in Shenzhen on the sidelines of the "
     "APEC summit, ahead of a trilateral meeting with Donald Trump set for "
     "19 November.",
     (76, 154, 255)),
    ("PELTOLA WINS ALASKA SENATE SEAT",
     "Democrat Mary Peltola won Alaska's US Senate seat, giving Democrats a "
     "56–44 majority in the Senate.",
     (245, 165, 36)),
    ("EBOLA IN DR CONGO PASSES 11,000",
     "The Ebola outbreak in DR Congo passed 11,000 cases, the second-largest "
     "on record, with children bearing the heaviest toll.",
     (63, 178, 127)),
    ("VOYAGER 1 REACHES ONE LIGHT-DAY",
     "NASA's Voyager 1 reached one light-day from Earth — about 16 billion "
     "miles — a distance no human-made object has crossed before.",
     (155, 126, 222)),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_one_line(draw, text, path, start_size, max_w, min_size=28):
    """Largest font size (<= start_size) that fits text on one line."""
    size = start_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap to max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    title = "WEDNESDAY, 18 NOVEMBER 2026"
    tf = fit_one_line(d, title, BOLD, 56, W - 64)
    d.text((W / 2, 30), title, font=tf, fill=TITLE, anchor="ma")
    sf = font(REG, 28)
    d.text((W / 2, 102), "World News in One Image", font=sf,
           fill=SUBHEAD, anchor="ma")
    d.line([(64, 148), (W - 64, 148)], fill=CARD_BORDER, width=2)

    # ---- story cards ----
    card_x, card_w = 32, W - 64
    card_h, gap, y = 156, 10, 162
    for i, (headline, body, accent) in enumerate(STORIES, 1):
        top = y + (i - 1) * (card_h + gap)
        # card background + accent bar
        d.rounded_rectangle([card_x, top, card_x + card_w, top + card_h],
                            radius=14, fill=CARD_BG, outline=CARD_BORDER,
                            width=1)
        d.rounded_rectangle([card_x, top, card_x + 10, top + card_h],
                            radius=5, fill=accent)
        # number circle
        cx, cy = card_x + 38, top + 34
        d.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=accent)
        nf = font(BOLD, 26)
        d.text((cx, cy), str(i), font=nf, fill=(255, 255, 255),
               anchor="mm")
        # headline (one line, shrink to fit)
        tx = card_x + 72
        max_text_w = card_x + card_w - 24 - tx
        hf = fit_one_line(d, headline, BOLD, 40, max_text_w, min_size=30)
        d.text((tx, top + 14), headline, font=hf, fill=WHITE, anchor="la")
        # body (wrap, max 3 lines; shrink if needed)
        bf = font(REG, 25)
        lines = wrap(d, body, bf, max_text_w)
        if len(lines) > 3:
            bf = font(REG, 23)
            lines = wrap(d, body, bf, max_text_w)
        assert len(lines) <= 3, f"story {i} needs {len(lines)} lines"
        by = top + 66
        for ln in lines:
            d.text((tx, by), ln, font=bf, fill=MUTED, anchor="la")
            by += 31
        print(f"card {i}: headline size {hf.size}, body lines {len(lines)}")

    # ---- footer ----
    ff = font(REG, 19)
    d.text((W / 2, 990),
           "Sources: Just Security, Open Chronicle, Zark News, OneTurn, "
           "Horizon — 18 November 2026",
           font=ff, fill=FOOTER, anchor="ma")

    img.save(out, format="PNG")
    print("saved", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
