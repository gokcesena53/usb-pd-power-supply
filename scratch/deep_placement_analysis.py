import pcbnew
import math
from collections import defaultdict
import json

def ToMM(val):
    return pcbnew.ToMM(val)

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

# 1. Loop Area & Proximity Analysis for U6, U4, U3
print("=== 1. CRITICAL BLOCK PROXIMITY & LOOP ANALYSIS ===")

# U6 Analysis
u6 = board.FindFootprintByReference('U6')
r50 = board.FindFootprintByReference('R50')
r51 = board.FindFootprintByReference('R51')

u6_p1 = [p for p in u6.Pads() if p.GetNumber() == '1'][0]
u6_p2 = [p for p in u6.Pads() if p.GetNumber() == '2'][0]
u6_p3 = [p for p in u6.Pads() if p.GetNumber() == '3'][0]

u6_p1_pos = (ToMM(u6_p1.GetPosition().x), ToMM(u6_p1.GetPosition().y))
u6_p2_pos = (ToMM(u6_p2.GetPosition().x), ToMM(u6_p2.GetPosition().y))
u6_p3_pos = (ToMM(u6_p3.GetPosition().x), ToMM(u6_p3.GetPosition().y))

r50_pos = (ToMM(r50.GetPosition().x), ToMM(r50.GetPosition().y))
r51_pos = (ToMM(r51.GetPosition().x), ToMM(r51.GetPosition().y))

# Before coordinates:
# R50: (111.0, 108.0), R51: (108.0, 108.0)
r50_old = (111.0, 108.0)
r51_old = (108.0, 108.0)

dist_r50_old = math.hypot(r50_old[0] - u6_p2_pos[0], r50_old[1] - u6_p2_pos[1])
dist_r50_new = math.hypot(r50_pos[0] - u6_p2_pos[0], r50_pos[1] - u6_p2_pos[1])

dist_r51_old = math.hypot(r51_old[0] - u6_p1_pos[0], r51_old[1] - u6_p1_pos[1])
dist_r51_new = math.hypot(r51_pos[0] - u6_p1_pos[0], r51_pos[1] - u6_p1_pos[1])

# Loop polygon calculation: U6_p1 -> R51_p1 -> R51_p2 -> U6_p3 -> U6_p2 -> R50_p1 -> R50_p2 -> U6_p1
# Shoelace formula for polygon area:
def polygon_area(pts):
    n = len(pts)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += pts[i][0] * pts[j][1]
        area -= pts[j][0] * pts[i][1]
    return abs(area) / 2.0

old_u6_pts = [u6_p1_pos, (108.0, 108.0), (111.0, 108.0), u6_p2_pos, u6_p3_pos]
new_u6_pts = [u6_p1_pos, r51_pos, r50_pos, u6_p2_pos, u6_p3_pos]

old_u6_area = polygon_area(old_u6_pts)
new_u6_area = polygon_area(new_u6_pts)

print(f"U6-R50 Center Distance: {dist_r50_old:.3f} mm -> {dist_r50_new:.3f} mm (Reduction: {(1 - dist_r50_new/dist_r50_old)*100:.1f}%)")
print(f"U6-R51 Center Distance: {dist_r51_old:.3f} mm -> {dist_r51_new:.3f} mm (Reduction: {(1 - dist_r51_new/dist_r51_old)*100:.1f}%)")
print(f"U6 Feedback Loop Area: {old_u6_area:.2f} mm^2 -> {new_u6_area:.2f} mm^2 (Reduction: {(1 - new_u6_area/old_u6_area)*100:.1f}%)")

# U4 Analysis
u4 = board.FindFootprintByReference('U4')
c9 = board.FindFootprintByReference('C9')
u4_p8 = [p for p in u4.Pads() if p.GetNumber() == '8'][0]
u4_p8_pos = (ToMM(u4_p8.GetPosition().x), ToMM(u4_p8.GetPosition().y))
c9_old = (137.5, 81.0)
c9_new = (ToMM(c9.GetPosition().x), ToMM(c9.GetPosition().y))

dist_c9_old = math.hypot(c9_old[0] - u4_p8_pos[0], c9_old[1] - u4_p8_pos[1])
dist_c9_new = math.hypot(c9_new[0] - u4_p8_pos[0], c9_new[1] - u4_p8_pos[1])

print(f"\nU4-C9 Center Distance: {dist_c9_old:.3f} mm -> {dist_c9_new:.3f} mm (Reduction: {(1 - dist_c9_new/dist_c9_old)*100:.1f}%)")

# U3 Analysis
u3 = board.FindFootprintByReference('U3')
r27 = board.FindFootprintByReference('R27')
u3_p3 = [p for p in u3.Pads() if p.GetNumber() == '3'][0]
u3_p3_pos = (ToMM(u3_p3.GetPosition().x), ToMM(u3_p3.GetPosition().y))
r27_old = (136.75, 107.0)
r27_new = (ToMM(r27.GetPosition().x), ToMM(r27.GetPosition().y))

dist_r27_old = math.hypot(r27_old[0] - u3_p3_pos[0], r27_old[1] - u3_p3_pos[1])
dist_r27_new = math.hypot(r27_new[0] - u3_p3_pos[0], r27_new[1] - u3_p3_pos[1])

print(f"\nU3-R27 Center Distance: {dist_r27_old:.3f} mm -> {dist_r27_new:.3f} mm (Reduction: {(1 - dist_r27_new/dist_r27_old)*100:.1f}%)")

# 2. Net-by-Net Wirelength and Crossing Analysis
print("\n=== 2. DETAILED NET-BY-NET IMPROVEMENT ANALYSIS ===")
# We import analyze_ratsnest from scratch
import sys
sys.path.append('scratch')
from force_repack_optimizer import analyze_ratsnest

rn = analyze_ratsnest(board)
print(f"Current Total Signal Ratsnest Length: {rn['wirelength_mm']} mm")
print(f"Current Total Signal Crossings:       {rn['crossings_count']}")

# Count crossings per net
from collections import Counter
net_crossings = Counter()
for e1, e2 in [(e1, e2) for i, e1 in enumerate(rn['edges']) for e2 in rn['edges'][i+1:]]:
    if e1['net'] != e2['net']:
        A = (e1['p1']['x'], e1['p1']['y'])
        B = (e1['p2']['x'], e1['p2']['y'])
        C = (e2['p1']['x'], e2['p1']['y'])
        D = (e2['p2']['x'], e2['p2']['y'])
        from force_repack_optimizer import intersect
        if intersect(A, B, C, D):
            net_crossings[e1['net']] += 1
            net_crossings[e2['net']] += 1

print("\nTop 10 Remaining Crossings by Net:")
for net, cnt in net_crossings.most_common(10):
    print(f"  {net:35}: {cnt:2d} crossings")
