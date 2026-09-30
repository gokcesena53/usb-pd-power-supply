import re
import math

pcb_path = "usb-pd-power-supply/hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's extract all nets connected to U2 and to connectors J3, J4, J7, J8, J9
# Re-run pad parser
from collections import defaultdict

lines = text.splitlines()
pad_list = []
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
            for pad_m in re.finditer(r'\(pad "([^"]+)"\s+(smd|thru_hole|np_thru_hole|connect)\s+([^\s]+)\s+\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\).*?\(net (?:[0-9]+ )?"([^"]+)"\)', block_text, re.DOTALL):
                p_num = pad_m.group(1)
                px = float(pad_m.group(4))
                py = float(pad_m.group(5))
                prot = float(pad_m.group(6)) if pad_m.group(6) else 0.0
                net = pad_m.group(7)
                rad = math.radians(frot)
                rx = px * math.cos(rad) - py * math.sin(rad)
                ry = px * math.sin(rad) + py * math.cos(rad)
                if net and net != "unconnected" and not any(kw in net.lower() for kw in ['gnd', 'vbus', '+3.3v', '+5v']):
                    pad_list.append({
                        'ref': ref, 'pad': p_num, 'x': fx + rx, 'y': fy + ry, 'net': net, 'layer': flayer
                    })
        i = j + 1
    else:
        i += 1

# Filter by connectors and MCU U2
connectors = {'J3', 'J7', 'J8', 'J9', 'J4'}
u2_pads = [p for p in pad_list if p['ref'] == 'U2']
u2_nets = {p['net']: p for p in u2_pads}

print(f"MCU U2 has {len(u2_pads)} signal pads connected.")

for conn in sorted(connectors):
    conn_pads = [p for p in pad_list if p['ref'] == conn]
    print(f"\n--- Connector {conn} ({len(conn_pads)} signal pads) ---")
    for cp in conn_pads:
        net = cp['net']
        if net in u2_nets:
            up = u2_nets[net]
            dist = math.hypot(cp['x'] - up['x'], cp['y'] - up['y'])
            print(f"  Direct to U2: Net '{net}' from {conn} pin {cp['pad']} ({cp['x']:.1f}, {cp['y']:.1f}) -> U2 pin {up['pad']} ({up['x']:.1f}, {up['y']:.1f}) | Dist: {dist:.1f} mm")
        else:
            # check intermediate ICs
            other_pads = [p for p in pad_list if p['net'] == net and p['ref'] not in (conn, 'U2')]
            other_refs = list(set(p['ref'] for p in other_pads))
            print(f"  Indirect/Other: Net '{net}' from {conn} pin {cp['pad']} ({cp['x']:.1f}, {cp['y']:.1f}) -> {', '.join(other_refs)}")
