import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('gopo-drc.rpt', 'r', encoding='utf-8') as f:
    text = f.read()

# find schematic parity section in gopo-drc.rpt
parity_idx = text.find('schematic parity')
if parity_idx != -1:
    print(text[parity_idx:parity_idx+4000])
else:
    # search for parity issues
    for line in text.splitlines():
        if 'parity' in line.lower():
            print(line)
