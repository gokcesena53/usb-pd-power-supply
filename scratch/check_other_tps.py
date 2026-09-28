with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for tp in ['TP1', 'TP2', 'TP3', 'TP4', 'TP6', 'TP7', 'TP8', 'TP9']:
    pos = text.find(f'(property "Reference" "{tp}"')
    start = text.rfind('(footprint', 0, pos)
    end = text.find('\n\t)', pos)
    tp_str = text[start:end+3]
    has_fp_text = 'fp_text' in tp_str
    ref_hidden = '(hide yes)' in tp_str[:tp_str.find('(property "Value"')]
    print(f'{tp}: has_fp_text={has_fp_text}, ref_hidden={ref_hidden}')
