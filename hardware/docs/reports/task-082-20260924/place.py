"""TASK-082 relative placement for TFT CONNECTOR J3 group (C34 bypass capacitor)."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

# C34 decoupling capacitor (100nF / 1u0, 0402) on F.Cu:
# Placed on the solder-pad side (+X) of locked anchor J3 (98.000, 109.300, rot 90.0)
# Immediately adjacent to J3 Pins 21-23 (+3.3V) and Pin 25 (GND).
targets = {
    'C34': (101.000, 105.550, 90.0)
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
