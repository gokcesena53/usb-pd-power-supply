import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# find J8 block
lines = text.splitlines()
i = 0
while i < len(lines):
    if lines[i].strip().startswith('(footprint ') and 'Reference" "J8"' in "\n".join(lines[i:i+400]):
        j = i
        depth = 0
        bl = []
        while j < len(lines):
            bl.append(lines[j])
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0: break
            j += 1
        j8_text = "\n".join(bl)
        print("Found J8 block, length:", len(j8_text))
        # find keepout and courtyard lines
        for l in j8_text.splitlines():
            if any(k in l for k in ['zone', 'keepout', 'crtyd', 'fp_rect', 'fp_poly', 'at ']):
                print(" ", l[:100])
        break
    i += 1
