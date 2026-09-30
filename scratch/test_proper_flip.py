with open("hardware/gopo.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

import re

def proper_flip_to_fcu(block_text):
    lines = block_text.splitlines()
    new_lines = []
    for line in lines:
        l = line
        if '(layer "B.' in l:
            l = l.replace('(layer "B.', '(layer "F.')
        if '"B.Cu"' in l or '"B.Mask"' in l or '"B.Paste"' in l:
            l = l.replace('"B.Cu"', '"F.Cu"').replace('"B.Mask"', '"F.Mask"').replace('"B.Paste"', '"F.Paste"')
        if '(justify mirror)' in l:
            continue
        new_lines.append(l)
    return "\n".join(new_lines)

def move_and_flip(pcb_txt, ref, new_x, new_y, new_rot=0.0):
    lines = pcb_txt.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('(footprint '):
            j = i
            depth = 0
            while j < len(lines):
                depth += lines[j].count('(') - lines[j].count(')')
                if depth == 0: break
                j += 1
            block_lines = lines[i:j+1]
            block_text = "\n".join(block_lines)
            if f'(property "Reference" "{ref}"' in block_text:
                flipped = proper_flip_to_fcu(block_text)
                def repl_at(m):
                    return f'(at {new_x:.3f} {new_y:.3f} {new_rot})'
                flipped = re.sub(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', repl_at, flipped, count=1)
                lines[i:j+1] = flipped.splitlines()
                return "\n".join(lines)
            i = j + 1
        else:
            i += 1
    return pcb_txt

def move_only(pcb_txt, ref, new_x, new_y, new_rot=0.0):
    lines = pcb_txt.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('(footprint '):
            j = i
            depth = 0
            while j < len(lines):
                depth += lines[j].count('(') - lines[j].count(')')
                if depth == 0: break
                j += 1
            block_lines = lines[i:j+1]
            block_text = "\n".join(block_lines)
            if f'(property "Reference" "{ref}"' in block_text:
                def repl_at(m):
                    return f'(at {new_x:.3f} {new_y:.3f} {new_rot})'
                new_block = re.sub(r'\(at ([0-9\.\-]+) ([0-9\.\-]+)(?: ([0-9\.\-]+))?\)', repl_at, block_text, count=1)
                lines[i:j+1] = new_block.splitlines()
                return "\n".join(lines)
            i = j + 1
        else:
            i += 1
    return pcb_txt

cand = text
# R34, R35, R36 to F.Cu at X=65.0, 67.5, 70.0, Y=96.0
cand = move_and_flip(cand, 'R34', 65.0, 96.0, 0.0)
cand = move_and_flip(cand, 'R35', 67.5, 96.0, 0.0)
cand = move_and_flip(cand, 'R36', 70.0, 96.0, 0.0)

# R2, R3 on F.Cu at X=66.0, 68.0, Y=86.0
cand = move_only(cand, 'R2', 66.0, 86.0, 90.0)
cand = move_only(cand, 'R3', 68.0, 86.0, 90.0)

with open("hardware/gopo_test.kicad_pcb", "w", encoding="utf-8") as f:
    f.write(cand)

print("Saved hardware/gopo_test.kicad_pcb with complete B->F flip")
