import re

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

symbols_to_find = ['Device:D_Schottky', 'Device:D_Zener', 'Device:LED', 'Power_Path_Custom:SMBJ30A', 'Device:D']

for sym in symbols_to_find:
    pattern = r'\(symbol\s+\"' + re.escape(sym) + r'\".*?\n\t\t\)'
    m = re.search(pattern, text, re.DOTALL)
    if m:
        block = m.group(0)
        print(f"================ {sym} ================")
        for pin in re.finditer(r'\(pin\s+([^\s]+)\s+([^\s]+)\s+\(at[^)]+\)\s+\(length[^)]+\)\s+\(name\s+\"([^\"]+)\"[^)]*\)\s+\(number\s+\"([^\"]+)\"', block):
            print(f"  Pin {pin.group(4)}: Name='{pin.group(3)}', Type={pin.group(1)}/{pin.group(2)}")
    else:
        print(f"Not found: {sym}")
