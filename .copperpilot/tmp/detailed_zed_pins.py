import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

def get_net_of_pin(comp_ref, pin_num):
    for net in root.findall('.//net'):
        for node in net.findall('node'):
            if node.attrib.get('ref') == comp_ref and node.attrib.get('pin') == str(pin_num):
                return net.attrib.get('name')
    return None

components = ['IC2', 'U13', 'U14', 'Q1', 'Q2', 'L3', 'J4', 'D1', 'C71', 'R32', 'R80', 'R81', 'R82', 'R83', 'R84', 'R85', 'R86', 'FL9', 'VR1']

for comp in components:
    print(f"=== {comp} ===")
    for net in root.findall('.//net'):
        for node in net.findall('node'):
            if node.attrib.get('ref') == comp:
                print(f"  Pin {node.attrib.get('pin')} ({node.attrib.get('pinfunction', '')}): Net '{net.attrib.get('name')}'")
