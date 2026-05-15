# TinyPracticeKit v0.1

Minecraft Java 1.21.10 速通练习工具 — 纯命令方块，无数据包。

扔桶 → 传送到目标维度 → 点击定位结构 → 获得练习物资。
一个循环命令方块驱动全部逻辑。

## 文件结构

```
config_barrels.py    ← 桶的物品配置（改这个）
config_layout.py     ← 热键栏布局     （改这个）
mpk_build.py         ← 生成脚本       （跑这个）
```

## 快速开始

```bash
pip install nbtlib
python mpk_build.py
```

将生成的 `hotbar.nbt` 复制到 `.minecraft` 目录

### 游戏内操作

1. 创造模式单人存档
2. 按 **Ctrl+1** 加载热键栏 — 桶在 1-4 格，引擎命令方块在第 9 格
3. 取出第 9 格的循环命令方块（名称 "TinyPracticeKit v0.1"），放在地面
4. 确认为**始终活动 + 无条件**（默认已设置）
5. 把任意桶扔在 3 格范围内
6. 约 1 秒后链式命令方块自动生成，桶立即被处理

## 四个分支

| 桶 | 颜色 | 效果 |
|----|------|------|
| **Bastion Enter** | 金色 | 传送到地狱高空 → 点 `[LOCATE]` → 点坐标 → 点 `[LAND]` 落地 |
| **Stronghold Enter** | 灰色 | 点 `[LOCATE]` → 点坐标（主世界，无需切维度） |
| **End City** | 暗紫 | 传送到末地高空 → 点 `[NE][NW][SE][SW]` 四象限定位 → 点坐标 → 点 `[LAND]` |
| **HDWGH** | 浅紫 | 自动 `spreadplayers` 到 (0,0) 附近 |

所有分支：设置 `difficulty easy` → 清空背包 → 发放对应物资。

## 重置

如果链式命令方块被破坏，需要重建：

```mcfunction
/data remove storage mpk:main built
```

然后重新扔桶即可。

## 配置物品

编辑 `config_barrels.py`。每个桶有 `type`、`name`、`color`、`items` 四个字段。

### 物品格式

```python
{"slot": <0-26>, "id": "minecraft:xxx", "count": <1-64>}
```

`count` 可省略，默认 1。

### 物品示例

```python
# 普通工具
{"slot": 0, "id": "minecraft:iron_axe"}

# 可堆叠物品
{"slot": 7, "id": "minecraft:bread", "count": 16}

# 药水（components 格式）
{"slot": 18, "id": "minecraft:splash_potion", "count": 1,
 "components": {"minecraft:potion_contents": {"potion": "minecraft:fire_resistance"}}}

# 附魔物品（tag 格式）（还未测试，需要实际用桶取 `data` 检查看看）
{"slot": 4, "id": "minecraft:diamond_sword",
 "tag": {"Enchantments": [{"id": "minecraft:sharpness", "lvl": 3}]}}

# 预装潜影盒（同上）
{"slot": 5, "id": "minecraft:shulker_box",
 "tag": {"BlockEntityTag": {"Items": [
     {"Slot": 0, "id": "minecraft:iron_axe", "Count": 1},
     {"Slot": 1, "id": "minecraft:golden_apple", "Count": 3},
 ]}}}

# 谜之炖菜（同上）
{"slot": 6, "id": "minecraft:suspicious_stew",
 "tag": {"effects": [{"effect_id": "minecraft:blindness", "duration": 160}]}}
```

### 添加新桶

1. 在 `config_barrels.py` 复制一个现有桶的定义
2. 修改 `type` / `name` / `color` / `items`
3. 加入文件末尾的 `ALL_BARRELS` 列表
4. 如果用到新的维度或结构，在 `mpk_build.py` 约 76 行的 `dim_map` 里加一行

## 配置热键栏布局

编辑 `config_layout.py`：

```python
BARRELS = [BASTION, STRONGHOLD, END_CITY, HDWGH]  # 热键栏第 1, 2, 3, 4 格
ENGINE_SLOT = 9                                     # 引擎命令方块位置 (1-9)
```

调整 `BARRELS` 列表的顺序即可改变桶在热键栏的位置。

## 运行环境

- Python 3.9+
- `nbtlib`（`pip install nbtlib`）
- Minecraft Java 1.21.10

## 杂项

目前仅在 `1.21.10` 上测试过，不保证其它版本的可用性。HDWGH 暂时不知道怎么实现，如果有人有想法欢迎pr，当然因为我看不懂命令全都是 AI 帮忙写的更欢迎自己 fork 一份改。
现在的运行机制和 `1.16.1` 的 MPK 不同，单个命令方块会生成所有的分支检测，而不像正版 MPK 一样只生成对应分支的命令方块。
Made with Gemini-3.1 + Deepseek-v4