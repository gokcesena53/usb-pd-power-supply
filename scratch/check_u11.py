from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')
fps, nets = extract_pcb_data(tree)
u11 = fps['U11']
print('U11 val:', u11['val'], 'pos:', u11['pos'])
for p in u11['pads']:
    print(f"U11 pad {p['number']}: {p['net_name']} at {p['abs_pos']}")
