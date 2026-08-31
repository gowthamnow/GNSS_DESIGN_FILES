import json

with open('.copperpilot/tmp/erc_v8_updated.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total sheets: {len(data.get('sheets', []))}")

for sheet in data.get('sheets', []):
    violations = sheet.get('violations', [])
    non_pin_violations = [v for v in violations if v.get('type') != 'pin_to_pin']
    if non_pin_violations:
        print(f"\n--- Sheet: {sheet.get('name')} ({len(non_pin_violations)} violations) ---")
        for v in non_pin_violations:
            print(f"  Type: {v.get('type')}, Severity: {v.get('severity')}, Description: {v.get('description')}")
            for item in v.get('items', []):
                print(f"    Item: {item.get('pos')} | {item.get('text')}")
