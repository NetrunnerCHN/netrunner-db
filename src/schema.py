from typing import Any

import toolbox


class IgnoreField:
    name: str
    is_trans: bool

    def __init__(self, data: dict[str, Any]):
        self.name = data["name"]
        self.is_trans = data["is_trans"]


class Field:
    name: str
    source: str
    is_trans: bool

    def __init__(self, data: dict[str, Any]):
        self.name = data["name"]
        self.source = data["source"]
        self.is_trans = data["is_trans"]


class Schema:
    name: str
    source_data: str
    translation_data: str
    source_id: str
    translation_id: str
    connection_id: str
    fields: list[Field]
    ignores: list[IgnoreField]

    def __init__(self, filename: str):
        data = toolbox.read_schema(filename)
        self.name = data["name"]
        self.source_data = data["source_data"]
        self.translation_data = data["translation_data"]
        self.source_id = data["source_id"]
        self.translation_id = data["translation_id"]
        self.connection_id = data["connection_id"]

        self.fields = list()
        for d in data["fields"]:
            field = Field(d)
            self.fields.append(field)

        self.ignores = list()
        for i in data["ignores"]:
            ignore = IgnoreField(i)
            self.ignores.append(ignore)
