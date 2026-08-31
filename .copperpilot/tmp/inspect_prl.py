import json

try:
    with open('GNSS.kicad_prl', 'r', encoding='utf-8') as f:
        prl = json.load(f)
    print("GNSS.kicad_prl loaded successfully.")
    print("Keys in prl:", list(prl.keys()))
    if 'board' in prl:
        print("Board settings in prl:", json.dumps(prl['board'], indent=2)[:1000])
except Exception as e:
    print("Error reading GNSS.kicad_prl:", e)

try:
    with open('GNSS.kicad_pro', 'r', encoding='utf-8') as f:
        pro = json.load(f)
    print("\nGNSS.kicad_pro loaded successfully.")
    print("Keys in pro:", list(pro.keys()))
except Exception as e:
    print("Error reading GNSS.kicad_pro:", e)
