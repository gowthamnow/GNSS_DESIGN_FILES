import re

def find_wire_connections(sch_file, x, y):
    with open(sch_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # In KiCad 8: (wire (pts (xy X1 Y1) (xy X2 Y2)) ...)
    # or (polyline (pts (xy X1 Y1) ...))
    print(f"\n--- Checking wires touching ({x}, {y}) in {sch_file} ---")
    wire_matches = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(xy\s+([\d\.-]+)\s+([\d\.-]+)\)\)', content)
    for x1, y1, x2, y2 in wire_matches:
        fx1, fy1, fx2, fy2 = float(x1), float(y1), float(x2), float(y2)
        if (abs(fx1 - x) < 0.01 and abs(fy1 - y) < 0.01) or (abs(fx2 - x) < 0.01 and abs(fy2 - y) < 0.01):
            print(f"  Connected wire: ({fx1}, {fy1}) <---> ({fx2}, {fy2})")

    # check symbols with pins at (x, y)
    # let's search (symbol ... (at sx sy rot) ... )
    for m in re.finditer(r'\(symbol\s+\(lib_id\s+"([^"]+)"\)\s+\(at\s+([\d\.-]+)\s+([\d\.-]+)\s+([\d\.-]+)\)[\s\S]*?\(property\s+"Reference"\s+"([^"]+)"[\s\S]*?\(property\s+"Value"\s+"([^"]+)"', content):
        lib_id, sx, sy, rot, ref, val = m.group(1), float(m.group(2)), float(m.group(3)), float(m.group(4)), m.group(5), m.group(6)
        if abs(sx - x) < 50 and abs(sy - y) < 50:
            print(f"  Near Symbol: {ref} ({val}, {lib_id}) at ({sx}, {sy}) rot {rot}")

find_wire_connections('Controller.kicad_sch', 264.16, 142.24)
find_wire_connections('USB_HUB_sch.kicad_sch', 168.91, 63.5)
