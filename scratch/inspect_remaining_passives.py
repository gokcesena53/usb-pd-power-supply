#!/usr/bin/env python3
import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
def to_mm(val): return pcbnew.ToMM(val)

# Check all passives not yet in compaction_moves
already_moved = {'R58', 'R56', 'R55', 'R54', 'C31', 'C32', 'C1', 'R21', 'R8', 'R64', 'R65', 'R9', 'R14', 'R13', 'R2', 'R3', 'R34', 'R35', 'R36', 'R63', 'R15', 'R37', 'R10', 'C23', 'R53', 'R52', 'C24', 'R49', 'C35', 'R61'}

print(f"Already identified/moved: {len(already_moved)}")

passives = []
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if (ref.startswith('R') or ref.startswith('C')) and not ref.startswith('RShunt'):
        if ref not in already_moved:
            passives.append(fp)

print(f"Remaining passives to audit: {len(passives)}")
for fp in sorted(passives, key=lambda f: f.GetReference()):
    ref = fp.GetReference()
    p = fp.GetPosition()
    px, py = to_mm(p.x), to_mm(p.y)
    rot = fp.GetOrientation().AsDegrees() % 360
    layer = fp.GetLayerName()
    nets = [(pad.GetNumber(), pad.GetNetname()) for pad in fp.Pads()]
    print(f"  {ref:5} ({layer:4}) at ({px:7.3f}, {py:7.3f}) rot={rot:5.1f} | nets={nets}")

