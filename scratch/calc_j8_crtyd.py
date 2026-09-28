import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's inspect J8 courtyard polygon on B.Cu
# In the earlier print:
# (xy 2.1 20.14) (xy 2.1 -2.36) (xy -51.4 -2.36) (xy -51.4 0.64) (xy -55.7 0.64) (xy -55.7 17.14) (xy -51.4 17.14) (xy -51.4 20.14)
# J8 at is (102.5, 79.61).
# So in absolute coords:
# X ranges from 102.5 + (-55.7) = 46.8 mm to 102.5 + 2.1 = 104.6 mm!
# Y ranges from 79.61 - 2.36 = 77.25 mm to 79.61 + 20.14 = 99.75 mm!
print("J8 B.CrtYd bounding box:")
print(f"X: [{102.5 - 55.7:.2f}, {102.5 + 2.1:.2f}] mm -> [46.80, 104.60] mm")
print(f"Y: [{79.61 - 2.36:.2f}, {79.61 + 20.14:.2f}] mm -> [77.25, 99.75] mm")
