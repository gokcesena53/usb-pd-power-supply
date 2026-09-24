"""Apply TASK-065 once to the recorded input; use KiCad Python from repo root.

Whole F-side buck/boost/USB groups are reflected about their own bounding
box centre, keeping local geometry (including the BOOST_FB track) intact.
Mixed-side groups keep component centres; later placement tasks pack them.
"""
import hashlib
import json
import sys
from pathlib import Path
import pcbnew as p

from audit import BOARD, HERE, ROOT

before = json.loads((HERE / 'inventory-before.json').read_text(encoding='utf-8'))
assert hashlib.sha256(BOARD.read_bytes()).hexdigest() == before['sha256'], 'Input changed; review before applying'
b = p.LoadBoard(str(BOARD))
fps = {f.GetReference(): f for f in b.GetFootprints()}
selected = ['TPS55340 PRE-BOOST', 'AOZ1284 3.3V BUCK', 'USB-C GIRIS',
            'RTC BQ32000 + 1F5 süper kapasitör',
            'ETHERNET MEZANIN (CH9121) + BESLEME ANAHTARI',
            'INA226 OLCUM + PANEL CIKISI',
            'AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR',
            'ESP32-C6-MINI-1-H4']
changed = []
for group in b.Groups():
    if group.GetName() not in selected:
        continue
    parts = [i for i in group.GetItems() if isinstance(i, p.FOOTPRINT)]
    assert not any(f.IsLocked() for f in parts)
    all_top = all(f.GetLayer() == p.F_Cu for f in parts)
    if all_top:
        bounds = [f.GetBoundingBox(False, False) for f in parts]
        pivot = p.VECTOR2I((min(v.GetLeft() for v in bounds)+max(v.GetRight() for v in bounds))//2,
                          (min(v.GetTop() for v in bounds)+max(v.GetBottom() for v in bounds))//2)
    for f in parts:
        if f.GetLayer() == p.F_Cu:
            f.Flip(pivot if all_top else f.GetPosition(), p.FLIP_DIRECTION_LEFT_RIGHT)
            changed.append(f.GetReference())
    if group.GetName() == 'TPS55340 PRE-BOOST':
        assert all_top
        for track in b.GetTracks():
            assert track.GetNetname() == '/USB_PD_CONTROLLER/BOOST_FB'
            track.Flip(pivot, p.FLIP_DIRECTION_LEFT_RIGHT)

# C33's anchor is one lead, not the body centre. Re-centre its mirrored
# body in the original staging slot; avoid moving it onto Y1.
fps['C33'].Move(p.VECTOR2I(p.FromMM(-20), 0))
# Keep mirrored reference text away from the now same-side copper.
fps['R43'].Reference().SetPosition(p.VECTOR2I(p.FromMM(90.975), p.FromMM(42.5)))
fps['D7'].Reference().SetPosition(p.VECTOR2I(p.FromMM(151.904288), p.FromMM(44.0)))

# J9 is a solder-wire footprint, not a connector housing. Envelope only:
# 5 insulated wires, OD 1.7 mm (footprint allowance), 10 mm straight exit.
sys.path.insert(0, str(ROOT / '.claude/skills/kicad-footprint/scripts'))
from step_boxes import StepBoxes, BLACK, SILVER
model_name = 'SolderWire-0.25sqmm_1x05_P4.2mm_D0.65mm_OD1.7mm.step'
model_rel = 'libraries/Generic_Custom.3dshapes/' + model_name
s = StepBoxes('J9_wire_exit_envelope_TASK065')
for i in range(5):
    s.cyl(f'Wire_{i+1}', BLACK, i*4.2, 0, 0.85, 0.3, 10.0, n=12)
    s.cyl(f'Conductor_{i+1}', SILVER, i*4.2, 0, 0.25, -1.8, 0.3, n=6)
s.write(str(ROOT / 'hardware' / model_rel))
assert len(list(fps['J9'].Models())) == 1
fps['J9'].Models()[0].m_Filename = '${KIPRJMOD}/' + model_rel

# Exact pad-centre and same-layer continuity for the existing FB connection.
def pad(ref, number):
    return next(a for a in fps[ref].Pads() if a.GetNumber() == number)
start, end = pad('D5', '2'), pad('U11', '9')
tracks = list(b.GetTracks())
assert len(tracks) == 4 and all(t.GetLayer() == p.B_Cu for t in tracks)
assert start.GetNetname() == end.GetNetname() == tracks[0].GetNetname()
edges = {}
for t in tracks:
    a, c = tuple(t.GetStart()), tuple(t.GetEnd())
    edges.setdefault(a, []).append(c); edges.setdefault(c, []).append(a)
seen, queue = set(), [tuple(start.GetPosition())]
while queue:
    q = queue.pop()
    if q in seen: continue
    seen.add(q); queue.extend(edges.get(q, []))
assert tuple(end.GetPosition()) in seen
p.SaveBoard(str(BOARD), b)
(HERE / 'applied.json').write_text(json.dumps(dict(groups=selected, flipped=sorted(changed),
    fb_length_mm=sum(p.ToMM(t.GetLength()) for t in tracks),
    fb_endpoints=[list(p.ToMM(start.GetPosition())), list(p.ToMM(end.GetPosition()))],
    fb_layer='B.Cu', j9_model=model_rel), ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Flipped {len(changed)} footprints; BOOST_FB connectivity preserved')
