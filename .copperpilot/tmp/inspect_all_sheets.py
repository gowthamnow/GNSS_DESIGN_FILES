with open('.copperpilot/tmp/circuit_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def print_sheet_section(name):
    start = text.find(f'SHEET: {name}')
    if start == -1:
        print(f"Sheet {name} not found!")
        return
    end = text.find('=======================================================', start + 20)
    print(f"\n#######################################################")
    print(text[start:end if end != -1 else len(text)])

for s in ['/ZED_Z9P/', '/Controller/', '/Ethernet/', '/ESP/', '/IMU/', '/Arduino/', '/Power/']:
    print_sheet_section(s)
