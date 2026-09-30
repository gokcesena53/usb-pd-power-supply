"""TASK-074 relative placement for LM74801 CIKIS ANAHTARI + IDEAL DIYOT group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # High-current power switch:
    'Q5':  (110.5, 54.0, 0.0),       # SQJB60EP Dual N-MOSFET (Common Source: Pins 1,3)
    'D6':  (106.8, 59.5, 0.0),       # BZT52C12 SOD-123 (VGS Zener clamp across Q5A)
    'R54': (106.8, 62.2, 0.0),       # 0402 1k0 dV/dt slew rate resistor
    'C30': (106.8, 64.4, 0.0),       # 0402 22n dV/dt slew rate capacitor
    
    # Controller U12 & decoupling/charge pump:
    'U12': (117.5, 56.5, 0.0),       # LM74801-Q1 WSON-12
    'C31': (122.0, 54.5, 90.0),      # 0603 220n charge pump cap (CAP to VS, away from Q5 heat)
    'C32': (121.5, 58.0, 90.0),      # 0402 100n VS bypass capacitor to GND
    
    # Overvoltage sensing divider and enable pull-down:
    'R55': (111.0, 62.5, 90.0),      # 0402 237k OV_SENSE high-side divider from PD_VBUS_SENSED
    'R56': (113.2, 62.5, 90.0),      # 0402 10k OV_SENSE low-side divider to GND
    'R58': (115.4, 62.5, 90.0),      # 0402 100k SW_EN pull-down to GND
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))
        if ref == 'C30':
            f.Reference().SetPosition(p.VECTOR2I(p.FromMM(106.8), p.FromMM(65.6)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
