with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('(property "Reference" "TP5"')
start = text.rfind('(footprint', 0, pos)
end = text.find('\n\t)', pos)
print(text[start:end+3])
