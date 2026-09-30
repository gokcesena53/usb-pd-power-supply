from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')
fps, nets = extract_pcb_data(tree)
u3 = fps['U3']
print('U3 val:', u3['val'], 'pos:', u3['pos'])
for p in u3['pads']:
    print(f"  pad {p['number']}: {p['net_name']} at {p['abs_pos']}")

rshunt = fps['RShunt1']
print('RShunt1 pos:', rshunt['pos'])
for p in rshunt['pads']:
    print(f"  pad {p['number']}: {p['net_name']} at {p['abs_pos']}")
