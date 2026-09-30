import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect where +3.3V symbols are
pwr_3v3 = re.findall(r'\(symbol\s+\(lib_id\s+"power:\+3\.3V"\).*?\(at\s+([-\d.]+)\s+([-\d.]+)', text, re.DOTALL)
print("+3.3V positions in sch:", pwr_3v3)

# Let's inspect around (186.69, 52.07) for V_PRE
print("\nObjects near (186.69, 52.07):")
symbols = re.findall(r'\(symbol\s+.*?\(at\s+([-\d.]+)\s+([-\d.]+).*?\(property\s+"Reference"\s+"([^"]+)"', text, re.DOTALL)
for x, y, ref in symbols:
    x, y = float(x), float(y)
    if abs(x - 186.69) <= 25 and abs(y - 52.07) <= 25:
        print(f"  Symbol {ref} at ({x}, {y})")

# Let's inspect around (302.26, 50.8) and (312.42, 78.74) for OUT_POS
print("\nObjects near (302.26, 50.8):")
for x, y, ref in symbols:
    x, y = float(x), float(y)
    if abs(x - 302.26) <= 25 and abs(y - 50.8) <= 25:
        print(f"  Symbol {ref} at ({x}, {y})")

# Let's inspect around (184.15, 67.31) for SW_EN
print("\nObjects near (184.15, 67.31):")
for x, y, ref in symbols:
    x, y = float(x), float(y)
    if abs(x - 184.15) <= 25 and abs(y - 67.31) <= 25:
        print(f"  Symbol {ref} at ({x}, {y})")
