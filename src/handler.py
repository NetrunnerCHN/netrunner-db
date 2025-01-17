import json
import logging
from typing import Any

from schema import Schema
from table import Table
from transformer import Transformer


class Handler:
    schema: Schema
    transformer: Transformer
    source_table: Table
    translation_table: Table

    def __init__(self, schema: Schema, transformer: Transformer):
        self.schema = schema
        self.transformer = transformer
        self.source_table = Table(self.schema.source_data, self.schema.source_id)
        self.translation_table = Table(self.schema.translation_data, self.schema.translation_id)
        self.transformer.transform(self.schema, self.source_table)

    def validate(self):
        self.__validate__(self.source_table, False)
        self.__validate__(self.translation_table, True)

    def __validate__(self, table: Table, is_trans: bool):
        result = set()
        for d in table.entries:
            for k in d:
                valid = False
                for f in self.schema.fields:
                    if f.is_trans == is_trans and f.source == k:
                        valid = True
                        break

                if not valid:
                    result.add(k)

        for i in self.schema.ignores:
            if i.is_trans == is_trans:
                result.discard(i.name)

        if len(result) > 0:
            text = ", ".join(result)
            filename = self.schema.translation_data if is_trans else self.schema.source_data
            logging.warning(f"属性 {self.schema.name} 的配置文件 {filename} 有未使用的字段: {text}!")

    def find_translation(self, source: dict[str, Any]) -> dict[str, Any] | None:
        if len(self.schema.connection_id) > 0:
            index = str(source[self.schema.connection_id])
        else:
            if len(self.schema.source_id) > 0:
                index = str(source[self.schema.source_id]).replace("_", "-")
            else:
                return None

        return self.translation_table.mappers.get(index)


    def create_header(self) -> list[str]:
        result = list()
        for f in self.schema.fields:
            result.append(f.name)

        return result

    def create_data(self, flatten_list: bool) -> list[dict[str, list | str]]:
        result = list()
        for source in self.source_table.entries:
            trans = self.find_translation(source)
            line = dict()
            for f in self.schema.fields:
                if f.is_trans:
                    line[f.name] = self.serialize_field(trans, f.source, flatten_list)
                else:
                    line[f.name] = self.serialize_field(source, f.source, flatten_list)

            result.append(line)

        return result

    def serialize_field(self, data: dict[str, Any] | None, index: str, flatten_list: bool) -> list | str:
        if (data is None) or (index not in data) or (data[index] is None):
            return ""

        if isinstance(data[index], list):
            if flatten_list:
                return json.dumps(data[index], ensure_ascii=False)
            else:
                result = list()
                for i in data[index]:
                    result.append(str(i))

                return result
        else:
            return str(data[index])
