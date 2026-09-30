import pcbnew
import math
import json

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

def to_mm(val):
    return round(pcbnew.ToMM(val), 3)

fps = {}
for fp in board.GetFootprints():
    ref = fp.GetReference()
    pos = (to_mm(fp.GetPosition().x), to_mm(fp.GetPosition().y))
    rot = round(fp.GetOrientation().AsDegrees() % 360, 2)
    layer = fp.GetLayerName()
    
    # Courtyard polygon bounding box
    poly = fp.GetCourtyard(fp.GetLayer())
    bbox = poly.BBox() if not poly.IsEmpty() else None
    
    crtyd = {
        'x_min': to_mm(bbox.GetX()) if bbox else pos[0]-1,
        'y_min': to_mm(bbox.GetY()) if bbox else pos[1]-1,
        'x_max': to_mm(bbox.GetRight()) if bbox else pos[0]+1,
        'y_max': to_mm(bbox.GetBottom()) if bbox else pos[1]+1,
    }
    
    fps[ref] = {
        'ref': ref,
        'val': fp.GetValue(),
        'layer': layer,
        'pos': pos,
        'rot': rot,
        'crtyd': crtyd,
        'fp_name': str(fp.GetFPID().GetLibItemName())
    }

# Check clearances between passives in same neighborhood on same layer
passives = [f for f in fps.values() if f['ref'].startswith(('R', 'C')) and not f['ref'].startswith('RShunt')]

print(f"Total passives to examine: {len(passives)}")

# Check distance between adjacent passives
pairs_distance = []
for i in range(len(passives)):
    for j in range(i + 1, len(passives)):
        p1 = passives[i]
        p2 = passives[j]
        if p1['layer'] != p2['layer']:
            continue
        # Euclidean center distance
        d = math.hypot(p1['pos'][0] - p2['pos'][0], p1['pos'][1] - p2['pos'][1])
        if d < 15.0: # Close neighbors
            # Courtyard gap
            # Gap in X and Y
            dx = max(0, max(p1['crtyd']['x_min'], p2['crtyd']['x_min']) - min(p1['crtyd']['x_max'], p2['crtyd']['x_max']))
            dy = max(0, max(p1['crtyd']['y_min'], p2['crtyd']['y_min']) - min(p1['crtyd']['y_max'], p2['crtyd']['y_max']))
            gap = math.hypot(dx, dy)
            pairs_distance.append((p1['ref'], p2['ref'], p1['layer'], round(d, 2), round(gap, 2), p1['pos'], p2['pos']))

pairs_distance.sort(key=lambda x: x[3])
print(f"Total neighbor pairs within 15mm: {len(pairs_distance)}")
print("\nTop 20 closest pairs:")
for p in pairs_distance[:20]:
    print(f"  {p[0]:6} - {p[1]:6} ({p[2]:4}): center={p[3]:5.2f} mm, crtyd_gap={p[4]:5.2f} mm | {p[5]} to {p[6]}")

