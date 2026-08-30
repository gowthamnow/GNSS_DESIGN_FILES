with open('.copperpilot/tmp/sheets_detailed.txt', 'r', encoding='utf-8') as f:
    text = f.read()

zed_start = text.find('SHEET: /ZED_Z9P/')
zed_end = text.find('#######################################################', zed_start + 20)
print(text[zed_start:zed_end if zed_end != -1 else len(text)])
