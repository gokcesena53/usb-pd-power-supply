import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's check all footprints and pads on F.Cu with X in [62, 72], Y in [82, 92]
lines = text.splitlines()
comps = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('(footprint '):
        j = i
        depth = 0
        bl = []
        while j < len(lines):
            bl.append(lines[j])
            depth += lines[j].count('(') - lines[j].count(')')
            if depth == 0:
                break
            j += 1
        bt = '\n'.join(bl)
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', bt)
        at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', bt)
        layer_m = re.search(r'\(layer "([^"]+)"\)', bt)
        if ref_m and at_m:
            ref = ref_m.group(1)
            x = float(at_m.group(1))
            y = float(at_m.group(2))
            layer = layer_m.group(1) if layer_m else "F.Cu"
            if layer == 'F.Cu' and 62 <= x <= 72 and 82 <= y <= 92:
                print(f"F.Cu: {ref:8} at ({x:6.2f}, {y:6.2f})")
            if layer == 'B.Cu' and 62 <= x <= 72 and 82 <= y <= 92:
                print(f"B.Cu: {ref:8} at ({x:6.2f}, {y:6.2f})")
        i = j + 1
    else:
        i += 1
