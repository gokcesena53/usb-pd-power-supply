import pcbnew
import subprocess

test_pcb = 'scratch/cand_repack.kicad_pcb'
rpt = 'scratch/cand_repack_drc.rpt'
board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

mods = {
    # U6
    'R50': (109.385, 102.500, 180.0),
    'R51': (107.485, 102.500, 0.0),
    
    # U4
    'C9': (140.525, 78.800, 90.0),
    
    # U13
    'C35': (130.137, 125.350, 90.0),
    'R61': (127.862, 125.350, 90.0),
    
    # U3
    'C11': (139.300, 114.250, 180.0),
    'R27': (136.750, 108.450, 0.0),
}

for ref, (x, y, rot) in mods.items():
    fp = board.FindFootprintByReference(ref)
    if fp:
        fp.SetPosition(pcbnew.VECTOR2I_MM(x, y))
        fp.SetOrientationDegrees(rot)

board.Save(test_pcb)

kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "-o", rpt, test_pcb]
subprocess.run(cmd, capture_output=True, text=True)

with open(rpt, 'r', encoding='utf-8') as f:
    text = f.read()

import re
overlaps = re.findall(r'\[courtyards_overlap\].*?(?=\n\s*\[|\Z)', text, re.DOTALL)
print(f"Total courtyards overlaps: {len(overlaps)}")
for o in overlaps:
    print(o.strip())
    print('---')
