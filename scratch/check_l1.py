from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')
fps, nets = extract_pcb_data(tree)
l1 = fps['L1']
print('L1 val:', l1['val'], 'pos:', l1['pos'])
for p in l1['pads']:
    print(f"L1 pad {p['number']}: {p['net_name']} at {p['abs_pos']}")
