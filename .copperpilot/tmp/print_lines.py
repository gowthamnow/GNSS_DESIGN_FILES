with open('Controller.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print("Controller lines 7090-7150:")
for i in range(7089, min(len(lines), 7150)):
    print(f"{i+1:5}: {lines[i]}", end='')

with open('USB_HUB_sch.kicad_sch', 'r', encoding='utf-8') as f:
    lines_hub = f.readlines()
print("\nUSB_HUB lines 4070-4130:")
for i in range(4069, min(len(lines_hub), 4130)):
    print(f"{i+1:5}: {lines_hub[i]}", end='')
