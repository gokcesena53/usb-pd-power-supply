import pcbnew
import json
import math

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

# Let's inspect decoupling capacitors and IC power pins
ics = {}
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref.startswith('U') and not ref.startswith('USB'):
        ics[ref] = {
            'pos': (round(pcbnew.ToMM(fp.GetPosition().x), 3), round(pcbnew.ToMM(fp.GetPosition().y), 3)),
            'layer': fp.GetLayerName(),
            'pads': {}
        }
        for pad in fp.Pads():
            net = pad.GetNetname()
            pad_pos = (round(pcbnew.ToMM(pad.GetPosition().x), 3), round(pcbnew.ToMM(pad.GetPosition().y), 3))
            ics[ref]['pads'][pad.GetNumber()] = {'net': net, 'pos': pad_pos}

power_nets = set(['+3.3V', '+5V', 'V_PRE', 'VBUS', 'VBUS_IN', 'VDD', 'OUT_POS'])

caps = {}
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref.startswith('C'):
        pads_info = []
        nets = []
        for pad in fp.Pads():
            n = pad.GetNetname()
            nets.append(n)
            pads_info.append({
                'num': pad.GetNumber(),
                'net': n,
                'pos': (round(pcbnew.ToMM(pad.GetPosition().x), 3), round(pcbnew.ToMM(pad.GetPosition().y), 3))
            })
        pwr = [n for n in nets if any(p in n for p in power_nets)]
        gnd = [n for n in nets if 'GND' in n]
        val = fp.GetValue()
        pos = (round(pcbnew.ToMM(fp.GetPosition().x), 3), round(pcbnew.ToMM(fp.GetPosition().y), 3))
        rot = round(fp.GetOrientation().AsDegrees() % 360, 1)
        layer = fp.GetLayerName()
        caps[ref] = {
            'val': val,
            'layer': layer,
            'pos': pos,
            'rot': rot,
            'nets': nets,
            'pads': pads_info,
            'is_decoupling': bool(pwr and gnd),
            'pwr': pwr
        }

print('=== DECOUPLING CAPACITORS AUDIT ===')
decoupling_mapping = []
for c, data in sorted(caps.items(), key=lambda x: int(x[0][1:])):
    if data['is_decoupling']:
        # Find closest IC and IC pad with same power net
        best_u = None
        best_pad = None
        min_dist = 999999.0
        c_pwr_pad = [p for p in data['pads'] if any(pn in p['net'] for pn in power_nets)]
        c_pwr_pos = c_pwr_pad[0]['pos'] if c_pwr_pad else data['pos']

        for u, u_data in ics.items():
            if u_data['layer'] != data['layer']:
                continue
            for p_num, p_info in u_data['pads'].items():
                if p_info['net'] in data['pwr']:
                    dist = math.hypot(c_pwr_pos[0] - p_info['pos'][0], c_pwr_pos[1] - p_info['pos'][1])
                    if dist < min_dist:
                        min_dist = dist
                        best_u = u
                        best_pad = (p_num, p_info['net'], p_info['pos'])

        decoupling_mapping.append({
            'cap': c,
            'val': data['val'],
            'layer': data['layer'],
            'pos': data['pos'],
            'rot': data['rot'],
            'pwr_net': data['pwr'],
            'target_ic': best_u,
            'target_pad': best_pad[0] if best_pad else None,
            'target_dist_mm': round(min_dist, 2) if best_u else None
        })
        print(f"{c:4} ({data['val']:10}) {data['layer']:4} at ({data['pos'][0]:6.2f}, {data['pos'][1]:6.2f}) -> IC: {str(best_u):4} Pad: {str(best_pad[0] if best_pad else '-'):4} Dist: {str(round(min_dist, 2) if best_u else '-'):5} mm Net: {data['pwr']}")

# Also let's inspect passives by circuit block / neighborhood
print('\n=== PASSIVES BY BLOCK / CORRIDOR ===')
fps = []
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref.startswith(('R', 'C')) and not ref.startswith('RShunt'):
        pos = (round(pcbnew.ToMM(fp.GetPosition().x), 3), round(pcbnew.ToMM(fp.GetPosition().y), 3))
        rot = round(fp.GetOrientation().AsDegrees() % 360, 1)
        val = fp.GetValue()
        layer = fp.GetLayerName()
        fp_name = fp.GetFPID().GetLibItemName()
        fps.append({'ref': ref, 'val': val, 'footprint': fp_name, 'layer': layer, 'pos': pos, 'rot': rot})

with open('scratch/task104_all_passives.json', 'w') as f:
    json.dump({'ics': ics, 'decoupling': decoupling_mapping, 'passives': fps}, f, indent=2)

print(f"Dumped {len(fps)} passives to scratch/task104_all_passives.json")
