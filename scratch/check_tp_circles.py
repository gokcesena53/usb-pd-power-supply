import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb.bak', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
for p in parts[1:]:
    m = re.search(r'\(property\s+"Reference"\s+"(TP[1-6])"', p)
    if m:
        ref = m.group(1)
        circles = re.findall(r'\(fp_circle.*?\n\t\t\)', p, re.DOTALL)
        print(f"=== {ref} circles ({len(circles)}) ===")
        for c in circles:
            print(c)
