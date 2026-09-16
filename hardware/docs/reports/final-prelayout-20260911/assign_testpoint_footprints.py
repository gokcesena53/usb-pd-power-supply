from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
files = [ROOT / "usb_pd_controller.kicad_sch", ROOT / "mcu.kicad_sch"]
targets = {f"TP{i}" for i in range(1, 11)}

def symbol_span(text, ref_pos):
    start = text.rfind("\n\t(symbol", 0, ref_pos) + 1
    depth = 0
    quoted = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if quoted:
            if escaped: escaped = False
            elif ch == "\\": escaped = True
            elif ch == '"': quoted = False
        else:
            if ch == '"': quoted = True
            elif ch == "(": depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return start, i + 1
    raise ValueError("Unbalanced symbol")

for path in files:
    text = path.read_text(encoding="utf-8")
    changed = []
    for ref in sorted(targets):
        marker = f'(property "Reference" "{ref}"'
        pos = text.find(marker)
        if pos < 0: continue
        a, b = symbol_span(text, pos)
        block = text[a:b]
        old = '(property "Footprint" ""'
        if old in block:
            block = block.replace(old, '(property "Footprint" "TestPoint:TestPoint_Pad_D1.0mm"', 1)
            text = text[:a] + block + text[b:]
            changed.append(ref)
    path.write_text(text, encoding="utf-8")
    print(path.name, changed)
