import re
import math
from itertools import combinations

import os
if os.path.exists("hardware/gopo.kicad_pcb"):
    pcb_path = "hardware/gopo.kicad_pcb"
else:
    pcb_path = "usb-pd-power-supply/hardware/gopo.kicad_pcb"

with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# We need pad positions and their nets
# Footprints:
# (footprint "..." (layer "...") (uuid "...") (at X Y [ROT]) (property "Reference" "REF") ...
#   (pad "NUM" smd/thru_hole ... (at X Y [ROT]) ... (net NET_NUM "NET_NAME"))

# Let's extract pads with their absolute board coordinates and net names
# To compute absolute pad coordinates, we take footprint (at fx fy frot) and pad (at px py prot)
def rotate_point(x, y, angle_deg):
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a

pads_by_net = {}

# Parse footprints
fp_blocks = list(re.finditer(r'\(footprint "([^"]+)".*?\(property "Reference" "([^"]+)".*?\n\t\)', text, re.DOTALL))
if not fp_blocks:
    # try another pattern
    fp_blocks = list(re.finditer(r'\(footprint ".*?\n  \)', text, re.DOTALL))

print(f"Total raw blocks: {len(fp_blocks)}")

# Let's do a more robust parse of footprints and pads
lines = text.splitlines()
current_fp = None
fp_x, fp_y, fp_rot = 0.0, 0.0, 0.0
fp_ref = ""
fp_layer = ""

pad_list = []

i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('(footprint '):
        # find ref, at, layer
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
            
            # find all pads in this footprint
            for pad_m in re.finditer(r'\(pad "([^"]+)"\s+(smd|thru_hole|np_thru_hole|connect)\s+([^\s]+)\s+\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\).*?\(net (?:[0-9]+ )?"([^"]+)"\)', block_text, re.DOTALL):
                p_num = pad_m.group(1)
                px = float(pad_m.group(4))
                py = float(pad_m.group(5))
                prot = float(pad_m.group(6)) if pad_m.group(6) else 0.0
                net = pad_m.group(7)
                
                # compute absolute position
                rx, ry = rotate_point(px, py, frot)
                abs_x = fx + rx
                abs_y = fy + ry
                
                if net and net != "" and net != "unconnected":
                    pad_list.append({
                        'ref': ref,
                        'pad': p_num,
                        'x': abs_x,
                        'y': abs_y,
                        'net': net,
                        'layer': flayer
                    })
        i = j + 1
    else:
        i += 1

print(f"Total connected pads parsed: {len(pad_list)}")

# Group pads by net
from collections import defaultdict
net_pads = defaultdict(list)
for p in pad_list:
    net_pads[p['net']].append(p)

print(f"Total electrical nets with >= 1 pad: {len(net_pads)}")

# Build Minimum Spanning Tree (MST) or nearest-neighbor ratsnest segments for each net
# (We exclude large power/GND planes from visual spiderweb analysis if desired, or analyze both with and without GND)
def get_mst_edges(pads):
    if len(pads) <= 1:
        return []
    # Prim's algorithm for MST
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

all_mst_edges = []
signal_mst_edges = [] # excluding GND, +3.3V, +5V, etc.

power_net_keywords = {'GND', 'power:GND', '+3.3V', '+3V3', '+5V', 'VBUS', 'USB_VBUS', 'PD_VOUT', 'V_PRE', 'OUT_POS'}

for net, pads in net_pads.items():
    mst = get_mst_edges(pads)
    for p1, p2, dist in mst:
        edge = {'net': net, 'p1': p1, 'p2': p2, 'dist': dist}
        all_mst_edges.append(edge)
        is_power = any(kw.lower() in net.lower() for kw in ['gnd', '+3.3v', '3v3', '5v', 'vbus', 'vout', 'v_pre', 'out_pos'])
        if not is_power:
            signal_mst_edges.append(edge)

print(f"Total ratsnest MST edges (all nets): {len(all_mst_edges)}")
print(f"Total ratsnest MST edges (signal nets only): {len(signal_mst_edges)}")

# Line intersection test
def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
    # Check if segment AB intersects CD
    # Exclude if they share endpoints
    if (abs(A[0]-C[0]) < 1e-4 and abs(A[1]-C[1]) < 1e-4) or \
       (abs(A[0]-D[0]) < 1e-4 and abs(A[1]-D[1]) < 1e-4) or \
       (abs(B[0]-C[0]) < 1e-4 and abs(B[1]-C[1]) < 1e-4) or \
       (abs(B[0]-D[0]) < 1e-4 and abs(B[1]-D[1]) < 1e-4):
        return False
    return (ccw(A,C,D) != ccw(B,C,D)) and (ccw(A,B,C) != ccw(A,B,D))

# Let's count intersections in signal nets
crossings = []
for i in range(len(signal_mst_edges)):
    e1 = signal_mst_edges[i]
    A = (e1['p1']['x'], e1['p1']['y'])
    B = (e1['p2']['x'], e1['p2']['y'])
    for j in range(i + 1, len(signal_mst_edges)):
        e2 = signal_mst_edges[j]
        # same net crossing is trivial or impossible in MST, but check different nets
        if e1['net'] == e2['net']:
            continue
        C = (e2['p1']['x'], e2['p1']['y'])
        D = (e2['p2']['x'], e2['p2']['y'])
        if intersect(A, B, C, D):
            crossings.append((e1, e2))

print(f"\n==========================================")
print(f"RATSNEST SIGNAL CROSSING TEST RESULTS")
print(f"==========================================")
print(f"Total signal ratsnest segments: {len(signal_mst_edges)}")
print(f"Total ratsnest intersections (crossings): {len(crossings)}")

# Group crossings by net to see which nets create the most "spiderweb" clutter
crossing_net_counts = defaultdict(int)
for e1, e2 in crossings:
    crossing_net_counts[e1['net']] += 1
    crossing_net_counts[e2['net']] += 1

print("\nTop 15 Nets causing the highest number of crossings (Spiderweb Hotspots):")
for net, count in sorted(crossing_net_counts.items(), key=lambda x: x[1], reverse=True)[:15]:
    print(f"  {net:35}: {count:3d} crossings")

# Also let's check total wirelength
total_signal_wirelength = sum(e['dist'] for e in signal_mst_edges)
print(f"\nTotal Signal Ratsnest Wirelength (MST): {total_signal_wirelength:.2f} mm")
