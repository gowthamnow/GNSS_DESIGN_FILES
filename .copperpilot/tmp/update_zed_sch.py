import os
import re

sch_path = os.path.abspath("ZED_Z9P.kicad_sch")
print(f"Reading schematic: {sch_path}")

with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update embedded SI1016CX symbol in lib_symbols
# Replace pin 4 S2 -> D1, pin 6 D1 -> S2 in lib_symbols
text_updated = text
lines = text_updated.splitlines(keepends=True)
for i in range(len(lines)):
    if '(name "S2"' in lines[i]:
        for j in range(i, min(i+10, len(lines))):
            if '(number "4"' in lines[j]:
                lines[i] = lines[i].replace('"S2"', '"D1"')
                print(f"Updated embedded lib_symbol Pin 4 to D1 (line {i+1})")
                break
    elif '(name "D1"' in lines[i]:
        for j in range(i, min(i+10, len(lines))):
            if '(number "6"' in lines[j]:
                lines[i] = lines[i].replace('"D1"', '"S2"')
                print(f"Updated embedded lib_symbol Pin 6 to S2 (line {i+1})")
                break

text_updated = "".join(lines)

# 2. Update R81 Value from 10K to 100R
# Find R81 symbol instance
def update_r81_value(txt):
    # Match R81 symbol block
    pattern = r'(\(symbol\s+\(lib_id\s+"[^"]+"\)\s+\(at\s+222\.25\s+72\.39[\s\S]*?\(property\s+"Reference"\s+"R81"[\s\S]*?\(property\s+"Value"\s+)"10K"'
    new_txt, count = re.subn(pattern, r'\1"100R"', txt)
    print(f"Updated R81 Value to 100R: {count} occurrence(s)")
    return new_txt

text_updated = update_r81_value(text_updated)

# Let's inspect all wire segments in text_updated
with open(".copperpilot/tmp/zed_sch_interim.txt", "w", encoding="utf-8") as f:
    f.write(text_updated)

print("Step 1 & 2 completed.")
