import logging
from abc import ABC, abstractmethod

from schema import Schema
from table import Table


class Transformer(ABC):
    @abstractmethod
    def transform(self, schema: Schema, table: Table):
        pass


class InvariantTransformer(Transformer):
    def transform(self, schema: Schema, table: Table):
        pass


class PrintingTransformer(Transformer):
    def transform(self, schema: Schema, table: Table):
        for e in table.entries:
            if not "faces" in e:
                continue

            candidates = list()
            if "flavor" in e:
                candidates.append(e["flavor"])

            for f in e["faces"]:
                if "flavor" in f:
                    candidates.append(f["flavor"])

            if len(candidates) > 1:
                e["flavor"] = "\n".join(candidates)
                logging.info(f"属性 {schema.name} 的条目: {e[schema.source_id]} 已整理字段!")
