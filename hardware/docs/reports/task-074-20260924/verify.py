import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
baseline = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in baseline['footprints']}
refs = 'U12 Q5 C30 C31 C32 D6 R54 R55 R56 R58'.split()
fs = {f.GetReference(): f for f in b.GetFootprints()}
groups = {f.GetReference(): g.GetName() for g in b.Groups() for f in g.GetItems() if isinstance(f, p.FOOTPRINT)}
mm = lambda v: tuple(round(x, 6) for x in p.ToMM(v))

rows = []
for ref in refs:
    f = fs[ref]
    box = f.GetBoundingBox(False, False)
    rows.append(dict(
        ref=ref,
        value=f.GetValue(),
        before_xy=old[ref]['xy'],
        before_angle=old[ref]['angle'],
        after_xy=mm(f.GetPosition()),
        after_angle=f.GetOrientationDegrees(),
        side=f.GetLayerName(),
        locked=f.IsLocked(),
        group=groups.get(ref),
        uuid=f.m_Uuid.AsString(),
        before_pads=old[ref]['pads'],
        after_pads=sorted((a.GetNumber(), a.GetNetname()) for a in f.Pads()),
        before_bbox=old[ref]['bbox'],
        after_bbox=[p.ToMM(box.GetLeft()), p.ToMM(box.GetTop()), p.ToMM(box.GetRight()), p.ToMM(box.GetBottom())]
    ))

def pad(ref, num):
    a = next(a for a in fs[ref].Pads() if a.GetNumber() == str(num))
    return dict(net=a.GetNetname(), xy=mm(a.GetPosition()))

def measure(a, na, c, nc):
    pa, pb = pad(a, na), pad(c, nc)
    return dict(
        a=f'{a}.{na}', a_net=pa['net'], a_xy=pa['xy'],
        b=f'{c}.{nc}', b_net=pb['net'], b_xy=pb['xy'],
        straight_mm=round(math.dist(pa['xy'], pb['xy']), 4)
    )

measures = [measure(*x) for x in [
    ('U12', '1', 'Q5', '4'),      # DGATE -> Q5B gate
    ('U12', '2', 'Q5', '3'),      # A (SRC_COMMON) -> Q5 common source
    ('U12', '8', 'Q5', '2'),      # HGATE (GATE_DRV) -> Q5A gate
    ('U12', '9', 'Q5', '1'),      # OUT (SRC_COMMON) -> Q5 common source
    ('U12', '12', 'Q5', '5'),     # C (SW_OUT) -> Q5B drain
    ('U12', '11', 'C31', '2'),    # CAP -> C31 charge pump cap
    ('U12', '10', 'C31', '1'),    # VS (V_PRE) -> C31
    ('U12', '10', 'C32', '1'),    # VS (V_PRE) -> C32 bypass
    ('U12', '7', 'C32', '2'),     # GND -> C32
    ('D6', '1', 'Q5', '2'),       # Zener cathode -> GATE_DRV
    ('D6', '2', 'Q5', '1'),       # Zener anode -> SRC_COMMON
    ('R54', '1', 'Q5', '2'),      # R54 slew resistor -> GATE_DRV
    ('R54', '2', 'C30', '1'),     # R54 -> C30 dV/dt cap
    ('R55', '2', 'U12', '5'),     # OV divider -> U12 OV_SENSE
    ('R56', '1', 'U12', '5'),     # OV divider ground resistor -> OV_SENSE
    ('R58', '1', 'U12', '6'),     # Enable pulldown -> U12 SW_EN
]]

before_drc = json.loads((here / 'drc-before.json').read_text(encoding='utf-8'))
after_drc = json.loads((here / 'drc-after.json').read_text(encoding='utf-8'))
counts = lambda d: {k: sum(v['type'] == k for v in d['violations']) for k in sorted({v['type'] for v in d['violations']})}

anchor_refs = 'J7 J3 J9 H1 H2 H3 H4 D5 U11'.split()
anchors = {ref: dict(
    before_xy=old[ref]['xy'], after_xy=mm(fs[ref].GetPosition()),
    before_angle=old[ref]['angle'], after_angle=fs[ref].GetOrientationDegrees(),
    before_uuid=old[ref]['uuid'], after_uuid=fs[ref].m_Uuid.AsString(),
    before_side=old[ref]['side'], after_side=fs[ref].GetLayerName()
) for ref in anchor_refs}

track_ids = {t.m_Uuid.AsString() for t in b.GetTracks()}
old_track_ids = {t['uuid'] for t in baseline['tracks']}

out = dict(
    placements=rows,
    pad_distances=measures,
    anchors=anchors,
    q5_pin_map=dict(
        q5a_load_switch=dict(
            drain=pad('Q5', '7'),
            gate=pad('Q5', '2'),
            source=pad('Q5', '1')
        ),
        q5b_ideal_diode=dict(
            source=pad('Q5', '3'),
            gate=pad('Q5', '4'),
            drain=pad('Q5', '5')
        ),
        common_source_net='/USB_PD_CONTROLLER/SRC_COMMON'
    ),
    u12_pin_map=dict(
        dgate=pad('U12', '1'),
        a_src=pad('U12', '2'),
        hgate=pad('U12', '8'),
        out_src=pad('U12', '9'),
        c_drain=pad('U12', '12'),
        cap=pad('U12', '11'),
        vs_pre=pad('U12', '10'),
        ov_sense=pad('U12', '5'),
        sw_en=pad('U12', '6')
    ),
    drc_before=counts(before_drc),
    drc_after=counts(after_drc),
    unconnected_before=len(before_drc['unconnected_items']),
    unconnected_after=len(after_drc['unconnected_items']),
    parity_before=len(before_drc['schematic_parity']),
    parity_after=len(after_drc['schematic_parity']),
    tracks_before=len(old_track_ids),
    tracks_after=len(track_ids),
    tracks_unchanged=(track_ids == old_track_ids)
)
(here / 'verification.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')

# Assertions
assert len(rows) == 10 and all(
    r['before_pads'] == [list(x) for x in r['after_pads']] and
    r['group'] == 'LM74801 CIKIS ANAHTARI + IDEAL DIYOT' and
    r['side'] == 'F.Cu' and
    r['uuid'] == old[r['ref']]['uuid']
    for r in rows
)
assert all(
    v['before_xy'] == list(v['after_xy']) and
    v['before_angle'] == v['after_angle'] and
    v['before_uuid'] == v['after_uuid'] and
    v['before_side'] == v['after_side']
    for v in anchors.values()
)
assert track_ids == old_track_ids and len(before_drc['violations']) == len(after_drc['violations'])
assert out['unconnected_before'] == out['unconnected_after'] and not out['parity_after']

# SVG Generation
def draw(after):
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width='950', height='600', viewBox='0 0 950 600')
    ET.SubElement(svg, 'rect', x='0', y='0', width='950', height='600', fill='#111827')
    t = ET.SubElement(svg, 'text', x='20', y='30', fill='white', style='font: bold 20px sans-serif')
    t.text = 'TASK-074 | ' + ('Sonra: F.Cu LM74801 koridorları ve yerleşim' if after else 'Önce: F.Cu yerleşim')
    x0, y0, s = 103, 49, 45
    def xy(x, y): return ((x - x0) * s, (y - y0) * s)
    def line(a, c, color, dash='', width='3'):
        x1, y1 = xy(*a)
        x2, y2 = xy(*c)
        attrs = dict(x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2), stroke=color, **{'stroke-width': width, 'marker-end': 'url(#arr)'})
        if dash: attrs['stroke-dasharray'] = dash
        ET.SubElement(svg, 'line', **attrs)
    defs = ET.SubElement(svg, 'defs')
    marker = ET.SubElement(defs, 'marker', id='arr', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker, 'path', d='M0,0 L8,4 L0,8', fill='#ffd166')
    
    for row in rows:
        bb = row['after_bbox' if after else 'before_bbox']
        x, y = xy(bb[0], bb[1])
        w = (bb[2] - bb[0]) * s
        h = (bb[3] - bb[1]) * s
        color = '#f59f64' if row['ref'] == 'Q5' else '#80d5aa' if row['ref'] == 'U12' else '#e74c3c' if row['ref'] == 'D6' else '#8da9e9'
        ET.SubElement(svg, 'rect', x=str(x), y=str(y), width=str(w), height=str(h), fill=color, **{'fill-opacity': '0.35', 'stroke': color, 'stroke-width': '1.5'})
        t = ET.SubElement(svg, 'text', x=str(x + w / 2), y=str(y + h / 2 + 4), fill='white', **{'text-anchor': 'middle'}, style='font: bold 12px sans-serif')
        t.text = row['ref']
    
    if after:
        # High current power path
        line((105.0, pad('Q5', '7')['xy'][1]), pad('Q5', '7')['xy'], '#ffd166', width='4')
        line(pad('Q5', '7')['xy'], pad('Q5', '5')['xy'], '#ff9f43', width='4')
        line(pad('Q5', '5')['xy'], (116.0, pad('Q5', '5')['xy'][1]), '#ff9f43', width='4')
        # DGATE drive to Q5.4
        line(pad('U12', '1')['xy'], pad('Q5', '4')['xy'], '#54a0ff', width='2')
        # Common source sense
        line(pad('U12', '2')['xy'], pad('Q5', '3')['xy'], '#48dbfb', '3 3', width='1.5')
        # HGATE drive to Q5.2
        line(pad('U12', '8')['xy'], pad('Q5', '2')['xy'], '#1dd1a1', width='2')
        # Cathode sense
        line(pad('U12', '12')['xy'], pad('Q5', '5')['xy'], '#a29bfe', '3 3', width='1.5')
        # Charge pump CAP-VS
        line(pad('U12', '11')['xy'], pad('C31', '2')['xy'], '#fdcb6e', width='2')
        line(pad('U12', '10')['xy'], pad('C31', '1')['xy'], '#fdcb6e', width='2')
        # Zener clamp
        line(pad('D6', '1')['xy'], pad('Q5', '2')['xy'], '#e74c3c', '4 3', width='1.5')
        
        t = ET.SubElement(svg, 'text', x='16', y='585', fill='white', style='font: 13px sans-serif')
        t.text = 'Sarı/Turuncu: Güç akışı (PD_VBUS_SENSED → Q5A → SRC_COMMON → Q5B → SW_OUT) | Mavi: DGATE | Yeşil: HGATE | Mor: Cathode | Sarı ince: Charge Pump. Oklar planlanan koridorlardır.'
    
    ET.ElementTree(svg).write(here / ('after.svg' if after else 'before.svg'), encoding='unicode', xml_declaration=True)

draw(False)
draw(True)

print(json.dumps({
    k: out[k] for k in ('drc_before', 'drc_after', 'unconnected_before', 'unconnected_after', 'parity_after', 'tracks_unchanged')
}, ensure_ascii=False))
