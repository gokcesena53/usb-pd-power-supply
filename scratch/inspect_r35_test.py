with open("hardware/gopo_test.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
lines = text.splitlines()
for i, l in enumerate(lines):
    if '(property "Reference" "R35"' in l:
        for sub in lines[max(0, i-5):min(len(lines), i+15)]:
            print(sub)
