#!/usr/bin/env python3
import pcbnew
import math

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
def to_mm(val):
    return pcbnew.ToMM(val)

print("--- ALL PASSIVES ON F.Cu ---")
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if (ref.startswith('R') or ref.startswith('C')) and not ref.startswith('RShunt') and fp.GetLayerName() == 'F.Cu':
        pos = fp.GetPosition()
        px, py = to_mm(pos.x), to_mm(pos.y)
        rot = fp.GetOrientation().AsDegrees() % 360
        fpid = fp.GetFPID().GetLibItemName()
        pads = [(p.GetNumber(), p.GetNetname()) for p in fp.Pads()]
        print(f"  {ref:5} at ({px:7.3f}, {py:7.3f}) rot={rot:5.1f} | {fpid} | pads={pads}")

