import re
import subprocess
import shutil

src_pcb = 'hardware/gopo.kicad_pcb'
test_pcb = 'scratch/cand_task103_all_hide.kicad_pcb'

with open(src_pcb, 'r', encoding='utf-8') as f:
    content = f.read()

shutil.copyfile('hardware/gopo.kicad_dru', 'scratch/cand_task103_all_hide.kicad_dru')
shutil.copyfile('hardware/gopo.kicad_pro', 'scratch/cand_task103_all_hide.kicad_pro')

# Load list of all 60 refs that had 0.1mm text from gopo-drc.rpt
with open('gopo-drc.rpt', 'r', encoding='utf-8') as f:
    drc_txt = f.read()

entries = re.split(r'\n(?=\[[a-zA-Z0-9_]+\])', drc_txt)
refs_01 = set()
for e in entries:
    if e.startswith('[text_thickness]'):
        m = re.search(r'Reference field of (\S+)', e)
        if m:
            refs_01.add(m.group(1))

print('Total 0.1mm refs to hide:', len(refs_01))

# Also add passives that caused overlap: R48, R49, R54, R62, R63, C5, C12, C16, C24, C26
passives_overlap = {'R48', 'R49', 'R54', 'R62', 'R63', 'C5', 'C12', 'C16', 'C24', 'C26'}
all_to_hide = refs_01.union(passives_overlap)

fp_pattern = re.compile(r'(\t\(footprint\s+.*?\n\t\)\n)', re.DOTALL)

def process_fp(match):
    fp_text = match.group(1)
    m_ref = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', fp_text)
    if not m_ref:
        return fp_text
    ref = m_ref.group(1)

    if ref in all_to_hide:
        m_prop = re.search(r'(\(property\s+"Reference"\s+"' + re.escape(ref) + r'"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            if '(hide yes)' not in prop_str:
                new_prop = prop_str.replace('(layer "B.SilkS")', '(layer "B.SilkS")\n\t\t\t(hide yes)').replace('(layer "F.SilkS")', '(layer "F.SilkS")\n\t\t\t(hide yes)')
                fp_text = fp_text.replace(prop_str, new_prop)

    # TP5 rogue text
    if ref == 'TP5':
        fp_text = fp_text.replace('(layer "B.SilkS")', '(layer "B.Fab")')

    # U2 lines
    if ref == 'U2':
        fp_text = fp_text.replace('(start -6.75 -11.15)\n\t\t\t(end 6.75 -11.15)', '(start -6.75 -5)\n\t\t\t(end 6.75 -5)')
        fp_text = fp_text.replace('(start -6.75 5.75)\n\t\t\t(end -6.75 -11.15)', '(start -6.75 5.75)\n\t\t\t(end -6.75 -5)')
        fp_text = fp_text.replace('(start 6.75 -11.15)\n\t\t\t(end 6.75 5.75)', '(start 6.75 -5)\n\t\t\t(end 6.75 5.75)')

    # C33
    if ref == 'C33':
        fp_text = fp_text.replace('(property "Reference" "C33"\n\t\t\t(at -10 11 0)', '(property "Reference" "C33"\n\t\t\t(at -10 6 0)')
        fp_text = fp_text.replace('(start 3.2 4)\n\t\t\t(end 3.2 2)', '(start 1.2 4)\n\t\t\t(end 1.2 2)')
        fp_text = fp_text.replace('(start 2.2 3)\n\t\t\t(end 4.2 3)', '(start 0.2 3)\n\t\t\t(end 2.2 3)')

    # J8 rect
    if ref == 'J8':
        fp_text = fp_text.replace('(start -51.27 20.01)', '(start -49 20.01)')

    # D8, D9, U13
    if ref == 'D8':
        m_prop = re.search(r'(\(property\s+"Reference"\s+"D8"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            new_prop = re.sub(r'\(at\s+[-0-9\.]+\s+[-0-9\.]+(\s+[-0-9\.]+)?\)', '(at 3 0 0)', prop_str)
            fp_text = fp_text.replace(prop_str, new_prop)

    if ref == 'D9':
        m_prop = re.search(r'(\(property\s+"Reference"\s+"D9"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            new_prop = re.sub(r'\(at\s+[-0-9\.]+\s+[-0-9\.]+(\s+[-0-9\.]+)?\)', '(at 3 0 0)', prop_str)
            fp_text = fp_text.replace(prop_str, new_prop)

    if ref == 'U13':
        m_prop = re.search(r'(\(property\s+"Reference"\s+"U13"[\s\S]*?\n\t\t\))', fp_text)
        if m_prop:
            prop_str = m_prop.group(1)
            new_prop = re.sub(r'\(at\s+[-0-9\.]+\s+[-0-9\.]+(\s+[-0-9\.]+)?\)', '(at 2.3 2.5 0)', prop_str)
            fp_text = fp_text.replace(prop_str, new_prop)

    return fp_text

new_content = fp_pattern.sub(process_fp, content)
with open(test_pcb, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Written test pcb.')
