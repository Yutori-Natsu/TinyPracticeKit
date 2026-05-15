"""
MiniPracticeKit v1.0 — Builder
==============================
Reads config_barrels.py + config_layout.py → generates hotbar.nbt
One repeating CB (engine) + falling_block tree of chain CBs.
"""
import sys
import nbtlib
from nbtlib.tag import Compound, List, String, Byte, Int, Short

# ── Config ──
from config_barrels import ALL_BARRELS
from config_layout import BARRELS, ENGINE_SLOT

DATA_VERSION = 3465
S = "storage mpk:main"
SUMMON_HEIGHT = "~ ~10 ~"

# ── SNBT builders ──

def nbt_barrel(bt):
    """@e[nbt=...] snippet for barrel detection (no type filter)"""
    return (f'nbt={{Item:{{id:"minecraft:barrel",'
            f'components:{{"minecraft:custom_data":{{mpk:1b}}}}}}}}')

def nbt_type(b):
    """@e[nbt=...] snippet for type-specific matching"""
    return (f'nbt={{Item:{{id:"minecraft:barrel",'
            f'components:{{"minecraft:custom_data":{{mpk:1b,mpk_type:"{b["type"]}"}}}}}}}}')

SEL = "@e[type=item,distance=..3,tag=!mpk_used,limit=1,sort=nearest,"

# ── Loot table helper ──

def make_loot_cmd(items):
    pools = []
    for e in items:
        name = e["id"]
        count = e.get("count", 1)
        comps = e.get("components", None)
        funcs = []
        if count > 1:
            funcs.append(f'{{"function":"minecraft:set_count","count":{count}}}')
        if comps:
            # components dict → set_components; quote string values only
            comp_json = _components_json(comps)
            funcs.append(f'{{"function":"minecraft:set_components","components":{comp_json}}}')
        if funcs:
            entry = f'{{"rolls":1,"entries":[{{"type":"item","name":"{name}","functions":[{",".join(funcs)}]}}]}}'
        else:
            entry = f'{{"rolls":1,"entries":[{{"type":"item","name":"{name}"}}]}}'
        pools.append(entry)
    return f'loot give @p loot {{"pools":[{",".join(pools)}]}}'


def _components_json(comps):
    """Convert a components dict to JSON string for inline loot table.
    Handles potion_contents, enchantments, etc."""
    import json
    return json.dumps(comps, separators=(',', ':'))

# ── Segment → chain commands ──

def make_segment(b, is_waiting_room=False, is_four_quadrant=False):
    """
    Build the 4 chain CB commands for one barrel type.
    Returns list of 4 command strings: [tellraw, tp, clear, loot_give]

    is_waiting_room: TP player to dimension sky before clicking (Bastion, End City)
    is_four_quadrant: show 4 locate buttons NE/NW/SE/SW (End City)
    """
    cmds = []
    nbt_t = nbt_type(b)

    # Fixed dimension mapping
    dim_map = {
        "bastion": ("minecraft:the_nether", "minecraft:bastion_remnant"),
        "end_city": ("minecraft:the_end", "minecraft:end_city"),
        "stronghold": (None, "minecraft:stronghold"),
        "hdwgh": (None, None),
    }

    dim, structure = dim_map.get(b["type"], (None, None))

    # ── tellraw ──
    if b["type"] == "hdwgh":
        # HDWGH: no tellraw, just spreadplayers
        pass  # handled in action below
    elif is_four_quadrant and dim:
        # 4-quadrant locate buttons + LAND
        quadrants = [
            ("NE", "1000 ~ 1000"),
            ("NW", "1000 ~ -1000"),
            ("SE", "-1000 ~ 1000"),
            ("SW", "-1000 ~ -1000"),
        ]
        buttons = ",".join(
            '{"text":"[%s]","color":"aqua","bold":true,'
            '"click_event":{"action":"run_command","command":'
            '"/execute in %s positioned %s run locate structure %s"}}'
            % (label, dim, pos, structure)
            for label, pos in quadrants
        )
        land_cmd = f'"/execute in {dim} run spreadplayers ~ ~ 0 50 under 80 false @s"'
        tellraw = (
            f'run tellraw @p ["",{{"text":"[MPK] {b["name"]}  ","color":"{b["color"]}"}},'
            f'{buttons},'
            f'{{"text":"  ","color":"{b["color"]}"}},'
            f'{{"text":"[LAND]","color":"green","bold":true,'
            f'"click_event":{{"action":"run_command","command":{land_cmd}}}}}'
        )
        cmds.append(f"execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1,{nbt_t}] {tellraw}]")
    elif dim and structure:
        # Single locate + LAND
        locate_cmd = f'"/execute in {dim} run locate structure {structure}"'
        land_cmd = f'"/execute in {dim} run spreadplayers ~ ~ 0 50 under 80 false @s"'
        tellraw = (
            f'run tellraw @p ["",{{"text":"[MPK] {b["name"]}  ","color":"{b["color"]}"}},'
            f'{{"text":"[LOCATE]","color":"aqua","bold":true,'
            f'"click_event":{{"action":"run_command","command":{locate_cmd}}}}},'
            f'{{"text":"  ","color":"{b["color"]}"}},'
            f'{{"text":"[LAND]","color":"green","bold":true,'
            f'"click_event":{{"action":"run_command","command":{land_cmd}}}}}'
        )
        cmds.append(f"execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1,{nbt_t}] {tellraw}]")
    elif structure:
        # Overworld locate (stronghold) — no dimension change, no LAND needed
        locate_cmd = f'"/locate structure {structure}"'
        tellraw = (
            f'run tellraw @p ["",{{"text":"[MPK] {b["name"]}  ","color":"{b["color"]}"}},'
            f'{{"text":"[LOCATE]","color":"aqua","bold":true,'
            f'"click_event":{{"action":"run_command","command":{locate_cmd}}}}}'
        )
        cmds.append(f"execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1,{nbt_t}] {tellraw}]")

    # ── TP to waiting room ──
    if is_waiting_room and dim:
        cmds.append(
            f"execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1,{nbt_t}]"
            f" as @p in {dim} run tp @s 0 999999 0"
        )
    elif b["type"] == "hdwgh":
        # HDWGH: spreadplayers (acts as both tellraw-replacement and action)
        cmds.append(
            f"execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1,{nbt_t}]"
            f" run spreadplayers 0 0 0 50 under 160 false @p"
        )

    # ── clear ──
    cmds.append(
        f"execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1,{nbt_t}]"
        f" run clear @p"
    )

    # ── loot give ──
    loot = make_loot_cmd(b["items"])
    cmds.append(
        f"execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1,{nbt_t}]"
        f" run {loot}"
    )

    return cmds


# ── Build chain ──

def build_chain():
    """Returns list of all chain CB commands in order."""
    chain = []

    # C1: detect + tag mpk_active
    nb = nbt_barrel(None)  # generic barrel detection
    chain.append(
        f"execute if entity {SEL}{nb}]"
        f" unless entity @e[tag=mpk_active,tag=!mpk_used,limit=1]"
        f" run tag {SEL}{nb}] add mpk_active"
    )

    # difficulty easy (all types)
    chain.append(
        "execute if entity @e[tag=mpk_active,tag=!mpk_used,limit=1]"
        " run difficulty easy"
    )

    # Segments per barrel type
    waiting = {"bastion", "end_city"}  # types needing dimension TP
    four_q = {"end_city"}              # types needing 4-quadrant locate

    for b in ALL_BARRELS:
        t = b["type"]
        chain.extend(make_segment(b,
            is_waiting_room=(t in waiting),
            is_four_quadrant=(t in four_q),
        ))

    # Cleanup
    chain.append(
        "execute if entity @e[tag=mpk_active,limit=1]"
        " run tag @e[tag=mpk_active,limit=1] add mpk_used"
    )

    return chain


# ── Engine command ──

def build_engine(chain):
    tree = build_tree(chain)
    nb = nbt_barrel(None)
    return (
        f"execute if entity {SEL}{nb}]"
        f" unless data {S} {{built:1b}}"
        f" store success {S} built byte 1"
        f" run summon falling_block {SUMMON_HEIGHT} "
        + nbtlib.serialize_tag(tree)
    )


# ── Falling_block tree ──

def chain_layer(command):
    return Compound({
        "id": String("falling_block"),
        "Time": Int(0),
        "DropItem": Byte(0),
        "BlockState": Compound({
            "Name": String("minecraft:chain_command_block"),
            "Properties": Compound({"facing": String("up")}),
        }),
        "TileEntityData": Compound({
            "Command": String(command),
            "auto": Byte(1),
        }),
        "Passengers": List[Compound]([
            Compound({
                "id": String("armor_stand"),
                "Health": Short(0),
                "Marker": Byte(1),
                "Invisible": Byte(1),
                "NoGravity": Byte(1),
            }),
        ]),
    })

def build_tree(commands):
    root = chain_layer(commands[-1])
    for cmd in reversed(commands[:-1]):
        node = chain_layer(cmd)
        node["Passengers"][0]["Passengers"] = List[Compound]([root])
        root = node
    return root


# ── Item builders ──

def make_barrel(b):
    tag = Compound()
    tag["display"] = Compound({
        "Name": String('{"text":"' + b["name"] + '","color":"' + b["color"] + '"}'),
        "Lore": List[String]([String('"(+NBT)"')]),
    })
    bet, il = Compound(), List[Compound]()
    bet["id"] = String("minecraft:barrel")
    for e in b["items"]:
        it = Compound({"Slot": Byte(e["slot"]), "id": String(e["id"]),
                        "Count": Byte(e.get("count", 1))})
        # Prefer explicit tag; auto-convert components→tag for legacy NBT
        item_tag = e.get("tag")
        if not item_tag and e.get("components"):
            item_tag = _components_to_tag(e["components"])
        if item_tag:
            it["tag"] = _tag_cpd(item_tag)
        il.append(it)
    bet["Items"] = il
    tag["BlockEntityTag"] = bet
    tag["mpk"], tag["mpk_type"] = Byte(1), String(b["type"])
    return Compound({"id": String("minecraft:barrel"), "Count": Byte(1), "tag": tag})


def _components_to_tag(comps):
    """Convert 1.21 components dict → legacy tag dict (for DataVersion 3465 NBT)."""
    tag = {}
    # potion_contents → Potion
    pc = comps.get("minecraft:potion_contents")
    if pc and isinstance(pc, dict) and "potion" in pc:
        tag["Potion"] = pc["potion"]
    # enchantments → Enchantments (legacy format: [{id:..., lvl:...}])
    ench = comps.get("minecraft:enchantments")
    if ench and isinstance(ench, dict):
        levels = ench.get("levels", {})
        if levels:
            tag["Enchantments"] = [
                {"id": k, "lvl": v} for k, v in levels.items()
            ]
    # custom_data passes through
    cd = comps.get("minecraft:custom_data")
    if cd:
        tag.update(cd)
    return tag if tag else None

def _tag_cpd(d):
    c = Compound()
    for k, v in d.items():
        if isinstance(v, str): c[k] = String(v)
        elif isinstance(v, int): c[k] = Int(v)
        elif isinstance(v, bool): c[k] = Byte(1 if v else 0)
        elif isinstance(v, dict): c[k] = _tag_cpd(v)
        elif isinstance(v, list):
            lst = List[Compound]()
            for i in v:
                if isinstance(i, dict): lst.append(_tag_cpd(i))
                elif isinstance(i, str): lst.append(String(i))
                elif isinstance(i, int): lst.append(Int(i))
            c[k] = lst
    return c

def make_cb(item_id, display, command):
    return Compound({
        "id": String(item_id), "Count": Byte(1),
        "tag": Compound({
            "display": Compound({"Name": String(display)}),
            "BlockEntityTag": Compound({"Command": String(command), "auto": Byte(1)}),
        }),
    })

def air():
    return Compound({"id": String("minecraft:air"), "Count": Byte(1)})


# ── Build hotbar ──

def build_hotbar(chain):
    row0 = List[Compound]()
    for b in BARRELS:
        row0.append(make_barrel(b))
    # Fill empty slots up to ENGINE_SLOT-1
    while len(row0) < ENGINE_SLOT - 1:
        row0.append(air())
    # Engine CB
    eng_full = build_engine(chain)
    row0.append(make_cb("minecraft:repeating_command_block",
        '{"text":"TinyPracticeKit v0.1","bold":true,"color":"dark_aqua"}', eng_full))
    # Fill remaining slots
    while len(row0) < 9:
        row0.append(air())

    root = Compound()
    root["0"] = row0
    for r in range(1, 9):
        root[str(r)] = List[Compound]([air() for _ in range(9)])
    root["DataVersion"] = Int(DATA_VERSION)
    return root


# ── Main ──

def main(out="hotbar.nbt"):
    chain = build_chain()
    hotbar = build_hotbar(chain)
    nbtlib.File(hotbar).save(out, gzipped=False)
    eng_full = build_engine(chain)

    print(f"Engine: {len(eng_full)} chars, {len(chain)} chain CBs")
    print(f"Barrels: {len(BARRELS)} (slots 1-{len(BARRELS)}), Engine: slot {ENGINE_SLOT}")
    for i, cmd in enumerate(chain):
        print(f"  C{i+1:2d} {len(cmd):4d}c  {cmd[:120]}...")
    print(f"Saved: {out}")

if __name__ == "__main__":
    main()
