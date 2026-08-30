import glob
import re

for fn in glob.glob('GNSS_LIBRARY/**/*.kicad_sym', recursive=True):
    with open(fn, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    if 'STM32H563' in c:
        print(f"Found STM32H563 in {fn}")
        pins = re.findall(r'\(pin\s+([^\s]+)\s+([^\s]+)\s+\(at[^)]+\)\s+\(length[^)]+\)\s*\(name\s+"([^"]+)"[^\)]*\)\s*\(number\s+"([^"]+)"', c)
        for ptype, pshape, pname, pnum in sorted(pins, key=lambda x: (0, int(x[3])) if x[3].isdigit() else (1, x[3])):
            print(f"  Pin {pnum:4} | {pname:25} | {ptype}")
