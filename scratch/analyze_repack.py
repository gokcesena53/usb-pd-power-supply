import pcbnew
import math
import json
from collections import defaultdict

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
fps = list(board.GetFootprints())
ics = {fp.GetReference(): fp for fp in fps if fp.GetReference().startswith('U')}
passives = {fp.GetReference(): fp for fp in fps if (fp.GetReference().startswith('R') or fp.GetReference().startswith('C')) and not fp.GetReference().startswith('RShunt')}

print(f"Total ICs: {len(ics)}: {list(sorted(ics.keys()))}")
print(f"Total Passives (R, C): {len(passives)}")

# Net to IC pads map
ic_pads_by_net = defaultdict(list)
for u_ref, u_fp in ics.items():
    for pad in u_fp.Pads():
        net = pad.GetNetname()
        if net and net != "":
            ic_pads_by_net[net].append({
                'ic': u_ref,
                'pin': pad.GetNumber(),
                'x': pcbnew.ToMM(pad.GetPosition().x),
                'y': pcbnew.ToMM(pad.GetPosition().y),
                'layer': u_fp.GetLayerName(),
                'net': net
            })

# Let's inspect decoupling capacitors identified in previous audits / schematics
# From task 104/105:
decoupling_targets = [
    ('U1', '10', 'Net-(U1-V18)', 'C1', '1', 'Net-(U1-V18)'),
    ('U1', '9', 'PD_INT_5V', 'C4', '1', 'PD_5V'),
    ('U1', '1', 'Net-(U1-IFB)', 'C2', '1', 'Net-(U1-IFB)'),
    ('U1', '19', 'PD_VOUT', 'C8', '1', 'PD_VOUT'),
    ('U2', '3', '+3.3V', 'C6', '1', '+3.3V'),
    ('U3', '1', '+3.3V', 'C11', '1', '+3.3V'),
    ('U4', '8', '+3.3V', 'C9', '1', '+3.3V'),
    ('U5', '2', 'V_PRE', 'C14', '1', 'V_PRE'),
    ('U5', '8', '/USB_PD_CONTROLLER/SS_RAMP', 'C18', '1', '/USB_PD_CONTROLLER/SS_RAMP'),
    ('U11', '2', 'PD_VOUT', 'C26', '1', 'PD_VOUT'),
    ('U11', '3', 'PD_VOUT', 'C27', '1', 'V_PRE'),
    ('U11', '6', 'Net-(U11-SS)', 'C23', '1', 'Net-(U11-SS)'),
    ('U12', '10', 'V_PRE', 'C32', '1', 'V_PRE'),
    ('U13', '5', '+3.3V', 'C35', '1', '+3.3V'),
]
decoupling_cap_refs = {t[3]: t for t in decoupling_targets}

power_nets = {'GND', '+3.3V', '+5V', 'VBUS', 'V_PRE', 'PD_VOUT', 'OUT_POS'}

report = []

for p_ref, p_fp in sorted(passives.items()):
    p_cx = pcbnew.ToMM(p_fp.GetPosition().x)
    p_cy = pcbnew.ToMM(p_fp.GetPosition().y)
    p_rot = p_fp.GetOrientation().AsDegrees() % 360
    p_layer = p_fp.GetLayerName()
    
    pads = list(p_fp.Pads())
    p_nets = [p.GetNetname() for p in pads]
    
    # Check if this passive is a dedicated decoupling cap
    if p_ref in decoupling_cap_refs:
        u_ref, u_pin, _, _, c_pin, _ = decoupling_cap_refs[p_ref]
        # find IC pad
        u_fp = ics[u_ref]
        u_pad = [p for p in u_fp.Pads() if p.GetNumber() == u_pin][0]
        ux = pcbnew.ToMM(u_pad.GetPosition().x)
        uy = pcbnew.ToMM(u_pad.GetPosition().y)
        
        # cap pad
        cp = [p for p in pads if p.GetNumber() == c_pin][0]
        cpx = pcbnew.ToMM(cp.GetPosition().x)
        cpy = pcbnew.ToMM(cp.GetPosition().y)
        
        pad_dist = math.hypot(cpx - ux, cpy - uy)
        center_dist = math.hypot(p_cx - ux, p_cy - uy)
        
        report.append({
            'ref': p_ref,
            'type': 'decoupling',
            'ic': u_ref,
            'ic_pin': u_pin,
            'center_dist': round(center_dist, 3),
            'pad_dist': round(pad_dist, 3),
            'pos': (round(p_cx, 3), round(p_cy, 3)),
            'rot': p_rot,
            'layer': p_layer,
            'pad_to_pin_limit': 1.2,
            'center_limit': 2.0,
            'violation': (pad_dist > 1.2 or center_dist > 2.0)
        })
        continue

    # Otherwise check non-power signal net connections to ICs
    ic_connections = []
    for pad in pads:
        net = pad.GetNetname()
        if net and net not in power_nets and net in ic_pads_by_net:
            for ic_pad_info in ic_pads_by_net[net]:
                ux, uy = ic_pad_info['x'], ic_pad_info['y']
                px = pcbnew.ToMM(pad.GetPosition().x)
                py = pcbnew.ToMM(pad.GetPosition().y)
                center_dist = math.hypot(p_cx - ux, p_cy - uy)
                pad_dist = math.hypot(px - ux, py - uy)
                ic_connections.append({
                    'ic': ic_pad_info['ic'],
                    'ic_pin': ic_pad_info['pin'],
                    'net': net,
                    'center_dist': round(center_dist, 3),
                    'pad_dist': round(pad_dist, 3),
                    'ic_pos': (round(ux, 3), round(uy, 3)),
                    'p_pad_pos': (round(px, 3), round(py, 3))
                })
                
    if ic_connections:
        # Sort by center_dist
        ic_connections.sort(key=lambda x: x['center_dist'])
        closest = ic_connections[0]
        report.append({
            'ref': p_ref,
            'type': 'signal_passive',
            'ic': closest['ic'],
            'ic_pin': closest['ic_pin'],
            'net': closest['net'],
            'center_dist': closest['center_dist'],
            'pad_dist': closest['pad_dist'],
            'pos': (round(p_cx, 3), round(p_cy, 3)),
            'rot': p_rot,
            'layer': p_layer,
            'center_limit': 2.0,
            'violation': closest['center_dist'] > 2.0
        })

print(f"Total passives evaluated against IC pins: {len(report)}")
violations = [r for r in report if r['violation']]
print(f"Total passives violating constraints: {len(violations)}")
print("\n--- VIOLATIONS LIST ---")
for v in violations:
    ptype = v['type']
    ref = v['ref']
    ic = v['ic']
    pin = v['ic_pin']
    cdist = v['center_dist']
    pdist = v['pad_dist']
    print(f"[{ptype:14}] {ic}-{ref} (pin {pin}): center_dist={cdist}mm (limit 2.0), pad_dist={pdist}mm (limit 1.2 if decoup)")

with open('scratch/repack_initial_violations.json', 'w') as f:
    json.dump({'all': report, 'violations': violations}, f, indent=2)
