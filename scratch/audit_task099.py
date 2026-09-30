import sys
import pcbnew
import json

pcb_path = r"hardware/gopo.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

def get_fp_data(fp):
    pos = fp.GetPosition()
    pos_mm = (pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))
    pads = []
    for pad in fp.Pads():
        pad_pos = pad.GetPosition()
        pads.append({
            'pad_num': pad.GetNumber(),
            'pad_name': pad.GetName(),
            'net_name': pad.GetNetname(),
            'pos_mm': (round(pcbnew.ToMM(pad_pos.x), 3), round(pcbnew.ToMM(pad_pos.y), 3))
        })
    return {
        'ref': fp.GetReference(),
        'val': fp.GetValue(),
        'layer': fp.GetLayerName(),
        'pos_mm': (round(pos_mm[0], 3), round(pos_mm[1], 3)),
        'orientation_deg': round(fp.GetOrientationDegrees(), 2),
        'pads': pads
    }

fps = list(board.GetFootprints())
data = {}
for fp in fps:
    ref = fp.GetReference()
    data[ref] = get_fp_data(fp)

# Let's inspect D*
diodes = {ref: data[ref] for ref in sorted(data.keys()) if ref.startswith('D')}
print("--- DIODES ---")
for ref, d in sorted(diodes.items()):
    print(f"{ref} ({d['val']}): Layer={d['layer']}, Pos={d['pos_mm']}, Orient={d['orientation_deg']}")
    for p in d['pads']:
        print(f"  Pad {p['pad_num']} ({p['net_name']}) at {p['pos_mm']}")

# Let's inspect Q*
qs = {ref: data[ref] for ref in sorted(data.keys()) if ref.startswith('Q')}
print("\n--- TRANSISTORS/FETS ---")
for ref, d in sorted(qs.items()):
    print(f"{ref} ({d['val']}): Layer={d['layer']}, Pos={d['pos_mm']}, Orient={d['orientation_deg']}")
    for p in d['pads']:
        print(f"  Pad {p['pad_num']} ({p['net_name']}) at {p['pos_mm']}")

# Let's inspect L*
inductors = {ref: data[ref] for ref in sorted(data.keys()) if ref.startswith('L')}
print("\n--- INDUCTORS ---")
for ref, d in sorted(inductors.items()):
    print(f"{ref} ({d['val']}): Layer={d['layer']}, Pos={d['pos_mm']}, Orient={d['orientation_deg']}")
    for p in d['pads']:
        print(f"  Pad {p['pad_num']} ({p['net_name']}) at {p['pos_mm']}")

# Let's inspect Y*
crystals = {ref: data[ref] for ref in sorted(data.keys()) if ref.startswith('Y')}
print("\n--- CRYSTALS ---")
for ref, d in sorted(crystals.items()):
    print(f"{ref} ({d['val']}): Layer={d['layer']}, Pos={d['pos_mm']}, Orient={d['orientation_deg']}")
    for p in d['pads']:
        print(f"  Pad {p['pad_num']} ({p['net_name']}) at {p['pos_mm']}")

# Let's inspect ICs U*
ics = {ref: data[ref] for ref in sorted(data.keys()) if ref.startswith('U')}
print("\n--- ICS ---")
for ref, d in sorted(ics.items()):
    print(f"{ref} ({d['val']}): Layer={d['layer']}, Pos={d['pos_mm']}, Orient={d['orientation_deg']}")
    for p in d['pads']:
        print(f"  Pad {p['pad_num']} ({p['net_name']}) at {p['pos_mm']}")

with open("scratch/task099_raw_data.json", "w", encoding="utf-8") as f:
    json.dump({'diodes': diodes, 'qs': qs, 'inductors': inductors, 'crystals': crystals, 'ics': ics}, f, indent=2)
print("\nSaved raw data to scratch/task099_raw_data.json")
