#!/usr/bin/env python3
import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
def to_mm(val): return pcbnew.ToMM(val)

anchors = {'H1', 'H2', 'H3', 'H4', 'J3', 'J4', 'J7', 'J8', 'J9', 'MECH_ENC', 'U2'}

for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref in anchors: continue
    boxes = []
    for g in fp.GraphicalItems():
        if "Crtyd" in g.GetLayerName():
            boxes.append(g.GetBoundingBox())
    if boxes:
        m = boxes[0]
        for b in boxes[1:]: m.Merge(b)
    else:
        m = fp.GetBoundingBox(False, False)
    y1 = to_mm(m.GetBottom())
    x0 = to_mm(m.GetX())
    x1 = to_mm(m.GetRight())
    y0 = to_mm(m.GetY())
    if y1 > 126.0:
        print(f"Bottom comp: {ref:6} ({fp.GetLayerName():4}) y1={y1:.3f}, pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), net={[p.GetNetname() for p in fp.Pads()]}")
    if x0 < 61.0:
        print(f"Left comp:   {ref:6} ({fp.GetLayerName():4}) x0={x0:.3f}, pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f})")
    if x1 > 146.0:
        print(f"Right comp:  {ref:6} ({fp.GetLayerName():4}) x1={x1:.3f}, pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f})")
    if y0 < 71.0:
        print(f"Top comp:    {ref:6} ({fp.GetLayerName():4}) y0={y0:.3f}, pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f})")

