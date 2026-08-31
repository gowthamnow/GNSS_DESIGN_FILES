import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

# Let's map all pins of U13, U14, Q1, Q2, IC2, L3, J4, D1, C71, R32, R80..R86
targets = ['U13', 'U14', 'Q1', 'Q2', 'IC2', 'L3', 'J4', 'D1', 'C71', 'R32', 'R80', 'R81', 'R82', 'R83', 'R84', 'R85', 'R86']

pin_map = {}
for comp in targets:
    pin_map[comp] = {}

for net in root.findall('.//net'):
    netname = net.attrib.get('name')
    for node in net.findall('node'):
        ref = node.attrib.get('ref')
        if ref in targets:
            pin = node.attrib.get('pin')
            pinfn = node.attrib.get('pinfunction', '')
            pin_map[ref][pin] = {'fn': pinfn, 'net': netname}

for comp, pins in pin_map.items():
    print(f"=== Component {comp} ===")
    for pin, info in sorted(pins.items(), key=lambda x: (len(x[0]), x[0])):
        print(f"  Pin {pin} ({info['fn']}): Net '{info['net']}'")
