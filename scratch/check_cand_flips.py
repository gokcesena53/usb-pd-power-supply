#!/usr/bin/env python3
import sys
sys.path.append('scratch')
import pcbnew
from force_repack_optimizer import analyze_ratsnest

b_cand = pcbnew.LoadBoard('scratch/candidate_compaction.kicad_pcb')

# Let's test rotating candidate 2-pin passives by 180 degrees to see if crossings decrease!
test_refs = ['R58', 'R56', 'R55', 'R54', 'C31', 'C32', 'C1', 'R21', 'R8', 'R64', 'R65', 'R9', 'R14', 'R13', 'R2', 'R3', 'R34', 'R35', 'R36', 'R63', 'R15', 'R37', 'R10', 'C23', 'R53', 'R52', 'C24', 'R49', 'C35', 'R61', 'C21']

rn_curr = analyze_ratsnest(b_cand)
base_crossings = rn_curr['crossings_count']
base_len = rn_curr['wirelength_mm']

print(f"Current cand: crossings={base_crossings}, len={base_len}")

for ref in test_refs:
    fp = b_cand.FindFootprintByReference(ref)
    old_rot = fp.GetOrientation().AsDegrees() % 360
    new_rot = (old_rot + 180.0) % 360
    fp.SetOrientationDegrees(new_rot)
    rn = analyze_ratsnest(b_cand)
    if rn['crossings_count'] < base_crossings or (rn['crossings_count'] == base_crossings and rn['wirelength_mm'] < base_len):
        print(f"Beneficial 180 flip for {ref:5}: rot {old_rot} -> {new_rot}: crossings={rn['crossings_count']} (delta={rn['crossings_count']-base_crossings}), len={rn['wirelength_mm']} (delta={rn['wirelength_mm']-base_len:.2f})")
    # restore
    fp.SetOrientationDegrees(old_rot)

