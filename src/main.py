import logging

import toolbox
from handler import Handler
from schema import Schema
from transformer import Transformer, InvariantTransformer


def initialize():
    # logging.disable()
    logging.basicConfig(filename="record.log", filemode="w", format="%(asctime)s [%(levelname)s] %(message)s", encoding="utf-8", level=logging.NOTSET)


def create_data(name: str, transformer: Transformer | None = None):
    if transformer is None:
        transformer = InvariantTransformer()

    schema = Schema(name)
    handler = Handler(schema, transformer)
    handler.validate()
    header = handler.create_header()
    data = handler.create_data()
    toolbox.write_csv(name, header, data)
    toolbox.write_dict(name, data)
    logging.info(f"属性 {name} 的数据生成完毕!")


def run():
    initialize()

    # 属性
    create_data("sides")
    create_data("factions")
    create_data("types")
    create_data("subtypes")

    # 卡包
    create_data("set_types")
    create_data("cycles")
    create_data("sets")

    # # 赛制
    # create_data("formats")
    # create_data("rotations")
    # create_data("restrictions")
    #
    # # 卡牌
    # create_data("rulings")
    # create_data("printings", PrintingHandler)
    # create_data("cards", CardHandler)


if __name__ == '__main__':
    run()
