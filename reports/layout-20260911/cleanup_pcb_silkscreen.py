from __future__ import annotations

import shutil
import uuid
from datetime import datetime
from pathlib import Path


BOARD = Path(r"C:\Users\Slayer\Desktop\masaüstü güç kaynağı\masaüstü güç kaynağı.kicad_pcb")
BACKUP_DIR = BOARD.parent / "reports" / "layout-20260911" / "backups"

TINY_FOOTPRINT_MARKERS = (
    "R_0402_1005Metric",
    "C_0402_1005Metric",
    "LED_0402_1005Metric",
    "D_SOD-882",
)

# These larger parts have no collision-free place for a readable reference at
# the current compact placement. Their identifiers remain available on F.Fab
# and in the assembly/BOM outputs.
EXTRA_HIDE_REFERENCE_REFS = {
    "J1",
    "U9",
    "U8",
    "D2",
    "R43",
    "TP6",
    "TP7",
    "TP8",
    "TP9",
    "TP10",
    "U6",
    "RShunt",
    "C16",
    "U7",
    "C20",
}


def matching_paren(text: str, start: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index + 1
    raise ValueError(f"Unbalanced expression beginning at byte {start}")


def footprint_ranges(text: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    cursor = 0
    marker = '\n\t(footprint "'
    while True:
        found = text.find(marker, cursor)
        if found < 0:
            break
        start = found + 2
        end = matching_paren(text, start)
        ranges.append((start, end))
        cursor = end
    return ranges


def hide_reference(block: str) -> tuple[str, bool]:
    prop = block.find('(property "Reference" ')
    if prop < 0:
        return block, False
    end = matching_paren(block, prop)
    field = block[prop:end]
    if "(hide yes)" in field:
        return block, False
    layer = field.find('(layer "F.SilkS")')
    if layer < 0:
        return block, False
    line_end = field.find("\n", layer)
    indent_start = field.rfind("\n", 0, layer) + 1
    indent = field[indent_start:layer]
    field = field[: line_end + 1] + indent + "(hide yes)\n" + field[line_end + 1 :]
    return block[:prop] + field + block[end:], True


def main() -> None:
    text = BOARD.read_text(encoding="utf-8")
    edits: list[tuple[int, int, str]] = []
    hidden: list[str] = []

    for start, end in footprint_ranges(text):
        block = text[start:end]
        header_end = block.find("\n")
        header = block[:header_end]
        ref_start = block.find('(property "Reference" "') + len('(property "Reference" "')
        ref_end = block.find('"', ref_start)
        reference = block[ref_start:ref_end] if ref_start >= 0 and ref_end >= 0 else ""
        is_tiny = any(marker in header for marker in TINY_FOOTPRINT_MARKERS)
        if not is_tiny and reference not in EXTRA_HIDE_REFERENCE_REFS:
            continue
        changed, did_change = hide_reference(block)
        if not did_change:
            continue
        hidden.append(reference)
        edits.append((start, end, changed))

    # The encoder body rectangle crossed its three upper copper pads. Replace
    # the closed rectangle with left/right/bottom silk lines; the top edge is
    # intentionally omitted around the protruding pins.
    sw3_uuid = '560ab2b8-46de-4bb3-bd12-847c078e9015'
    sw3_uuid_pos = text.find(sw3_uuid)
    if sw3_uuid_pos >= 0:
        sw3_start = text.rfind("\t\t(fp_rect", 0, sw3_uuid_pos)
        sw3_end = matching_paren(text, sw3_start)
        line_template = (
            '\t\t(fp_line\n'
            '\t\t\t(start {starts})\n'
            '\t\t\t(end {ends})\n'
            '\t\t\t(stroke\n'
            '\t\t\t\t(width 0.3)\n'
            '\t\t\t\t(type default)\n'
            '\t\t\t)\n'
            '\t\t\t(layer "F.SilkS")\n'
            '\t\t\t(uuid "{uuid}")\n'
            '\t\t)'
        )
        lines = [
            line_template.format(starts="-7.2 -1.5", ends="-7.2 21.5", uuid=uuid.uuid4()),
            line_template.format(starts="7.2 -1.5", ends="7.2 21.5", uuid=uuid.uuid4()),
            line_template.format(starts="-7.2 21.5", ends="7.2 21.5", uuid=uuid.uuid4()),
        ]
        edits.append((sw3_start, sw3_end, "\n".join(lines)))

    if not edits:
        print("No new silkscreen cleanup was needed.")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = BACKUP_DIR / f"{BOARD.stem}_before_silkscreen_cleanup_{stamp}{BOARD.suffix}"
    shutil.copy2(BOARD, backup)

    for start, end, replacement in sorted(edits, key=lambda item: item[0], reverse=True):
        text = text[:start] + replacement + text[end:]
    BOARD.write_text(text, encoding="utf-8", newline="\n")

    print(f"Hidden {len(hidden)} collision-prone references from F.SilkS.")
    print("References remain in the PCB data and assembly/Fab output.")
    print(f"Backup: {backup}")


if __name__ == "__main__":
    main()
