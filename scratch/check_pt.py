import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
pt = pcbnew.VECTOR2I(pcbnew.FromMM(112.3), pcbnew.FromMM(78.0))

print('Checking all drawings, zones, pads near pt:')
for d in board.GetDrawings():
    if pcbnew.ToMM((d.GetPosition() - pt).EuclideanNorm()) < 2.0:
        print('Drawing:', d.GetLayerName(), d.GetShapeStr())

for z in board.Zones():
    if z.HitTest(pt):
        print('Zone hit:', z.GetLayerName(), z.GetNetname())

for pad in board.GetPads():
    pos = pad.GetPosition()
    if pcbnew.ToMM((pos - pt).EuclideanNorm()) < 3.0:
        print('Pad:', pad.GetParentFootprint().GetReference(), pad.GetName(), pad.GetLayerName(), pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))
