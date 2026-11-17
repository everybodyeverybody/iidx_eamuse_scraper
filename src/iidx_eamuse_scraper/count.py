#!/usr/bin/env python3
import os
import json
from pathlib import Path


def sort_method(entry: tuple[str, int]) -> int:
    rank_json = """ [ { "id": 0, "name": "七級" }, { "id": 1, "name": "六級" }, { "id": 2, "name": "五級" }, { "id": 3, "name": "四級" }, { "id": 4, "name": "三級" }, { "id": 5, "name": "二級" }, { "id": 6, "name": "一級" }, { "id": 7, "name": "初段" }, { "id": 8, "name": "二段" }, { "id": 9, "name": "三段" }, { "id": 10, "name": "四段" }, { "id": 11, "name": "五段" }, { "id": 12, "name": "六段" }, { "id": 13, "name": "七段" }, { "id": 14, "name": "八段" }, { "id": 15, "name": "九段" }, { "id": 16, "name": "十段" }, { "id": 17, "name": "中伝" }, { "id": 18, "name": "皆伝" } ] """
    dan_list = {entry["name"]: entry["id"] for entry in json.loads(rank_json)}
    return dan_list[entry[0]]


data = Path("./data")
sp_output = {}
dp_output = {}


for file in sorted(os.listdir(data)):
    file_path = data / Path(file)
    ver, rank, play_type, _, _ = file.split(".")
    with open(file_path) as reader:
        player_count = len(json.load(reader))
        if play_type == "SP":
            if rank not in sp_output:
                sp_output[rank] = 0
            sp_output[rank] += player_count
        else:
            if rank not in dp_output:
                dp_output[rank] = 0
            dp_output[rank] += player_count
sp_data = sorted(sp_output.items(), key=sort_method)
dp_data = sorted(dp_output.items(), key=sort_method)

print("SP Dan Data for EPOLIS")
for entry in sp_data:
    print(f"{entry[0]}\t{entry[1]}")

print("")

print("DP Dan Data for EPOLIS")
for entry in dp_data:
    print(f"{entry[0]}\t{entry[1]}")
