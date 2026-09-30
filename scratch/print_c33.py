with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_c33 = False
depth = 0
for line in lines:
    if 'footprint "Power_Output_Custom:Korchip_DCL_H-Type_D19.0mm_P20.00mm_Horizontal"' in line:
        in_c33 = True
    if in_c33:
        print(line, end='')
        if line.startswith('\t)'):
            break
