import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

# search for (net 
m = re.findall(r'\(net\s+\d+\s+.*?\)', pcb)
print(f"Total (net ...) matches: {len(m)}")
for x in m[:20]:
    print(" ", x)
