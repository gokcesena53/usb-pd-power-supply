import re

with open("hardware/gopo.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

from simulate_task102 import move_comp

# Let's test candidate positions:
# R34, R35, R36 on B.Cu at X=64.0, 66.5, 69.0, Y=89.0 (0402 pitch = 2.5 mm, rot=90)
cand = text
cand = move_comp(cand, 'R34', 64.0, 89.0, 90.0, 'B.Cu')
cand = move_comp(cand, 'R35', 66.5, 89.0, 90.0, 'B.Cu')
cand = move_comp(cand, 'R36', 69.0, 89.0, 90.0, 'B.Cu')

# R2, R3 on F.Cu between U10 and U2
# U10 is at (61.5, 88.5). C6 is at (71.0, 83.0).
# Let's check R2, R3 coordinates:
# R2 at (66.0, 85.5, rot=90), R3 at (68.0, 85.5, rot=90) on F.Cu
cand = move_comp(cand, 'R2', 66.0, 85.5, 90.0, 'F.Cu')
cand = move_comp(cand, 'R3', 68.0, 85.5, 90.0, 'F.Cu')

with open("scratch/candidate_task102.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(cand)

print("Saved scratch/candidate_task102.kicad_pcb")
