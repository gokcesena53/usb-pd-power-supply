import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

m = re.findall(r'\(pad\s+.*?\n\t\t\)', pcb, re.DOTALL)
print(f"Total pads: {len(m)}")
if m:
    print("Example pad:")
    print(m[0])
    for p in m[:10]:
        if 'net' in p:
            print("Pad with net:")
            print(p)
            break
