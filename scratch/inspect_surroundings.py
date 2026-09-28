import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

# Let's inspect Edge.Cuts
gr_items = re.findall(r'\(gr_\w+\s+.*?\n\t\)', pcb, re.DOTALL)
print("=== EDGE CUTS ===")
for item in gr_items:
    if 'Edge.Cuts' in item:
        lines = [l.strip() for l in item.splitlines() if l.strip()]
        print(" | ".join(lines))

# Let's inspect footprints around UART TP11-13 (X: 130-145, Y: 68-75)
print("\n=== FOOTPRINTS NEAR TP11-TP13 (X: 125-145, Y: 68-75) ===")
parts = re.split(r'\n\s*\(footprint\s+', pcb)
for p in parts[1:]:
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
    if at_m:
        x, y = float(at_m.group(1)), float(at_m.group(2))
        if 125 <= x <= 145 and 65 <= y <= 76:
            ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
            layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
            print(f"  {ref_m.group(1) if ref_m else '?'}: Pos=({x}, {y}), Layer={layer_m.group(1) if layer_m else '?'}")

# Let's inspect footprints near TP9-TP10 (X: 90-102, Y: 75-90)
print("\n=== FOOTPRINTS NEAR TP9-TP10 (X: 90-105, Y: 75-90) ===")
for p in parts[1:]:
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
    if at_m:
        x, y = float(at_m.group(1)), float(at_m.group(2))
        if 90 <= x <= 105 and 75 <= y <= 90:
            ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
            layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
            print(f"  {ref_m.group(1) if ref_m else '?'}: Pos=({x}, {y}), Layer={layer_m.group(1) if layer_m else '?'}")

# Let's inspect footprints near TP6-TP8 (X: 70-85, Y: 68-76)
print("\n=== FOOTPRINTS NEAR TP6-TP8 (X: 70-85, Y: 68-76) ===")
for p in parts[1:]:
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
    if at_m:
        x, y = float(at_m.group(1)), float(at_m.group(2))
        if 70 <= x <= 85 and 68 <= y <= 76:
            ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
            layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
            print(f"  {ref_m.group(1) if ref_m else '?'}: Pos=({x}, {y}), Layer={layer_m.group(1) if layer_m else '?'}")

# Let's inspect footprints near J8 and TP14 (X: 95-115, Y: 75-86)
print("\n=== FOOTPRINTS NEAR J8 / TP14 (X: 95-115, Y: 75-86) ===")
for p in parts[1:]:
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
    if at_m:
        x, y = float(at_m.group(1)), float(at_m.group(2))
        if 95 <= x <= 115 and 75 <= y <= 86:
            ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
            layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
            print(f"  {ref_m.group(1) if ref_m else '?'}: Pos=({x}, {y}), Layer={layer_m.group(1) if layer_m else '?'}")
