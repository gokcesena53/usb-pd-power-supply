import re
import sys
import math

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
all_fps = []
for p in parts[1:]:
    ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p).group(1)
    layer = re.search(r'\(layer\s+"([^"]+)"\)', p).group(1)
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
    x, y = float(at_m.group(1)), float(at_m.group(2))
    all_fps.append({'ref': ref, 'layer': layer, 'x': x, 'y': y})

def find_nearby(x, y, layer, radius=8.0):
    res = []
    for fp in all_fps:
        if fp['layer'] == layer:
            d = math.hypot(fp['x'] - x, fp['y'] - y)
            if d <= radius:
                res.append((fp['ref'], fp['x'], fp['y'], d))
    res.sort(key=lambda item: item[3])
    return res

candidates = [
    ("GND (I2C)", 71.0, 72.0, "B.Cu"),
    ("+3.3V Option 1", 125.0, 72.0, "B.Cu"),
    ("+3.3V Option 2 (near L1/U5)", 131.0, 97.0, "B.Cu"),
    ("+3.3V Option 3 (near U13)", 132.5, 120.0, "B.Cu"),
    ("V_PRE Option 1 (near C12/C13)", 117.0, 101.5, "B.Cu"),
    ("V_PRE Option 2 (near D4)", 104.0, 110.0, "B.Cu"),
    ("OUT_POS Option 1 (near J4)", 143.0, 107.0, "B.Cu"),
    ("OUT_POS Option 2 (near D7/R59)", 140.0, 122.0, "B.Cu"),
    ("SW_EN Option 1 (near U13/Q4)", 124.0, 121.0, "B.Cu"),
    ("SW_EN Option 2 (near U13)", 127.0, 126.0, "B.Cu"),
]

for name, cx, cy, layer in candidates:
    print(f"=== {name} at ({cx}, {cy}) on {layer} ===")
    nearby = find_nearby(cx, cy, layer, radius=6.0)
    for ref, x, y, d in nearby:
        print(f"   {ref:8s} @ ({x:6.2f}, {y:6.2f}) dist={d:4.2f} mm")
