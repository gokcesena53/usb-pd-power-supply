import pcbnew
import subprocess
import json

def test_cand(modifications, test_pcb='scratch/cand_repack.kicad_pcb', rpt='scratch/cand_repack_drc.rpt'):
    board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
    for ref, (x, y, rot) in modifications.items():
        fp = board.FindFootprintByReference(ref)
        if fp:
            fp.SetPosition(pcbnew.VECTOR2I_MM(x, y))
            fp.SetOrientationDegrees(rot)
        else:
            print(f"FP not found: {ref}")
            
    board.Save(test_pcb)
    
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "-o", rpt, test_pcb]
    subprocess.run(cmd, capture_output=True, text=True)
    
    drc_count = None
    unconn = None
    parity = 0
    overlaps = []
    
    with open(rpt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for l in lines:
            if "Found" in l and "DRC violations" in l:
                drc_count = int(l.split()[2])
            elif "Found" in l and "unconnected pads" in l:
                unconn = int(l.split()[2])
            elif "courtyards_overlap" in l:
                overlaps.append(l.strip())
            elif "schematic_parity" in l:
                parity += 1
                
    print(f"Results: DRC violations={drc_count}, unconn={unconn}, parity={parity}, overlaps={len(overlaps)}")
    if overlaps:
        print("Overlap details:")
        for o in overlaps[:5]:
            print("  ", o)
    return drc_count, len(overlaps), parity

# Test U6, U4, U13, U3 first!
mods = {
    # U6
    'R50': (109.385, 102.500, 180.0),
    'R51': (107.485, 102.500, 0.0),
    
    # U4
    'C9': (139.300, 80.100, 0.0),
    'R24': (139.300, 81.500, 0.0),
    
    # U13
    'C35': (131.250, 124.050, 0.0),
    'R61': (126.750, 124.050, 0.0),
    
    # U3
    'C11': (138.800, 114.250, 180.0),
    'R27': (136.750, 108.600, 90.0),
}

test_cand(mods)
