# netrunner-db

《矩阵潜袭》中文卡牌数据生成工具。

## 数据源

* [NetrunnerDB/netrunner-cards-json](https://github.com/NetrunnerDB/netrunner-cards-json)：官方英文卡牌数据库
* [NoahTheDuke/netrunner-data](https://github.com/NoahTheDuke/netrunner-data)：卡牌中文翻译数据库

## 使用说明

* 生成数据

```shell
python src/main.py
```

* 验证数据

```shell
python -m unittest src/tests.py
```

## 规范文件格式

* `name`：数据结构名称
* `source_data`：英文数据文件路径
* `translation_data`：中文数据文件路径
* `source_id`：英文数据标识符
* `translation_id`：中文数据标识符
* `connection_id`：英文数据与中文数据对应标识符
* `fields`：输出数据字段
  * `name`：字段名称
  * `source`：读入字段名称
  * `is_trans`：是/否来自中文数据
* `ignores`：忽略字段名称
  * `name`：字段名称
  * `is_trans`：是/否来自中文数据

## 数据结构

* **sides / 阵营**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称
* **factions / 派系**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称
  * `en_description`：英文简介
  * `cn_description`：中文简介
  * `color`：颜色
  * `is_mini`：是/否迷你派系
  * `side_codename`：所属阵营标识符



## 笔记

### 环境相关

- formats: 赛制
* snapshots: 环境
- card_pools: 卡池
* restrictions: 禁卡表

snapshots -> formats
snapshots -> card_pools
snapshots -> restrictions
card_pools -> formats
restrictions -> formats
card_pools -> cycles[]
card_pools -> sets[]
restrictions -> cards[]

每个 format 引用一个 card_pool 和一个 restrictions

### 卡包相关

- cycles: 循环
- sets: 卡包
- set_types: 卡包类型

**关联**

sets -> cycles
sets -> set_types

### 卡牌相关

- printings: 卡图
- cards: 信息
- rulings: FAQ

**关联**

printings -> cards
printings -> sets
cards -> types
cards -> factions
cards -> sides
cards -> subtypes[]
rulings -> cards

### 属性相关

- sides: 阵营
- factions: 派系
- types: 类型
- subtypes: 子类型
