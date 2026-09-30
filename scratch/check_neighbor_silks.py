import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
for ref_target in ['C13', 'Q8', 'L1']:
    for p in parts[1:]:
        if f'(property "Reference" "{ref_target}"' in p:
            at_fp = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
            ref_prop = re.search(r'\(property\s+"Reference".*?\n\t\t\)', p, re.DOTALL)
            print(f"=== {ref_target} at ({at_fp.group(1)}, {at_fp.group(2)}) ===")
            print(ref_prop.group(0) if ref_prop else "None")
