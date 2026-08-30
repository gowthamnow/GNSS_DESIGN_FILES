import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review.xml')
root = tree.getroot()

comps = {}
for comp in root.findall('.//comp'):
    ref = comp.get('ref')
    val = comp.find('value').text if comp.find('value') is not None else ''
    fp = comp.find('footprint').text if comp.find('footprint') is not None else ''
    sheet = comp.find('sheetpath').get('names') if comp.find('sheetpath') is not None else ''
    comps[ref] = {'val': val, 'fp': fp, 'sheet': sheet, 'pins': {}}

for net in root.findall('.//net'):
    net_name = net.get('name')
    for node in net.findall('node'):
        ref = node.get('ref')
        pin = node.get('pin')
        pfunc = node.get('pfunction', '')
        ptype = node.get('ptype', '')
        if ref in comps:
            comps[ref]['pins'][pin] = (net_name, pfunc, ptype)

def dump_sheet_comps(sheet_name):
    print(f"\n=======================================================================")
    print(f"=== SHEET: {sheet_name} ===")
    print(f"=======================================================================")
    sheet_comps = [r for r, d in comps.items() if d['sheet'] == sheet_name]
    for ref in sorted(sheet_comps, key=lambda x: (0, int(x[1:])) if x[1:].isdigit() else (1, x)):
        d = comps[ref]
        print(f"\n--- {ref}: {d['val']} [{d['fp']}] ---")
        for pin in sorted(d['pins'].keys(), key=lambda x: (0, int(x)) if x.isdigit() else (1, str(x))):
            net, pfunc, ptype = d['pins'][pin]
            print(f"  Pin {pin:6} | {pfunc:25} | {ptype:12} -> {net}")

with open('.copperpilot/tmp/full_detailed_by_sheet.txt', 'w', encoding='utf-8') as f:
    import sys
    orig_stdout = sys.stdout
    sys.stdout = f
    for s in ['/Controller/', '/Ethernet/', '/ESP/', '/IMU/', '/Arduino/', '/USB_HUB/', '/ZED_Z9P/', '/Power/']:
        dump_sheet_comps(s)
    sys.stdout = orig_stdout

print("Saved full_detailed_by_sheet.txt successfully.")
