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
            if depth == 0:
                break
            j += 1
        bt = '\n'.join(bl)
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', bt)
        at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', bt)
        layer_m = re.search(r'\(layer "([^"]+)"\)', bt)
        fp_m = re.search(r'\(footprint "([^"]+)"', bt)
        if ref_m and at_m:
            ref = ref_m.group(1)
            x = float(at_m.group(1))
            y = float(at_m.group(2))
            rot = float(at_m.group(3)) if at_m.group(3) else 0.0
            layer = layer_m.group(1) if layer_m else "F.Cu"
            comps.append({'ref': ref, 'fp': fp_m.group(1) if fp_m else "", 'layer': layer, 'x': x, 'y': y, 'rot': rot})
        i = j + 1
    else:
        i += 1

print("--- Components with X in [50, 85], Y in [75, 115] ---")
for c in sorted(comps, key=lambda x: (x['layer'], x['y'], x['x'])):
    if 50 <= c['x'] <= 85 and 70 <= c['y'] <= 118:
        print(f"{c['ref']:8} | {c['layer']:4} | ({c['x']:6.2f}, {c['y']:6.2f}) | rot={c['rot']:5.1f} | {c['fp'][:30]}")

print("\n--- Keepout and Board Boundary for Left Side ---")
# Let's check MECH_ENC, H1, H3, Edge.Cuts
for c in comps:
    if c['ref'] in ['MECH_ENC', 'H1', 'H3', 'J7', 'J9', 'U10', 'D3', 'D8', 'D9', 'R62', 'R63']:
        print(f"{c['ref']:8} | {c['layer']:4} | ({c['x']:6.2f}, {c['y']:6.2f}) | {c['fp'][:30]}")
