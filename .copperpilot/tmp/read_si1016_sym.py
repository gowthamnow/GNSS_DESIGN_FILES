import os
import glob

for root, dirs, files in os.walk('GNSS_LIBRARY'):
    for f in files:
        if f.endswith('.kicad_sym') and 'SI1016' in root:
            p = os.path.join(root, f)
            print("Found sym file:", p)
            with open(p, 'r', encoding='utf-8') as sf:
                print(sf.read())
