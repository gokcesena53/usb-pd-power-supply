import pcbnew
board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

target = pcbnew.VECTOR2I(pcbnew.FromMM(112.3), pcbnew.FromMM(78.0))
print('Checking near 112.3, 78.0...')
for pad in board.GetPads():
    pos = pad.GetPosition()
    dist = pcbnew.ToMM((pos - target).EuclideanNorm())
    if dist < 5.0:
        ref = pad.GetParentFootprint().GetReference() if pad.GetParentFootprint() else 'None'
        print(f'Pad {ref}.{pad.GetName()} at ({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f}), dist={dist:.2f}mm, size=({pcbnew.ToMM(pad.GetSize().x):.2f}, {pcbnew.ToMM(pad.GetSize().y):.2f})')
