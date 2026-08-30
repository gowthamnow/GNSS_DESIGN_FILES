with open('.copperpilot/tmp/sheets_detailed.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
sheets = re.findall(r'SHEET:\s+([^\n]+)', text)
print("Sheets found in sheets_detailed.txt:", sheets)
