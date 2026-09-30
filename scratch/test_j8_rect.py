import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
j8 = board.FindFootprintByReference('J8')

# The rect goes from (51.23, 77.38) to (104.47, 99.62)
# The corners are:
# (51.23, 99.62) - top-left or bottom-left
# Let's check all pads within 1.0mm of the rectangle lines!
lines = [
    ((51.23, 77.38), (104.47, 77.38)),
    ((104.47, 77.38), (104.47, 99.62)),
    ((104.47, 99.62), (51.23, 99.62)),
    ((51.23, 99.62), (51.23, 77.38))
]

def pt_seg_dist(p, a, b):
    # p, a, b are tuples (x, y)
    px, py = p
    ax, ay = a
    bx, by = b
    dx = bx - ax
    dy = by - ay
    if dx == 0 and dy == 0:
        return ((px-ax)**2 + (py-ay)**2)**0.5
    t = ((px - ax)*dx + (py - ay)*dy) / (dx*dx + dy*dy)
    t = max(0, min(1, t))
    cx = ax + t*dx
    cy = ay + t*dy
    return ((px-cx)**2 + (py-cy)**2)**0.5

for pad in board.GetPads():
    pos = (pcbnew.ToMM(pad.GetPosition().x), pcbnew.ToMM(pad.GetPosition().y))
    # pad radius approx
    prad = max(pcbnew.ToMM(pad.GetSize().x), pcbnew.ToMM(pad.GetSize().y)) / 2.0
    for idx, (a, b) in enumerate(lines):
        d = pt_seg_dist(pos, a, b)
        if d - prad < 0.2: # less than 0.2mm to pad copper/mask
            print(f'Pad {pad.GetParentFootprint().GetReference()}.{pad.GetName()} (layer={pad.GetLayerName()}, pos={pos}, prad={prad:.2f}) close to line {idx} (a={a}, b={b}): dist={d:.3f}, clearance={d-prad:.3f}')
