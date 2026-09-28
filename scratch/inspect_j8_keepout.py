import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
i = 0
while i < len(lines):
    if lines[i].strip().startswith('(footprint ') and 'Reference" "J8"' in "\n".join(lines[i:i+50]):
        j = i
        depth = 0
        bl = []
        while j < len(lines):
            bl.append(lines[j])
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0: break
            j += 1
        j8_text = "\n".join(bl)
        for l in bl:
            if any(k in l for k in ['layer', 'at', 'start', 'end', 'pts', 'xy', 'zone', 'keepout', 'crtyd']):
                print(l.strip()[:100])
        break
    i += 1
