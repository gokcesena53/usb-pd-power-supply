"""TASK-077 relative placement for ESP32-C6-MINI-1-H4 group."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))

targets = {
    'U2':   (160.620, 93.600, 90.0),     # ESP32-C6-MINI-1-H4 module on B.Cu; antenna points EAST
    
    # Power Decoupling along south edge under Pin 3 (163.02, 99.50) & Pin 1,2 GND:
    'C6':   (163.000, 102.500, 0.0),     # 0402 100n high-frequency RF bypass
    'C5':   (163.000, 105.500, 0.0),     # 0805 22uF bulk decoupling for TX bursts
    
    # Reset Timing & Pullup along south edge under Pin 8 (159.02, 99.50):
    'C7':   (159.000, 102.500, 0.0),     # 0402 1uF EN delay timing capacitor
    'R1':   (156.500, 102.500, 0.0),     # 0402 10k EN pull-up resistor
    
    # Tactile buttons (PTS810) stacked in safe corridor below module:
    'SW2':  (158.500, 109.500, 90.0),    # RESET switch (PTS810)
    'SW1':  (158.500, 116.500, 90.0),    # BOOT switch (PTS810)
    
    # West side signals (USB, Boot, Strapping, Enable) in vertical column at x = 152.0 (clear of Edge.Cuts x=149.7):
    'R2':   (152.000, 94.400, 0.0),      # 0402 22R series damping on USB_DM (Pin 17: 155.72, 94.40)
    'R3':   (152.000, 93.000, 0.0),      # 0402 22R series damping on USB_DP (Pin 18: 155.72, 93.60)
    'R16':  (152.000, 98.400, 0.0),      # 0402 10k pull-down on IO0 / ETH_PWR_EN (Pin 12: 155.72, 98.40)
    'R10':  (152.000, 89.600, 0.0),      # 0402 10k pull-up on IO9 / Boot strapping (Pin 23: 155.72, 89.60)
    'R37':  (152.000, 91.200, 0.0),      # 0402 10k pull-up on IO8 (Pin 22: 155.72, 90.40)
    'R15':  (152.000, 87.500, 0.0),      # 0402 22R series damping on ETH_CFG0 (IO8)
    
    # Test points on non-RF west side (clear of Edge.Cuts):
    'TP9':  (152.000, 84.500, 0.0),      # TestPoint on ETH_CFG0
    'TP10': (152.000, 105.000, 0.0),     # TestPoint on ETH_PWR_EN
}

for f in b.GetFootprints():
    ref = f.GetReference()
    if ref in targets:
        x, y, a = targets[ref]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))

p.SaveBoard(str(path), b)
print(f"Applied placement to {len(targets)} footprints in {path}")
