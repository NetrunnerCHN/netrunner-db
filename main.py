import logging

import toolbox
from handler import Handler


def initialize():
    # logging.disable()
    logging.basicConfig(filename="record.log", filemode="w", format="%(message)s", encoding="utf-8", level=logging.NOTSET)


def create_data(name: str):
    schema = toolbox.read_schema(name)
    handler = Handler(schema)
    handler.validate()
    header = handler.create_header()
    data = handler.create_data()
    toolbox.write_data(name, header, data)
    logging.info(f"属性 {name} 的数据生成完毕!")


def create_attributes():
    create_data("sides")
    create_data("types")
    create_data("factions")
    create_data("subtypes")


def run():
    initialize()
    create_attributes()
    # with open('side.csv', mode='w', encoding='utf-8', newline='') as f:
    #     writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    #     writer.writerow(['1001', 1002, None, 'abc', '123.456', 789.012])
    #
    # with open('side.csv', mode='r', encoding='utf-8', newline='') as f2:
    #     reader = csv.reader(f2)
    #     for line in reader:
    #         for item in line:
    #             print(item, type(item))


if __name__ == '__main__':
    run()
