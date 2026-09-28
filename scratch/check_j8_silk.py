with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos = text.find('(property "Reference" "J8"')
end = text.find('\n\t)', pos)
for m in re.finditer(r'\(pad "MP"[\s\S]*?\)', text[pos:end]):
    print(m.group(0))
