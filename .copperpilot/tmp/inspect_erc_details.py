import json

with open('.copperpilot/tmp/review_erc_v8.json', 'r', encoding='utf-8') as f:
    erc = json.load(f)

all_v = []
for s in erc.get('sheets', []):
    sheet_name = s.get('name', '')
    sheet_path = s.get('path', '')
    for v in s.get('violations', []):
        v['sheet_name'] = sheet_name
        v['sheet_path'] = sheet_path
        all_v.append(v)

print("=== MULTIPLE NET NAMES ===")
for v in all_v:
    if v.get('type') == 'multiple_net_names':
        print(f"Sheet: {v['sheet_name']}, Description: {v.get('description')}")
        for item in v.get('items', []):
            print(f"  Item: {item}")

print("\n=== DANGLING LABELS ===")
for v in all_v:
    if v.get('type') == 'label_dangling':
        print(f"Sheet: {v['sheet_name']}, Description: {v.get('description')}")
        for item in v.get('items', []):
            print(f"  Item: {item}")

print("\n=== NO CONNECT VIOLATIONS ===")
for v in all_v:
    if 'no_connect' in v.get('type'):
        print(f"Type: {v.get('type')}, Sheet: {v['sheet_name']}, Description: {v.get('description')}")
        for item in v.get('items', []):
            print(f"  Item: {item}")

print("\n=== POWER PIN NOT DRIVEN ===")
for v in all_v:
    if v.get('type') == 'power_pin_not_driven':
        print(f"Sheet: {v['sheet_name']}, Description: {v.get('description')}")
        for item in v.get('items', []):
            print(f"  Item: {item}")

print("\n=== SAMPLE PIN_TO_PIN (Errors / Unique Descriptions) ===")
unique_p2p = {}
for v in all_v:
    if v.get('type') == 'pin_to_pin':
        desc = v.get('description')
        severity = v.get('severity')
        key = (severity, desc)
        if key not in unique_p2p:
            unique_p2p[key] = []
        unique_p2p[key].append(v)

print(f"Unique pin-to-pin combinations count: {len(unique_p2p)}")
for (sev, desc), vlist in unique_p2p.items():
    print(f"[{sev}] ({len(vlist)} occurrences) {desc}")
    # print one example
    ex = vlist[0]
    print(f"   Example on sheet {ex['sheet_name']}:")
    for item in ex.get('items', []):
        print(f"     {item}")
