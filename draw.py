#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic as a 1024x1024 PNG.

Writes entry.png next to this file. One dark-navy page: a centred header,
five numbered story cards with a coloured accent each, and a sources footer.
"""

import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 36
CARD_LEFT = MARGIN
CARD_RIGHT = SIZE - MARGIN
CARD_TOP = 152
CARD_HEIGHT = 150
CARD_GAP = 12

BG = (11, 18, 38)
CARD_BG = (27, 39, 68)
TITLE = (255, 255, 255)
SUBTITLE = (140, 175, 230)
DIVIDER = (52, 68, 104)
HEADLINE = (255, 255, 255)
BODY = (198, 209, 228)
FOOTER = (139, 150, 176)
BADGE_TEXT = (255, 255, 255)

STORIES = [
    (
        "IRAN STRIKES KUWAIT AND BAHRAIN",
        "Iran struck Ali Al Salem Air Base in Kuwait, home to US forces, "
        "and targets in Bahrain \u2014 a day after US warplanes hit an "
        "Iranian missile site on Qeshm Island.",
        (229, 72, 77),
    ),
    (
        "XI AND PUTIN MEET IN SHENZHEN",
        "Xi Jinping and Vladimir Putin met in Shenzhen on the sidelines "
        "of the APEC summit, ahead of a trilateral meeting with Donald "
        "Trump set for 19 November.",
        (74, 144, 226),
    ),
    (
        "PELTOLA WINS ALASKA SENATE SEAT",
        "Democrat Mary Peltola won Alaska's US Senate seat, giving "
        "Democrats a 56-44 majority in the Senate.",
        (245, 166, 35),
    ),
    (
        "EBOLA IN DR CONGO PASSES 11,000",
        "The Ebola outbreak in DR Congo passed 11,000 cases, the "
        "second-largest on record, with children bearing the heaviest toll.",
        (63, 185, 127),
    ),
    (
        "VOYAGER 1 REACHES ONE LIGHT-DAY",
        "NASA's Voyager 1 reached one light-day from Earth \u2014 about 16 "
        "billion miles \u2014 a distance no human-made object has crossed before.",
        (155, 126, 222),
    ),
]

FOOTER_TEXT = (
    "Sources: Just Security, Open Chronicle, Zark News, OneTurn, Horizon "
    "\u2014 18 November 2026"
)


def load_font(bold, size):
    """Try the common system sans fonts, falling back to PIL's default."""
    if bold:
        names = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"]
    else:
        names = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    for name in names:
        for folder in ("/usr/share/fonts/truetype/dejavu",
                       "/usr/share/fonts/truetype/liberation"):
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap using the font's real text lengths."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_header(draw):
    title_font = load_font(True, 46)
    sub_font = load_font(False, 29)
    title = "WEDNESDAY, 18 NOVEMBER 2026"
    subtitle = "World News in One Image"
    title_x = (SIZE - draw.textlength(title, font=title_font)) / 2
    draw.text((title_x, 26), title, font=title_font, fill=TITLE)
    sub_x = (SIZE - draw.textlength(subtitle, font=sub_font)) / 2
    draw.text((sub_x, 92), subtitle, font=sub_font, fill=SUBTITLE)
    draw.line([(MARGIN, 138), (SIZE - MARGIN, 138)], fill=DIVIDER, width=2)


def draw_card(draw, index, headline, body, accent, top):
    bottom = top + CARD_HEIGHT
    draw.rounded_rectangle(
        [CARD_LEFT, top, CARD_RIGHT, bottom], radius=16, fill=CARD_BG
    )
    # Thin coloured bar hugging the card's left edge.
    draw.rounded_rectangle(
        [CARD_LEFT + 2, top + 10, CARD_LEFT + 14, bottom - 10],
        radius=6,
        fill=accent,
    )
    # Numbered disc above the headline's left side.
    badge_cx = CARD_LEFT + 52
    badge_cy = top + 30
    badge_r = 21
    draw.ellipse(
        [badge_cx - badge_r, badge_cy - badge_r,
         badge_cx + badge_r, badge_cy + badge_r],
        fill=accent,
    )
    number_font = load_font(True, 26)
    draw.text(
        (badge_cx, badge_cy), str(index + 1),
        font=number_font, fill=BADGE_TEXT, anchor="mm",
    )
    text_x = CARD_LEFT + 92
    headline_font = load_font(True, 32)
    draw.text((text_x, top + 14), headline, font=headline_font, fill=HEADLINE)
    body_font = load_font(False, 22)
    max_width = CARD_RIGHT - text_x - 24
    lines = wrap_text(draw, body, body_font, max_width)
    line_y = top + 58
    for line in lines:
        draw.text((text_x, line_y), line, font=body_font, fill=BODY)
        line_y += 28


def draw_footer(draw):
    footer_font = load_font(False, 20)
    footer_x = (SIZE - draw.textlength(FOOTER_TEXT, font=footer_font)) / 2
    draw.text((footer_x, 968), FOOTER_TEXT, font=footer_font, fill=FOOTER)


def main():
    image = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)
    draw_header(draw)
    top = CARD_TOP
    for index, (headline, body, accent) in enumerate(STORIES):
        draw_card(draw, index, headline, body, accent, top)
        top += CARD_HEIGHT + CARD_GAP
    draw_footer(draw)
    here = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(here, "entry.png")
    image.save(out_path, "PNG")
    print(f"wrote {out_path} ({os.path.getsize(out_path)} bytes)")


if __name__ == "__main__":
    main()
