import json

with open('GNSS.kicad_prl', 'r', encoding='utf-8') as f:
    prl = json.load(f)

# Standard KiCad 8 visible items (strings / all objects enabled)
default_visible_items = [
    "vias",
    "footprint_text",
    "footprint_anchors",
    "ratsnest",
    "grid",
    "footprints_front",
    "footprints_back",
    "footprint_values",
    "footprint_references",
    "tracks",
    "drc_errors",
    "drawing_sheet",
    "bitmaps",
    "pads",
    "zones",
    "drc_warnings",
    "locked_item_shadows",
    "conflict_shadows",
    "shapes"
]

prl['board']['visible_items'] = default_visible_items
prl['board']['visible_layers'] = "fffffff_ffffffff"

with open('GNSS.kicad_prl', 'w', encoding='utf-8') as f:
    json.dump(prl, f, indent=2)

print("Updated GNSS.kicad_prl with full object visibility.")
