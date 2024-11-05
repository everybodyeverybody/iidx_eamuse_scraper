#!/usr/bin/env python3
import os
import time
import json
import shutil
import logging
import argparse  # type: ignore
from enum import Enum  # type: ignore
from pathlib import Path
from dataclasses import dataclass

import requests  # type: ignore


class PlayStyle(Enum):
    SP = 0
    DP = 1


@dataclass
class DanRanking:
    grade_id: int
    name: str

    def to_dict(self) -> dict[str, str | int]:
        return {"id": self.grade_id, "name": self.name}


def get_dan_data(
    dan_rank: DanRanking,
    play_style: PlayStyle,
    output_directory: Path,
    version: int = 31,
) -> list[Path]:
    files_written: list[Path] = []
    log.info(f"Getting {dan_rank} data for {play_style.name}")
    page_count = 0
    limit = 50000
    base_url = f"https://p.eagate.573.jp/game/2dx/{version}/ranking"
    request_url = f"{base_url}/json/dani.html"
    referer_url = f"{base_url}/dani.html?grade_id={dan_rank.grade_id}&display=1&play_style={play_style.value}"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": referer_url,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0",
        "XMLHttpRequest": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }

    # We discovered while attempting to paginate over this endpoint that the
    # `page` value actually does not paginate. One must instead increase the
    # limit to above what they think the API will return which works.
    # I'm leaving the code this way in case konami ever fixes it.
    got_all_data = False
    while not got_all_data:
        log.info(f"Getting {dan_rank} data for {play_style.name} page {page_count}")
        form_data = {
            "grade_id": dan_rank.grade_id,
            "play_style": play_style.value,
            "page": page_count,
            "limit": limit,
            "release_9_10_kaiden": 2,
        }
        log.info(form_data)
        output_filename = (
            f"epolis.{dan_rank.name}.{play_style.name}.{page_count:03d}.json"
        )
        output_path = output_directory / Path(output_filename)
        with open(output_path, "wt") as writer:
            response = requests.post(request_url, headers=headers, data=form_data)
            log.info(f"response: {response.status_code}")
            log.info(f"encoding: {response.encoding}")
            if response.status_code != 200:
                raise RuntimeError(response.text)
            try:
                response_data = response.json()
            except requests.RequestsJSONDecodeError as json_error:
                log.error("Could not read response, likely bad request.")
                raise json_error
            djs = response_data["list"]
            writer.write(json.dumps(djs, indent=2))
            files_written.append(output_path)
            log.info(f"page {page_count} dj count: {len(djs)}")
            if len(djs) < limit:
                got_all_data = True
            else:
                page_count += 1
        time.sleep(5)
    return files_written


def read_data_dir(data_dir: Path) -> list[Path]:
    log.warning(f"skipping scrape and reading local data from {data_dir}")
    return [file for file in data_dir.iterdir()]


def scrape_data(dan_ranking: list[DanRanking], data_dir: Path) -> list[Path]:
    all_files: list[Path] = []
    sp_or_dp = [style for style in PlayStyle]
    for play_style in sp_or_dp:
        for dan in dan_ranking:
            all_files.extend(get_dan_data(dan, play_style, data_dir))
    return all_files


def get_ranking_list() -> list[DanRanking]:
    def __sort_method(entry: dict[str, str | int]) -> int:
        result: int = int(entry["id"])
        return result

    # TODO: get this from a fresh request? it doesn't really matter though
    rank_json = """ [ { "id": 0, "name": "七級" }, { "id": 1, "name": "六級" }, { "id": 2, "name": "五級" }, { "id": 3, "name": "四級" }, { "id": 4, "name": "三級" }, { "id": 5, "name": "二級" }, { "id": 6, "name": "一級" }, { "id": 7, "name": "初段" }, { "id": 8, "name": "二段" }, { "id": 9, "name": "三段" }, { "id": 10, "name": "四段" }, { "id": 11, "name": "五段" }, { "id": 12, "name": "六段" }, { "id": 13, "name": "七段" }, { "id": 14, "name": "八段" }, { "id": 15, "name": "九段" }, { "id": 16, "name": "十段" }, { "id": 17, "name": "中伝" }, { "id": 18, "name": "皆伝" } ] """
    ranks: list[dict[str, str | int]] = sorted(json.loads(rank_json), key=__sort_method)
    dan_ranks = [
        DanRanking(grade_id=int(entry["id"]), name=str(entry["name"]))
        for entry in ranks
    ]
    log.info(dan_ranks)
    return dan_ranks


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="iidx_eamuse_scraper",
        description="A script that gets player dan ranking data for IIDX Epolis.",
    )
    parser.add_argument(
        "--data-dir",
        dest="data_dir",
        type=Path,
        default=Path("data/"),
        help=(
            "The output directory for JSON scraped from the site. Defaults to data/. "
            "This directory is re-made any time `--skip-scrape` is not invoked."
        ),
    )
    parser.add_argument(
        "--skip-scrape",
        dest="skip_scrape",
        action="store_true",
        help="Whether or not to re-scrape the data and instead read from local `--data-dir`. Defaults to false.",
    )
    return parser.parse_args()


def main():
    log.info("starting up")
    args = parse_arguments()
    if not args.skip_scrape:
        if args.data_dir.exists() and args.data_dir.is_dir():
            log.warning(f"Removing {args.data_dir}")
            shutil.rmtree(args.data_dir)
        if not args.data_dir.exists():
            os.makedirs(args.data_dir)
        ranking_list = get_ranking_list()
        data_files = scrape_data(ranking_list, args.data_dir)
    else:
        data_files = read_data_dir(args.data_dir)
    log.info(data_files)


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
main()
