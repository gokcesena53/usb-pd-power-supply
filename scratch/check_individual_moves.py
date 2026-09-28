import pcbnew
import subprocess
import shutil

shutil.copy('hardware/gopo.kicad_dru', 'scratch/cand_repack.kicad_dru')
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

def check_moves(candidate_moves):
    test_pcb = 'scratch/cand_repack.kicad_pcb'
    rpt = 'scratch/cand_repack_drc.rpt'
    board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
    for ref, (x, y, rot) in candidate_moves.items():
        fp = board.FindFootprintByReference(ref)
        if fp:
            fp.SetPosition(pcbnew.VECTOR2I_MM(x, y))
            fp.SetOrientationDegrees(rot)
    board.Save(test_pcb)
    
    subprocess.run([kicad_cli, "pcb", "drc", "--schematic-parity", "-o", rpt, test_pcb], capture_output=True, text=True)
    with open(rpt, 'r', encoding='utf-8') as f:
        text = f.read()
        
    violations = 0
    unconnected = 0
    parity = 0
    overlaps = []
    for line in text.splitlines():
        if "Found" in line and "DRC violations" in line:
            violations = int(line.split()[2])
        elif "Found" in line and "unconnected pads" in line:
            unconnected = int(line.split()[2])
        elif "schematic_parity" in line:
            parity += 1
        elif "[courtyards_overlap]" in line:
            overlaps.append(line)
            
    return violations, unconnected, parity, len(overlaps), text

# Let's test U6 moves alone
v, u, p, o, txt = check_moves({
    'R50': (109.385, 102.500, 180.0),
    'R51': (107.485, 102.500, 0.0),
})
print(f"U6 only: violations={v}, unconn={u}, parity={p}, overlaps={o}")
