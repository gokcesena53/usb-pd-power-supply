import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

# Let's inspect tracks and vias in X: 104-114, Y: 80-87
tracks = re.findall(r'\(segment\s+.*?\(start\s+([-\d.]+)\s+([-\d.]+)\)\s+\(end\s+([-\d.]+)\s+([-\d.]+)\).*?\(layer\s+"([^"]+)"\)', pcb)
print("=== TRACKS in X: 104-114, Y: 80-87 ===")
for sx, sy, ex, ey, layer in tracks:
    sx, sy, ex, ey = float(sx), float(sy), float(ex), float(ey)
    if (104 <= sx <= 114 and 80 <= sy <= 87) or (104 <= ex <= 114 and 80 <= ey <= 87):
        print(f"  Track ({sx}, {sy}) -> ({ex}, {ey}) on {layer}")

vias = re.findall(r'\(via\s+.*?\(at\s+([-\d.]+)\s+([-\d.]+)\)', pcb)
print("=== VIAS in X: 104-114, Y: 80-87 ===")
for vx, vy in vias:
    vx, vy = float(vx), float(vy)
    if 104 <= vx <= 114 and 80 <= vy <= 87:
        print(f"  Via at ({vx}, {vy})")
