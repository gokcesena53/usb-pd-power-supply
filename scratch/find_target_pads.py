import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

parts = re.split(r'\n\s*\(footprint\s+', pcb)

target_nets = ['+3.3V', 'V_PRE', 'OUT_POS', 'SW_EN', '/USB_PD_CONTROLLER/SW_EN']

for target in target_nets:
    print(f"\n=== PADS FOR {target} ===")
    count = 0
    for p in parts[1:]:
        if f'(net "{target}")' in p:
            ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
            ref = ref_m.group(1) if ref_m else '?'
            layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
            fp_layer = layer_m.group(1) if layer_m else '?'
            at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
            fx, fy = (float(at_m.group(1)), float(at_m.group(2))) if at_m else (0,0)
            
            # find all pads in this footprint with target net
            pads = re.findall(rf'\(pad\s+"([^"]+)".*?\(net\s+"{re.escape(target)}"\)', p, re.DOTALL)
            print(f"  {ref} ({fp_layer}): pos=({fx:.2f}, {fy:.2f}) pads={pads}")
            count += 1
    print(f"Total footprints with {target}: {count}")
