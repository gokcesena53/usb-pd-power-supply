import pcbnew
import shutil
import subprocess
import json

src_pcb = 'hardware/gopo.kicad_pcb'
cand_pcb = 'scratch/candidate_task104.kicad_pcb'
shutil.copyfile(src_pcb, cand_pcb)

board = pcbnew.LoadBoard(cand_pcb)

# Define proposed modifications:
# ref: (new_x, new_y, new_rot)
modifications = {
    # 1. AP33772S Passive Rail (B.Cu) - Snap to clean 0.25mm grid & uniform 2.25mm pitch
    'R21': (76.000, 125.500, 0.0),
    'R8':  (78.250, 125.500, 0.0),
    'R64': (80.500, 125.500, 0.0),
    'R65': (82.750, 125.500, 0.0),
    'R9':  (85.000, 125.500, 0.0),
    
    # 2. U1 Passives (B.Cu)
    'C2':  (72.000, 122.750, 0.0),
    'C3':  (72.500, 107.000, 180.0),
    'C8':  (82.750, 117.000, 0.0),
    'R14': (81.250, 120.500, 0.0),
    
    # 3. Boost U11 Area (B.Cu)
    'C28': (110.000, 125.000, 180.0),
    'R50': (111.000, 108.000, 180.0),
    'R51': (108.000, 108.000, 180.0),
    
    # 4. Buck U5 Area (B.Cu)
    'C12': (120.750, 105.000, 90.0),
    'C14': (128.000, 110.000, 90.0),
    'C18': (121.750, 108.500, 180.0),
    'C19': (120.750, 112.500, 90.0),
    'C15': (113.250, 96.750, 180.0),
    'C16': (120.000, 97.250, 270.0),
    
    # 5. Buck / LM74801 Area on F.Cu
    'R54': (125.000, 107.250, 0.0),
    'C30': (125.000, 109.250, 0.0),
    
    # 6. VE Logic / Active Discharge (F.Cu & B.Cu)
    # F.Cu: Tighten R55, R56, R58 from pitch 2.20mm to pitch 2.00mm or clean 0.25mm
    'R55': (129.000, 107.500, 90.0),
    'R56': (131.000, 107.500, 90.0),
    'R58': (133.000, 107.500, 90.0),
    'C35': (132.500, 124.000, 0.0),
    'R61': (125.500, 124.000, 0.0),
    
    # 7. UI / Encoder Area (F.Cu)
    'R62': (61.500, 96.750, 0.0),
    'R63': (61.500, 98.500, 0.0),
    'R28': (81.000, 108.250, 0.0),
    'R29': (83.750, 109.250, 270.0),
    'C34': (104.750, 105.500, 90.0),
    
    # 8. Digital / MCU / RTC Area (B.Cu & F.Cu)
    'C20': (96.500, 93.500, 90.0),
    'C21': (111.500, 89.750, 0.0),
    'R17': (111.500, 87.250, 0.0),
    'C11': (141.250, 114.000, 0.0),
    
    # Standardize R4 rotation from 180 to 0 (align with R7)
    'R4':  (105.750, 70.500, 0.0),
}

applied = 0
for ref, (x, y, rot) in modifications.items():
    fp = board.FindFootprintByReference(ref)
    if fp:
        fp.SetPosition(pcbnew.VECTOR2I_MM(x, y))
        fp.SetOrientationDegrees(rot)
        applied += 1
    else:
        print(f"Warning: footprint {ref} not found!")

board.Save(cand_pcb)
print(f"Applied {applied} component adjustments to {cand_pcb}")

# Now run DRC on candidate board
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
rpt_file = "candidate_task104-drc.rpt"
cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "-o", rpt_file, cand_pcb]
res = subprocess.run(cmd, capture_output=True, text=True)
print("DRC Exit code:", res.returncode)
print(res.stdout)
if res.stderr:
    print("DRC Stderr:", res.stderr)
