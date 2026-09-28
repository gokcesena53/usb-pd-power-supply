import glob
import re
import os

sch_files = glob.glob('hardware/**/*.kicad_sch', recursive=True)
print(f"Found {len(sch_files)} sch files:")

for sf in sorted(sch_files):
    with open(sf, 'r', encoding='utf-8') as f:
        txt = f.read()
    
    # Extract instances of C and U
    caps = re.findall(r'\(property "Reference" "(C\d+)"', txt)
    ics = re.findall(r'\(property "Reference" "(U\d+)"', txt)
    fname = os.path.basename(sf)
    print(f"File: {fname:25} -> ICs: {ics} | Caps: {caps}")
