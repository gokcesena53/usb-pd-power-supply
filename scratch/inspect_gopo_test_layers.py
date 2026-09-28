with open("hardware/gopo_test.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re
for ref in ['R34', 'R35', 'R36', 'R2', 'R3']:
    m = re.search(r'\(footprint "([^"]+)".*?\(property "Reference" "' + ref + r'".*?\n  \)', text, re.DOTALL)
    if m:
        block = m.group(0)
        at = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)', block)
        layer = re.search(r'\(layer "([^"]+)"\)', block)
        print(f"{ref}: layer={layer.group(1)} at ({at.group(1)}, {at.group(2)})")
    else:
        print(f"{ref}: NOT FOUND")
