# netrunner-db

《矩阵潜袭》中文卡牌数据生成工具。

## 简介

本项目将 [NetrunnerDB](https://netrunnerdb.com/) 中的英文卡牌数据与 [jinteki.net](https://www.jinteki.net/) 中的中文卡牌数据合并，生成可用于其它项目开发的中英文数据库。

## 数据源

* [NetrunnerDB/netrunner-cards-json](https://github.com/NetrunnerDB/netrunner-cards-json)：官方英文卡牌数据库
* [NoahTheDuke/netrunner-data](https://github.com/NoahTheDuke/netrunner-data)：卡牌中文翻译数据库

## 生成数据

* [result/csv](result/csv)：以 .csv 格式输出的数据
* [result/json](result/json)：以 .json 格式输出的数据

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

### 卡牌属性相关

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
* **types / 类型**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称
  * `side_codename`：所属阵营标识符
* **subtypes / 子类型**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称

### 卡包相关

* **set_types / 卡包类型**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称
  * `en_description`：英文简介
  * `cn_description`：中文简介
* **publishers / 发行商**
  * `codename`：标识符
  * `en_name`：英文名称
* **cycles / 循环**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称
  * `position`：位置
  * `released_by`：发行商
* **sets / 卡包**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称
  * `cycle_codename`：所属循环标识符
  * `set_type_codename`：卡包类型标识符
  * `release_date`：发行日期
  * `position`：位置
  * `released_by`：发行商
  * `size`：卡牌数量

### 卡牌相关

> 注：NRDB的新版API将“卡牌文本”（cards）和“卡图”（printings）做了拆分，多个卡图不同但文本内容相同的卡牌现在会被视作同一张卡牌的不同卡图（或称之为异画）。
> 
> 举例：「伊索的典当铺」这张牌共有四个版本，分别来自 [核心系列](https://netrunnerdb.com/en/card/01047)、[核心系列修订版](https://netrunnerdb.com/en/card/20052)、[系统核心 2019](https://netrunnerdb.com/en/card/25056) 和 [系统革新 2021](https://netrunnerdb.com/en/card/31035)。
> 在NRDB旧版的数据格式中，这四个版本的「伊索的典当铺」会被视作四张不同的卡牌，它们（至少在理论上）可以拥有不同的卡牌文本、甚至是不同的数值。而新版的数据结构会将这四个版本视作同一个卡牌「伊索的典当铺」的四个不同卡图。

* **printings / 卡图**
  * `codename`：标识符
  * `card_codename`：所属卡牌
  * `set_codename`：所属卡包
  * `en_flavor`：英文背景描述/风味文字
  * `cn_flavor`：中文背景描述/风味文字
  * `illustrator`：画师
  * `position`：序号
  * `quantity`：数量
  * `released_by`：发行商
* **cards / 卡牌**
  * `codename`：标识符
  * `en_title`：英文标题
  * `cn_title`：中文标题
  * `stripped_title`：简化标题
  * `en_text`：英文文本
  * `cn_text`：中文文本
  * `stripped_text`：简化文本
  * `advancement_requirement`：推进需求
  * `agenda_points`：议案分数
  * `attribution`：冠名
  * `base_link`：基础中转
  * `type_codename`：类型
  * `subtype_codenames`：子类型
  * `cost`：费用
  * `deck_limit`：牌组数量限制
  * `designed_by`：发行商
  * `faction_codename`：派系
  * `influence_cost`：影响力费用
  * `influence_limit`：影响力上限
  * `is_unique`：是否独有
  * `memory_cost`：内存费用
  * `minimum_deck_size`：最低牌组张数
  * `pronouns`：人称代词
  * `pronunciation_approx`：读音
  * `pronunciation_ipa`：国际音标读音
  * `side_codename`：阵营
  * `strength`：强度
  * `trash_cost`：销毁费用
* **rulings / FAQ**
  * `card_codename`：所属卡牌
  * `update_date`：更新日期
  * `text_ruling`：规则文本
  * `question`：提问
  * `answer`：回答
  * `nsg_rules_team_verified`：是否由NSG规则团队验证

### 环境相关

* **formats / 赛制**
  * `codename`：标识符
  * `en_name`：英文名称
  * `cn_name`：中文名称
* **snapshots / 环境**
  * `codename`：标识符
  * `format_codename`：所属赛制
  * `active`：是否启用
  * `card_pool_codename`：所用卡池
  * `restriction_codename`：所用禁卡表
  * `start_date`：启用日期
* **card_pools / 卡池**
  * `codename`：标识符
  * `format_codename`：所属赛制
  * `en_name`：英文名称
  * `cycle_codename`：所用循环
  * `set_codename`：所用卡包


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
