with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lines = text.splitlines()
for i, l in enumerate(lines):
    if 'B.CrtYd' in l:
        print(f"Line {i}: {l.strip()}")
        for sub in lines[max(0, i-5):min(len(lines), i+15)]:
            if 'Reference' in sub:
                print(f"  Owner: {sub.strip()}")
