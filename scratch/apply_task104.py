import pcbnew
import subprocess
import shutil

pcb_path = 'hardware/gopo.kicad_pcb'

# Backup original pcb
shutil.copyfile(pcb_path, pcb_path + '.bak_task104')

board = pcbnew.LoadBoard(pcb_path)

modifications = {
    # 1. AP33772S Passive Rail (B.Cu Y=125.50 mm)
    # Snap to clean 0.25mm grid & uniform 2.25mm pitch (IPC Least Courtyard tight spacing)
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
    'R55': (129.000, 107.500, 90.0),
    'R56': (131.250, 107.500, 90.0),
    'R58': (133.500, 107.500, 90.0),
    'C35': (132.500, 124.000, 0.0),
    'R61': (125.500, 124.000, 0.0),
    
    # 7. UI / Encoder Area (F.Cu)
    'R62': (61.500, 96.750, 0.0),
    'R63': (61.500, 98.500, 0.0),
    'R28': (81.000, 108.250, 0.0),
    'R29': (83.750, 109.250, 270.0),
    'C34': (104.750, 105.500, 90.0),
    
    # 8. Digital / MCU / RTC Area (B.Cu & F.Cu)
    'C20': (96.500, 94.000, 90.0),
    'C21': (111.500, 89.750, 0.0),
    'R17': (111.500, 87.250, 0.0),
    'C11': (141.250, 114.000, 0.0),
    'R4':  (105.750, 70.500, 0.0),
}

applied = 0
for ref, (x, y, rot) in sorted(modifications.items()):
    fp = board.FindFootprintByReference(ref)
    if fp:
        old_x = round(pcbnew.ToMM(fp.GetPosition().x), 3)
        old_y = round(pcbnew.ToMM(fp.GetPosition().y), 3)
        old_rot = round(fp.GetOrientation().AsDegrees() % 360, 1)
        fp.SetPosition(pcbnew.VECTOR2I_MM(x, y))
        fp.SetOrientationDegrees(rot)
        applied += 1
        print(f"Applied {ref:5}: ({old_x:7.3f}, {old_y:7.3f}) rot={old_rot:5.1f} -> ({x:7.3f}, {y:7.3f}) rot={rot:5.1f}")
    else:
        print(f"Error: {ref} not found!")

board.Save(pcb_path)
print(f"\nSuccessfully saved {applied} modifications to {pcb_path}")
