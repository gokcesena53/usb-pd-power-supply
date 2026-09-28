import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find any text, wire, label, symbol in X: 340-410, Y: 200-260
for block in re.findall(r'\((?:symbol|wire|text|label|global_label)\s+.*?\n\t\)', text, re.DOTALL):
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', block)
    if at_m:
        x, y = float(at_m.group(1)), float(at_m.group(2))
        if 340 <= x <= 410 and 200 <= y <= 260:
            print(f"Object at ({x}, {y}): {block.splitlines()[0]}")
