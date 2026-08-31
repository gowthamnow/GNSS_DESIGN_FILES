import os, glob

s = os.path.getsize('.copperpilot/tmp/pcb_top.svg')
print(f"SVG file size: {s} bytes")
with open('.copperpilot/tmp/pcb_top.svg', 'r', encoding='utf-8') as f:
    text = f.read()
print(f"SVG lines: {len(text.splitlines())}")

# Let's also check all .pretty or .kicad_mod directories in GNSS_LIBRARY
mod_files = glob.glob('GNSS_LIBRARY/**/*.kicad_mod', recursive=True)
print(f"\nFound {len(mod_files)} footprint files (.kicad_mod) in GNSS_LIBRARY:")
for m in mod_files[:20]:
    print("  ", m)

# Let's check if we should create a comprehensive fp-lib-table
# In sym-lib-table:
with open('sym-lib-table', 'r', encoding='utf-8') as f:
    sym_tbl = f.read()
print("\nSym-lib-table entries count:", sym_tbl.count('(lib '))
