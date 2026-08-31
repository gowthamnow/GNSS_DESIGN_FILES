with open('GNSS.kicad_pcb', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
edge_elements = re.findall(r'\(gr_[a-z]+\s+[^\)]*Edge\.Cuts[^\)]*\)', text)
print(f"Edge.Cuts graphical elements found in PCB: {len(edge_elements)}")
for e in edge_elements:
    print("  ", e)
