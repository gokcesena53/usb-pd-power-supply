import re
from collections import defaultdict

pcb_path = "usb-pd-power-supply/hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's extract all footprints with reference, at (x, y, rot), layer
fp_pattern = re.compile(
    r'\(footprint "([^"]+)"\s+'
    r'\(layer "([^"]+)"\)\s+'
    r'\(uuid "[^"]+"\)\s+'
    r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)\s+'
    r'\(property "Reference" "([^"]+)"',
    re.MULTILINE
)

# Also let's extract footprints where (at ...) might be structured slightly differently
matches = []
for m in re.finditer(r'\(footprint "([^"]+)".*?\(property "Reference" "([^"]+)".*?\)', text, re.DOTALL):
    fp_text = m.group(0)
    ref_match = re.search(r'\(property "Reference" "([^"]+)"', fp_text)
    at_match = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', fp_text)
    layer_match = re.search(r'\(layer "([^"]+)"\)', fp_text)
    fp_name = re.search(r'\(footprint "([^"]+)"', fp_text).group(1)
    if ref_match and at_match and layer_match:
        ref = ref_match.group(1)
        x = float(at_match.group(1))
        y = float(at_match.group(2))
        rot = float(at_match.group(3)) if at_match.group(3) else 0.0
        layer = layer_match.group(1)
        matches.append((ref, fp_name, layer, x, y, rot))

print(f"Total footprints extracted: {len(matches)}")

# Rotation analysis
rotations = defaultdict(list)
for ref, fp_name, layer, x, y, rot in matches:
    norm_rot = rot % 360
    rotations[norm_rot].append(ref)

print("\n--- Rotation Analysis ---")
for rot, refs in sorted(rotations.items()):
    print(f"Angle {rot:6.1f} deg: {len(refs)} components (e.g. {', '.join(refs[:10])})")

# Categorize components by block
# Let's inspect coordinates of key functional groups
print("\n--- Key Functional ICs and Connectors ---")
for ref, fp_name, layer, x, y, rot in sorted(matches, key=lambda x: x[0]):
    if ref.startswith(('U', 'J', 'Q', 'D', 'L', 'MECH')) and not ref.startswith(('D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10')):
        print(f"{ref:10} {layer:6} at ({x:6.2f}, {y:6.2f}) rot={rot:5.1f}")
    elif ref in ['U1', 'U2', 'U3', 'U4', 'U5', 'U10', 'U11', 'U12', 'U13', 'J3', 'J4', 'J7', 'J8', 'J9', 'L1', 'L3', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q8']:
        print(f"{ref:10} {layer:6} at ({x:6.2f}, {y:6.2f}) rot={rot:5.1f}")
