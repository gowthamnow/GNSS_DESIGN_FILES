import re

with open('GNSS.kicad_pcb', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

segments = re.findall(r'\(segment\s+', text)
vias = re.findall(r'\(via\s+', text)
zones = re.findall(r'\(zone\s+', text)
print(f"Total segments (tracks): {len(segments)}")
print(f"Total vias: {len(vias)}")
print(f"Total zones: {len(zones)}")
