import re

def check_coords_in_file(sf, target_x, target_y):
    print(f"\nChecking around ({target_x}, {target_y}) in {sf}:")
    with open(sf, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # find wires, symbols, power symbols
    # wires: (wire (pts (xy x1 y1) (xy x2 y2)))
    wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\)', content)
    for x1, y1, x2, y2 in wires:
        x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
        if (abs(x1 - target_x) < 2 and abs(y1 - target_y) < 2) or (abs(x2 - target_x) < 2 and abs(y2 - target_y) < 2):
            print(f"  Wire: ({x1}, {y1}) -> ({x2}, {y2})")

    # symbols
    # (symbol (lib_id ...) (at x y rot) ... (property "Reference" "..." ...) ... )
    for m in re.finditer(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)', content):
        lib_id = m.group(1)
        sx, sy = float(m.group(2)), float(m.group(3))
        if abs(sx - target_x) < 15 and abs(sy - target_y) < 15:
            print(f"  Symbol near: {lib_id} at ({sx}, {sy})")

check_coords_in_file('Controller.kicad_sch', 264.16, 142.24)
check_coords_in_file('USB_HUB_sch.kicad_sch', 168.91, 63.5)
