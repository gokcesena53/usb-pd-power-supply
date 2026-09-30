import re

pcb_path = "usb-pd-power-supply/hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
for i, line in enumerate(lines):
    if '(property "Reference" "TP' in line:
        ref = re.search(r'\(property "Reference" "(TP\d+)"', line).group(1)
        # look backward a few lines for layer and at
        context = lines[max(0, i-10):i+5]
        layer = None
        at = None
        for cl in lines[max(0, i-10):i]:
            if '(layer "' in cl:
                layer = cl.strip()
            if '(at ' in cl:
                at = cl.strip()
        print(f"{ref}: {layer}, {at}")
