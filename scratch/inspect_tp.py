import re
import glob
import os

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    content = f.read()

parts = re.split(r'\n\s*\(footprint\s+', content)

pcb_tps = []
for p in parts[1:]:
    m_ref = re.search(r'\(property\s+"Reference"\s+"(TP\d+)"', p)
    if m_ref:
        ref = m_ref.group(1)
        layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
        at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', p)
        fp_name = p.split()[0].strip('"')
        net_m = re.search(r'\(pad\s+"[^"]+"\s+smd\s+.*?\s*\(net\s+\d+\s+"([^"]+)"\)', p, re.DOTALL)
        uuid_m = re.search(r'\(uuid\s+"([^"]+)"\)', p)
        pcb_tps.append({
            'ref': ref,
            'layer': layer_m.group(1) if layer_m else '',
            'x': float(at_m.group(1)) if at_m else None,
            'y': float(at_m.group(2)) if at_m else None,
            'rot': float(at_m.group(3)) if at_m and at_m.group(3) else 0.0,
            'fp': fp_name,
            'net': net_m.group(1) if net_m else '',
            'uuid': uuid_m.group(1) if uuid_m else ''
        })

pcb_tps.sort(key=lambda x: int(x['ref'][2:]))
print(f"Found {len(pcb_tps)} test points on PCB:")
for tp in pcb_tps:
    print(f"  {tp['ref']}: Net='{tp['net']}', Layer={tp['layer']}, Pos=({tp['x']:.2f}, {tp['y']:.2f}), Rot={tp['rot']}, FP={tp['fp']}, UUID={tp['uuid']}")

# Let's inspect LCD footprint and J8 footprint
print("\n--- LCD and J8 footprints ---")
for p in parts[1:]:
    for target in ['LCD', 'DISP', 'TFT', 'J8', 'U8']:
        m = re.search(rf'\(property\s+"Reference"\s+"({target})"', p)
        if m:
            layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
            at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?\)', p)
            fp_name = p.split()[0].strip('"')
            print(f"  {m.group(1)}: Layer={layer_m.group(1) if layer_m else ''}, Pos=({at_m.group(1)}, {at_m.group(2)}), FP={fp_name}")

# Let's also check for graphical outlines or bounding boxes of the LCD
# Check for LCD outline on Edge.Cuts, User.Drawings, User.Comments, or F.Fab / F.SilkS
