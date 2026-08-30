import re

for sf in ['Controller.kicad_sch', 'USB_HUB_sch.kicad_sch']:
    with open(sf, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"\n==================== {sf} ====================")
    for i, line in enumerate(lines):
        if 'USB_SCL' in line:
            start = max(0, i - 15)
            end = min(len(lines), i + 20)
            print(f"--- Around line {i+1} ---")
            for j in range(start, end):
                print(f"{j+1:5}: {lines[j]}", end='')
