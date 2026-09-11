from pathlib import Path

path = Path(__file__).resolve().parents[2] / "mcu.kicad_sch"
text = path.read_text(encoding="utf-8")

def symbol_span(text, ref_pos):
    start = text.rfind("\n\t(symbol", 0, ref_pos) + 1
    depth = 0; quoted = False; escaped = False
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
                if depth == 0: return start, i + 1
    raise ValueError("unbalanced")

for ref, value in {"SW1":"BOOT / PTS810", "SW2":"RESET / PTS810"}.items():
    pos = text.find(f'(property "Reference" "{ref}"')
    a,b = symbol_span(text,pos)
    block = text[a:b]
    old_value = '"BOOT"' if ref == "SW1" else '"RESET"'
    block = block.replace(f'(property "Value" {old_value}', f'(property "Value" "{value}"', 1)
    block = block.replace('(property "Footprint" ""', '(property "Footprint" "Button_Switch_SMD:SW_SPST_PTS810"', 1)
    text = text[:a] + block + text[b:]

path.write_text(text, encoding="utf-8")
print("SW1/SW2 -> PTS810 SMD")
