from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')
fps, nets = extract_pcb_data(tree)
u5 = fps['U5']
print('U5 pos:', u5['pos'])
for p in u5['pads']:
    print(f"Pad {p['number']}: {p['net_name']} at {p['abs_pos']}")
