import re

with open('ZED_Z9P.kicad_sch', 'r', encoding='utf-8') as f:
    sch_content = f.read()

print("Length of ZED_Z9P.kicad_sch:", len(sch_content))

# Extract all symbol instances with their reference, value, position, and pin connections
symbols = re.findall(r'\(symbol\s+\(lib_id "([^"]+)"\)\s+\(at ([\d\.\-]+) ([\d\.\-]+)[^\)]*\)[\s\S]*?\(property "Reference" "([^"]+)"[\s\S]*?\(property "Value" "([^"]+)"[\s\S]*?\)', sch_content)
print(f"Found {len(symbols)} symbols")
for s in symbols:
    print(f"  Ref: {s[3]}, Val: {s[4]}, Lib: {s[0]} at ({s[1]}, {s[2]})")

# Extract all labels
labels = re.findall(r'\(label "([^"]+)"\s+\(at ([\d\.\-]+) ([\d\.\-]+)', sch_content)
print(f"\nFound {len(labels)} local labels:")
for l in labels:
    print(f"  Label: {l[0]} at ({l[1]}, {l[2]})")

global_labels = re.findall(r'\(global_label "([^"]+)"\s+\(shape [^\)]+\)\s+\(at ([\d\.\-]+) ([\d\.\-]+)', sch_content)
print(f"\nFound {len(global_labels)} global labels:")
for gl in global_labels:
    print(f"  Global Label: {gl[0]} at ({gl[1]}, {gl[2]})")
