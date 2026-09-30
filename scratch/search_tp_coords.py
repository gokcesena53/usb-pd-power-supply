import re
import sys
import math

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb.bak', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
bcu_pads = []
bcu_silks = []

for p in parts[1:]:
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
    layer = layer_m.group(1) if layer_m else ''
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
    fx, fy = (float(at_m.group(1)), float(at_m.group(2))) if at_m else (0,0)
    ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p).group(1)
    
    # Pads
    for pm in re.finditer(r'\(pad\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+).*?\(size\s+([-\d.]+)\s+([-\d.]+).*?\(layers\s+(.*?)\)', p, re.DOTALL):
        pnum = pm.group(1)
        px, py = float(pm.group(2)), float(pm.group(3))
        sx, sy = float(pm.group(4)), float(pm.group(5))
        layers = pm.group(6)
        if 'B.Cu' in layers or '*.Cu' in layers:
            # ignore existing TP9, 10, 14 as they are being repositioned
            if ref not in ['TP9', 'TP10', 'TP14']:
                bcu_pads.append({'ref': ref, 'pnum': pnum, 'x': fx + px, 'y': fy + py, 'r': max(sx, sy)/2.0})
            
    # Silk text
    for sm in re.finditer(r'\(property\s+"Reference"\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?.*?\((layer|effects)', p, re.DOTALL):
        sx, sy = float(sm.group(2)), float(sm.group(3))
        if ref not in ['TP9', 'TP10', 'TP14']:
            bcu_silks.append({'ref': ref, 'x': fx + sx, 'y': fy + sy})

def eval_pos(cx, cy):
    min_pad = min(math.hypot(p['x'] - cx, p['y'] - cy) - p['r'] - 0.5 for p in bcu_pads)
    min_silk = min(math.hypot(s['x'] - cx, s['y'] - cy) - 1.2 for s in bcu_silks)
    # clearance to edge cuts (Y=69.48, Y=130.52, X=53.3, X=146.7)
    edge_dist = min(cx - 53.3, 146.7 - cx, cy - 69.48, 130.52 - cy) - 0.5
    return min_pad, min_silk, edge_dist

# Test search for TP16 (+3.3V):
print("Best spots for TP16 (+3.3V):")
for x in [120, 125, 128, 130, 133]:
    for y in [72, 73, 74, 91, 92]:
        p, s, e = eval_pos(x, y)
        if p > 1.8 and s > 1.2 and e > 1.0:
            print(f"  ({x:.1f}, {y:.1f}): pad_clear={p:.2f}, silk_clear={s:.2f}, edge={e:.2f}")

# Test search for TP17 (V_PRE):
print("\nBest spots for TP17 (V_PRE):")
for x in [104, 105, 106, 114, 115, 116]:
    for y in [100, 101, 102, 109, 110, 111]:
        p, s, e = eval_pos(x, y)
        if p > 1.5 and s > 1.0 and e > 1.0:
            print(f"  ({x:.1f}, {y:.1f}): pad_clear={p:.2f}, silk_clear={s:.2f}, edge={e:.2f}")

# Test search for TP9, TP10, TP14:
print("\nBest spots for TP9, TP10, TP14 (X: 106-112, Y: 79-85):")
for x in [107.5, 108.0, 110.0, 110.5, 111.0]:
    for y in [79.5, 80.0, 82.5, 85.0]:
        p, s, e = eval_pos(x, y)
        if p > 1.2 and s > 0.8:
            print(f"  ({x:.1f}, {y:.1f}): pad_clear={p:.2f}, silk_clear={s:.2f}")
