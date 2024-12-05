import csv
import json
import os
from typing import Any


CSV_EXT = ".csv"
JSON_EXT = ".json"

SCHEMA_FOLDER = "schema"

def read_schema(filename: str) -> dict[str, Any]:
    fullname = os.path.join(SCHEMA_FOLDER, filename + JSON_EXT)
    with open(fullname, mode="r", encoding="utf-8") as f:
        data = json.load(f)
        return data


def read_data(filename: str) -> list[dict[str, Any]]:
    result = list()
    if os.path.isdir(filename):
        content = sorted(os.listdir(filename))
        for fn in content:
            fullname = os.path.join(filename, fn)
            children = read_data(fullname)
            result.extend(children)
    elif os.path.isfile(filename):
        if filename.endswith(JSON_EXT):
            with open(filename, mode="r", encoding="utf-8") as f:
                items = json.load(f)
                if isinstance(items, list):
                    result.extend(items)
                elif isinstance(items, dict):
                    result.append(items)
                else:
                    raise RuntimeError(f"文件格式不符合规范: {filename}!")

    return result


RESULT_FOLDER = "result"
CSV_RESULT_FOLDER = "csv"
JSON_RESULT_FOLDER = "json"

def write_csv(name: str, header: list[str], data: list[dict[str, str]]):
    fullname = os.path.join(RESULT_FOLDER, CSV_RESULT_FOLDER, name + CSV_EXT)
    with open(fullname, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data)


def write_dict(name: str, data: list[dict[str, str]]):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    fullname = os.path.join(RESULT_FOLDER, JSON_RESULT_FOLDER, name + JSON_EXT)
    with open(fullname, mode="w", encoding="utf-8", newline="") as f:
        f.write(text)
