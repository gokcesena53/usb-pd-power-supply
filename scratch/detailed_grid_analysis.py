import pcbnew
import math
import json
from collections import defaultdict

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

def to_mm(val):
    return round(pcbnew.ToMM(val), 3)

passives = {}
ics = {}
others = {}

for fp in board.GetFootprints():
    ref = fp.GetReference()
    val = fp.GetValue()
    pos = (to_mm(fp.GetPosition().x), to_mm(fp.GetPosition().y))
    rot = round(fp.GetOrientation().AsDegrees() % 360, 2)
    layer = fp.GetLayerName()
    fp_name = str(fp.GetFPID().GetLibItemName())
    
    pads = []
    for p in fp.Pads():
        pads.append({
            'num': str(p.GetNumber()),
            'net': str(p.GetNetname()),
            'pos': (to_mm(p.GetPosition().x), to_mm(p.GetPosition().y))
        })
    
    data = {
        'ref': ref,
        'val': val,
        'footprint': fp_name,
        'pos': pos,
        'rot': rot,
        'layer': layer,
        'pads': pads
    }
    
    if ref.startswith(('R', 'C')) and not ref.startswith('RShunt'):
        passives[ref] = data
    elif ref.startswith('U') and not ref.startswith('USB'):
        ics[ref] = data
    else:
        others[ref] = data

print(f"Total passives: {len(passives)}")
print(f"Total ICs: {len(ics)}")
print(f"Total others: {len(others)}")

# Check courtyard bounding boxes
crtyds = {}
for fp in board.GetFootprints():
    ref = fp.GetReference()
    poly = fp.GetCourtyard(fp.GetLayer())
    if not poly.IsEmpty():
        box = poly.BBox()
        crtyds[ref] = {
            'min_x': to_mm(box.GetX()),
            'min_y': to_mm(box.GetY()),
            'max_x': to_mm(box.GetRight()),
            'max_y': to_mm(box.GetBottom()),
            'width': to_mm(box.GetWidth()),
            'height': to_mm(box.GetHeight())
        }

print(f"Components with valid courtyard: {len(crtyds)}")

# Check grid snapping on 0.5mm, 0.25mm, 0.1mm, 0.05mm
grid_stats = defaultdict(list)
for ref, p in passives.items():
    x, y = p['pos']
    rem_05 = max(abs(round(x/0.5)*0.5 - x), abs(round(y/0.5)*0.5 - y))
    rem_025 = max(abs(round(x/0.25)*0.25 - x), abs(round(y/0.25)*0.25 - y))
    rem_01 = max(abs(round(x/0.1)*0.1 - x), abs(round(y/0.1)*0.1 - y))
    rem_005 = max(abs(round(x/0.05)*0.05 - x), abs(round(y/0.05)*0.05 - y))
    
    if rem_05 < 0.001:
        grid_stats['0.50mm'].append(ref)
    elif rem_025 < 0.001:
        grid_stats['0.25mm'].append(ref)
    elif rem_01 < 0.001:
        grid_stats['0.10mm'].append(ref)
    elif rem_005 < 0.001:
        grid_stats['0.05mm'].append(ref)
    else:
        grid_stats['off_grid'].append(ref)

print("\n=== GRID STATS FOR PASSIVES ===")
for g, refs in grid_stats.items():
    print(f"Grid {g}: {len(refs)} components")

# Save detailed dump
with open('scratch/task104_detailed_passives.json', 'w') as f:
    json.dump({
        'passives': passives,
        'ics': ics,
        'others': others,
        'courtyards': crtyds,
        'grid_stats': {k: v for k, v in grid_stats.items()}
    }, f, indent=2)
print("Saved to scratch/task104_detailed_passives.json")
