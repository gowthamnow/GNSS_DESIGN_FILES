with open('.copperpilot/tmp/sheets_detailed.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def print_section(title, start_str, end_str):
    start = text.find(start_str)
    if start == -1:
        print(f"{title} not found")
        return
    end = text.find(end_str, start + 20)
    print(f"\n=======================================================")
    print(f"=== {title} ===")
    print(f"=======================================================")
    print(text[start:end if end != -1 else len(text)])

print_section("CONTROLLER", "SHEET: /Controller/", "SHEET: /Ethernet/")
print_section("ETHERNET", "SHEET: /Ethernet/", "SHEET: /ESP/")
print_section("ESP", "SHEET: /ESP/", "SHEET: /IMU/")
print_section("IMU", "SHEET: /IMU/", "SHEET: /Arduino/")
print_section("ARDUINO", "SHEET: /Arduino/", "SHEET: /Power/")
