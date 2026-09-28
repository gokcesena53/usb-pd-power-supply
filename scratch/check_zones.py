import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
for z in board.Zones():
    poly = z.Outline()
    bbox = poly.BBox()
    name = z.GetZoneName()
    net = z.GetNetname()
    layers = [board.GetLayerName(l) for l in z.GetLayerSet().Seq()]
    print(f"Zone '{name}' Net: {net} Layers: {layers} BBox: ({pcbnew.ToMM(bbox.GetX()):.2f}, {pcbnew.ToMM(bbox.GetY()):.2f}) to ({pcbnew.ToMM(bbox.GetRight()):.2f}, {pcbnew.ToMM(bbox.GetBottom()):.2f}) is_keepout={z.GetIsKeepout()}")
