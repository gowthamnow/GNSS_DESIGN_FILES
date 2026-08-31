import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

print("=== CONTROLLER OSC & TCXO CIRCUIT ===")
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    for node in net.findall('node'):
        ref = node.attrib.get('ref')
        if ref in ['U8', 'C66', 'R22', 'IC3'] and (ref != 'IC3' or node.attrib.get('pin') in ['23', '24', '14']):
            print(f"  {ref}.{node.attrib.get('pin')}({node.attrib.get('pinfunction','')}) in Net '{name}'")
