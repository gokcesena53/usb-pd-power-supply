import re
import sys
import math

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb.bak', 'r', encoding='utf-8') as f:
    pcb = f.read()

# Collect all pads on B.Cu with their absolute coordinates and sizes
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
            bcu_pads.append({'ref': ref, 'pnum': pnum, 'x': fx + px, 'y': fy + py, 'r': max(sx, sy)/2.0})
            
    # Silk text
    for sm in re.finditer(r'\(property\s+"Reference"\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+)(?:\s+([-\d.]+))?.*?\((layer|effects)', p, re.DOTALL):
        sx, sy = float(sm.group(2)), float(sm.group(3))
        # rough approx of silk pos
        bcu_silks.append({'ref': ref, 'x': fx + sx, 'y': fy + sy})

def check_clearance(cx, cy, label):
    # clearance to all B.Cu pads (pad radius 0.5 + other pad radius + 0.5 clearance)
    min_pad_dist = 999.0
    closest_pad = None
    for p in bcu_pads:
        d = math.hypot(p['x'] - cx, p['y'] - cy) - p['r'] - 0.5
        if d < min_pad_dist:
            min_pad_dist = d
            closest_pad = p
            
    min_silk_dist = 999.0
    closest_silk = None
    for s in bcu_silks:
        d = math.hypot(s['x'] - cx, s['y'] - cy) - 1.5 # approx 1.5mm text extent
        if d < min_silk_dist:
            min_silk_dist = d
            closest_silk = s
            
    print(f"Candidate {label} @ ({cx:.2f}, {cy:.2f}):")
    print(f"  Pad clearance: {min_pad_dist:.2f} mm (closest {closest_pad['ref']}.{closest_pad['pnum']})")
    print(f"  Silk clearance: {min_silk_dist:.2f} mm (closest {closest_silk['ref']})")
    return min_pad_dist > 1.0 and min_silk_dist > 0.5

print("=== EVALUATING CANDIDATES ===")
check_clearance(107.5, 82.5, "TP9")
check_clearance(110.5, 82.5, "TP14")
check_clearance(107.5, 79.5, "TP10 (Option A)")
check_clearance(110.5, 85.5, "TP10 (Option B)")
check_clearance(71.0, 72.0, "TP15")
check_clearance(128.0, 93.0, "TP16 (Option A)")
check_clearance(131.0, 93.0, "TP16 (Option B)")
check_clearance(114.0, 101.5, "TP17 (Option A)")
check_clearance(117.0, 99.0, "TP17 (Option B)")
check_clearance(143.0, 107.0, "TP18")
check_clearance(124.0, 121.0, "TP19")
