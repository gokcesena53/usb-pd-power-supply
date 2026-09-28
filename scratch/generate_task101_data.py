import math
import re
from collections import defaultdict

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
comps = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('(footprint '):
        j = i
        depth = 0
        block_lines = []
        while j < len(lines):
            l = lines[j]
            block_lines.append(l)
            depth += l.count('(') - l.count(')')
            if depth == 0:
                break
            j += 1
        block_text = "\n".join(block_lines)
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block_text)
        at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', block_text)
        layer_m = re.search(r'\(layer "([^"]+)"\)', block_text)
        fp_m = re.search(r'\(footprint "([^"]+)"', block_text)
        if ref_m and at_m:
            ref = ref_m.group(1)
            fx = float(at_m.group(1))
            fy = float(at_m.group(2))
            frot = float(at_m.group(3)) if at_m.group(3) else 0.0
            flayer = layer_m.group(1) if layer_m else "F.Cu"
            comps.append({
                'ref': ref,
                'fp': fp_m.group(1) if fp_m else "",
                'layer': flayer,
                'x': fx,
                'y': fy,
                'rot': frot
            })
        i = j + 1
    else:
        i += 1

comp_by_ref = {c['ref']: c for c in comps}

print(f"Total footprints parsed: {len(comps)}")

# 1. Power Chain Left-to-Right verification
stages = [
    ("Stage 1: Input & Protection", ["J7", "U10", "D3"]),
    ("Stage 2: PD Controller & Switch", ["U1", "Q3", "R11"]),
    ("Stage 3: Pre-Boost Converter", ["L3", "U11", "D4", "C29", "C27"]),
    ("Stage 4: Buck Regulator", ["U5", "L1", "C12", "C13"]),
    ("Stage 5: Ideal Diode & Reverse Cut", ["Q5", "U12", "C32"]),
    ("Stage 6: Current Sense & Monitor", ["RShunt1", "U3", "C11"]),
    ("Stage 7: Output Terminal", ["J4", "D7"])
]

print("\n=== STAGE-BY-STAGE POWER PIPELINE ANALYSIS ===")
prev_max_x = -float('inf')
for stage_name, refs in stages:
    stage_comps = [comp_by_ref[r] for r in refs if r in comp_by_ref]
    min_x = min(c['x'] for c in stage_comps)
    max_x = max(c['x'] for c in stage_comps)
    avg_x = sum(c['x'] for c in stage_comps) / len(stage_comps)
    layers = set(c['layer'] for c in stage_comps)
    print(f"\n{stage_name}:")
    print(f"  Layers: {', '.join(layers)}")
    print(f"  X Range: [{min_x:.2f}, {max_x:.2f}] mm (Center: {avg_x:.2f} mm)")
    for c in stage_comps:
        print(f"    - {c['ref']:8} ({c['layer']:4}) at ({c['x']:6.2f}, {c['y']:6.2f})")

# 2. Zoning Verification
print("\n=== ZONING VERIFICATION ===")
north_zone = [c for c in comps if c['y'] < 90.0 and c['ref'] != 'MECH_ENC']
south_zone = [c for c in comps if c['y'] >= 90.0 and c['ref'] != 'MECH_ENC']

print(f"North Zone (Y < 90 mm - Digital/RF/Interfaces): {len(north_zone)} components")
print(f"  Sample refs: {', '.join(sorted([c['ref'] for c in north_zone])[:15])}")

print(f"South Zone (Y >= 90 mm - Power Conversion & High Current): {len(south_zone)} components")
print(f"  Sample refs: {', '.join(sorted([c['ref'] for c in south_zone])[:15])}")

# 3. Noise Isolation Distances
print("\n=== NOISE ISOLATION DISTANCES ===")
# Switching nodes: L1 (Buck), L3 (Boost)
l1 = comp_by_ref['L1']
l3 = comp_by_ref['L3']
u11 = comp_by_ref['U11']
u5 = comp_by_ref['U5']

# Sensitive nodes: Y1 (RTC crystal), U3 (INA226), RShunt1, U2 (MCU)
sensitive = ['Y1', 'U3', 'RShunt1', 'U2', 'R11']
for s_ref in sensitive:
    s = comp_by_ref[s_ref]
    d_l1 = math.hypot(s['x'] - l1['x'], s['y'] - l1['y'])
    d_l3 = math.hypot(s['x'] - l3['x'], s['y'] - l3['y'])
    print(f"{s_ref:8} at ({s['x']:6.2f}, {s['y']:6.2f}, {s['layer']}):")
    print(f"  Distance to L1 (Buck Inductor):  {d_l1:6.2f} mm")
    print(f"  Distance to L3 (Boost Inductor): {d_l3:6.2f} mm")
