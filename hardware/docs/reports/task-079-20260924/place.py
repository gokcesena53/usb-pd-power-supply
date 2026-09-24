"""TASK-079 relative placement for I2C SEVIYE DONUSTURUCU 5V <-> 3.3V group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # Channel 1: SCL level shifter column at x = 209.0 mm (B.Cu)
    'R4': (209.000, 107.500, 180.0),    # 4.7k 0402 pull-up to +3.3V on SCL_3V3 (Pad 1: SCL_3V3, Pad 2: +3.3V)
    'Q1': (209.000, 111.000, 270.0),    # BSS138P SOT-23 N-MOSFET (Pad 1: +3.3V Gate, Pad 2: SCL_3V3 Source, Pad 3: SCL_5V Drain)
    'R5': (209.000, 114.500, 90.0),     # 4.7k 0402 pull-up to PD_5V on SCL_5V (Pad 1: PD_5V, Pad 2: SCL_5V)
    
    # Channel 2: SDA level shifter column at x = 213.5 mm (B.Cu)
    'R7': (213.500, 107.500, 0.0),      # 4.7k 0402 pull-up to +3.3V on SDA_3V3 (Pad 1: +3.3V, Pad 2: SDA_3V3)
    'Q2': (213.500, 111.000, 270.0),    # BSS138P SOT-23 N-MOSFET (Pad 1: +3.3V Gate, Pad 2: SDA_3V3 Source, Pad 3: SDA_5V Drain)
    'R6': (213.500, 114.500, 90.0),     # 4.7k 0402 pull-up to PD_5V on SDA_5V (Pad 1: PD_5V, Pad 2: SDA_5V)
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
