"""TASK-075 relative placement for INA226 OLCUM + PANEL CIKISI group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # Precision shunt & current/power monitor:
    'RShunt1': (157.0, 56.5, 0.0),       # 2512 5m0 (Pad 1: SW_OUT west, Pad 2: OUT_POS east)
    'U3':      (157.75, 51.0, -90.0),    # TSSOP-10 INA226 (Kelvin pins face south towards RShunt1)
    'C11':     (162.2, 53.0, 0.0),       # 0402 100n VS decoupling next to U3 pins 6,7
    'R27':     (152.5, 48.85, 0.0),      # 0402 10k ALERT pullup next to U3.3
    
    # TVS, passive bleed & Output connector:
    'J4':      (168.0, 51.5, 0.0),       # 1x02 wire terminal (Pad 1: OUT_POS, Pad 2: GND)
    'D7':      (167.0, 57.5, 0.0),       # SMB TVS SMBJ30A (Pad 1: OUT_POS, Pad 2: GND)
    'R59':     (167.0, 62.5, 0.0),       # 0603 100k passive backup bleed (Pad 1: OUT_POS, Pad 2: GND)
    
    # Logic & protection gate:
    'U13':     (150.0, 62.0, 0.0),       # SOT-23-5 74LVC1G08
    'R61':     (146.5, 62.95, 0.0),      # 0402 4k7 OUT_EN pulldown next to U13.1
    'C35':     (153.5, 62.95, 0.0),      # 0402 100n U13 VCC decoupling next to U13.5
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
