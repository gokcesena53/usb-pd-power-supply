from audit_rc_extractor import parse_kicad_pcb, extract_pcb_data

tree = parse_kicad_pcb('hardware/gopo.kicad_pcb')
fps, nets = extract_pcb_data(tree)
print("U5 val:", fps['U5']['val'])
print("U5 footprint:", fps['U5']['footprint'])
print("U11 val:", fps['U11']['val'])
print("U11 footprint:", fps['U11']['footprint'])
