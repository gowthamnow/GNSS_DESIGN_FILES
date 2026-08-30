with open('.copperpilot/tmp/other_sheets_dump.txt', 'r', encoding='utf-8') as f:
    text = f.read()

ctrl_start = text.find('=== CONTROLLER ===')
ctrl_end = text.find('=== ETHERNET ===')
print(text[ctrl_start:ctrl_end])
