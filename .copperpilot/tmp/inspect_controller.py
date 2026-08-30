with open('.copperpilot/tmp/full_detailed_by_sheet.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def get_sheet_text(sheet_name):
    start = text.find(f"=== SHEET: {sheet_name} ===")
    if start == -1:
        return ""
    end = text.find("=== SHEET: ", start + 20)
    return text[start:end if end != -1 else len(text)]

print(get_sheet_text('/Controller/'))
