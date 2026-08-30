# Let's search all .kicad_sch files for lines with "USB_SCL" and find why it's on GND
import glob

for fname in glob.glob('*.kicad_sch'):
    with open(fname, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        if 'USB_SCL' in l:
            print(f"File {fname} at line {i+1}: {l.strip()}")
            # print surrounding 5 lines
            for j in range(max(0, i-5), min(len(lines), i+6)):
                print(f"   {lines[j].strip()}")
