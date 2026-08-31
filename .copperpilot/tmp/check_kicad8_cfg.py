import json

with open(r'C:\Users\SUBASRI\AppData\Roaming\kicad\8.0\pcbnew.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

print("pcbnew.json keys:", list(cfg.keys())[:20])
if 'board' in cfg:
    print("board in pcbnew.json:", json.dumps(cfg['board'], indent=2)[:1000])

# Check if there are defaults or visible_items in pcbnew.json
for k, v in cfg.items():
    if 'visible' in k.lower() or 'item' in k.lower() or 'appearance' in k.lower():
        print(f"Key {k}: {v}")
