import os
import re

sch_files = [f for f in os.listdir('.') if f.endswith('.kicad_sch')]

print("=== SEARCHING FOR USB_SCL IN SCHEMATIC FILES ===")
for sf in sch_files:
    with open(sf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if 'USB_SCL' in content:
        print(f"\n--- File: {sf} ---")
        for line in content.splitlines():
            if 'USB_SCL' in line:
                print(f"  {line.strip()}")
