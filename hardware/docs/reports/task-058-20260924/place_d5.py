"""Place the FB clamp next to U11 and route its sensitive FB connection."""

import pcbnew as pcb


BOARD = "hardware/gopo.kicad_pcb"
board = pcb.LoadBoard(BOARD)
parts = {fp.GetReference(): fp for fp in board.GetFootprints()}
d5 = parts["D5"]
d5.SetOrientationDegrees(180)
d5.SetPosition(pcb.VECTOR2I(pcb.FromMM(60.05), pcb.FromMM(57.6)))
d5.Reference().SetPosition(pcb.VECTOR2I(pcb.FromMM(63.0), pcb.FromMM(57.75)))
d5.Reference().SetTextAngle(pcb.EDA_ANGLE(0, pcb.DEGREES_T))

fb = board.FindNet("/USB_PD_CONTROLLER/BOOST_FB")
assert fb is not None
points = [
    (59.0, 57.6),  # D5 anode, pad 2
    (58.7, 57.6),
    (58.2, 57.1),
    (58.2, 56.64),
    (57.0825, 56.64),  # U11 FB, pad 9
]
for (x1, y1), (x2, y2) in zip(points, points[1:]):
    track = pcb.PCB_TRACK(board)
    track.SetStart(pcb.VECTOR2I(pcb.FromMM(x1), pcb.FromMM(y1)))
    track.SetEnd(pcb.VECTOR2I(pcb.FromMM(x2), pcb.FromMM(y2)))
    track.SetWidth(pcb.FromMM(0.2))
    track.SetLayer(pcb.F_Cu)
    track.SetNet(fb)
    board.Add(track)

pcb.SaveBoard(BOARD, board)
