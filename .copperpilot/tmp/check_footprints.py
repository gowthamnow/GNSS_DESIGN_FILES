import re, os, glob

with open('GNSS.kicad_pcb', 'r', encoding='utf-8', errors='ignore') as f:
    pcb_text = f.read()

# Extract footprints placed in PCB
fps_in_pcb = re.findall(r'\(footprint\s+"([^"]+)"', pcb_text)
print(f"Unique footprint types in PCB ({len(fps_in_pcb)} instances):")
for fp in sorted(set(fps_in_pcb)):
    print("  ", fp)

# Check schematic footprints across all .kicad_sch
sch_files = glob.glob('*.kicad_sch')
sch_fps = {}
for sch in sch_files:
    with open(sch, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    matches = re.findall(r'\(property\s+"Footprint"\s+"([^"]*)"', content)
    for m in matches:
        if m:
            sch_fps[m] = sch_fps.get(m, 0) + 1

print(f"\nUnique footprint types in Schematics ({len(sch_fps)} unique):")
for fp, count in sorted(sch_fps.items()):
    print(f"  {fp} ({count} symbols)")
