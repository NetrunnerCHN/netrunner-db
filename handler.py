import logging

import langcode
import toolbox
from schema import Schema


LEGACY_CODE = "legacy_code"
IDENTIFIER = "codename"


class Handler:
    schema: Schema
    english_entries: list[dict]
    chinese_entries: list[dict]
    english_tables: dict[str, dict]
    chinese_tables: dict[str, dict]

    def __init__(self, schema: Schema):
        self.schema = schema
        self.english_entries = toolbox.read_data(self.schema.en_filename, langcode.LANGCODE_ENGLISH)
        self.chinese_entries = toolbox.read_data(self.schema.cn_filename, langcode.LANGCODE_CHINESE)
        self.english_tables = toolbox.convert_data(self.english_entries, langcode.LANGCODE_ENGLISH)
        self.chinese_tables = toolbox.convert_data(self.chinese_entries, langcode.LANGCODE_CHINESE)

    def validate(self):
        self.__validate__(self.english_entries, langcode.LANGCODE_ENGLISH)
        self.__validate__(self.chinese_entries, langcode.LANGCODE_CHINESE)

    def __validate__(self, entries: list[dict], lang: int):
        result = set()
        for d in entries:
            for k in d:
                if k == toolbox.select_identifier(lang):
                    continue

                valid = False
                for f in self.schema.fields:
                    if f.lang == lang and f.source == k:
                        valid = True
                        break

                if not valid:
                    result.add(k)

        for i in self.schema.ignores:
            result.discard(i)

        if len(result) > 0:
            text = ", ".join(result)
            language = toolbox.select_language(lang)
            logging.warning(f"属性 {self.schema.name} 的 {language} 配置文件有未使用的字段: {text}!")

    def create_header(self) -> list[str]:
        result = list()
        result.append(IDENTIFIER)
        for f in self.schema.fields:
            result.append(f.name)

        return result

    def create_data(self) -> list[dict[str, str]]:
        result = list()
        id_name = toolbox.select_identifier(langcode.LANGCODE_ENGLISH)
        for e in self.english_entries:
            line = dict()
            if len(self.english_tables) > 0 and len(self.chinese_tables) > 0:
                index1 = str(e[id_name])
                index2 = e[LEGACY_CODE] if LEGACY_CODE in e else index1.replace("_", "-")
                # 英文ID以下划线连接，中文ID以短横线连接，这里需要做兼容处理
                item1 = self.english_tables.get(index1)
                item2 = self.chinese_tables.get(index2)

                line[IDENTIFIER] = index1
                for f in self.schema.fields:
                    if f.lang == langcode.LANGCODE_ENGLISH:
                        line[f.name] = (str(item1[f.source]) if (f.source in item1) else "") if item1 else ""
                    elif f.lang == langcode.LANGCODE_CHINESE:
                        line[f.name] = (str(item2[f.source]) if (f.source in item2) else "") if item2 else ""
                    else:
                        raise RuntimeError(f"属性 {self.schema.name} 的字段 {f.name} 使用了不合法的语言: {f.lang}!")

                result.append(line)
            else:
                for f in self.schema.fields:
                    line[f.name] = str(e[f.source]) if (f.source in e) else ""

                result.append(line)

        return result
