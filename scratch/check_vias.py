import re
from audit_rc_extractor import parse_kicad_pcb

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')

vias = []
for node in tree:
    if isinstance(node, list) and len(node) > 0 and node[0] == 'via':
        # (via (at 123.4 56.7) (size 0.8) (drill 0.4) (layers "F.Cu" "B.Cu") (net 1 "GND"))
        vx, vy = 0.0, 0.0
        vnet = ""
        for elem in node[1:]:
            if isinstance(elem, list) and len(elem) > 0:
                if elem[0] == 'at':
                    vx = float(elem[1])
                    vy = float(elem[2])
                elif elem[0] == 'net':
                    vnet = elem[1] if len(elem) == 2 else elem[2]
        vias.append({'pos': (vx, vy), 'net': vnet})

print(f"Total vias on board: {len(vias)}")
gnd_vias = [v for v in vias if v['net'] == 'GND']
print(f"GND vias on board: {len(gnd_vias)}")
