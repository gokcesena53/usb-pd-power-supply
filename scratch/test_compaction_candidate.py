#!/usr/bin/env python3
"""
Test script for verifying compaction candidates
"""
import pcbnew
import math
import shutil
import subprocess

def to_mm(val):
    return pcbnew.ToMM(val)

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

def get_crtyd_poly(fp):
    boxes = []
    for g in fp.GraphicalItems():
        if "Crtyd" in g.GetLayerName():
            boxes.append(g.GetBoundingBox())
    if boxes:
        m = boxes[0]
        for b in boxes[1:]:
            m.Merge(b)
    else:
        m = fp.GetBoundingBox(False, False)
    return {
        'x0': to_mm(m.GetX()),
        'y0': to_mm(m.GetY()),
        'x1': to_mm(m.GetRight()),
        'y1': to_mm(m.GetBottom()),
        'w': to_mm(m.GetWidth()),
        'h': to_mm(m.GetHeight())
    }

print("=== INSPECTING BLOCK DETAILS FOR COMPACTION ===")

# 1. U12 and R58, R56, R55, R54 on F.Cu
u12 = board.FindFootprintByReference('U12')
print("U12 Crtyd:", get_crtyd_poly(u12))
for p in u12.Pads():
    print(f"  U12 pad {p.GetNumber():2} ({p.GetNetname():25}): ({to_mm(p.GetPosition().x):.3f}, {to_mm(p.GetPosition().y):.3f})")

for r in ['R58', 'R56', 'R55', 'R54', 'C31', 'C32']:
    fp = board.FindFootprintByReference(r)
    print(f"{r:5} pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), rot={fp.GetOrientation().AsDegrees()%360}, Crtyd={get_crtyd_poly(fp)}")

# 2. U1 and bottom row on B.Cu
u1 = board.FindFootprintByReference('U1')
print("\nU1 Crtyd:", get_crtyd_poly(u1))
for p in u1.Pads():
    if to_mm(p.GetPosition().y) > 121.5 or to_mm(p.GetPosition().x) > 78.0:
        print(f"  U1 pad {p.GetNumber():2} ({p.GetNetname():25}): ({to_mm(p.GetPosition().x):.3f}, {to_mm(p.GetPosition().y):.3f})")

for r in ['C1', 'R21', 'R8', 'R64', 'R65', 'R9', 'R14', 'R13']:
    fp = board.FindFootprintByReference(r)
    print(f"{r:5} pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), rot={fp.GetOrientation().AsDegrees()%360}, Crtyd={get_crtyd_poly(fp)}")

# 3. U10 and R2, R3 on F.Cu
u10 = board.FindFootprintByReference('U10')
print("\nU10 Crtyd:", get_crtyd_poly(u10))
for p in u10.Pads():
    print(f"  U10 pad {p.GetNumber():2} ({p.GetNetname():25}): ({to_mm(p.GetPosition().x):.3f}, {to_mm(p.GetPosition().y):.3f})")
for r in ['R2', 'R3']:
    fp = board.FindFootprintByReference(r)
    print(f"{r:5} pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), rot={fp.GetOrientation().AsDegrees()%360}, Crtyd={get_crtyd_poly(fp)}")

# 4. Encoder pull-ups R34, R35, R36 on F.Cu
print("\nEncoder pull-ups:")
for r in ['R34', 'R35', 'R36', 'R62', 'R63']:
    fp = board.FindFootprintByReference(r)
    print(f"{r:5} pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), rot={fp.GetOrientation().AsDegrees()%360}, Crtyd={get_crtyd_poly(fp)}")

# 5. U2 strap pull-ups R15, R37, R10 on F.Cu
print("\nU2 pull-ups:")
u2 = board.FindFootprintByReference('U2')
print("U2 Crtyd:", get_crtyd_poly(u2))
for r in ['R15', 'R37', 'R10', 'R16', 'R1', 'C7', 'C5', 'C6']:
    fp = board.FindFootprintByReference(r)
    print(f"{r:5} pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), rot={fp.GetOrientation().AsDegrees()%360}, Crtyd={get_crtyd_poly(fp)}")

# 6. U11 passives on B.Cu
print("\nU11 passives:")
u11 = board.FindFootprintByReference('U11')
print("U11 Crtyd:", get_crtyd_poly(u11))
for r in ['C23', 'R53', 'R52', 'C24', 'R49', 'R48', 'R47']:
    fp = board.FindFootprintByReference(r)
    print(f"{r:5} pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), rot={fp.GetOrientation().AsDegrees()%360}, Crtyd={get_crtyd_poly(fp)}")

# 7. U13 passives on B.Cu
print("\nU13 passives:")
u13 = board.FindFootprintByReference('U13')
print("U13 Crtyd:", get_crtyd_poly(u13))
for r in ['C35', 'R61']:
    fp = board.FindFootprintByReference(r)
    print(f"{r:5} pos=({to_mm(fp.GetPosition().x):.3f}, {to_mm(fp.GetPosition().y):.3f}), rot={fp.GetOrientation().AsDegrees()%360}, Crtyd={get_crtyd_poly(fp)}")
