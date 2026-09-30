import pcbnew
import re

pcb_path = r"hardware/gopo.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

# Let's inspect the footprint pad definitions and net connections for D1..D10
for ref in [f"D{i}" for i in range(1, 11)]:
    fp = board.FindFootprintByReference(ref)
    if not fp:
        print(f"Footprint {ref} NOT FOUND!")
        continue
    pos = fp.GetPosition()
    pos_mm = (round(pcbnew.ToMM(pos.x), 3), round(pcbnew.ToMM(pos.y), 3))
    orient = round(fp.GetOrientationDegrees(), 2)
    layer = fp.GetLayerName()
    fp_name = fp.GetFPID().GetLibItemName()
    print(f"=== {ref}: {fp.GetValue()} ({fp_name}) ===")
    print(f"  Layer: {layer}, Pos: {pos_mm}, Orient: {orient}")
    for pad in fp.Pads():
        p_num = pad.GetNumber()
        p_name = pad.GetName()
        p_pos = (round(pcbnew.ToMM(pad.GetPosition().x), 3), round(pcbnew.ToMM(pad.GetPosition().y), 3))
        p_net = pad.GetNetname()
        print(f"  Pad {p_num} (Name: '{p_name}'): Net='{p_net}' at {p_pos}")
