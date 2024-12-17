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
                logging.info(f"属性 {schema.name} 的条目: {e[schema.source_id]} 已重新整理字段!")


class CardTransformer(Transformer):
    def transform(self, schema: Schema, table: Table):
        from handler import Handler
        printing_schema = Schema("printings")
        printing_handler = Handler(printing_schema, PrintingTransformer())
        candidates = list()
        for e in table.entries:
            e[schema.connection_id] = ""
            for t in printing_handler.source_table.entries:
                if t["card_id"] == e[schema.source_id] and t[printing_schema.source_id] > e[schema.connection_id]:
                    e[schema.connection_id] = t[printing_schema.source_id]

            if "faces" in e:
                for idx, f in enumerate(e["faces"]):
                    copy = e.copy()
                    copy[schema.source_id] = copy[schema.source_id] + f"_face{idx}"
                    for k, v in f.items():
                        copy[k] = v

                    candidates.append(copy)

        for e in candidates:
            table.entries.append(e)
            table.mappers[e[schema.source_id]] = e
            logging.info(f"属性 {schema.name} 新增条目: {e[schema.source_id]}!")


class SnapshotTransformer(Transformer):
    def transform(self, schema: Schema, table: Table):
        result = list()
        for e in table.entries:
            for s in e["snapshots"]:
                s["format_id"] = e["id"]
                result.append(s)

        table.entries = result


class RestrictionTransformer(Transformer):
    def transform(self, schema: Schema, table: Table):
        for e in table.entries:
            if "subtypes" in e:
                banlist = e["subtypes"]
                flatten = list()
                for k in banlist:
                    flatten.extend(banlist[k])

                e["subtypes"] = flatten
