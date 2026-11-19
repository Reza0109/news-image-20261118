# Wednesday, 18 November 2026 — World News in One Image

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/reza0109/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/reza0109/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Entry for the make.fun bounty **"Sum up 18 November's world news in one image"**
(`news-image-20261118`).

## What it is

A 1024×1024 infographic summarising the world news of Wednesday, 18 November 2026
in five stories: Iran's strikes on Kuwait and Bahrain after the US hit an Iranian
missile site on Qeshm Island, Xi Jinping and Vladimir Putin meeting in Shenzhen
ahead of the trilateral with Trump, Mary Peltola winning Alaska's Senate seat,
the Ebola outbreak in DR Congo passing 11,000 cases, and NASA's Voyager 1
reaching one light-day from Earth. Every fact in the image was cross-checked
against Just Security, Open Chronicle, Zark News, OneTurn and Horizon — no
speculation, no rumours, no casualty figures beyond what was reported.

## How the image was made

`entry.png` was rendered with [Pillow](https://python-pillow.org/) by the
reproducible script `draw.py` (fixed layout, Noto Sans fonts, no randomness,
no clock), then checked by eye for legibility: every headline fits on one line
and every summary fits its card with no overflow or clipping.

## How to run

```sh
python3 main.py
```

`main.py` (Python 3.13, standard library only) copies the pre-rendered
`entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), first
checking it is a real PNG of at most 1024×1024 and then verifying the copy's
magic bytes and size. Running it twice writes byte-identical output. To
re-render the image from scratch:

```sh
python3 draw.py
```
