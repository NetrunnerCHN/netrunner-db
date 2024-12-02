import csv
import json
import os

import langcode
from schema import Schema


CSV_EXT = ".csv"
JSON_EXT = ".json"
SCHEMA_FOLDER = "schema"
RESULT_FOLDER = "result"


def read_schema(filename: str) -> Schema:
    fullname = os.path.join(SCHEMA_FOLDER, filename + JSON_EXT)
    with open(fullname, mode="r", encoding="utf-8") as f:
        data = json.load(f)
        result = Schema(**data)
        return result


CN_FOLDER = "data/CN/json/translations/zh-hans"
EN_FOLDER = "data/EN/v2"


def select_folder(lang: int) -> str:
    if lang == langcode.LANGCODE_ENGLISH:
        return EN_FOLDER
    elif lang == langcode.LANGCODE_CHINESE:
        return CN_FOLDER
    else:
        raise RuntimeError(f"不合法的语言: {lang}!")


CN_IDENTIFIER = "code"
EN_IDENTIFIER = "id"


def select_identifier(lang: int) -> str:
    if lang == langcode.LANGCODE_ENGLISH:
        return EN_IDENTIFIER
    elif lang == langcode.LANGCODE_CHINESE:
        return CN_IDENTIFIER
    else:
        raise RuntimeError(f"不合法的语言: {lang}!")


CN_LANGUAGE = "中文"
EN_LANGUAGE = "英文"


def select_language(lang: int) -> str:
    if lang == langcode.LANGCODE_ENGLISH:
        return EN_LANGUAGE
    elif lang == langcode.LANGCODE_CHINESE:
        return CN_LANGUAGE
    else:
        raise RuntimeError(f"不合法的语言: {lang}!")


def read_data(filename: str, lang: int) -> list[dict]:
    folder = select_folder(lang)
    fullname = os.path.join(folder, filename)
    if os.path.isdir(fullname):
        return read_folder_data(fullname)
    else:
        fullname = os.path.join(folder, filename + JSON_EXT)
        return read_file_data(fullname)


def read_file_data(filename: str) -> list[dict]:
    with open(filename, mode="r", encoding="utf-8") as f:
        items = json.load(f)
        if not isinstance(items, list):
            raise RuntimeError(f"文件格式不合法: {filename}!")

        return items


def read_folder_data(filename: str) -> list[dict]:
    items = list()
    filenames = sorted(os.listdir(filename))
    for fn in filenames:
        if not fn.endswith(JSON_EXT):
            continue

        fullname = os.path.join(filename, fn)
        with open(fullname, mode="r", encoding="utf-8") as f:
            item = json.load(f)
            if isinstance(item, list):
                items.extend(item)
            elif isinstance(item, dict):
                items.append(item)
            else:
                raise RuntimeError(f"文件格式不合法: {filename}!")

    return items


def convert_data(entries: list[dict], lang: int) -> dict[str, dict]:
    identifier = select_identifier(lang)
    result = dict()
    for v in entries:
        if identifier in v:
            k = v[identifier]
            result[k] = v

    return result


def write_data(name: str, header: list[str], data: list[dict[str, str]]):
    fullname = os.path.join(RESULT_FOLDER, name + CSV_EXT)
    with open(fullname, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for l in data:
            writer.writerow(l)
