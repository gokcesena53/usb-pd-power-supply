import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find all symbols, wires, labels, texts
elements = []
for m in re.finditer(r'\(at\s+([-\d.]+)\s+([-\d.]+)', text):
    elements.append((float(m.group(1)), float(m.group(2))))

print(f"Total placed objects: {len(elements)}")

# Let's check a grid of 20x20 mm from X: 20 to 400, Y: 20 to 280
grid = {}
for x in range(30, 400, 20):
    for y in range(30, 280, 20):
        # count elements within 15mm
        cnt = sum(1 for ex, ey in elements if abs(ex - x) < 15 and abs(ey - y) < 15)
        if cnt == 0:
            grid[(x, y)] = 0

print("Completely empty 30x30 regions:")
for (x, y) in sorted(grid.keys()):
    if x in [50, 70, 90, 110, 130, 150, 350, 370, 390] and y in [30, 50, 210, 230, 250]:
        print(f"  Empty @ ({x}, {y})")
