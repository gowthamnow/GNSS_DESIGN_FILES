import json
import xml.etree.ElementTree as ET
import re

# Parse ERC
with open('.copperpilot/tmp/erc_v8_updated.json', 'r', encoding='utf-8') as f:
    erc_data = json.load(f)

sheets = erc_data.get('sheets', [])
print(f"ERC sheets count: {len(sheets)}")

violations_by_type = {}
for s in sheets:
    for v in s.get('violations', []):
        t = v.get('type', 'unknown')
        violations_by_type[t] = violations_by_type.get(t, 0) + 1

print("ERC violations by type:")
for t, c in sorted(violations_by_type.items(), key=lambda x: x[1], reverse=True):
    print(f"  {t}: {c}")

# Parse XML netlist
tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

components = {}
for comp in root.findall('.//comp'):
    ref = comp.attrib.get('ref')
    val = comp.find('value').text if comp.find('value') is not None else ''
    fp = comp.find('footprint').text if comp.find('footprint') is not None else ''
    sheetpath = comp.find('sheetpath').attrib.get('names') if comp.find('sheetpath') is not None else ''
    components[ref] = {'value': val, 'footprint': fp, 'sheetpath': sheetpath}

nets = {}
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    nodes = []
    for node in net.findall('node'):
        nodes.append({
            'ref': node.attrib.get('ref'),
            'pin': node.attrib.get('pin'),
            'pinfunction': node.attrib.get('pinfunction', '')
        })
    nets[name] = nodes

print(f"\nTotal components: {len(components)}")
print(f"Total nets: {len(nets)}")

# Check Ground nets and USB_SCL net
print("\n--- Check Ground / USB_SCL nets ---")
for netname, nodes in nets.items():
    if 'GND' in netname.upper() or 'SCL' in netname.upper():
        print(f"Net '{netname}': {len(nodes)} nodes")
        if len(nodes) < 10:
            print("  Nodes:", nodes)
