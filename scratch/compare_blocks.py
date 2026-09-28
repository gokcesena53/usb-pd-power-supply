with open("hardware/gopo.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Let's inspect R16 (which is F.Cu R_0402) vs R34
def get_block(ref, txt):
    lines = txt.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('(footprint '):
            j = i
            depth = 0
            while j < len(lines):
                depth += lines[j].count('(') - lines[j].count(')')
                if depth == 0: break
                j += 1
            bt = "\n".join(lines[i:j+1])
            if f'(property "Reference" "{ref}"' in bt:
                return bt
            i = j + 1
        else:
            i += 1
    return None

r16_block = get_block('R16', text)
r34_block = get_block('R34', text)
print("R16 block lines:", len(r16_block.splitlines()))
print("R34 block lines:", len(r34_block.splitlines()))
