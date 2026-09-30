import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

nets = re.findall(r'\(net\s+(\d+)\s+"([^"]*)"\)', pcb[:20000])
print(f"Found {len(nets)} nets:")
for nid, nname in nets:
    if any(k in nname for k in ['3V3', '3.3V', 'PRE', 'OUT', 'SW_EN', 'EN', 'POS']):
        print(f"  Net {nid}: '{nname}'")
