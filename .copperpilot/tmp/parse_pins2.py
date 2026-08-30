fn = r'GNSS_LIBRARY\LIB_STM32H563VGT6\STM32H563VGT6\KiCad\STM32H563VGT6.kicad_sym'
with open(fn, 'r', encoding='utf-8') as f:
    text = f.read()

import re
pins = re.findall(r'\(pin\s+([^\s]+)\s+([^\s]+)\s+\(at\s+[\d\.-]+\s+[\d\.-]+\s+[\d\.-]+\)\s+\(length\s+[\d\.-]+\)\s+\(name\s+"([^"]+)"[\s\S]*?\(number\s+"([^"]+)"', text)
print(f"Total pins matched: {len(pins)}")
for ptype, pshape, pname, pnum in sorted(pins, key=lambda x: (0, int(x[3])) if x[3].isdigit() else (1, x[3])):
    print(f"Pin {pnum:4} : {pname:35} ({ptype})")
