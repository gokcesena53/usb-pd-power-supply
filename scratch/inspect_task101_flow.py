import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.splitlines()
comps = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('(footprint '):
        j = i
        depth = 0
        block_lines = []
        while j < len(lines):
            l = lines[j]
            block_lines.append(l)
            depth += l.count('(') - l.count(')')
            if depth == 0:
                break
            j += 1
        block_text = "\n".join(block_lines)
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block_text)
        at_m = re.search(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', block_text)
        layer_m = re.search(r'\(layer "([^"]+)"\)', block_text)
        fp_name_m = re.search(r'\(footprint "([^"]+)"', block_text)
        if ref_m and at_m:
            ref = ref_m.group(1)
            fx = float(at_m.group(1))
            fy = float(at_m.group(2))
            frot = float(at_m.group(3)) if at_m.group(3) else 0.0
            flayer = layer_m.group(1) if layer_m else "F.Cu"
            comps.append((ref, fp_name_m.group(1) if fp_name_m else "", flayer, fx, fy, frot))
        i = j + 1
    else:
        i += 1

print(f"Total footprints: {len(comps)}")

# Check key components
keys = [
    'J7', 'U10', 'D3', 'U1', 'Q3', 
    'L3', 'U11', 'D4', 'C25', 'C27', 'C29',
    'L1', 'U5', 'D1', 'C12', 'C13', 'C14',
    'U12', 'Q5', 'RShunt1', 'U3', 'Q4', 'J4',
    'U2', 'J8', 'J3', 'J9', 'Y1', 'U4', 'U6', 'Q1', 'Q2', 'Q8'
]

comp_dict = {c[0]: c for c in comps}

print("\n--- Key Power Chain Flow (Left-to-Right) ---")
power_chain = [
    ('J7', 'Input USB-C'),
    ('U10', 'ESD Protection'),
    ('D3', 'Input TVS'),
    ('U1', 'AP33772S PD Controller'),
    ('Q3', 'Input Switch MOSFET'),
    ('L3', 'Boost Inductor'),
    ('U11', 'TPS55340 Boost IC'),
    ('D4', 'Boost Schottky Diode'),
    ('L1', 'Buck Inductor'),
    ('U5', 'AOZ1284 Buck IC'),
    ('U12', 'LM74801 Ideal Diode'),
    ('Q5', 'Ideal Diode & Output Switch MOSFET'),
    ('RShunt1', 'Current Sense Resistor'),
    ('U3', 'INA226 Power Monitor'),
    ('J4', 'Output Banana Jacks / Terminals')
]

for ref, desc in power_chain:
    if ref in comp_dict:
        c = comp_dict[ref]
        print(f"{ref:8} | {desc:32} | {c[2]:6} | X={c[3]:6.2f}, Y={c[4]:6.2f} | rot={c[5]:5.1f}")
    else:
        print(f"{ref:8} | {desc:32} | NOT FOUND")

print("\n--- Digital / RF / UI / Other Key ICs ---")
others = ['U2', 'J8', 'J3', 'J9', 'Y1', 'U4', 'U6', 'Q1', 'Q2', 'Q4', 'Q8']
for ref in others:
    if ref in comp_dict:
        c = comp_dict[ref]
        print(f"{ref:8} | {c[1][:25]:25} | {c[2]:6} | X={c[3]:6.2f}, Y={c[4]:6.2f} | rot={c[5]:5.1f}")
