import subprocess
import json

test_dru = """(version 1)

(rule "Fine pitch package clearance"
	(condition "A.Reference == 'U1' || A.Reference == 'U7'")
	(constraint clearance (min 0.15mm))
)

(rule "USB-C J7 edge clearance"
	(condition "A.Reference == 'J7'")
	(constraint edge_clearance (min 0.25mm))
)

(rule "USB-C J7 NPTH to pad hole clearance"
	(condition "A.Reference == 'J7' && B.Reference == 'J7'")
	(constraint hole_clearance (min 0.18mm))
)

(rule "U11 Thermal Via hole size"
	(condition "A.Reference == 'U11'")
	(constraint hole (min 0.2mm))
)
"""

with open("hardware/gopo.kicad_dru", "w", encoding="utf-8") as f:
    f.write(test_dru)

print("Wrote test dru. Running DRC...")
res = subprocess.run([
    r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe", "pcb", "drc",
    "--format", "json",
    "-o", "hardware/docs/reports/task-010-20260925/drc_test.json",
    "hardware/gopo.kicad_pcb"
], capture_output=True, text=True)

print("Returncode:", res.returncode)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)

with open("hardware/docs/reports/task-010-20260925/drc_test.json", encoding="utf-8") as f:
    d = json.load(f)

from collections import Counter
counts = Counter(v['type'] for v in d.get('violations', []))
print("Violation counts:")
for k, v in counts.items():
    print(f"  {k}: {v}")
