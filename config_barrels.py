"""
Barrel definitions for MiniPracticeKit.
Each barrel = one "segment" (split type).

Item format (Python dict, one per slot):
    {"slot": <0-26>, "id": "minecraft:xxx", "count": <1-64>}

    "count" is optional, defaults to 1.
    "tag"  is optional, for potions / enchanted items / shulker boxes.

══════════════════════  ITEM EXAMPLES  ══════════════════════

# Basic tool (unstackable, no tag)
{"slot": 0, "id": "minecraft:iron_axe"}

# Stackable item
{"slot": 1, "id": "minecraft:cooked_salmon", "count": 4}

# Potion (tag with Potion key)
{"slot": 2, "id": "minecraft:splash_potion", "count": 1, "components": {"minecraft:potion_contents": {"potion": "minecraft:fire_resistance"}}}

# Splash potion
{"slot": 3, "id": "minecraft:splash_potion", "tag": {"Potion": "minecraft:harming"}}

# Enchanted item
{"slot": 4, "id": "minecraft:diamond_sword", "tag": {
    "Enchantments": [{"id": "minecraft:sharpness", "lvl": 3}]
}}

# Pre-filled shulker box (BlockEntityTag.Items)
{"slot": 5, "id": "minecraft:shulker_box", "tag": {
    "BlockEntityTag": {
        "Items": [
            {"Slot": 0, "id": "minecraft:iron_axe", "Count": 1},
            {"Slot": 1, "id": "minecraft:golden_apple", "Count": 3},
        ]
    }
}}

# Suspicious stew with effect
{"slot": 6, "id": "minecraft:suspicious_stew", "tag": {
    "effects": [{"effect_id": "minecraft:blindness", "duration": 160}]
}}

╔══════════════════════════════════════════════════════════╗
║  To add a new barrel: copy a section & edit the values  ║
╚══════════════════════════════════════════════════════════╝
"""

# ── Bastion (Nether fortress bastion remnant) ──
BASTION = dict(
    type="bastion",
    name="Bastion Enter",
    color="gold",
    items=[
        {"slot": 0, "id": "minecraft:iron_axe"},
        {"slot": 1, "id": "minecraft:iron_pickaxe"},
        {"slot": 2, "id": "minecraft:oak_boat"},
        {"slot": 3, "id": "minecraft:lava_bucket"},
        {"slot": 4, "id": "minecraft:flint_and_steel"},
        {"slot": 5, "id": "minecraft:crafting_table", "count": 1},
        {"slot": 6, "id": "minecraft:iron_shovel"},
        {"slot": 7, "id": "minecraft:bread", "count": 16},
        {"slot": 8, "id": "minecraft:dirt", "count": 64},
        {"slot": 9, "id": "minecraft:golden_helmet"},
        {"slot": 10, "id": "minecraft:tnt", "count": 1},
        {"slot": 11, "id": "minecraft:oak_planks", "count": 32},
        {"slot": 12, "id": "minecraft:gold_ingot", "count": 1},
        {"slot": 13, "id": "minecraft:gold_block", "count": 1},
    ],
)

# ── Stronghold (Overworld end portal) ──
STRONGHOLD = dict(
    type="stronghold",
    name="Stronghold Enter",
    color="gray",
    items=[
        {"slot": 0, "id": "minecraft:iron_axe"},
        {"slot": 1, "id": "minecraft:iron_pickaxe"},
        {"slot": 2, "id": "minecraft:oak_boat"},
        {"slot": 3, "id": "minecraft:lava_bucket"},
        {"slot": 4, "id": "minecraft:flint_and_steel"},
        {"slot": 5, "id": "minecraft:ender_pearl", "count": 4},
        {"slot": 6, "id": "minecraft:iron_shovel"},
        {"slot": 7, "id": "minecraft:bread", "count": 16},
        {"slot": 8, "id": "minecraft:blackstone", "count": 64},
        {"slot": 9, "id": "minecraft:golden_helmet"},
        {"slot": 10, "id": "minecraft:ender_eye", "count": 12},
        {"slot": 11, "id": "minecraft:oak_planks", "count": 18},
        {"slot": 12, "id": "minecraft:white_wool", "count": 18},
        {"slot": 13, "id": "minecraft:crying_obsidian", "count": 32},
        {"slot": 14, "id": "minecraft:glowstone", "count": 9},
        {"slot": 15, "id": "minecraft:bow"},
        {"slot": 16, "id": "minecraft:spectral_arrow", "count": 64},
        {"slot": 17, "id": "minecraft:crafting_table", "count": 1},
        {"slot": 18, "id": "minecraft:splash_potion", "count": 1, "components": {"minecraft:potion_contents": {"potion": "minecraft:fire_resistance"}}},
        {"slot": 19, "id": "minecraft:soul_sand", "count": 64},
        {"slot": 20, "id": "minecraft:leather", "count": 64},
        {"slot": 21, "id": "minecraft:string", "count": 16},
    ],
)

# ── End City (outer End islands) ──
END_CITY = dict(
    type="end_city",
    name="End City",
    color="dark_purple",
    items=[
        {"slot": 0, "id": "minecraft:iron_axe"},
        {"slot": 1, "id": "minecraft:iron_pickaxe"},
        {"slot": 2, "id": "minecraft:oak_boat"},
        {"slot": 3, "id": "minecraft:lava_bucket"},
        {"slot": 4, "id": "minecraft:flint_and_steel"},
        {"slot": 5, "id": "minecraft:ender_pearl", "count": 8},
        {"slot": 6, "id": "minecraft:iron_shovel"},
        {"slot": 7, "id": "minecraft:bread", "count": 16},
        {"slot": 8, "id": "minecraft:blackstone", "count": 64},
        {"slot": 9, "id": "minecraft:golden_helmet"},
        {"slot": 10, "id": "minecraft:blackstone", "count": 64},
        {"slot": 11, "id": "minecraft:oak_planks", "count": 32},
        {"slot": 12, "id": "minecraft:gravel", "count": 64},
        {"slot": 13, "id": "minecraft:crying_obsidian", "count": 32},
        {"slot": 14, "id": "minecraft:quartz", "count": 64},
        {"slot": 15, "id": "minecraft:bow"},
        {"slot": 16, "id": "minecraft:spectral_arrow", "count": 64},
        {"slot": 17, "id": "minecraft:crafting_table", "count": 1},
        {"slot": 18, "id": "minecraft:splash_potion", "count": 1, "components": {"minecraft:potion_contents": {"potion": "minecraft:fire_resistance"}}},
        {"slot": 19, "id": "minecraft:soul_sand", "count": 64},
        {"slot": 20, "id": "minecraft:leather", "count": 64},
        {"slot": 21, "id": "minecraft:string", "count": 16},
        {"slot": 22, "id": "minecraft:gunpowder", "count": 32},
        {"slot": 23, "id": "minecraft:paper", "count": 32},
        {"slot": 24, "id": "minecraft:lead", "count": 2},
    ],
)

# ── HDWGH (How Did We Get Here) ──
HDWGH = dict(
    type="hdwgh",
    name="HDWGH",
    color="light_purple",
    items=[
        {"slot": 0, "id": "minecraft:enchanted_golden_apple"},
        {"slot": 1, "id": "minecraft:ominous_bottle"},
    ],
)

# ── Register all barrels here ──
ALL_BARRELS = [BASTION, END_CITY, STRONGHOLD, HDWGH]
