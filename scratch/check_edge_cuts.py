from audit_rc_extractor import parse_kicad_pcb

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')

lines = []
for node in tree:
    if isinstance(node, list) and len(node) > 0 and node[0] == 'gr_line':
        # (gr_line (start 57.5 70.0) (end 157.5 70.0) (layer "Edge.Cuts") ...)
        l_layer = None
        start = None
        end = None
        for elem in node[1:]:
            if isinstance(elem, list) and len(elem) > 0:
                if elem[0] == 'layer':
                    l_layer = elem[1]
                elif elem[0] == 'start':
                    start = (float(elem[1]), float(elem[2]))
                elif elem[0] == 'end':
                    end = (float(elem[1]), float(elem[2]))
        if l_layer == 'Edge.Cuts' and start and end:
            lines.append((start, end))

print(f"Edge.Cuts lines: {len(lines)}")
xs = [p[0] for l in lines for p in l]
ys = [p[1] for l in lines for p in l]
print(f"X range: {min(xs)} to {max(xs)}")
print(f"Y range: {min(ys)} to {max(ys)}")
