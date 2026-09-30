import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb.bak', 'r', encoding='utf-8') as f:
    text = f.read()

parts = re.split(r'\n\s*\(footprint\s+', text)
for p in parts[1:]:
    for i in range(1, 6):
        if f'(property "Reference" "TP{i}"' in p:
            at = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
            layer = re.search(r'\(layer\s+"([^"]+)"\)', p)
            print(f"TP{i}: ({at.group(1)}, {at.group(2)}) on {layer.group(1)}")
