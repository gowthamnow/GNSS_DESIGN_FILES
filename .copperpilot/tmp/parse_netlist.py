import xml.etree.ElementTree as ET
import os

tree = ET.parse('.copperpilot/tmp/review.xml')
root = tree.getroot()

print("=== COMPONENTS ===")
components = root.find('components')
comp_list = []
if components is not None:
    for comp in components.findall('comp'):
        ref = comp.get('ref')
        val = comp.find('value').text if comp.find('value') is not None else ''
        footprint = comp.find('footprint').text if comp.find('footprint') is not None else ''
        sheetpath = comp.find('sheetpath').get('names') if comp.find('sheetpath') is not None else ''
        comp_list.append((ref, val, footprint, sheetpath))
        print(f"{ref:10} | {val:25} | {sheetpath:25} | {footprint}")

print(f"\nTotal components: {len(comp_list)}")

print("\n=== NETS SUMMARY ===")
nets = root.find('nets')
if nets is not None:
    net_list = []
    for net in nets.findall('net'):
        code = net.get('code')
        name = net.get('name')
        nodes = net.findall('node')
        node_strs = [f"{n.get('ref')}.{n.get('pin')}" for n in nodes]
        net_list.append((name, len(nodes), node_strs))
    print(f"Total nets: {len(net_list)}")
    # print single-node nets (floating or unconnected)
    single_node_nets = [n for n in net_list if n[1] <= 1]
    print(f"\nSingle-node / Unconnected nets ({len(single_node_nets)}):")
    for name, count, nodes in single_node_nets:
        print(f"  {name:35} : {nodes}")
