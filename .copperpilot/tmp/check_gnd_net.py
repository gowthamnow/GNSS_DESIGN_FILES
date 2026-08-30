import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review.xml')
root = tree.getroot()

for net in root.findall('.//net'):
    name = net.get('name')
    nodes = net.findall('node')
    if 'SCL' in name or 'GND' in name or len(nodes) > 30:
        print(f"Net: {name} (Total nodes: {len(nodes)})")
        for node in nodes[:20]:
            print(f"   {node.get('ref')}.{node.get('pin')} ({node.get('pfunction', '')})")
        if len(nodes) > 20:
            print(f"   ... and {len(nodes) - 20} more nodes")
