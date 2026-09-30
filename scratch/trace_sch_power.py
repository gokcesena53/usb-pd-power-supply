with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for C12, C13, C14, C15, C16, C25, C26, C27, C28, C29
import re
for c in ['C12', 'C13', 'C14', 'C15', 'C16', 'C25', 'C26', 'C27', 'C28', 'C29', 'R11', 'RShunt1']:
    m = re.search(r'\(property "Reference" "' + c + r'"[^)]*\)', text)
    if m:
        # find the enclosing symbol block
        start = text.rfind('(symbol', 0, m.start())
        end = text.find('\n\t)', m.end())
        block = text[start:end]
        val = re.search(r'\(property "Value" "([^"]+)"', block)
        print(f"=== {c} ===")
        print(f"Value: {val.group(1) if val else '?'}")
