import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
comps = {}
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('(footprint '):
        j = i
        depth = 0
        block_lines = []
        while j < len(lines):
            l = lines[j]
            block_lines.append(l)
            depth += l.count('(') - l.count(')')
            if depth == 0:
                break
            j += 1
        block_text = "\n".join(block_lines)
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block_text)
        at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', block_text)
        layer_m = re.search(r'\(layer "([^"]+)"\)', block_text)
        if ref_m and at_m:
            ref = ref_m.group(1)
            fx = float(at_m.group(1))
            fy = float(at_m.group(2))
            frot = float(at_m.group(3)) if at_m.group(3) else 0.0
            flayer = layer_m.group(1) if layer_m else "F.Cu"
            nets = set(re.findall(r'\(net (?:[0-9]+ )?"([^"]+)"\)', block_text))
            comps[ref] = {
                'ref': ref, 'layer': flayer, 'x': fx, 'y': fy, 'rot': frot, 'nets': nets
            }
        i = j + 1
    else:
        i += 1

targets = ['J9', 'R34', 'R35', 'R36', 'R2', 'R3', 'U10', 'J7', 'U2', 'U3']
for ref in targets:
    if ref in comps:
        c = comps[ref]
        print(f"{ref:6}: {c['layer']:4} at ({c['x']:6.2f}, {c['y']:6.2f}) rot={c['rot']:5.1f} | nets: {c['nets']}")
