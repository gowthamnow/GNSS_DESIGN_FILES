import re

with open('Controller.kicad_sch', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's find IC3 definition in Controller.kicad_sch
# In KiCad 8 symbols in lib_symbols contain pin definitions: (pin <type> <shape> (at ...) (length ...) (name "..." ...) (number "..." ...))
matches = re.findall(r'\(pin\s+([^\s]+)\s+([^\s]+)\s+\(at[^)]+\)\s+\(length[^)]+\)\s*\(name\s+"([^"]+)"[^\)]*\)\s*\(number\s+"([^"]+)"', content)
print(f"Found {len(matches)} pins in Controller.kicad_sch:")
for ptype, pshape, pname, pnum in sorted(matches, key=lambda x: (0, int(x[3])) if x[3].isdigit() else (1, x[3])):
    print(f"  Pin {pnum:4} | {pname:25} | {ptype}")
