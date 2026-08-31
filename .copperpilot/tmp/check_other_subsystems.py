import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

# Let's inspect Power_sch in detail
print("=== POWER SCHEMATIC ===")
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    for node in net.findall('node'):
        ref = node.attrib.get('ref')
        if ref in ['U7', 'R46', 'R47', 'U9', 'VR1', 'U6']:
            print(f"  {ref}.{node.attrib.get('pin')} in Net '{name}'")

# Let's inspect Arduino_sch in detail
print("\n=== ARDUINO SCHEMATIC ===")
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    for node in net.findall('node'):
        ref = node.attrib.get('ref')
        if ref in ['A1', 'J5']:
            print(f"  {ref}.{node.attrib.get('pin')}({node.attrib.get('pinfunction','')}) in Net '{name}'")

# Let's inspect Ethernet_sch in detail
print("\n=== ETHERNET SCHEMATIC ===")
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    for node in net.findall('node'):
        ref = node.attrib.get('ref')
        if ref in ['U4', 'T1', 'Y1', 'R22', 'R23', 'R48', 'R49', 'R50']:
            print(f"  {ref}.{node.attrib.get('pin')}({node.attrib.get('pinfunction','')}) in Net '{name}'")
