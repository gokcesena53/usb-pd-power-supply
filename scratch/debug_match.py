import re

pcb_path = "hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    text = f.read()

pattern = r'(\(footprint "[^"]+".*?\(property "Reference" "R34".*?\n  \))'
m = re.search(pattern, text, re.DOTALL)
print("Matched R34:", m is not None)
if not m:
    # try another regex
    m2 = re.search(r'\(property "Reference" "R34"', text)
    print("Found 'Reference R34':", m2 is not None)
    if m2:
        start = text.rfind('(footprint ', 0, m2.start())
        print("Start index:", start)
        print("Slice:", text[start:start+200])
