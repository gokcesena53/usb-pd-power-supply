with open("hardware/gopo.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

from simulate_task102 import move_comp

# Let's test placing R34, R35, R36 on F.Cu at X=65.0, 67.5, 70.0, Y=96.0 (or Y=92.0)
cand = text
cand = move_comp(cand, 'R34', 65.0, 96.0, 0.0, 'F.Cu')
cand = move_comp(cand, 'R35', 67.5, 96.0, 0.0, 'F.Cu')
cand = move_comp(cand, 'R36', 70.0, 96.0, 0.0, 'F.Cu')

# And R2, R3 on F.Cu
# Where should R2 and R3 go?
# Let's see: U10 is at (61.5, 88.5). U2 pins 17, 18 at (77.12, 79.97), (77.92, 79.97).
# Let's test R2 at (66.0, 86.0), R3 at (68.0, 86.0) on F.Cu
cand = move_comp(cand, 'R2', 66.0, 86.0, 90.0, 'F.Cu')
cand = move_comp(cand, 'R3', 68.0, 86.0, 90.0, 'F.Cu')

with open("scratch/candidate_task102.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(cand)

print("Saved candidate PCB with R34-R36 and R2-R3 on F.Cu")
