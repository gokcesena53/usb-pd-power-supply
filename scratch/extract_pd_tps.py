import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

symbols = re.findall(r'\(symbol\s+.*?\(uuid\s+"[^"]+"\)\s*\)', sch, re.DOTALL)
print(f"Total symbols in usb_pd_controller.kicad_sch: {len(symbols)}")

for s in symbols:
    m_ref = re.search(r'\(property\s+"Reference"\s+"(TP\d+)"', s)
    if m_ref:
        print("--------------------")
        print(f"Ref: {m_ref.group(1)}")
        for line in s.splitlines():
            if any(k in line for k in ['property "Value"', 'property "Footprint"', 'at ', 'uuid ']):
                print(" ", line.strip())
