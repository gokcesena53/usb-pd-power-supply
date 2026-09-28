with open("hardware/gopo.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
lines = text.splitlines()
i = 0
while i < len(lines):
    if lines[i].strip().startswith('(footprint '):
        j = i
        depth = 0
        bl = []
        while j < len(lines):
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0: break
            j += 1
        bt = '\n'.join(lines[i:j+1])
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', bt)
        at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)', bt)
        layer_m = re.search(r'\(layer "([^"]+)"\)', bt)
        if ref_m and at_m and layer_m:
            ref = ref_m.group(1)
            x = float(at_m.group(1))
            y = float(at_m.group(2))
            layer = layer_m.group(1)
            if 55 <= x <= 75 and 68 <= y <= 77:
                print(f"{layer}: {ref:8} at ({x:6.2f}, {y:6.2f})")
        i = j + 1
    else:
        i += 1
