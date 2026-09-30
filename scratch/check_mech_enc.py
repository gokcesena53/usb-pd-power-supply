import re
import math
from collections import defaultdict

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect where R34, R35, R36 could be placed on B.Cu
# Currently R34=(62.5, 125.5), R35=(65.0, 125.5), R36=(67.5, 125.5)
# J9 is at (61.5, 104.0) on F.Cu.
# If R34, R35, R36 are placed on B.Cu near J9 (e.g. at X=63.0, 65.5, 68.0, Y=102.0 or Y=95.0)
# Let's check MECH_ENC bounding box!
# MECH_ENC is the panel encoder 3D model:
mech_enc_m = re.search(r'\(footprint "MECH_ENC".*?\n  \)', text, re.DOTALL)
if not mech_enc_m:
    mech_enc_m = re.search(r'\(footprint "([^"]+)".*?\(property "Reference" "MECH_ENC".*?\n  \)', text, re.DOTALL)
if mech_enc_m:
    print("Found MECH_ENC:")
    at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)', mech_enc_m.group(0))
    print(f"  At: {at_m.group(1)}, {at_m.group(2)}")

# Let's check encoder clearance rules from TASK-094 and TASK-096:
# In TASK-096:
# "Enkoder Kablo Hacmi Açıklığı: R36 ile X in [57.8, 70.0], Y in [102, 123] arası: 1.4 mm"
# Notice that! MECH_ENC cable volume is on F.Cu/B.Cu: X in [57.8, 70.0], Y in [102, 123]!
# Wait! Let's check what TASK-096 said about MECH_ENC and encoder volume!
