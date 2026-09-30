"""TASK-083 relative placement for ROTARY ENCODER pull-up group (R34, R35, R36)."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

# R34, R35, R36 pull-up resistors (10k 0402) on B.Cu:
# Unified orientation (rot = 90.0):
# Pad 1 (+3.3V) aligned along common supply bus at Y = 116.710 mm
# Pad 2 (ENCODER_A, ENCODER_B, ENCODER_SW) aligned along parallel exit bus at Y = 115.690 mm
targets = {
    'R34': (40.700, 116.200, 90.0),
    'R35': (42.700, 116.200, 90.0),
    'R36': (44.700, 116.200, 90.0),
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
