import os, glob

# Look for template or default prl files in KiCad installation
kicad_dirs = [
    r'C:\Program Files\KiCad\8.0',
    r'C:\Program Files\KiCad\10.0',
    os.path.expandvars(r'%APPDATA%\kicad\8.0'),
    os.path.expandvars(r'%APPDATA%\kicad\10.0'),
]

for kd in kicad_dirs:
    if os.path.exists(kd):
        print(f"Searching in {kd}:")
        for root, dirs, files in os.walk(kd):
            for file in files:
                if file.endswith('.kicad_prl') or file.endswith('pcbnew.json') or file.endswith('pcbnew'):
                    p = os.path.join(root, file)
                    print("Found file:", p)
                    try:
                        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                            c = f.read()
                            if 'visible_items' in c:
                                print(f"  --> visible_items in {file}:")
                                import json, re
                                m = re.search(r'"visible_items":\s*\[[^\]]*\]', c)
                                if m:
                                    print("     ", m.group(0))
                    except Exception as e:
                        pass
