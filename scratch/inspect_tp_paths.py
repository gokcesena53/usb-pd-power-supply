import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"(TP\d+)"', p)
    if ref_m:
        ref = ref_m.group(1)
        path = re.search(r'\(path\s+"([^"]+)"\)', p)
        sheetname = re.search(r'\(sheetname\s+"([^"]+)"\)', p)
        sheetfile = re.search(r'\(sheetfile\s+"([^"]+)"\)', p)
        uuid = re.search(r'\(uuid\s+"([^"]+)"\)', p)
        print(f"{ref}: path={path.group(1) if path else 'None'} | sheet={sheetfile.group(1) if sheetfile else 'None'} | fp_uuid={uuid.group(1) if uuid else 'None'}")
