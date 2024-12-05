from typing import Any

import toolbox


JSON_EXT = ".json"


class Table:
    entries: list[dict[str, Any]]
    mappers: dict[str, dict[str, Any]]

    def __init__(self, filename: str, uuid: str):
        self.entries = list()
        self.mappers = dict()

        self.entries = toolbox.read_data(filename)

        if len(uuid) > 0:
            for e in self.entries:
                if not uuid in e:
                    raise RuntimeError(f"文件中有缺少唯一标识符的配置项: {filename}!")

                self.mappers[e[uuid]] = e
