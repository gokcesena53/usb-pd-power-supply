import re
import math
import json
import os

from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data, sha256_file

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def analyze_all():
    pcb_path = 'hardware/gopo.kicad_pcb'
    print(f"PCB SHA256: {sha256_file(pcb_path)}")
    tree = parse_kicad_pcb(pcb_path)
    fps, nets = extract_pcb_data(tree)

    # Invert nets to net -> list of (ref, pin_number, abs_pos, layer, fp_val, fp_footprint)
    net_to_pads = {}
    for ref, fp in fps.items():
        for p in fp['pads']:
            net = p['net_name']
            if not net:
                continue
            if net not in net_to_pads:
                net_to_pads[net] = []
            net_to_pads[net].append({
                'ref': ref,
                'pin': p['number'],
                'pos': p['abs_pos'],
                'layer': fp['layer'],
                'val': fp['val'],
                'footprint': fp['footprint']
            })

    r_and_c = {}
    for ref, fp in fps.items():
        if ref.startswith('R') or ref.startswith('C') or ref.startswith('RShunt'):
            r_and_c[ref] = fp

    print(f"Found {len(r_and_c)} R/C components.")

    # Let's inspect each R and C
    records = []
    for ref in sorted(r_and_c.keys(), key=lambda x: (x[0], int(re.sub(r'\D', '', x)) if re.sub(r'\D', '', x) else 0, x)):
        fp = r_and_c[ref]
        pads = fp['pads']
        p1 = pads[0] if len(pads) > 0 else None
        p2 = pads[1] if len(pads) > 1 else None

        p1_net = p1['net_name'] if p1 else ""
        p2_net = p2['net_name'] if p2 else ""

        # Find connected components on p1 and p2 nets
        p1_targets = [p for p in net_to_pads.get(p1_net, []) if p['ref'] != ref]
        p2_targets = [p for p in net_to_pads.get(p2_net, []) if p['ref'] != ref]

        records.append({
            'ref': ref,
            'val': fp['val'],
            'footprint': fp['footprint'],
            'layer': fp['layer'],
            'pos': fp['pos'],
            'p1': {
                'number': p1['number'] if p1 else None,
                'net': p1_net,
                'pos': p1['abs_pos'] if p1 else None,
                'targets': [(t['ref'], t['pin'], t['pos']) for t in p1_targets]
            },
            'p2': {
                'number': p2['number'] if p2 else None,
                'net': p2_net,
                'pos': p2['abs_pos'] if p2 else None,
                'targets': [(t['ref'], t['pin'], t['pos']) for t in p2_targets]
            }
        })

    with open('scratch/all_rc_extracted.json', 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2)

    print("Wrote scratch/all_rc_extracted.json")

if __name__ == '__main__':
    analyze_all()
