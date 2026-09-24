"""TASK-081 relative placement for TFT BACKLIGHT (3.3V + PWM) group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # N-MOSFET backlight low-side switch (IRLML6344TRPBF SOT-23) on F.Cu:
    'Q7':  (22.000, 99.000, 0.0),    # Pad 1 (Gate) at (21.06, 98.05); Pad 2 (GND) at (21.06, 99.95); Pad 3 (BL_K) faces EAST at (22.94, 99.00)
    
    # Gate pull-down resistor (100k 0402) on F.Cu:
    'R29': (18.800, 99.000, 270.0),  # Pad 1 (Gate) at (18.80, 98.49); Pad 2 (GND) at (18.80, 99.51); bridges Gate to Source vertically
    
    # PWM series gate damping resistor (100R 0402) on F.Cu:
    'R28': (16.000, 98.050, 0.0),    # Pad 1 (TFT_BL_PWM) at (15.49, 98.05) faces WEST; Pad 2 (Gate) at (16.51, 98.05) faces EAST
    
    # Backlight current limiting resistor (5R6 0805) on F.Cu:
    'R60': (22.000, 94.500, 0.0)     # Pad 1 (+3.3V) at (21.09, 94.50); Pad 2 (BL_A) at (22.91, 94.50) faces EAST directly to J3.2
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
