import json
import xml.etree.ElementTree as ET

print("=== Analyzing KiCad 8.0 ERC JSON ===")
with open('.copperpilot/tmp/review_erc_v8.json', 'r', encoding='utf-8') as f:
    erc = json.load(f)

print("Top-level keys in ERC JSON:", list(erc.keys()))
violations = erc.get('sheets', []) or erc.get('violations', []) or erc.get('schematic', {}).get('erc', [])
print("Number of violations/sheets:", len(violations))

# If sheets structure:
if 'sheets' in erc:
    all_v = []
    for s in erc['sheets']:
        all_v.extend(s.get('violations', []))
    print(f"Total violations across sheets: {len(all_v)}")
    v_types = {}
    for v in all_v:
        t = v.get('type')
        v_types[t] = v_types.get(t, 0) + 1
    for t, c in sorted(v_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {t}: {c}")

print("\n=== Analyzing KiCad 8.0 DRC JSON ===")
with open('.copperpilot/tmp/review_drc_v8.json', 'r', encoding='utf-8') as f:
    drc = json.load(f)

print("Top-level keys in DRC JSON:", list(drc.keys()))
drc_violations = drc.get('violations', [])
print("DRC violations count:", len(drc_violations))
drc_unconnected = drc.get('unconnected_items', [])
print("DRC unconnected count:", len(drc_unconnected))

drc_types = {}
for v in drc_violations:
    t = v.get('type')
    drc_types[t] = drc_types.get(t, 0) + 1
for t, c in sorted(drc_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {t}: {c}")
