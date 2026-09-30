"""TASK-071 relative B.Cu placement for AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # High-current power stage:
    'R11': (52.0, 140.0, 0.0),       # 2512 shunt resistor (Pin 1 USB_VBUS, Pin 2 PD_VBUS_SENSED)
    'C3':  (51.5, 145.0, 180.0),     # 0805 cSnkBulk cap (facing input/boundary)
    'Q3':  (59.5, 140.0, 0.0),       # Vishay PowerPAK SO-8L Dual MOSFET
    'C8':  (65.5, 140.0, -90.0),     # 1210 PD_VOUT output cap
    'TH1': (56.0, 145.2, 90.0),      # 0402 NTC thermistor near Q3 thermal pad
    'R12': (61.0, 145.2, 90.0),      # 0402 gate drive resistor between U1.23 and Q3.2/4
    'R13': (65.5, 144.5, 0.0),       # 0402 VOUT sense resistor near Q3.5 and C8
    
    # Test points:
    'TP1': (46.5, 140.0, 0.0),       # USB_VBUS test point
    'TP2': (54.5, 135.5, 0.0),       # PD_VBUS_SENSED test point
    'TP3': (69.5, 140.0, 0.0),       # PD_VOUT test point
    'TP5': (61.0, 134.5, 0.0),       # PD_GATE test point
    'TP4': (52.0, 149.0, 0.0),       # PD_5V test point
    
    # Controller U1 and direct bypass capacitors:
    'U1':  (60.0, 150.5, 180.0),     # AP33772SDKZ-13-FA02 QFN-24 (CC pins face left towards USB-C)
    'C4':  (56.0, 148.5, 0.0),       # 0402 1u0 PD_5V bypass (pin 20)
    'C2':  (55.5, 151.5, 0.0),       # 0402 100n IFB filter (pin 15)
    'C1':  (57.5, 155.5, 0.0),       # 0402 100n V18 bypass (pin 12)
    'R21': (59.8, 155.5, 0.0),       # 0402 100k VSEL pull-down (pin 11)
    
    # Interrupt divider / level shifter:
    'R8':  (62.2, 155.5, 0.0),       # 0402 10k PD_INT_5V
    'R64': (64.5, 155.5, 0.0),       # 0402 2k0
    'R65': (66.8, 155.5, 0.0),       # 0402 10k
    'R9':  (69.1, 155.5, 0.0),       # 0402 10k PD_INT_3V3
    
    # LED indicator:
    'R14': (64.2, 150.5, 0.0),       # 0402 2k2 LED series resistor
    'D1':  (67.2, 150.5, 180.0),     # 0402 LED indicator
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
