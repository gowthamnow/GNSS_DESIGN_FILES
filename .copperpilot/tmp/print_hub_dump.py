with open('.copperpilot/tmp/circuit_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# find section for USB_HUB
hub_start = text.find('SHEET: /USB_HUB/')
hub_end = text.find('=======================================================', hub_start + 20)
print(text[hub_start:hub_end if hub_end != -1 else len(text)])
