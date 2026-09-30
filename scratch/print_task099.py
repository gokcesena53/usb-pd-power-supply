import json

with open('scratch/task099_raw_data.json', encoding='utf-8') as f:
    d = json.load(f)

print('=== DIODES (D1-D10) ===')
for k, v in sorted(d['diodes'].items()):
    pads_str = ', '.join([f"P{p['pad_num']}({p['net_name']})" for p in v['pads']])
    print(f"{k}: {v['val']} | Layer: {v['layer']} | Pos: {v['pos_mm']} | Orient: {v['orientation_deg']} | Pads: {pads_str}")

print('\n=== TRANSISTORS/FETS (Q1-Q8) ===')
for k, v in sorted(d['qs'].items()):
    pads_str = ', '.join([f"P{p['pad_num']}({p['net_name']})" for p in v['pads']])
    print(f"{k}: {v['val']} | Layer: {v['layer']} | Pos: {v['pos_mm']} | Orient: {v['orientation_deg']} | Pads: {pads_str}")

print('\n=== INDUCTORS ===')
for k, v in sorted(d['inductors'].items()):
    pads_str = ', '.join([f"P{p['pad_num']}({p['net_name']})" for p in v['pads']])
    print(f"{k}: {v['val']} | Layer: {v['layer']} | Pos: {v['pos_mm']} | Orient: {v['orientation_deg']} | Pads: {pads_str}")

print('\n=== CRYSTALS ===')
for k, v in sorted(d['crystals'].items()):
    pads_str = ', '.join([f"P{p['pad_num']}({p['net_name']})" for p in v['pads']])
    print(f"{k}: {v['val']} | Layer: {v['layer']} | Pos: {v['pos_mm']} | Orient: {v['orientation_deg']} | Pads: {pads_str}")
