import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

nets = set(re.findall(r'\(net\s+"([^"]+)"\)', pcb))
print(f"Total distinct nets in PCB: {len(nets)}")
for n in sorted(nets):
    if any(k in n for k in ['SW', 'EN', 'DISCH', 'ALERT', 'OUT']):
        print(f"  {n}")
