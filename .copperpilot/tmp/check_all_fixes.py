import xml.etree.ElementTree as ET
import json

tree = ET.parse('.copperpilot/tmp/review_v8_updated.xml')
root = tree.getroot()

comps = {}
for comp in root.findall('.//comp'):
    ref = comp.attrib.get('ref')
    val = comp.find('value').text if comp.find('value') is not None else ''
    fp = comp.find('footprint').text if comp.find('footprint') is not None else ''
    sheetpath = comp.find('sheetpath').attrib.get('names') if comp.find('sheetpath') is not None else ''
    comps[ref] = {'value': val, 'footprint': fp, 'sheetpath': sheetpath}

nets = {}
for net in root.findall('.//net'):
    name = net.attrib.get('name')
    nodes = []
    for node in net.findall('node'):
        nodes.append({
            'ref': node.attrib.get('ref'),
            'pin': node.attrib.get('pin'),
            'pinfunction': node.attrib.get('pinfunction', '')
        })
    nets[name] = nodes

print("=== CHECK PREVIOUS CRITICAL & MAJOR ISSUES ===")

# 1. Ground Plane Shorted to USB_SCL
print("\n1. Ground & USB_SCL:")
gnd_net = nets.get('GND', [])
usb_scl_net = nets.get('USB_SCL', [])
print(f"  GND nodes: {len(gnd_net)}")
print(f"  USB_SCL nodes: {len(usb_scl_net)} -> {usb_scl_net}")

# 2. USB Hub IC Power Rail Disconnected (+3V3_HUB vs +3.3V_HUB)
print("\n2. USB Hub Power Rail:")
hub_pwr = [k for k in nets.keys() if 'HUB' in k]
for k in hub_pwr:
    print(f"  Net '{k}' ({len(nets[k])} nodes): {nets[k]}")

# 3. STM32 Analog Ground (VSSA Pin 19)
print("\n3. STM32 VSSA Pin 19 & VREF- Pin 20:")
for netname, nodes in nets.items():
    for n in nodes:
        if n['ref'] == 'IC3' and n['pin'] in ['19', '20']:
            print(f"  IC3 pin {n['pin']} ({n['pinfunction']}): Net '{netname}'")

# 4. Ethernet Crystal Input Cap (C27)
print("\n4. Ethernet C27 value:")
print(f"  C27: {comps.get('C27')}")

# 5. RMII Reference Clock Loaded by RJ45 LED (R22)
print("\n5. Ethernet REFCLK net:")
for netname, nodes in nets.items():
    if 'REFCLK' in netname.upper() or '50M' in netname.upper():
        print(f"  Net '{netname}': {nodes}")
    for n in nodes:
        if n['ref'] == 'R22':
            print(f"  R22 in Net '{netname}': {n}")

# 6. DP83825 Thermal Ground Pad (EXP)
print("\n6. DP83825 U4 Thermal Pad:")
for netname, nodes in nets.items():
    for n in nodes:
        if n['ref'] == 'U4' and n['pin'] in ['25', '26', '27', '28', '29', '30']:
            print(f"  U4 Pin {n['pin']} ({n['pinfunction']}): Net '{netname}'")

# 7. STM32 GPIO Contention (PE7 vs PE9 on ETH_RST_N)
print("\n7. ETH_RST_N net:")
for netname, nodes in nets.items():
    if 'ETH_RST' in netname.upper():
        print(f"  Net '{netname}': {nodes}")

# 8. Arduino D2 & D3 on SWD lines
print("\n8. Arduino D2 & D3 and SWD lines:")
for netname, nodes in nets.items():
    if 'SWD' in netname.upper() or 'SWC' in netname.upper():
        print(f"  Net '{netname}': {nodes}")
for netname, nodes in nets.items():
    for n in nodes:
        if n['ref'] == 'A1' and n['pin'] in ['17', '18']:
            print(f"  A1 pin {n['pin']} ({n['pinfunction']}): Net '{netname}'")

# 9. Arduino Reset Pin
print("\n9. Arduino Reset Pin (A1 pin 3):")
for netname, nodes in nets.items():
    for n in nodes:
        if n['ref'] == 'A1' and n['pin'] == '3':
            print(f"  A1 pin 3 ({n['pinfunction']}): Net '{netname}'")

# 10. ESP32-C3 Enable RC Delay & Pull-ups
print("\n10. ESP_EN net:")
for netname, nodes in nets.items():
    if 'ESP_EN' in netname.upper() or 'CHIP_EN' in netname.upper():
        print(f"  Net '{netname}': {nodes}")

# 11. USB Hub Strapping (NON_REM1, NON_REM0)
print("\n11. USB Hub Strapping pins:")
for netname, nodes in nets.items():
    for n in nodes:
        if n['ref'] == 'IC1' and 'NON_REM' in n['pinfunction']:
            print(f"  IC1 pin {n['pin']} ({n['pinfunction']}): Net '{netname}'")

# 12. Ethernet MDC Pull-up (R49)
print("\n12. Ethernet MDC / MDIO:")
for netname, nodes in nets.items():
    if 'MDC' in netname.upper() or 'MDIO' in netname.upper():
        print(f"  Net '{netname}': {nodes}")

# 13. Ethernet Magnetics TD/RD Polarity
print("\n13. Ethernet RJ45 Magnetics T1:")
for netname, nodes in nets.items():
    for n in nodes:
        if n['ref'] == 'T1':
            print(f"  T1 pin {n['pin']} ({n['pinfunction']}): Net '{netname}'")

# 14. Buck Regulator UVLO Divider (R46 / R47)
print("\n14. Buck IR3883 U7 EN pin & R46 / R47:")
for netname, nodes in nets.items():
    for n in nodes:
        if n['ref'] in ['R46', 'R47', 'U7'] and (n['ref'] != 'U7' or n['pin'] == '5'):
            print(f"  {n['ref']} pin {n['pin']} ({n['pinfunction']}): Net '{netname}'")

# 15. Typo in 10]K resistors
print("\n15. Typo in resistor values (10]K):")
typo_res = [r for r, d in comps.items() if ']' in d['value']]
print(f"  Resistors with ']' in value ({len(typo_res)}): {typo_res}")
