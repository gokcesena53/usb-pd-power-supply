#!/usr/bin/env python3
"""
Test full expanded compaction pass on scratch board and run DRC
"""
import pcbnew
import math
import shutil
import subprocess
import json
import re

def to_mm(val):
    return pcbnew.ToMM(val)

shutil.copy('hardware/gopo.kicad_dru', 'scratch/candidate_compaction.kicad_dru')
src_pcb = 'hardware/gopo.kicad_pcb'
test_pcb = 'scratch/candidate_compaction.kicad_pcb'
board = pcbnew.LoadBoard(src_pcb)

# Define expanded compaction modifications
compaction_moves = {
    # 1. U12 block passives (F.Cu)
    # Pull R58, R56, R55 up to Y=104.5 (from Y=107.5), and pack side-by-side with 0.15mm gap
    'R58': {'x': 134.000, 'y': 104.500, 'rot': 90.0, 'silk_x': 134.000, 'silk_y': 106.000},
    'R56': {'x': 132.860, 'y': 104.500, 'rot': 270.0, 'silk_x': 132.860, 'silk_y': 106.000},
    'R55': {'x': 131.720, 'y': 104.500, 'rot': 90.0, 'silk_x': 131.720, 'silk_y': 106.000},
    'R54': {'x': 129.500, 'y': 104.500, 'rot': 0.0, 'silk_x': 129.500, 'silk_y': 106.000},
    'C31': {'x': 138.800, 'y':  99.500, 'rot': 270.0, 'silk_x': 138.800, 'silk_y':  97.200},
    'C32': {'x': 138.800, 'y': 103.000, 'rot':  90.0, 'silk_x': 138.800, 'silk_y': 104.700},

    # 2. U1 block bottom row passives (B.Cu)
    # Pull up from Y=125.500 to Y=124.300
    # Pack side-by-side with 0.15mm gap (pitch = 1.91 + 0.15 = 2.06mm)
    'C1':  {'x':  73.500, 'y': 124.300, 'rot': 180.0, 'silk_x':  73.500, 'silk_y': 125.500},
    'R21': {'x':  75.560, 'y': 124.300, 'rot':   0.0, 'silk_x':  75.560, 'silk_y': 125.500},
    'R8':  {'x':  77.620, 'y': 124.300, 'rot':   0.0, 'silk_x':  77.620, 'silk_y': 125.500},
    'R64': {'x':  79.680, 'y': 124.300, 'rot':   0.0, 'silk_x':  79.680, 'silk_y': 125.500},
    'R65': {'x':  81.740, 'y': 124.300, 'rot': 180.0, 'silk_x':  81.740, 'silk_y': 125.500},
    'R9':  {'x':  83.800, 'y': 124.300, 'rot': 180.0, 'silk_x':  83.800, 'silk_y': 125.500},
    'R14': {'x':  80.800, 'y': 120.500, 'rot':   0.0, 'silk_x':  80.800, 'silk_y': 119.300},
    'R13': {'x':  81.800, 'y': 122.500, 'rot':   0.0, 'silk_x':  81.800, 'silk_y': 121.300},

    # 3. U10 passives R2, R3 (F.Cu)
    'R2':  {'x':  64.500, 'y':  86.500, 'rot': 270.0, 'silk_x':  64.500, 'silk_y':  85.000},
    'R3':  {'x':  65.640, 'y':  86.500, 'rot': 270.0, 'silk_x':  65.640, 'silk_y':  85.000},

    # 4. Encoder pull-ups R34, R35, R36 & Type-C pulldowns R62, R63 (F.Cu)
    'R34': {'x':  65.440, 'y':  96.000, 'rot':   0.0, 'silk_x':  65.440, 'silk_y':  94.800},
    'R35': {'x':  67.500, 'y':  96.000, 'rot':   0.0, 'silk_x':  67.500, 'silk_y':  94.800},
    'R36': {'x':  69.560, 'y':  96.000, 'rot':   0.0, 'silk_x':  69.560, 'silk_y':  94.800},
    'R63': {'x':  61.500, 'y':  97.890, 'rot':   0.0, 'silk_x':  61.500, 'silk_y':  99.000},

    # 5. U2 strap pull-up bus R15, R37, R10 (F.Cu)
    'R15': {'x':  88.500, 'y':  83.000, 'rot':  90.0, 'silk_x':  88.500, 'silk_y':  84.500},
    'R37': {'x':  89.640, 'y':  83.000, 'rot':  90.0, 'silk_x':  89.640, 'silk_y':  84.500},
    'R10': {'x':  90.780, 'y':  83.000, 'rot': 270.0, 'silk_x':  90.780, 'silk_y':  84.500},

    # 6. U11 passives (B.Cu)
    'C23': {'x': 100.500, 'y': 124.420, 'rot': 180.0, 'silk_x': 100.500, 'silk_y': 125.600},
    'R53': {'x': 102.560, 'y': 124.420, 'rot': 180.0, 'silk_x': 102.560, 'silk_y': 125.600},
    'R52': {'x':  94.500, 'y': 126.500, 'rot': 180.0, 'silk_x':  94.500, 'silk_y': 127.700},
    'C24': {'x':  91.500, 'y': 126.500, 'rot': 180.0, 'silk_x':  91.500, 'silk_y': 127.700},
    'R49': {'x':  89.000, 'y': 126.500, 'rot':   0.0, 'silk_x':  89.000, 'silk_y': 127.700},

    # 7. U13 passives C35, R61 (B.Cu)
    'C35': {'x': 132.160, 'y': 124.000, 'rot':   0.0, 'silk_x': 132.160, 'silk_y': 125.200},
    'R61': {'x': 125.820, 'y': 124.000, 'rot': 180.0, 'silk_x': 125.820, 'silk_y': 125.200},

    # 8. Ethernet power enable pull-up pair R17, C21 (B.Cu)
    # R17 at (111.5, 87.25), C21 at (111.5, 88.39) -> gap = 0.150mm!
    'C21': {'x': 111.500, 'y':  88.390, 'rot': 180.0, 'silk_x': 111.500, 'silk_y':  89.600},

    # 9. TP4 on B.Cu (pull up from 127.5 to 125.0)
    'TP4': {'x':  70.000, 'y': 125.000, 'rot':   0.0, 'silk_x':  70.000, 'silk_y': 126.200},
}

for ref, d in compaction_moves.items():
    fp = board.FindFootprintByReference(ref)
    if fp:
        fp.SetPosition(pcbnew.VECTOR2I_MM(d['x'], d['y']))
        fp.SetOrientationDegrees(d['rot'])
        if 'silk_x' in d:
            fp.Reference().SetPosition(pcbnew.VECTOR2I_MM(d['silk_x'], d['silk_y']))

board.Save(test_pcb)
print(f"Saved candidate board with {len(compaction_moves)} compacted components to {test_pcb}")

# Run DRC
print("Running KiCad DRC...")
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
drc_rpt = 'scratch/candidate_compaction_drc.rpt'
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "-o", drc_rpt, test_pcb]
subprocess.run(cmd, capture_output=True, text=True)

with open(drc_rpt, 'r', encoding='utf-8') as f:
    text = f.read()

violations = 0
unconnected = 0
parity = 0
for line in text.splitlines():
    if "Found" in line and "DRC violations" in line:
        violations = int(line.split()[2])
    elif "Found" in line and "unconnected pads" in line:
        unconnected = int(line.split()[2])
    elif "schematic_parity" in line or "schematic parity" in line:
        parity += 1

courtyard_overlaps = re.findall(r'\[courtyards_overlap\].*?(?=\n\s*\[|\Z)', text, re.DOTALL)
print(f"DRC Violations:   {violations} (baseline: 25)")
print(f"Unconnected Pads: {unconnected} (baseline: 360)")
print(f"Schematic Parity: {parity} (must be 0)")
print(f"Courtyard Overlaps: {len(courtyard_overlaps)} (must be 0)")
if courtyard_overlaps:
    for co in courtyard_overlaps:
        print("   " + co.strip().replace('\n', ' '))
