import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

print("=== SEARCH FOR OSC NET & MCU PINS ===")
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    if 'OSC' in name.upper():
        print(f"Net '{name}':")
        for node in net.findall('node'):
            print(f"  {node.attrib.get('ref')}.{node.attrib.get('pin')} ({node.attrib.get('pinfunction','')})")

print("\n=== IC3 (STM32) OSC PINS ===")
for comp in root.findall('.//comp'):
    if comp.attrib.get('ref') == 'IC3':
        for net in root.findall('.//net'):
            for node in net.findall('node'):
                if node.attrib.get('ref') == 'IC3' and ('OSC' in node.attrib.get('pinfunction','').upper() or 'PH0' in node.attrib.get('pinfunction','').upper() or 'PH1' in node.attrib.get('pinfunction','').upper()):
                    print(f"  IC3 Pin {node.attrib.get('pin')} ({node.attrib.get('pinfunction')}): Net '{net.attrib.get('name')}'")
