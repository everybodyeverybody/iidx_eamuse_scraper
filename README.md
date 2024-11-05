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
