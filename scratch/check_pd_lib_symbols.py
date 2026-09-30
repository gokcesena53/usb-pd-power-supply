import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# find lib_symbols section
idx = text.find('(lib_symbols')
end_idx = text.find('\n  (symbol\n', idx)
lib_syms = text[idx:idx+15000]

syms = re.findall(r'\(symbol\s+"([^"]+)"', lib_syms)
for s in syms:
    if any(k in s for k in ['3V3', '3.3V', 'TestPoint', 'GND']):
        print("Lib symbol:", s)
