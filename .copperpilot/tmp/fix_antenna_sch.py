import os
import re

sym_path = os.path.abspath(r"GNSS_LIBRARY/LIB_SI1016CX-T1-GE3/SI1016CX-T1-GE3/KiCad/SI1016CX-T1-GE3.kicad_sym")
print(f"Opening symbol: {sym_path}")

with open(sym_path, "r", encoding="utf-8") as f:
    sym_text = f.read()

# Replace Pin 4 name to D1 and Pin 6 name to S2
# In Vishay Si1016CX SC-89 package:
# Pin 1 = S1, Pin 2 = G1, Pin 3 = D2, Pin 4 = D1, Pin 5 = G2, Pin 6 = S2
sym_text = re.sub(r'\(name\s+"S2"\s+\(effects\s+\(font\s+\(size\s+1\.27\s+1\.27\)\)\)\s+\(number\s+"4"', 
                  '(name "D1"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "4"', 
                  sym_text)

# Also handle without line-breaks regex
lines = sym_text.splitlines(keepends=True)
for i in range(len(lines)):
    if '(name "S2"' in lines[i]:
        # check if near number "4"
        for j in range(i, min(i+10, len(lines))):
            if '(number "4"' in lines[j]:
                lines[i] = lines[i].replace('"S2"', '"D1"')
                print(f"Replaced S2 with D1 on pin 4 (line {i+1})")
                break
    elif '(name "D1"' in lines[i]:
        # check if near number "6"
        for j in range(i, min(i+10, len(lines))):
            if '(number "6"' in lines[j]:
                lines[i] = lines[i].replace('"D1"', '"S2"')
                print(f"Replaced D1 with S2 on pin 6 (line {i+1})")
                break

sym_text_updated = "".join(lines)
with open(sym_path, "w", encoding="utf-8") as f:
    f.write(sym_text_updated)

print("Symbol file written successfully!")
