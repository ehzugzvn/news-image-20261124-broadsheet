# The World in One Page — Tuesday 24 November 2026 (BROADSHEET)

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/ehzugzvn/news-image-20261124-broadsheet/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/ehzugzvn/news-image-20261124-broadsheet/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A classic newspaper front page summing up 24 November 2026's world news in one
image: a giant date masthead, four leads each with a literal illustration
(Huawei verdict, Hormuz tankers, Ukraine's strikes on Russian ships, Cartagena
hostages), a numbered-pin world map, ten verified tier-2 stories, 24 briefs,
a UTC timeline, and a date-check strip naming the stories deliberately excluded.

Entry for the [make.fun bounty "Sum up 24 November's world news in one image"](https://make.fun/bounty/news-image-20261124).

## How it works

`render.py` (Pillow, run locally) draws `entry.png` (1024×1024) entirely in
code — vector-style maps, pictograms, badges and type, no borrowed images.
`main.py` is stdlib-only and simply copies the pre-rendered `entry.png` to
`MAKEFUN_OUTPUT_DIR/entry.png` at run time.

## Reproduce

```sh
python3 render.py        # regenerates entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```
