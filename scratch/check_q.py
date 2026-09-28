from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')
fps, nets = extract_pcb_data(tree)
for q in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']:
    if q in fps:
        print(q, fps[q]['val'], fps[q]['pos'], fps[q]['layer'])
        for p in fps[q]['pads']:
            print(f"  pad {p['number']}: {p['net_name']} at {p['abs_pos']}")
