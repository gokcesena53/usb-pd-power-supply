import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# find symbols with at between 120 and 200, 40 and 70
symbols = re.findall(r'\(symbol\s+.*?\(uuid\s+"[^"]+"\)\s*\)', sch, re.DOTALL)
for s in symbols:
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', s)
    if at_m:
        x, y = float(at_m.group(1)), float(at_m.group(2))
        if 130 <= x <= 200 and 40 <= y <= 70:
            ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', s)
            val_m = re.search(r'\(property\s+"Value"\s+"([^"]+)"', s)
            print(f"Symbol {ref_m.group(1) if ref_m else '?'}: {val_m.group(1) if val_m else '?'} at ({x}, {y})")

wires = re.findall(r'\(wire\s+.*?\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)', sch)
for w in wires:
    x1, y1, x2, y2 = map(float, w)
    if 130 <= x1 <= 200 and 40 <= y1 <= 70 and 130 <= x2 <= 200 and 40 <= y2 <= 70:
        print(f"Wire: ({x1}, {y1}) -> ({x2}, {y2})")
