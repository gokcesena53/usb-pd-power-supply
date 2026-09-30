#!/usr/bin/env python3
import pcbnew
import math

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
fps = list(board.GetFootprints())

print(f"Total footprints: {len(fps)}")

by_group = {}
for fp in fps:
    ref = fp.GetReference()
    pos = fp.GetPosition()
    px, py = pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)
    rot = fp.GetOrientation().AsDegrees() % 360
    layer = fp.GetLayerName()
    fpid = fp.GetFPID().GetLibItemName()
    
    # Courtyard polygon / bbox
    crtyd_shapes = []
    for g in fp.GraphicalItems():
        if "Crtyd" in g.GetLayerName():
            b = g.GetBoundingBox()
            crtyd_shapes.append(b)
    if crtyd_shapes:
        merged = crtyd_shapes[0]
        for s in crtyd_shapes[1:]:
            merged.Merge(s)
        cw, ch = pcbnew.ToMM(merged.GetWidth()), pcbnew.ToMM(merged.GetHeight())
        cx0, cy0 = pcbnew.ToMM(merged.GetX()), pcbnew.ToMM(merged.GetY())
        cx1, cy1 = pcbnew.ToMM(merged.GetRight()), pcbnew.ToMM(merged.GetBottom())
    else:
        merged = fp.GetBoundingBox(False, False)
        cw, ch = pcbnew.ToMM(merged.GetWidth()), pcbnew.ToMM(merged.GetHeight())
        cx0, cy0 = pcbnew.ToMM(merged.GetX()), pcbnew.ToMM(merged.GetY())
        cx1, cy1 = pcbnew.ToMM(merged.GetRight()), pcbnew.ToMM(merged.GetBottom())
        
    print(f"{ref:8} | layer={layer:4} | pos=({px:7.3f}, {py:7.3f}) | rot={rot:5.1f} | crtyd=({cx0:7.3f},{cy0:7.3f} to {cx1:7.3f},{cy1:7.3f} size {cw:5.2f}x{ch:5.2f}) | {fpid}")
