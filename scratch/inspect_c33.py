with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '(property "Reference" "C33"' in line:
        print(''.join(lines[i+250:i+340]))
        break
