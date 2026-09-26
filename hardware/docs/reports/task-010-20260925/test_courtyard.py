import subprocess

dru_content = """(version 1)

(rule "Mezzanine courtyard exception"
    (condition "A.intersectsCourtyard('J8') && A.Reference != 'J8'")
    (constraint courtyard_clearance (min -100mm))
)
"""

with open("hardware/test_dru.kicad_dru", "w", encoding="utf-8") as f:
    f.write(dru_content)

res = subprocess.run([
    r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe", "pcb", "drc",
    "--format", "json",
    "hardware/gopo.kicad_pcb"
], capture_output=True, text=True)

print("Returncode:", res.returncode)
print("STDOUT:", res.stdout[:200])
print("STDERR:", res.stderr)
