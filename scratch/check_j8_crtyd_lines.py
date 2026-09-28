with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lines = text.splitlines()
for i, l in enumerate(lines):
    if '(property "Reference" "J8"' in l:
        for sub in lines[max(0, i-50):min(len(lines), i+120)]:
            if 'crtyd' in sub.lower():
                print(sub.strip())
