"""TASK-080 relative placement for ETHERNET MEZANIN (CH9121) + BESLEME ANAHTARI group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    # Soft-start capacitor (100nF 0402) on B.Cu:
    'C21': (140.500, 142.990, 270.0),   # Pad 1 (+3.3V) at (140.50, 142.51); Pad 2 (ETH_PWR_EN) at (140.50, 143.47)
    
    # Gate pull-up resistor (100k 0402) on B.Cu:
    'R17': (143.500, 142.990, 270.0),   # Pad 1 (+3.3V) at (143.50, 142.48); Pad 2 (ETH_PWR_EN) at (143.50, 143.50)
    
    # P-MOSFET high-side switch (TSM3443CX6 SOT-23-6) on B.Cu:
    'Q8':  (147.000, 142.990, 90.0),    # Pad 4 (+3.3V S) at (146.05, 141.85); Pad 3 (ETH_PWR_EN G) at (146.05, 144.13); Pads 1,2,5,6 (ETH_3V3 D) face EAST
    
    # High-frequency bypass capacitor (100nF 0402) on B.Cu:
    'C20': (150.800, 144.260, 270.0),   # Pad 1 (ETH_3V3) at (150.80, 143.78); Pad 2 (GND) at (150.80, 144.74)
    
    # Bulk reservoir capacitor (22uF 0805) on B.Cu:
    'C10': (154.000, 144.260, 270.0),   # Pad 1 (ETH_3V3) at (154.00, 143.31); Pad 2 (GND) at (154.00, 145.21)
    
    # Diagnostic test point for ETH_RUN (D1.0mm) on B.Cu:
    'TP14': (153.000, 155.690, 0.0),    # Pad 1 (ETH_RUN) at (153.00, 155.69), fully accessible for probing
    
    # Waveshare 2-CH UART TO ETH mezzanine module anchor on B.Cu:
    'J8':  (158.287, 158.230, 180.0)    # 2x8 2.54mm header at x=[158.29..160.83], y=[140.45..158.23]; RJ45 at x=[205..214]
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
