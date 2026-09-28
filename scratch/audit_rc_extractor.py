import re
import math
import json
import hashlib

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def parse_kicad_pcb(pcb_path):
    with open(pcb_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to extract all footprints, their pads, nets, positions, rotations, layers
    # A simple recursive or token-based parser for s-expressions:
    tokens = re.findall(r'\(|\)|"[^"]*"|[^\s()]+', content)
    
    # Parse into nested list
    def parse_tokens(tokens):
        stack = [[]]
        for token in tokens:
            if token == '(':
                new_list = []
                stack[-1].append(new_list)
                stack.append(new_list)
            elif token == ')':
                stack.pop()
            else:
                # strip quotes if any
                if token.startswith('"') and token.endswith('"'):
                    token = token[1:-1]
                stack[-1].append(token)
        return stack[0][0]

    tree = parse_tokens(tokens)
    return tree

def extract_pcb_data(tree):
    footprints = {}
    nets = {} # net_num -> net_name

    for node in tree:
        if not isinstance(node, list):
            continue
        tag = node[0]
        if tag == 'net':
            # (net 1 "GND")
            net_num = int(node[1])
            net_name = node[2]
            nets[net_num] = net_name
        elif tag == 'footprint':
            fp_name = node[1]
            ref = None
            val = None
            layer = 'F.Cu'
            pos = (0.0, 0.0, 0.0) # x, y, rot
            pads = []

            for elem in node[2:]:
                if not isinstance(elem, list) or len(elem) == 0:
                    continue
                etag = elem[0]
                if etag == 'layer':
                    layer = elem[1]
                elif etag == 'at':
                    x = float(elem[1])
                    y = float(elem[2])
                    rot = float(elem[3]) if len(elem) > 3 else 0.0
                    pos = (x, y, rot)
                elif etag == 'property':
                    if elem[1] == 'Reference':
                        ref = elem[2]
                    elif elem[1] == 'Value':
                        val = elem[2]
                elif etag == 'fp_text':
                    if elem[1] == 'reference' and not ref:
                        ref = elem[2]
                    elif elem[1] == 'value' and not val:
                        val = elem[2]
                elif etag == 'pad':
                    pad_num = elem[1]
                    pad_type = elem[2]
                    pad_shape = elem[3]
                    pad_x, pad_y, pad_rot = 0.0, 0.0, 0.0
                    pad_net_num = 0
                    pad_net_name = ""
                    pad_layers = []

                    for pelem in elem[4:]:
                        if not isinstance(pelem, list) or len(pelem) == 0:
                            continue
                        ptag = pelem[0]
                        if ptag == 'at':
                            pad_x = float(pelem[1])
                            pad_y = float(pelem[2])
                            pad_rot = float(pelem[3]) if len(pelem) > 3 else 0.0
                        elif ptag == 'net':
                            if len(pelem) == 2:
                                pad_net_name = pelem[1]
                            elif len(pelem) >= 3:
                                pad_net_num = int(pelem[1]) if pelem[1].isdigit() else 0
                                pad_net_name = pelem[2]
                        elif ptag == 'layers':
                            pad_layers = pelem[1:]

                    # Calculate absolute pad position taking footprint pos & rot into account
                    fp_x, fp_y, fp_rot = pos
                    rad = math.radians(fp_rot)
                    # Note: in KiCad, rot is CCW or CW? KiCad Y is downwards.
                    # Footprint rotation rot is CCW in Cartesian, but since Y is downwards:
                    # standard KiCad rotation formula:
                    # cos = cos(rad), sin = sin(rad)
                    # abs_x = fp_x + pad_x * cos - pad_y * sin
                    # abs_y = fp_y + pad_x * sin + pad_y * cos
                    # Wait, if layer is B.Cu, footprints are mirrored! Let's check mirroring.
                    # On B.Cu, X pad coordinate is negated before rotation: pad_x = -pad_x
                    is_back = (layer == 'B.Cu')
                    px = -pad_x if is_back else pad_x
                    py = pad_y
                    cos_r = math.cos(rad)
                    sin_r = math.sin(rad)
                    abs_x = fp_x + px * cos_r - py * sin_r
                    abs_y = fp_y + px * sin_r + py * cos_r

                    pads.append({
                        'number': pad_num,
                        'type': pad_type,
                        'shape': pad_shape,
                        'rel_pos': (pad_x, pad_y, pad_rot),
                        'abs_pos': (round(abs_x, 4), round(abs_y, 4)),
                        'net_num': pad_net_num,
                        'net_name': pad_net_name,
                        'layers': pad_layers
                    })

            if ref:
                footprints[ref] = {
                    'ref': ref,
                    'val': val,
                    'footprint': fp_name,
                    'layer': layer,
                    'pos': pos,
                    'pads': pads
                }

    return footprints, nets

if __name__ == '__main__':
    pcb_path = 'hardware/gopo.kicad_pcb'
    print(f"Hashing PCB: {sha256_file(pcb_path)}")
    tree = parse_kicad_pcb(pcb_path)
    fps, nets = extract_pcb_data(tree)
    print(f"Total footprints: {len(fps)}")
    r_fps = {k: v for k, v in fps.items() if k.startswith('R') or k.startswith('RShunt')}
    c_fps = {k: v for k, v in fps.items() if k.startswith('C')}
    print(f"R footprints: {len(r_fps)}")
    print(f"C footprints: {len(c_fps)}")
    print(f"Total R+C: {len(r_fps) + len(c_fps)}")
