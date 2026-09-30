#!/usr/bin/env python3
import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
def to_mm(val):
    return pcbnew.ToMM(val)

fps = list(board.GetFootprints())
comps = []
for fp in fps:
    ref = fp.GetReference()
    b = None
    for g in fp.GraphicalItems():
        if "Crtyd" in g.GetLayerName():
            if b is None:
                b = g.GetBoundingBox()
            else:
                b.Merge(g.GetBoundingBox())
    if b is None:
        b = fp.GetBoundingBox(False, False)
    comps.append({
        'ref': ref,
        'layer': fp.GetLayerName(),
        'x0': to_mm(b.GetX()),
        'y0': to_mm(b.GetY()),
        'x1': to_mm(b.GetRight()),
        'y1': to_mm(b.GetBottom())
    })

comps_by_x0 = sorted(comps, key=lambda c: c['x0'])
comps_by_x1 = sorted(comps, key=lambda c: c['x1'], reverse=True)
comps_by_y0 = sorted(comps, key=lambda c: c['y0'])
comps_by_y1 = sorted(comps, key=lambda c: c['y1'], reverse=True)

print("Top 5 min_x:")
for c in comps_by_x0[:5]:
    print(f"  {c['ref']:8} ({c['layer']}): x0={c['x0']:.3f}, x1={c['x1']:.3f}")

print("\nTop 5 max_x:")
for c in comps_by_x1[:5]:
    print(f"  {c['ref']:8} ({c['layer']}): x0={c['x0']:.3f}, x1={c['x1']:.3f}")

print("\nTop 5 min_y:")
for c in comps_by_y0[:5]:
    print(f"  {c['ref']:8} ({c['layer']}): y0={c['y0']:.3f}, y1={c['y1']:.3f}")

print("\nTop 5 max_y:")
for c in comps_by_y1[:5]:
    print(f"  {c['ref']:8} ({c['layer']}): y0={c['y0']:.3f}, y1={c['y1']:.3f}")

