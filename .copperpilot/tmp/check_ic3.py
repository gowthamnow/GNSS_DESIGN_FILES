import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review.xml')
root = tree.getroot()

print("=== ALL LABELS / NETS CONNECTED TO IC3 (STM32H563VGT6) ===")
for net in root.findall('.//net'):
    net_name = net.get('name')
    for node in net.findall('node'):
        if node.get('ref') == 'IC3':
            pin = node.get('pin')
            pfunc = node.get('pfunction', '')
            ptype = node.get('ptype', '')
            other_nodes = [f"{n.get('ref')}.{n.get('pin')}" for n in net.findall('node') if n.get('ref') != 'IC3']
            print(f"Pin {pin:4} | {pfunc:25} | {ptype:10} | Net: {net_name:30} -> Connected to: {other_nodes[:5]}")
