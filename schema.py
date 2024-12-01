import json


class Field:
    name: str
    comment: str
    lang: int
    source: str

    def __init__(self, name: str, comment: str, lang: int, source: str):
        self.name = name
        self.comment = comment
        self.lang = lang
        self.source = source

    def __str__(self) -> str:
        return json.dumps(self, ensure_ascii=False, default=lambda x: x.__dict__)


class Schema:
    name: str
    comment: str
    en_filename: str
    cn_filename: str
    ignores: list[str]
    fields: list[Field]

    def __init__(self, name: str, comment: str, en_filename: str, cn_filename: str, fields: list, ignores: list[str]):
        self.name = name
        self.comment = comment
        self.en_filename = en_filename
        self.cn_filename = cn_filename
        self.ignores = ignores
        self.fields = []
        for f in fields:
            field = Field(**f)
            self.fields.append(field)

    def __str__(self) -> str:
        return json.dumps(self, ensure_ascii=False, default=lambda x: x.__dict__)
