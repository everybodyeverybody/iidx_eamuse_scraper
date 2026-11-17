# iidx_eamuse_scraper

A script that gets player dan ranking data for IIDX Epolis.

Intended to maybe do more in the future.

## Setup

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Usage

### Scraping the Data

```
python3 -m src.iidx_eamuse_scraper
```

```
usage: iidx_eamuse_scraper [-h] [--data-dir DATA_DIR] [--skip-scrape]

A script that gets player dan ranking data for IIDX Epolis.

options:
  -h, --help           show this help message and exit
  --data-dir DATA_DIR  The output directory for JSON scraped from the site. Defaults to data/. This directory is re-made any time
                       `--skip-scrape` is not invoked.
  --skip-scrape        Whether or not to re-scrape the data and instead read from local `--data-dir`. Defaults to false.
```

### Counting the Output

Run after running the above.

```
python3 -m src.iidx_eamuse_scraper.count
```

#### Latest Results (2026-11-17)

```
SP Dan Data for EPOLIS
七級    498
六級    380
五級    649
四級    232
三級    307
二級    521
一級    543
初段    718
二段    527
三段    837
四段    1920
五段    1456
六段    5679
七段    2606
八段    11215
九段    4172
十段    7279
中伝    4438
皆伝    5244
```

```
DP Dan Data for EPOLIS
七級    118
六級    85
五級    72
四級    82
三級    81
二級    38
一級    104
初段    322
二段    185
三段    157
四段    218
五段    358
六段    913
七段    1172
八段    1370
九段    616
十段    664
中伝    577
皆伝    617
```
