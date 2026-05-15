"""
Hotbar layout — which barrels go in which slot.
Change the order to rearrange barrels on the hotbar (Ctrl+1).

The last slot (9) is always the engine repeating command block.
Empty slots (air) fill the remaining positions between barrels and engine.
"""

# Order: slot 1, 2, 3, ... (left to right)
# Engine CB always goes in slot 9.

from project.config_barrels import BASTION, END_CITY, STRONGHOLD, HDWGH

# Barrels in hotbar order (slot 1, 2, 3, 4)
BARRELS = [BASTION, STRONGHOLD, END_CITY, HDWGH]

# Which slot the engine CB occupies (1-9, default 9)
ENGINE_SLOT = 9
