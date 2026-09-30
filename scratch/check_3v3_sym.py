import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'\(symbol\s+\(lib_id\s+"power:\+3\.3V"\).*?\(instances.*?\n\t\)', text, re.DOTALL)
print(f"Total +3.3V symbols: {len(matches)}")
if matches:
    print(matches[0])
