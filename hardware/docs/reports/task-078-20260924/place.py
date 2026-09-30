"""TASK-078 relative placement for RTC BQ32000 + 1F5 supercapacitor group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # 1.5F 5.5V horizontal coin cell supercapacitor (Korchip DCL) on B.Cu:
    'C33': (207.980, 82.500, 180.0),    # Pad 1 (VBACK) at (207.98, 82.50); Pad 2 (GND) at (227.98, 82.50)
    
    # BQ32000 Real-Time Clock IC (SOIC-8) on B.Cu:
    'U4':  (214.000, 99.000, 180.0),    # Pins 1-4 (OSCI, OSCO, VBACK, GND) face EAST; Pins 5-8 face WEST
    
    # 32.768kHz Tuning Fork Crystal (Abracon ABS25) on B.Cu:
    'Y1':  (223.500, 97.725, 270.0),    # Pad 1 (OSCI) & Pad 4 (OSCO) face WEST directly towards U4; Pads 2,3 GND face EAST
    
    # 1uF 0402 VCC bypass capacitor on B.Cu:
    'C9':  (211.500, 94.500, 90.0),     # Pad 1 (+3.3V) faces SOUTH directly towards U4.8; Pad 2 (GND) faces NORTH
    
    # 4.7k 0402 IRQ pull-up resistor on B.Cu:
    'R24': (208.500, 97.700, 0.0),      # Pad 1 (+3.3V) faces WEST; Pad 2 (RTC_INT) faces EAST directly to U4.7
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
