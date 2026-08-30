import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review.xml')
root = tree.getroot()

for net in root.findall('.//net'):
    name = net.get('name')
    if name == 'EXP':
        nodes = [f"{n.get('ref')}.{n.get('pin')}" for n in net.findall('node')]
        print(f"Net EXP nodes: {nodes}")
