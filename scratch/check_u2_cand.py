with open('scratch/cand_task103.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('(property "Reference" "U2"')
start = text.rfind('(footprint', 0, pos)
end = text.find('\n\t)', pos)
u2_str = text[start:end+3]
for l in u2_str.splitlines():
    if 'Silk' in l or 'start' in l or 'end' in l:
        print(l)
