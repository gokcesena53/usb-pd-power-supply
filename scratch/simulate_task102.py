import re
import math
from collections import defaultdict

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

def rotate_point(x, y, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a

def get_mst_edges(pads):
    if len(pads) <= 1:
        return []
    edges = []
    visited = [0]
    unvisited = list(range(1, len(pads)))
    while unvisited:
        best_dist = float('inf')
        best_u, best_v = -1, -1
        for u in visited:
            p1 = pads[u]
            for v in unvisited:
                p2 = pads[v]
                d = math.hypot(p1['x'] - p2['x'], p1['y'] - p2['y'])
                if d < best_dist:
                    best_dist = d
                    best_u = u
                    best_v = v
        visited.append(best_v)
        unvisited.remove(best_v)
        edges.append((pads[best_u], pads[best_v], best_dist))
    return edges

def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
    if (abs(A[0]-C[0]) < 1e-4 and abs(A[1]-C[1]) < 1e-4) or \
       (abs(A[0]-D[0]) < 1e-4 and abs(A[1]-D[1]) < 1e-4) or \
       (abs(B[0]-C[0]) < 1e-4 and abs(B[1]-C[1]) < 1e-4) or \
       (abs(B[0]-D[0]) < 1e-4 and abs(B[1]-D[1]) < 1e-4):
        return False
    return (ccw(A,C,D) != ccw(B,C,D)) and (ccw(A,B,C) != ccw(A,B,D))

def evaluate_pcb(pcb_text):
    lines = pcb_text.splitlines()
    pad_list = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith('(footprint '):
            j = i
            depth = 0
            block_lines = []
            while j < len(lines):
                l = lines[j]
                block_lines.append(l)
                depth += l.count('(') - l.count(')')
                if depth == 0:
                    break
                j += 1
            block_text = "\n".join(block_lines)
            ref_m = re.search(r'\(property "Reference" "([^"]+)"', block_text)
            at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', block_text)
            layer_m = re.search(r'\(layer "([^"]+)"\)', block_text)
            if ref_m and at_m:
                ref = ref_m.group(1)
                fx = float(at_m.group(1))
                fy = float(at_m.group(2))
                frot = float(at_m.group(3)) if at_m.group(3) else 0.0
                flayer = layer_m.group(1) if layer_m else "F.Cu"
                for pad_m in re.finditer(r'\(pad "([^"]+)"\s+(?:smd|thru_hole|np_thru_hole|connect)\s+[^\s]+\s+\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\).*?\(net (?:[0-9]+ )?"([^"]+)"\)', block_text, re.DOTALL):
                    p_num = pad_m.group(1)
                    px = float(pad_m.group(2))
                    py = float(pad_m.group(3))
                    prot = float(pad_m.group(4)) if pad_m.group(4) else 0.0
                    net = pad_m.group(5)
                    rx, ry = rotate_point(px, py, frot)
                    if net and net != "unconnected":
                        pad_list.append({
                            'ref': ref, 'pad': p_num, 'x': fx + rx, 'y': fy + ry, 'net': net, 'layer': flayer
                        })
            i = j + 1
        else:
            i += 1
    
    net_pads = defaultdict(list)
    for p in pad_list:
        net_pads[p['net']].append(p)
    
    signal_mst_edges = []
    for net, p_list in net_pads.items():
        is_power = any(kw in net.lower() for kw in ['gnd', '+3.3v', '3v3', '5v', 'vbus', 'vout', 'v_pre', 'out_pos'])
        if not is_power:
            edges = get_mst_edges(p_list)
            for p1, p2, dist in edges:
                signal_mst_edges.append({'net': net, 'p1': p1, 'p2': p2, 'dist': dist})
    
    crossings = 0
    for i in range(len(signal_mst_edges)):
        e1 = signal_mst_edges[i]
        A = (e1['p1']['x'], e1['p1']['y'])
        B = (e1['p2']['x'], e1['p2']['y'])
        for k in range(i + 1, len(signal_mst_edges)):
            e2 = signal_mst_edges[k]
            if e1['net'] == e2['net']: continue
            C = (e2['p1']['x'], e2['p1']['y'])
            D = (e2['p2']['x'], e2['p2']['y'])
            if intersect(A, B, C, D):
                crossings += 1
    
    wirelength = sum(e['dist'] for e in signal_mst_edges)
    return len(signal_mst_edges), crossings, wirelength

def move_comp(pcb_txt, ref, new_x, new_y, new_rot=None, new_layer=None):
    lines = pcb_txt.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('(footprint '):
            j = i
            depth = 0
            while j < len(lines):
                depth += lines[j].count('(') - lines[j].count(')')
                if depth == 0: break
                j += 1
            block_lines = lines[i:j+1]
            block_text = "\n".join(block_lines)
            if f'(property "Reference" "{ref}"' in block_text:
                # modify block_lines
                for idx in range(len(block_lines)):
                    if block_lines[idx].strip().startswith('(at '):
                        m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', block_lines[idx])
                        cur_rot = m.group(3) if m and m.group(3) else "0"
                        rot_to_use = str(new_rot) if new_rot is not None else cur_rot
                        indent = block_lines[idx][:block_lines[idx].find('(at')]
                        block_lines[idx] = f"{indent}(at {new_x:.3f} {new_y:.3f} {rot_to_use})"
                        break
                if new_layer is not None:
                    for idx in range(len(block_lines)):
                        if block_lines[idx].strip().startswith('(layer '):
                            indent = block_lines[idx][:block_lines[idx].find('(layer')]
                            block_lines[idx] = f'{indent}(layer "{new_layer}")'
                            break
                lines[i:j+1] = block_lines
                return "\n".join(lines)
            i = j + 1
        else:
            i += 1
    return pcb_txt

# Let's test moving R34, R35, R36 to B.Cu corridor between J9 and U2
# J9 is at X=61.5, Y=104.0. U2 pins 27-29 at X=83.82, Y=76-77.5.
# Let's test placing R34, R35, R36 at X=64.0, 66.5, 69.0, Y=89.0
txt_test = text
txt_test = move_comp(txt_test, 'R34', 64.0, 89.0, 90.0, 'B.Cu')
txt_test = move_comp(txt_test, 'R35', 66.5, 89.0, 90.0, 'B.Cu')
txt_test = move_comp(txt_test, 'R36', 69.0, 89.0, 90.0, 'B.Cu')

_, c_enc, wl_enc = evaluate_pcb(txt_test)
print(f"R34-R36 Moved to (64..69, 89): Crossings: 185 -> {c_enc}, Wirelength: 1450.84 -> {wl_enc:.2f} mm")

# Also test moving R2 and R3 to natural flow between U10 and U2
# U10 is at (61.5, 88.5). U2 pins 17, 18 at (77.12, 79.97), (77.92, 79.97).
# Let's test placing R2 at (66.5, 85.0), R3 at (68.5, 85.0) on F.Cu
txt_test2 = txt_test
txt_test2 = move_comp(txt_test2, 'R2', 66.5, 85.0, 90.0, 'F.Cu')
txt_test2 = move_comp(txt_test2, 'R3', 68.5, 85.0, 90.0, 'F.Cu')

_, c_both, wl_both = evaluate_pcb(txt_test2)
print(f"Plus R2, R3 Moved to (66.5..68.5, 85.0): Crossings: 185 -> {c_both}, Wirelength: 1450.84 -> {wl_both:.2f} mm")
