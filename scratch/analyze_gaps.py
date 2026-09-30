#!/usr/bin/env python3
import pcbnew
import math
from collections import defaultdict

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
fps = {fp.GetReference(): fp for fp in board.GetFootprints()}

def to_mm(val):
    return pcbnew.ToMM(val)

def get_crtyd(fp):
    boxes = []
    for g in fp.GraphicalItems():
        if "Crtyd" in g.GetLayerName():
            boxes.append(g.GetBoundingBox())
    if boxes:
        m = boxes[0]
        for b in boxes[1:]:
            m.Merge(b)
    else:
        m = fp.GetBoundingBox(False, False)
    return {
        'x0': to_mm(m.GetX()),
        'y0': to_mm(m.GetY()),
        'x1': to_mm(m.GetRight()),
        'y1': to_mm(m.GetBottom()),
        'w': to_mm(m.GetWidth()),
        'h': to_mm(m.GetHeight())
    }

# Find all passives and their nearest IC or neighbor
passives = [ref for ref, fp in fps.items() if (ref.startswith('R') or ref.startswith('C')) and not ref.startswith('RShunt')]
ics = [ref for ref, fp in fps.items() if ref.startswith('U')]

print(f"Total passives: {len(passives)}")

# Check clearances between all pairs of passives on the same layer
by_layer = defaultdict(list)
for p in passives:
    fp = fps[p]
    by_layer[fp.GetLayerName()].append(p)

for layer, plist in by_layer.items():
    print(f"\nLayer {layer} ({len(plist)} passives):")
    # check closest neighbors
    for i, p1 in enumerate(plist):
        fp1 = fps[p1]
        c1 = get_crtyd(fp1)
        min_clearance = 999.0
        closest_neighbor = None
        for j, p2 in enumerate(plist):
            if i == j:
                continue
            fp2 = fps[p2]
            c2 = get_crtyd(fp2)
            # clearance between boxes
            dx = max(0, max(c1['x0'] - c2['x1'], c2['x0'] - c1['x1']))
            dy = max(0, max(c1['y0'] - c2['y1'], c2['y0'] - c1['y1']))
            clearance = math.hypot(dx, dy)
            if clearance < min_clearance:
                min_clearance = clearance
                closest_neighbor = p2
        # Also check distance to nearest IC on the same layer
        min_ic_dist = 999.0
        nearest_ic = None
        for u in ics:
            fpu = fps[u]
            if fpu.GetLayerName() != layer:
                continue
            cu = get_crtyd(fpu)
            dx = max(0, max(c1['x0'] - cu['x1'], cu['x0'] - c1['x1']))
            dy = max(0, max(c1['y0'] - cu['y1'], cu['y0'] - c1['y1']))
            dist = math.hypot(dx, dy)
            if dist < min_ic_dist:
                min_ic_dist = dist
                nearest_ic = u
        p1_pos = fp1.GetPosition()
        print(f"  {p1:5} at ({to_mm(p1_pos.x):7.3f}, {to_mm(p1_pos.y):7.3f}) | closest passive {closest_neighbor:5} (gap={min_clearance:.3f} mm) | nearest IC {nearest_ic} (gap={min_ic_dist:.3f} mm)")
