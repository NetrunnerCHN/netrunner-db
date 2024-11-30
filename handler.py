import logging

import langcode
import toolbox
from schema import Schema


IDENTIFIER = "codename"


class Handler:
    schema: Schema
    entries: list[dict]
    en_data: dict[str, dict]
    cn_data: dict[str, dict]

    def __init__(self, schema: Schema):
        self.schema = schema

        list1 = toolbox.read_data(self.schema.en_filename, langcode.LANGCODE_ENGLISH)
        list2 = toolbox.read_data(self.schema.cn_filename, langcode.LANGCODE_CHINESE)
        self.entries = list1
        self.en_data = toolbox.convert_data(list1, langcode.LANGCODE_ENGLISH)
        self.cn_data = toolbox.convert_data(list2, langcode.LANGCODE_CHINESE)


    def validate(self):
        self.__validate__(self.en_data, langcode.LANGCODE_ENGLISH)
        self.__validate__(self.cn_data, langcode.LANGCODE_CHINESE)

    def __validate__(self, data: dict[str, dict], lang: int):
        result = set()
        for d in data.values():
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
        for line in self.entries:
            index = str(line[id_name])
            # 英文ID以下划线连接，中文ID以短横线连接，这里需要做兼容处理
            item1 = self.en_data.get(index)
            item2 = self.cn_data.get(index.replace("_", "-"))

            line = dict()
            line[IDENTIFIER] = index
            for f in self.schema.fields:
                if f.lang == langcode.LANGCODE_ENGLISH:
                    line[f.name] = (str(item1[f.source]) if (f.source in item1) else "") if item1 else ""
                elif f.lang == langcode.LANGCODE_CHINESE:
                    line[f.name] = (str(item2[f.source]) if (f.source in item2) else "") if item2 else ""
                else:
                    raise RuntimeError(f"属性 {self.schema.name} 的字段 {f.name} 使用了不合法的语言: {f.lang}!")

            result.append(line)

        return result
