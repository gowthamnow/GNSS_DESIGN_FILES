# Let's inspect visible_items in KiCad
# In KiCad PCB Editor (pcbnew):
# The "Appearance" panel -> "Objects" tab controls object visibility (Pads, Vias, Tracks, Footprints Front/Back, etc.)
# Each object type has an ID (e.g., enum PCB_VISIBLE).
# When visible_items contains only [ 12 ], only item ID 12 is visible and ALL other items (Pads, Tracks, Footprints, References, Values, Text) are turned OFF / UNCHECKED!

import json

with open('GNSS.kicad_prl', 'r', encoding='utf-8') as f:
    prl = json.load(f)

print("Full board config in GNSS.kicad_prl:")
print(json.dumps(prl.get('board', {}), indent=2))
