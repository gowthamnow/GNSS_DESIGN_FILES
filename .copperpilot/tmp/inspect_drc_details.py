import json

with open('.copperpilot/tmp/review_drc_v8.json', 'r', encoding='utf-8') as f:
    drc = json.load(f)

violations = drc.get('violations', [])
unconnected = drc.get('unconnected_items', [])

print(f"Total DRC Violations: {len(violations)}")
print(f"Total Unconnected Items: {len(unconnected)}")

# Group violations by type
by_type = {}
for v in violations:
    t = v.get('type')
    by_type.setdefault(t, []).append(v)

for t, vlist in by_type.items():
    print(f"\n--- {t} ({len(vlist)}) ---")
    for v in vlist[:3]:
        print(f"  [{v.get('severity')}] {v.get('description')}")
        for it in v.get('items', []):
            print(f"    Item: {it.get('description')}")

print("\n--- SAMPLE UNCONNECTED ITEMS (First 10) ---")
for item in unconnected[:10]:
    print(f"  {item.get('description')}")
    for it in item.get('items', []):
        print(f"    {it.get('description')} at {it.get('pos')}")
