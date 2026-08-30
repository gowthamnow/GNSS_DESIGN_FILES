with open('Controller.kicad_sch', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Controller.kicad_sch lines 7100-7160:")
for i in range(7100, min(len(lines), 7160)):
    print(f"{i+1:5}: {lines[i]}", end='')

with open('USB_HUB_sch.kicad_sch', 'r', encoding='utf-8') as f:
    lines_hub = f.readlines()

print("\nUSB_HUB_sch.kicad_sch lines 4080-4130:")
for i in range(4080, min(len(lines_hub), 4130)):
    print(f"{i+1:5}: {lines_hub[i]}", end='')
