import re
from collections import defaultdict

pcb_path = "usb-pd-power-supply/hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Extract footprints
fps = []
for m in re.finditer(r'\(footprint "([^"]+)".*?\(property "Reference" "([^"]+)".*?\)', text, re.DOTALL):
    fp_text = m.group(0)
    ref_match = re.search(r'\(property "Reference" "([^"]+)"', fp_text)
    at_match = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', fp_text)
    layer_match = re.search(r'\(layer "([^"]+)"\)', fp_text)
    if ref_match and at_match and layer_match:
        ref = ref_match.group(1)
        x = float(at_match.group(1))
        y = float(at_match.group(2))
        rot = float(at_match.group(3)) if at_match.group(3) else 0.0
        layer = layer_match.group(1)
        fps.append({'ref': ref, 'x': x, 'y': y, 'rot': rot, 'layer': layer})

# Check alignment of passives (R, C)
r_c_fps = [f for f in fps if f['ref'].startswith(('R', 'C'))]

# Group by similar X (within 0.5 mm) or similar Y (within 0.5 mm)
x_coords = sorted(set(round(f['x'], 2) for f in r_c_fps))
y_coords = sorted(set(round(f['y'], 2) for f in r_c_fps))

print(f"Total R/C components: {len(r_c_fps)}")
print(f"Unique X coordinates for R/C: {len(x_coords)}")
print(f"Unique Y coordinates for R/C: {len(y_coords)}")

# Check groups of components that could share alignment rails
# e.g., components in the same functional neighborhood
neighborhoods = {
    'AP33772S & Input': [f for f in r_c_fps if 65 <= f['x'] <= 85 and 100 <= f['y'] <= 130],
    'Boost U11': [f for f in r_c_fps if 85 <= f['x'] <= 105 and 100 <= f['y'] <= 130],
    'Buck U5': [f for f in r_c_fps if 115 <= f['x'] <= 135 and 95 <= f['y'] <= 115],
    'Output & INA226': [f for f in r_c_fps if 130 <= f['x'] <= 145 and 95 <= f['y'] <= 125],
    'MCU & Digital Top': [f for f in r_c_fps if 60 <= f['x'] <= 105 and 68 <= f['y'] <= 90],
    'Ethernet / Mezzanine': [f for f in r_c_fps if 105 <= f['x'] <= 125 and 68 <= f['y'] <= 95],
}

print("\n--- Neighborhood Alignment Stats ---")
for name, comp_list in neighborhoods.items():
    print(f"\n{name} ({len(comp_list)} components):")
    for c in sorted(comp_list, key=lambda k: (k['y'], k['x'])):
        print(f"  {c['ref']:6} ({c['layer']:4}) at ({c['x']:6.2f}, {c['y']:6.2f}) rot={c['rot']:5.1f}")
