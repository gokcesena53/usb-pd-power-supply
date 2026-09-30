import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb.bak', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
for p in parts[1:]:
    m = re.search(r'\(property\s+"Reference"\s+"(TP[1-8])"', p)
    if m:
        ref = m.group(1)
        ref_prop = re.search(r'\(property\s+"Reference".*?\n\t\t\)', p, re.DOTALL)
        print(f"=== {ref} ===")
        print(ref_prop.group(0) if ref_prop else "None")
