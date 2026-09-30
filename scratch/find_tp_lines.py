import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for target in ['TP9', 'TP10', 'TP11', 'TP12', 'TP13', 'TP14']:
    for i, l in enumerate(lines):
        if f'(property "Reference" "{target}"' in l:
            # find start of footprint
            start = i
            while start >= 0 and not lines[start].startswith('\t(footprint '):
                start -= 1
            # find end of footprint
            end = i
            paren_count = 0
            for j in range(start, len(lines)):
                paren_count += lines[j].count('(') - lines[j].count(')')
                if paren_count == 0:
                    end = j
                    break
            print(f"{target}: starts line {start+1}, ends line {end+1}, length={end - start + 1}")
