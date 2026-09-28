from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')
fps, nets = extract_pcb_data(tree)
for d in ['D1', 'D2', 'D3', 'D4']:
    if d in fps:
        print(d, fps[d]['val'], fps[d]['pos'])
        for p in fps[d]['pads']:
            print(f"  pad {p['number']}: {p['net_name']} at {p['abs_pos']}")
