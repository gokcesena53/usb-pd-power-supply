"""TASK-076 relative placement for CIKIS DESARJI (R59 yerine aktif) group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # Power discharge resistor (2512 2W) on F.Cu:
    'R67': (184.0, 57.5, 0.0),       # Pin 1 (OUT_POS) faces WEST towards INA226/J4; Pin 2 faces EAST
    
    # Discharge switch MOSFET (BSS138P SOT-23) on F.Cu:
    'Q6':  (190.5, 57.5, 180.0),     # Pin 3 (Drain) faces WEST directly to R67.2; Pin 1 (DISCH_G) & Pin 2 (GND) face EAST
    
    # Gate clamp Zener diode (BZT52C12 SOD-123) on F.Cu:
    'D10': (195.0, 57.5, 90.0),      # Pin 1 (Cathode/DISCH_G) on SOUTH; Pin 2 (Anode/GND) on NORTH
    
    # Gate pull-up resistor (100k 0603) on F.Cu:
    'R66': (198.5, 57.5, -90.0),     # Pin 1 (SW_OUT) on NORTH; Pin 2 (DISCH_G) on SOUTH
    
    # Enable inverter MOSFET (BSS138P SOT-23) on B.Cu:
    'Q4':  (191.0, 62.5, 0.0),       # Pin 1 (SW_EN) & Pin 2 (GND) face WEST towards U13; Pin 3 (DISCH_G) faces EAST
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
