import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

for comp in root.findall('.//comp'):
    if comp.attrib.get('ref') == 'Q1':
        print("Comp Q1:")
        for child in comp:
            print(f"  {child.tag}: {child.attrib} {child.text}")

for net in root.findall('.//net'):
    for node in net.findall('node'):
        if node.attrib.get('ref') == 'Q1':
            print(f"Net {net.attrib.get('name')}: pin {node.attrib.get('pin')} pinfunction {node.attrib.get('pinfunction')}")
