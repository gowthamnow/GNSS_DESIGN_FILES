import re

with open('Controller.kicad_sch', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search all symbols in Controller.kicad_sch
for m in re.finditer(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)\s+([\d\.-]+)\)(.*?)\(property "Reference" "([^"]+)"', content, re.DOTALL):
    lib_id, x, y, rot, rest, ref = m.group(1), float(m.group(2)), float(m.group(3)), m.group(4), m.group(5), m.group(6)
    if abs(x - 264.16) < 30 and abs(y - 142.24) < 30:
        print(f"Symbol {ref} ({lib_id}) at ({x}, {y})")

# Let's search all wires touching (264.16, 142.24)
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\)', content)
for x1, y1, x2, y2 in wires:
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    if (abs(x1 - 264.16) < 1 and abs(y1 - 142.24) < 1) or (abs(x2 - 264.16) < 1 and abs(y2 - 142.24) < 1):
        print(f"Wire connected to (264.16, 142.24): ({x1}, {y1}) -> ({x2}, {y2})")
