import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/mcu.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Let's find wires and labels near 220-270, 120-145
wires = re.findall(r'\(wire\s+.*?\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)', sch)
for w in wires:
    x1, y1, x2, y2 = map(float, w)
    if (220 <= x1 <= 270 and 120 <= y1 <= 145) or (220 <= x2 <= 270 and 120 <= y2 <= 145):
        print(f"Wire: ({x1}, {y1}) -> ({x2}, {y2})")

labels = re.findall(r'\((?:label|global_label|hierarchical_label)\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+)', sch, re.DOTALL)
for l in labels:
    name, x, y = l[0], float(l[1]), float(l[2])
    if 220 <= x <= 270 and 120 <= y <= 145:
        print(f"Label: '{name}' at ({x}, {y})")
