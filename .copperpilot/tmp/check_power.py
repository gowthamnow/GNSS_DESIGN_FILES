import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review.xml')
root = tree.getroot()

def get_comp_pins(comp_ref):
    comp = root.find(f".//comp[@ref='{comp_ref}']")
    val = comp.find('value').text if comp.find('value') is not None else ''
    fp = comp.find('footprint').text if comp.find('footprint') is not None else ''
    sheet = comp.find('sheetpath').get('names') if comp.find('sheetpath') is not None else ''
    pins = {}
    for net in root.findall('.//net'):
        net_name = net.get('name')
        for node in net.findall('node'):
            if node.get('ref') == comp_ref:
                pins[node.get('pin')] = (net_name, node.get('pfunction', ''), node.get('ptype', ''))
    return val, fp, sheet, pins

def print_comp(ref):
    val, fp, sheet, pins = get_comp_pins(ref)
    print(f"=== {ref}: {val} ({fp}) [Sheet: {sheet}] ===")
    for pin in sorted(pins.keys(), key=lambda x: (0, int(x)) if x.isdigit() else (1, str(x))):
        net, func, ptype = pins[pin]
        print(f"  Pin {pin:4} | {func:20} | {ptype:12} -> {net}")

print("--- POWER SECTION COMPONENTS ---")
for ref in ['J1', 'J2', 'F1', 'F2', 'D3', 'D4', 'U2', 'U9', 'U7', 'U6', 'VR1', 'L1', 'R1', 'R2', 'R3', 'R4', 'R11', 'R12', 'R13', 'R14', 'R31', 'R46', 'R47', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'FL6', 'FL7', 'FL8', 'TP1', 'TP2', 'TP4', 'TP5', 'TP12']:
    print_comp(ref)
