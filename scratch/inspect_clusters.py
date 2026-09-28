#!/usr/bin/env python3
import pcbnew
import math

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

def to_mm(val):
    return pcbnew.ToMM(val)

# Check all footprints within [104, 112] x [69, 80]
print("--- Components in I2C / Q1-Q2 area ---")
for fp in board.GetFootprints():
    pos = fp.GetPosition()
    px, py = to_mm(pos.x), to_mm(pos.y)
    if 100 <= px <= 115 and 68 <= py <= 85:
        print(f"  {fp.GetReference():8} ({fp.GetLayerName()}): pos=({px:.3f}, {py:.3f}), rot={fp.GetOrientation().AsDegrees()%360:.1f}, fpid={fp.GetFPID().GetLibItemName()}")

print("\n--- Components in U1 area [70, 88] x [114, 128] ---")
for fp in board.GetFootprints():
    pos = fp.GetPosition()
    px, py = to_mm(pos.x), to_mm(pos.y)
    if 70 <= px <= 88 and 114 <= py <= 128:
        print(f"  {fp.GetReference():8} ({fp.GetLayerName()}): pos=({px:.3f}, {py:.3f}), rot={fp.GetOrientation().AsDegrees()%360:.1f}")

print("\n--- Components in U11 area [87, 107] x [116, 130] ---")
for fp in board.GetFootprints():
    pos = fp.GetPosition()
    px, py = to_mm(pos.x), to_mm(pos.y)
    if 87 <= px <= 107 and 116 <= py <= 130:
        print(f"  {fp.GetReference():8} ({fp.GetLayerName()}): pos=({px:.3f}, {py:.3f}), rot={fp.GetOrientation().AsDegrees()%360:.1f}")

print("\n--- Components in U12 area [123, 142] x [95, 110] ---")
for fp in board.GetFootprints():
    pos = fp.GetPosition()
    px, py = to_mm(pos.x), to_mm(pos.y)
    if 123 <= px <= 142 and 95 <= py <= 110:
        print(f"  {fp.GetReference():8} ({fp.GetLayerName()}): pos=({px:.3f}, {py:.3f}), rot={fp.GetOrientation().AsDegrees()%360:.1f}")

print("\n--- Components in U2 South area [63, 95] x [80, 88] ---")
for fp in board.GetFootprints():
    pos = fp.GetPosition()
    px, py = to_mm(pos.x), to_mm(pos.y)
    if 63 <= px <= 95 and 80 <= py <= 88:
        print(f"  {fp.GetReference():8} ({fp.GetLayerName()}): pos=({px:.3f}, {py:.3f}), rot={fp.GetOrientation().AsDegrees()%360:.1f}")

