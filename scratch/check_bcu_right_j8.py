import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
all_bcu = []
for p in parts[1:]:
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
    layer = layer_m.group(1) if layer_m else ''
    if layer == 'B.Cu':
        at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
        if at_m:
            x, y = float(at_m.group(1)), float(at_m.group(2))
            ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p).group(1)
            val = re.search(r'\(property\s+"Value"\s+"([^"]+)"', p).group(1)
            all_bcu.append((ref, val, x, y))

all_bcu.sort(key=lambda item: (item[3], item[2]))
print(f"Total components on B.Cu: {len(all_bcu)}")
for ref, val, x, y in all_bcu:
    print(f"  {ref:8s} ({val:15s}) @ ({x:6.2f}, {y:6.2f})")
