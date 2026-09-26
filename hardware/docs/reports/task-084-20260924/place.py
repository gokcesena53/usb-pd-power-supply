"""TASK-084 relative placement for TEST NOKTALARI group (TP6-TP8, TP11-TP13)."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

# Standardized 100 mil (2.540 mm) pitch clusters:
# 1. UART debug & programming port on F.Cu: TP11 (TX), TP12 (RX), TP13 (GND)
# 2. I2C bus diagnostic port on B.Cu: TP6 (SCL), TP7 (SDA), TP8 (INT)
targets = {
    'TP11': (207.500, 122.000, 0.0),
    'TP12': (210.040, 122.000, 0.0),
    'TP13': (212.580, 122.000, 0.0),
    'TP6':  (207.500, 126.000, 0.0),
    'TP7':  (210.040, 126.000, 0.0),
    'TP8':  (212.580, 126.000, 0.0),
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
