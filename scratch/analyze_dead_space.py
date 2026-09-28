#!/usr/bin/env python3
import pcbnew
import math
from collections import defaultdict

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
fps = list(board.GetFootprints())
print(f"Total footprints: {len(fps)}")

anchors = {'H1', 'H2', 'H3', 'H4', 'J3', 'J4', 'J7', 'J8', 'J9', 'MECH_ENC', 'U2'}

def to_mm(val):
    return pcbnew.ToMM(val)

# Group footprints by type
ics = {}
passives = {}
connectors = {}
others = {}

for fp in fps:
    ref = fp.GetReference()
    fpid = fp.GetFPID().GetLibItemName()
    layer = fp.GetLayerName()
    pos = fp.GetPosition()
    px, py = to_mm(pos.x), to_mm(pos.y)
    rot = fp.GetOrientation().AsDegrees() % 360
    
    # Get courtyard bounding box
    crtyd_box = None
    for shape in fp.GraphicalItems():
        if "Crtyd" in shape.GetLayerName():
            box = shape.GetBoundingBox()
            if crtyd_box is None:
                crtyd_box = box
            else:
                crtyd_box.Merge(box)
    if crtyd_box is None:
        # Fallback to pads bounding box or fp bounding box
        crtyd_box = fp.GetBoundingBox(False, False) # without text
        
    cb = {
        'x0': to_mm(crtyd_box.GetX()),
        'y0': to_mm(crtyd_box.GetY()),
        'x1': to_mm(crtyd_box.GetRight()),
        'y1': to_mm(crtyd_box.GetBottom()),
        'w': to_mm(crtyd_box.GetWidth()),
        'h': to_mm(crtyd_box.GetHeight())
    }
    
    entry = {
        'ref': ref,
        'fpid': fpid,
        'layer': layer,
        'x': round(px, 3),
        'y': round(py, 3),
        'rot': round(rot, 1),
        'crtyd': cb,
        'pads': []
    }
    for p in fp.Pads():
        pp = p.GetPosition()
        entry['pads'].append({
            'num': p.GetNumber(),
            'net': p.GetNetname(),
            'x': round(to_mm(pp.x), 3),
            'y': round(to_mm(pp.y), 3)
        })
        
    if ref.startswith('U') and ref != 'U2':
        ics[ref] = entry
    elif ref == 'U2':
        others[ref] = entry
    elif (ref.startswith('R') or ref.startswith('C')) and not ref.startswith('RShunt'):
        passives[ref] = entry
    elif ref.startswith('J'):
        connectors[ref] = entry
    else:
        others[ref] = entry

print(f"ICs: {len(ics)} ({list(ics.keys())})")
print(f"Passives: {len(passives)}")
print(f"Connectors: {len(connectors)}")
print(f"Others: {len(others)}")

# Overall bounding box of all components (using center positions and courtyard bounds)
min_x = min(fp['crtyd']['x0'] for fp in list(ics.values()) + list(passives.values()) + list(connectors.values()) + list(others.values()))
max_x = max(fp['crtyd']['x1'] for fp in list(ics.values()) + list(passives.values()) + list(connectors.values()) + list(others.values()))
min_y = min(fp['crtyd']['y0'] for fp in list(ics.values()) + list(passives.values()) + list(connectors.values()) + list(others.values()))
max_y = max(fp['crtyd']['y1'] for fp in list(ics.values()) + list(passives.values()) + list(connectors.values()) + list(others.values()))

print(f"Current component bounding box: X=[{min_x:.3f}, {max_x:.3f}] (W={max_x-min_x:.3f} mm), Y=[{min_y:.3f}, {max_y:.3f}] (H={max_y-min_y:.3f} mm)")

# Let's inspect passives on F.Cu vs B.Cu
fcu_passives = [ref for ref, p in passives.items() if p['layer'] == 'F.Cu']
bcu_passives = [ref for ref, p in passives.items() if p['layer'] == 'B.Cu']
print(f"Passives on F.Cu: {len(fcu_passives)}")
print(f"Passives on B.Cu: {len(bcu_passives)}")

# Check bus / pull-up groups of passives (passives near each other sharing nets or bus functions)
# For example: R34, R35, R36 (SPI/I2C/Encoder bus); R55, R56, R58; R22, R23; etc.
print("\n--- ICs and their passives & distances ---")
for u_ref, u_data in sorted(ics.items()):
    print(f"\nIC: {u_ref} ({u_data['fpid']}) at ({u_data['x']}, {u_data['y']}) on {u_data['layer']}:")
    u_nets = {p['net'] for p in u_data['pads'] if p['net'] and p['net'] != "" and "unconnected" not in p['net']}
    connected_passives = []
    for p_ref, p_data in passives.items():
        if p_data['layer'] != u_data['layer']:
            continue
        p_nets = {p['net'] for p in p_data['pads']}
        shared = u_nets.intersection(p_nets)
        # ignore GND and power only if that's the only connection
        sig_shared = [net for net in shared if net not in ['GND', '+3.3V', '3V3', '+5V', 'VBUS', 'V_PRE', 'PD_VOUT', 'OUT_POS']]
        if sig_shared or ('+3.3V' in shared and p_ref in ['C1', 'C2', 'C4', 'C6', 'C8', 'C9', 'C11', 'C14', 'C18', 'C23', 'C26', 'C32', 'C35']):
            dist = math.hypot(p_data['x'] - u_data['x'], p_data['y'] - u_data['y'])
            connected_passives.append((p_ref, dist, sig_shared, p_data['x'], p_data['y'], p_data['rot']))
    connected_passives.sort(key=lambda x: x[1])
    for cp in connected_passives:
        print(f"   {cp[0]:5}: dist_to_IC_center={cp[1]:.3f} mm, pos=({cp[3]:.3f}, {cp[4]:.3f}), rot={cp[5]:.1f}, nets={cp[2]}")
