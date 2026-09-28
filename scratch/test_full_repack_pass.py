#!/usr/bin/env python3
import os
import sys
import json
import math
import shutil
import subprocess
import pcbnew
from repack_engine import run_repack

# Copy dru to test directory
shutil.copy('hardware/gopo.kicad_dru', 'scratch/cand_repack.kicad_dru')

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
targets = run_repack()

print("\n--- APPLYING CANDIDATE MODIFICATIONS ---")
applied = {}
for ref, t in sorted(targets.items()):
    fp = board.FindFootprintByReference(ref)
    if fp:
        old_pos = fp.GetPosition()
        old_x, old_y = pcbnew.ToMM(old_pos.x), pcbnew.ToMM(old_pos.y)
        old_rot = fp.GetOrientation().AsDegrees() % 360
        fp.SetPosition(pcbnew.VECTOR2I_MM(t['x'], t['y']))
        fp.SetOrientationDegrees(t['rot'])
        applied[ref] = {
            'ref': ref,
            'ic': t['ic'],
            'pin': t['pin'],
            'old': (round(old_x, 3), round(old_y, 3), round(old_rot, 1)),
            'new': (t['x'], t['y'], t['rot'])
        }
        print(f"Applied {t['ic']}-{ref:4}: ({old_x:7.3f}, {old_y:7.3f}) rot={old_rot:5.1f} -> ({t['x']:7.3f}, {t['y']:7.3f}) rot={t['rot']:5.1f}")

test_pcb = 'scratch/cand_repack.kicad_pcb'
board.Save(test_pcb)

print("\n--- MEASURING GEOMETRIC CONSTRAINTS ---")
# Now measure distances with updated board
reloaded = pcbnew.LoadBoard(test_pcb)
distance_results = []
unoptimized_list = []

decoupling_caps = {'C1', 'C2', 'C4', 'C8', 'C6', 'C11', 'C9', 'C14', 'C18', 'C26', 'C23', 'C32', 'C35'}

for ref, t in sorted(targets.items()):
    fp = reloaded.FindFootprintByReference(ref)
    ic_fp = reloaded.FindFootprintByReference(t['ic'])
    
    # find ic pin
    ic_pad = [p for p in ic_fp.Pads() if p.GetNumber() == t['pin']][0]
    ux, uy = pcbnew.ToMM(ic_pad.GetPosition().x), pcbnew.ToMM(ic_pad.GetPosition().y)
    
    px, py = pcbnew.ToMM(fp.GetPosition().x), pcbnew.ToMM(fp.GetPosition().y)
    center_dist = math.hypot(px - ux, py - uy)
    
    is_dec = ref in decoupling_caps
    min_pad_dist = 999.0
    for pad in fp.Pads():
        pax, pay = pcbnew.ToMM(pad.GetPosition().x), pcbnew.ToMM(pad.GetPosition().y)
        d = math.hypot(pax - ux, pay - uy)
        if d < min_pad_dist:
            min_pad_dist = d
            
    violates = False
    reasons = []
    if center_dist > 2.0:
        violates = True
        reasons.append(f"center_dist={center_dist:.3f}mm > 2.0mm")
    if is_dec and min_pad_dist > 1.2:
        violates = True
        reasons.append(f"pad_dist={min_pad_dist:.3f}mm > 1.2mm")
        
    res_entry = {
        'comp': f"{t['ic']}-{ref}",
        'ref': ref,
        'ic': t['ic'],
        'pin': t['pin'],
        'center_dist_mm': round(center_dist, 3),
        'min_pad_dist_mm': round(min_pad_dist, 3),
        'is_decoupling': is_dec,
        'violates': violates,
        'reasons': reasons
    }
    distance_results.append(res_entry)
    if violates:
        unoptimized_list.append(res_entry)
    status_str = "PASS" if not violates else "FAIL"
    print(f"  [{status_str:4}] {t['ic']}-{ref:4} (pin {t['pin']:2}): center={center_dist:.3f}mm (limit 2.0), pad={min_pad_dist:.3f}mm (limit 1.2) -> {', '.join(reasons) if reasons else 'OK'}")

print(f"\nTotal components evaluated: {len(distance_results)}")
print(f"Compliant: {len(distance_results) - len(unoptimized_list)}")
print(f"Unoptimized / Violating: {len(unoptimized_list)}")

print("\n--- RUNNING KICAD 10 DRC & SCHEMATIC PARITY ---")
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
rpt = 'scratch/cand_repack_drc.rpt'
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "-o", rpt, test_pcb]
subprocess.run(cmd, capture_output=True, text=True)

with open(rpt, 'r', encoding='utf-8') as f:
    text = f.read()

import re
drc_violations_count = None
unconnected_count = None
footprint_errors_count = None
schematic_parity_count = 0

for line in text.splitlines():
    if "Found" in line and "DRC violations" in line:
        drc_violations_count = int(line.split()[2])
    elif "Found" in line and "unconnected pads" in line:
        unconnected_count = int(line.split()[2])
    elif "Found" in line and "Footprint errors" in line:
        footprint_errors_count = int(line.split()[2])
    elif "schematic_parity" in line or "schematic parity" in line:
        schematic_parity_count += 1

overlaps = re.findall(r'\[courtyards_overlap\].*?(?=\n\s*\[|\Z)', text, re.DOTALL)
print(f"DRC Violations:   {drc_violations_count} (baseline <= 165)")
print(f"Unconnected Pads: {unconnected_count} (baseline == 360)")
print(f"Footprint Errors: {footprint_errors_count} (must be 0)")
print(f"Schematic Parity: {schematic_parity_count} (must be 0)")
print(f"Courtyard Overlaps: {len(overlaps)}")
for o in overlaps:
    print("  " + o.strip().replace('\n', ' '))
