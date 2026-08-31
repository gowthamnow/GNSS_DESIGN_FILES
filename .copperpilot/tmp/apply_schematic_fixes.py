import os
import re

sch_path = os.path.abspath("ZED_Z9P.kicad_sch")
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update embedded SI1016CX symbol in lib_symbols
# Ensure Pin 4 is D1 and Pin 6 is S2
lines = text.splitlines(keepends=True)
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

text = "".join(lines)

# 2. Update R81 Value to 100R
# Find R81 instance
lines = text.splitlines(keepends=True)
for i in range(len(lines)):
    if '(property "Reference" "R81"' in lines[i]:
        for j in range(max(0, i-5), min(len(lines), i+10)):
            if '(property "Value" "10K"' in lines[j]:
                lines[j] = lines[j].replace('"10K"', '"100R"')
                print(f"Updated R81 Value to 100R (line {j+1})")
                break

text = "".join(lines)

# 3. Fix Wires
# Replace wire (218.44 82.55) -> (218.44 49.53) with (218.44 82.55) -> (218.44 44.45)
# Replace wire (218.44 49.53) -> (236.22 49.53) with (218.44 44.45) -> (236.22 44.45)
# Delete wire (217.17 76.2) -> (222.25 76.2)
# Delete wire (217.17 76.2) -> (217.17 96.52)
# Add wire (217.17 85.09) -> (217.17 96.52)
# Add power symbol or wire connecting U13 V+ / C72 to +3V3_GNSS (e.g. wire from (236.22 76.2) to (217.17 99.06) +3V3_GNSS or power symbol)

# Let's do structured regex replacement on wire blocks
# Pattern for a wire segment:
# (wire (pts (xy X1 Y1) (xy X2 Y2)) (stroke (width 0) (type default)) (uuid "UUID"))

def remove_wire(txt, x1, y1, x2, y2):
    # Match either order
    p1 = rf'\(wire\s+\(pts\s+\(xy\s+{x1}\s+{y1}\)\s+\(xy\s+{x2}\s+{y2}\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"[^"]+"\)\)\n'
    p2 = rf'\(wire\s+\(pts\s+\(xy\s+{x2}\s+{y2}\)\s+\(xy\s+{x1}\s+{y1}\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"[^"]+"\)\)\n'
    new_txt, c1 = re.subn(p1, '', txt)
    new_txt, c2 = re.subn(p2, '', new_txt)
    print(f"Removed wire ({x1}, {y1}) -> ({x2}, {y2}): {c1+c2} removed")
    return new_txt

def replace_wire(txt, old_x1, old_y1, old_x2, old_y2, new_x1, new_y1, new_x2, new_y2):
    p1 = rf'(\(wire\s+\(pts\s+\(xy\s+){old_x1}\s+{old_y1}(\)\s+\(xy\s+){old_x2}\s+{old_y2}(\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"[^"]+"\)\))'
    p2 = rf'(\(wire\s+\(pts\s+\(xy\s+){old_x2}\s+{old_y2}(\)\s+\(xy\s+){old_x1}\s+{old_y1}(\)\)\s+\(stroke[^)]+\)\s+\(uuid\s+"[^"]+"\)\))'
    sub1 = rf'\g<1>{new_x1} {new_y1}\g<2>{new_x2} {new_y2}\g<3>'
    new_txt, c1 = re.subn(p1, sub1, txt)
    if c1 == 0:
        new_txt, c2 = re.subn(p2, sub1, txt)
        print(f"Replaced wire: {c2} matched (reverse)")
    else:
        print(f"Replaced wire: {c1} matched")
    return new_txt

# Update Q1 Source 2 connection:
text = replace_wire(text, 218.44, 82.55, 218.44, 49.53, 218.44, 82.55, 218.44, 44.45)
text = replace_wire(text, 218.44, 49.53, 236.22, 49.53, 218.44, 44.45, 236.22, 44.45)

# Remove the short from ANT_SHORT_N to R81/R82 tap:
text = remove_wire(text, 217.17, 76.2, 222.25, 76.2)
text = remove_wire(text, 217.17, 76.2, 217.17, 96.52)

# Connect U14.OC (217.17, 85.09) to ANT_SHORT_N (217.17, 96.52)
# Add wire segment:
import uuid
wire_oc = f'  (wire (pts (xy 217.17 85.09) (xy 217.17 96.52)) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))\n'
wire_power_u13 = f'  (wire (pts (xy 236.22 76.2) (xy 247.65 74.93)) (stroke (width 0) (type default)) (uuid "{uuid.uuid4()}"))\n' # connects U13 V+ to +3V3_GNSS at R84.1

# Insert new wires before the last closing paren
idx = text.rfind(')')
text = text[:idx] + wire_oc + wire_power_u13 + text[idx:]

# Save updated schematic
with open(sch_path, "w", encoding="utf-8") as f:
    f.write(text)

print("ZED_Z9P.kicad_sch updated successfully!")
