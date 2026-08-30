fn = r'GNSS_LIBRARY\LIB_STM32H563VGT6\STM32H563VGT6\KiCad\STM32H563VGT6.kicad_sym'
with open(fn, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(min(len(lines), 70)):
    print(f"{i+1:3}: {lines[i]}", end='')
