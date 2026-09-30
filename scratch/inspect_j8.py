import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
for p in parts[1:]:
    if re.search(r'\(property\s+"Reference"\s+"J8"', p):
        # find fp_rect and pads
        for match in re.finditer(r'\((fp_rect|pad)\s+.*?\n\t\t\)', p, re.DOTALL):
            print(match.group(0))
