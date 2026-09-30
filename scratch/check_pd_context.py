import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

points = [
    ("V_PRE #1", 186.69, 52.07),
    ("V_PRE #2", 154.94, 158.75),
    ("OUT_POS #1", 302.26, 50.8),
    ("OUT_POS #2", 312.42, 78.74),
    ("OUT_POS #3", 377.19, 154.94),
    ("SW_EN #1", 184.15, 67.31),
    ("SW_EN #2", 402.59, 43.18),
    ("SW_EN #3", 332.74, 180.34),
]

for name, px, py in points:
    print(f"=== {name} at ({px}, {py}) ===")
    # find labels, symbols, wires within +/- 15 mm
    labels = re.findall(rf'\((?:label|global_label|hierarchical_label)\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+)', sch, re.DOTALL)
    for l in labels:
        lx, ly = float(l[1]), float(l[2])
        if abs(lx - px) <= 15 and abs(ly - py) <= 15:
            print(f"  Label '{l[0]}' at ({lx}, {ly})")
