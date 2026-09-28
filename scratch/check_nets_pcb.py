import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect where +3.3V, V_PRE, OUT_POS, SW_EN are on the PCB
with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

target_nets = ['+3.3V', 'V_PRE', 'OUT_POS', 'SW_EN']

# Find pads belonging to these nets
parts = re.split(r'\n\s*\(footprint\s+', pcb)
print("=== PADS ON PCB FOR TARGET NETS ===")
for p in parts[1:]:
    ref_m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', p)
    ref = ref_m.group(1) if ref_m else '?'
    layer_m = re.search(r'\(layer\s+"([^"]+)"\)', p)
    fp_layer = layer_m.group(1) if layer_m else '?'
    at_m = re.search(r'\(at\s+([-\d.]+)\s+([-\d.]+)', p)
    fx, fy = (float(at_m.group(1)), float(at_m.group(2))) if at_m else (0,0)
    
    pads = re.findall(r'\(pad\s+"([^"]+)".*?\(net\s+\d+\s+"([^"]+)".*?\(at\s+([-\d.]+)\s+([-\d.]+)', p, re.DOTALL)
    for pad_num, net, px, py in pads:
        if net in target_nets:
            print(f"  {ref}.{pad_num} [{net}]: FP pos=({fx}, {fy}) on {fp_layer}")

