import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

last_fp_start = -1
for i, l in enumerate(lines):
    if l.startswith('\t(footprint '):
        last_fp_start = i

# find end of last footprint
paren_count = 0
last_fp_end = -1
for j in range(last_fp_start, len(lines)):
    paren_count += lines[j].count('(') - lines[j].count(')')
    if paren_count == 0:
        last_fp_end = j
        break

print(f"Last footprint: starts line {last_fp_start+1}, ends line {last_fp_end+1}")
print(f"Next line after last footprint ({last_fp_end+2}): {lines[last_fp_end+1].strip()}")
