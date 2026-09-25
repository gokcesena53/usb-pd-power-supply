import subprocess

dru = """(version 1)

(rule "Fine pitch package clearance"
	(condition "A.Reference =~ 'U1|U7'")
	(constraint clearance (min 0.15mm))
)
"""

with open("hardware/gopo.kicad_dru", "w", encoding="utf-8") as f:
    f.write(dru)

res = subprocess.run([
    r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe", "pcb", "drc",
    "hardware/gopo.kicad_pcb"
], capture_output=True, text=True)

print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
