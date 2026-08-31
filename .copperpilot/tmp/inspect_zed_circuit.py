import xml.etree.ElementTree as ET
import json

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

# Let's inspect components in /ZED_Z9P sheet
zed_comps = []
for comp in root.findall('.//comp'):
    sheetpath = comp.find('sheetpath').attrib.get('names') if comp.find('sheetpath') is not None else ''
    ref = comp.attrib.get('ref')
    val = comp.find('value').text if comp.find('value') is not None else ''
    fp = comp.find('footprint').text if comp.find('footprint') is not None else ''
    if 'ZED' in sheetpath:
        zed_comps.append((ref, val, fp))

print(f"ZED_Z9P components ({len(zed_comps)}):")
for r, v, f in sorted(zed_comps):
    print(f"  {r}: {v} ({f})")

# Let's inspect all nets connecting to ZED_Z9P components
zed_refs = {r for r, v, f in zed_comps}
print("\n--- Nets in ZED_Z9P ---")
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    nodes = []
    has_zed = False
    for node in net.findall('node'):
        r = node.attrib.get('ref')
        p = node.attrib.get('pin')
        fn = node.attrib.get('pinfunction', '')
        nodes.append(f"{r}.{p}({fn})")
        if r in zed_refs:
            has_zed = True
    if has_zed:
        print(f"Net '{name}': {', '.join(nodes)}")
