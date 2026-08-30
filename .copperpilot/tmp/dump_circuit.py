import xml.etree.ElementTree as ET

tree = ET.parse('.copperpilot/tmp/review.xml')
root = tree.getroot()

# Map component ref to info
comps = {}
for comp in root.findall('.//comp'):
    ref = comp.get('ref')
    val = comp.find('value').text if comp.find('value') is not None else ''
    fp = comp.find('footprint').text if comp.find('footprint') is not None else ''
    sheet = comp.find('sheetpath').get('names') if comp.find('sheetpath') is not None else ''
    comps[ref] = {'val': val, 'fp': fp, 'sheet': sheet, 'pins': {}}

# Map nets
nets = {}
for net in root.findall('.//net'):
    net_name = net.get('name')
    nets[net_name] = []
    for node in net.findall('node'):
        ref = node.get('ref')
        pin = node.get('pin')
        pfunction = node.get('pfunction', '')
        ptype = node.get('ptype', '')
        nets[net_name].append((ref, pin, pfunction, ptype))
        if ref in comps:
            comps[ref]['pins'][pin] = (net_name, pfunction, ptype)

def dump_sheet(sheet_name):
    print(f"\n=======================================================")
    print(f" SHEET: {sheet_name}")
    print(f"=======================================================")
    sheet_comps = [r for r, d in comps.items() if d['sheet'] == sheet_name]
    for ref in sorted(sheet_comps):
        d = comps[ref]
        print(f"\n--- {ref} ({d['val']}) [{d['fp']}] ---")
        for pin in sorted(d['pins'].keys(), key=lambda x: (0, int(x)) if x.isdigit() else (1, str(x))):
            net, pfunc, ptype = d['pins'][pin]
            print(f"  Pin {pin:4} | {pfunc:20} | {ptype:12} -> {net}")

with open('.copperpilot/tmp/sheet_names.txt', 'w') as f:
    unique_sheets = sorted(list(set(d['sheet'] for d in comps.values())))
    for s in unique_sheets:
        f.write(s + '\n')
    print("Unique sheets:", unique_sheets)

# Let's inspect each sheet
for s in sorted(list(set(d['sheet'] for d in comps.values()))):
    dump_sheet(s)
