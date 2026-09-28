import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

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
            if depth == 0: break
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
            comps.append({'ref': ref, 'layer': layer, 'x': x, 'y': y})
        i = j + 1
    else:
        i += 1

print("--- Components on B.Cu with X in [70, 85], Y in [80, 105] ---")
for c in comps:
    if c['layer'] == 'B.Cu' and 70 <= c['x'] <= 85 and 80 <= c['y'] <= 105:
        print(f"B.Cu: {c['ref']:8} at ({c['x']:6.2f}, {c['y']:6.2f})")

print("\n--- Components on F.Cu with X in [62, 75], Y in [75, 105] ---")
for c in comps:
    if c['layer'] == 'F.Cu' and 62 <= c['x'] <= 75 and 75 <= c['y'] <= 105:
        print(f"F.Cu: {c['ref']:8} at ({c['x']:6.2f}, {c['y']:6.2f})")
