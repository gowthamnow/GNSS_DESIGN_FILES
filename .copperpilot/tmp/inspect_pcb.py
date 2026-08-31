import re

with open('GNSS.kicad_pcb', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("File length:", len(text))
lines = text.splitlines()
print("First 20 lines:")
for l in lines[:20]:
    print("  ", l)

# Search for footprint entries
# In KiCad 7/8/9/10: (footprint "..." ... or (module ...
fps = re.findall(r'\((?:footprint|module)\s+"?([^"\s\)]+)"?', text)
print(f"\nTotal footprints found: {len(fps)}")

# Extract footprint blocks to check references and coordinates
# Let's find all (footprint ...) or (module ...)
fp_blocks = []
in_fp = False
curr_block = []
paren_count = 0

for line in lines:
    if line.strip().startswith('(footprint ') or line.strip().startswith('(module '):
        in_fp = True
        paren_count = 0
        curr_block = [line]
        paren_count += line.count('(') - line.count(')')
        if paren_count == 0:
            fp_blocks.append('\n'.join(curr_block))
            in_fp = False
    elif in_fp:
        curr_block.append(line)
        paren_count += line.count('(') - line.count(')')
        if paren_count <= 0:
            fp_blocks.append('\n'.join(curr_block))
            in_fp = False

print(f"Extracted {len(fp_blocks)} footprint blocks")

positions = []
refs = []
layers = []

for block in fp_blocks:
    # Reference
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if not m_ref:
        m_ref = re.search(r'\(fp_text\s+reference\s+"?([^"\s\)]+)"?', block)
    ref = m_ref.group(1) if m_ref else "UNKNOWN"
    refs.append(ref)
    
    # Layer
    m_layer = re.search(r'\(layer\s+"?([^"\s\)]+)"?', block)
    layer = m_layer.group(1) if m_layer else "UNKNOWN"
    layers.append(layer)
    
    # (at X Y ...) for the footprint
    # Typically first (at ...) right after (footprint ...) / (layer ...)
    m_at = re.search(r'\(at\s+([-0-9.]+)\s+([-0-9.]+)(?:\s+([-0-9.]+))?\)', block)
    if m_at:
        positions.append((float(m_at.group(1)), float(m_at.group(2)), ref, layer))

print(f"\nTotal positioned footprints: {len(positions)}")
if positions:
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]
    print(f"X coordinate range: min={min(xs)}, max={max(xs)}")
    print(f"Y coordinate range: min={min(ys)}, max={max(ys)}")
    print("\nSample footprint coordinates:")
    for p in positions[:20]:
        print(f"  {p[2]}: at ({p[0]}, {p[1]}) on {p[3]}")

# Check Edge.Cuts
edge_cuts = [l for l in lines if 'Edge.Cuts' in l]
print(f"\nEdge.Cuts lines count: {len(edge_cuts)}")
for l in edge_cuts[:10]:
    print("  ", l)

# Check setup / visibility / display settings in kicad_pcb
setup_lines = []
in_setup = False
for l in lines:
    if l.strip().startswith('(setup'):
        in_setup = True
    if in_setup:
        setup_lines.append(l)
        if l.strip() == ')' and in_setup:
            # check paren balance or end of setup
            pass

print("\nChecking layers in setup / file:")
layer_defs = [l for l in lines if '(0 "' in l or '(31 "' in l or 'F.Cu' in l or 'B.Cu' in l or 'F.SilkS' in l]
for l in layer_defs[:15]:
    print("  ", l)
