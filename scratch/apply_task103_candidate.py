import re
import subprocess
import shutil

src_pcb = 'hardware/gopo.kicad_pcb'
test_pcb = 'scratch/cand_task103.kicad_pcb'

with open(src_pcb, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure cand_task103 pro and dru exist
shutil.copyfile('hardware/gopo.kicad_dru', 'scratch/cand_task103.kicad_dru')
shutil.copyfile('hardware/gopo.kicad_pro', 'scratch/cand_task103.kicad_pro')

# Parse footprints using regex
# Footprint structure: (footprint "..." ... \n\t)
fp_pattern = re.compile(r'(\t\(footprint\s+.*?\n\t\)\n)', re.DOTALL)

def process_footprint(fp_match):
    fp_text = fp_match.group(1)
    
    # Extract reference
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
    if not m_ref:
        return fp_text
    ref = m_ref.group(1)
    
    # 1. TP1-TP14: hide reference
    if re.match(r'^TP\d+$', ref):
        # Add (hide yes) if not already hidden
        # Find property Reference block
        m_prop = re.search(r'(\(property\s+"Reference"\s+"' + ref + r'"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            if '(hide yes)' not in prop_str:
                new_prop = prop_str.replace('(layer "B.SilkS")', '(layer "B.SilkS")\n\t\t\t(hide yes)').replace('(layer "F.SilkS")', '(layer "F.SilkS")\n\t\t\t(hide yes)')
                fp_text = fp_text.replace(prop_str, new_prop)
        
        # In TP5, fix the rogue fp_text on B.SilkS
        if ref == 'TP5':
            fp_text = fp_text.replace('(layer "B.SilkS")', '(layer "B.Fab")')

    # 2. Resistors and Capacitors 0402 / 0603 / small passives + TH1: hide reference
    is_passive_0402_0603 = False
    if (ref.startswith('R') or ref.startswith('C') or ref == 'TH1') and ref not in ['R11', 'R43', 'R67', 'RShunt1', 'C33']:
        # check fpid
        if any(pkg in fp_text for pkg in ['0402', '0603', 'R_0402', 'C_0402', 'R_0603', 'C_0603', '0805', 'C_0805', 'R_0805', '1206', 'C_1206', '1210', 'C_1210']):
            is_passive_0402_0603 = True

    if is_passive_0402_0603:
        m_prop = re.search(r'(\(property\s+"Reference"\s+"' + ref + r'"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            if '(hide yes)' not in prop_str:
                new_prop = prop_str.replace('(layer "B.SilkS")', '(layer "B.SilkS")\n\t\t\t(hide yes)').replace('(layer "F.SilkS")', '(layer "F.SilkS")\n\t\t\t(hide yes)')
                fp_text = fp_text.replace(prop_str, new_prop)

    # 3. Remaining footprints with small text size: SW1, SW2, J7, Q1, Q2, U1, U3, U5, U6, D1, D2
    if ref in ['SW1', 'SW2', 'J7', 'Q1', 'Q2', 'U1', 'U3', 'U5', 'U6', 'D1', 'D2']:
        # Fix size: 0.1 0.1 -> 0.8 0.8, thickness 0.12
        m_prop = re.search(r'(\(property\s+"Reference"\s+"' + ref + r'"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            new_prop = re.sub(r'\(size\s+0\.1\s+0\.1\)', '(size 0.8 0.8)', prop_str)
            new_prop = re.sub(r'\(thickness\s+0\.15\)', '(thickness 0.12)', new_prop)
            fp_text = fp_text.replace(prop_str, new_prop)

    # 4. Fix U2 silkscreen lines clipping board edge
    if ref == 'U2':
        # replace the lines extending to 63.915
        fp_text = fp_text.replace('(start 71.17 63.915)\n\t\t\t(end 84.67 63.915)', '(start 71.17 70)\n\t\t\t(end 84.67 70)')
        fp_text = fp_text.replace('(start 71.17 80.815)\n\t\t\t(end 71.17 63.915)', '(start 71.17 80.815)\n\t\t\t(end 71.17 70)')
        fp_text = fp_text.replace('(start 84.67 63.915)\n\t\t\t(end 84.67 80.815)', '(start 84.67 70)\n\t\t\t(end 84.67 80.815)')

    # 5. Fix C33 reference pos and polarity line
    if ref == 'C33':
        # reference pos was (at -10 11 0)
        fp_text = fp_text.replace('(property "Reference" "C33"\n\t\t\t(at -10 11 0)', '(property "Reference" "C33"\n\t\t\t(at -10 6 0)')
        # '+' sign lines
        fp_text = fp_text.replace('(start 3.2 4)\n\t\t\t(end 3.2 2)', '(start 1.2 4)\n\t\t\t(end 1.2 2)')
        fp_text = fp_text.replace('(start 2.2 3)\n\t\t\t(end 4.2 3)', '(start 0.2 3)\n\t\t\t(end 2.2 3)')

    # 6. Fix J8 rectangle on B.SilkS
    if ref == 'J8':
        fp_text = fp_text.replace('(start -51.27 20.01)', '(start -49 20.01)')

    # 7. Fix D8, D9, U13 reference positions
    if ref == 'D8':
        # Move ref to (at 3 0 0)
        m_prop = re.search(r'(\(property\s+"Reference"\s+"D8"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            new_prop = re.sub(r'\(at\s+[-0-9\.]+\s+[-0-9\.]+(\s+[-0-9\.]+)?\)', '(at 3 0 0)', prop_str)
            fp_text = fp_text.replace(prop_str, new_prop)

    if ref == 'D9':
        # Move ref to (at 3 0 0)
        m_prop = re.search(r'(\(property\s+"Reference"\s+"D9"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            new_prop = re.sub(r'\(at\s+[-0-9\.]+\s+[-0-9\.]+(\s+[-0-9\.]+)?\)', '(at 3 0 0)', prop_str)
            fp_text = fp_text.replace(prop_str, new_prop)

    if ref == 'U13':
        # Move ref to (at 2.3 2 0)
        m_prop = re.search(r'(\(property\s+"Reference"\s+"U13"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            new_prop = re.sub(r'\(at\s+[-0-9\.]+\s+[-0-9\.]+(\s+[-0-9\.]+)?\)', '(at 2.3 2 0)', prop_str)
            fp_text = fp_text.replace(prop_str, new_prop)

    return fp_text

new_content = fp_pattern.sub(process_footprint, content)

with open(test_pcb, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Modified test PCB written.')
