import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

# Let's search for gr_rect, gr_line, gr_text that relate to LCD / TFT
gr_items = re.findall(r'\(gr_\w+\s+.*?\n\t\)', pcb, re.DOTALL)
print(f"Total gr_items: {len(gr_items)}")

for item in gr_items:
    if any(k in item for k in ['TFT', 'LCD', 'User.', 'Edge.Cuts', 'Fab']):
        # print first few lines of item
        lines = [l.strip() for l in item.splitlines() if l.strip()]
        print("GR ITEM:", " | ".join(lines[:4]))
