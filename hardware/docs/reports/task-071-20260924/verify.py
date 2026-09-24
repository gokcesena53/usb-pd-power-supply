import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
baseline = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in baseline['footprints']}
refs = 'U1 Q3 R11 TH1 D1 C1 C2 C3 C4 C8 R8 R9 R12 R13 R14 R21 R64 R65 TP1 TP2 TP3 TP4 TP5'.split()
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
    ('U1', '20', 'C4', '1'),
    ('U1', '12', 'C1', '1'),
    ('U1', '15', 'C2', '1'),
    ('U1', '13', 'TH1', '2'),
    ('U1', '23', 'R12', '1'),
    ('R12', '2', 'Q3', '2'),
    ('U1', '22', 'R13', '1'),
    ('R13', '2', 'Q3', '5'),
    ('R11', '2', 'Q3', '7'),
    ('Q3', '5', 'C8', '1'),
    ('R11', '1', 'U1', '1'),
    ('R11', '2', 'U1', '24'),
    ('R11', '1', 'TP1', '1'),
    ('R11', '2', 'TP2', '1'),
    ('Q3', '5', 'TP3', '1'),
    ('C4', '1', 'TP4', '1'),
    ('R12', '2', 'TP5', '1'),
    ('U1', '8', 'R14', '1'),
    ('R14', '2', 'D1', '2'),
    ('U1', '11', 'R21', '2'),
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
    u1_orientation=dict(
        rotation=fs['U1'].GetOrientationDegrees(),
        cc1_pad=pad('U1', '17'),
        cc2_pad=pad('U1', '16'),
        vbus_in_pad=pad('U1', '1'),
        vbus_sense_pad=pad('U1', '24'),
        pwr_en_pad=pad('U1', '23'),
        vout_sense_pad=pad('U1', '22')
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
assert len(rows) == 23 and all(
    r['before_pads'] == [list(x) for x in r['after_pads']] and
    r['group'] == 'AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR' and
    r['side'] == 'B.Cu' and
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
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width='1050', height='700', viewBox='0 0 1050 700')
    ET.SubElement(svg, 'rect', x='0', y='0', width='1050', height='700', fill='#111827')
    t = ET.SubElement(svg, 'text', x='20', y='30', fill='white', style='font: bold 20px sans-serif')
    t.text = 'TASK-071 | ' + ('Sonra: B.Cu AP33772S koridorları ve yerleşim' if after else 'Önce: B.Cu yerleşim')
    x0, y0, s = 44, 132, 35
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
        color = '#f59f64' if row['ref'] in ('Q3', 'R11', 'C8') else '#80d5aa' if row['ref'] == 'U1' else '#f472b6' if row['ref'].startswith('TP') else '#8da9e9'
        ET.SubElement(svg, 'rect', x=str(x), y=str(y), width=str(w), height=str(h), fill=color, **{'fill-opacity': '0.35', 'stroke': color, 'stroke-width': '1.5'})
        t = ET.SubElement(svg, 'text', x=str(x + w / 2), y=str(y + h / 2 + 4), fill='white', **{'text-anchor': 'middle'}, style='font: bold 12px sans-serif')
        t.text = row['ref']
    
    if after:
        # High current power path
        line(pad('R11', '1')['xy'], pad('R11', '2')['xy'], '#ffd166', width='4')
        line(pad('R11', '2')['xy'], pad('Q3', '7')['xy'], '#ffd166', width='4')
        line(pad('Q3', '7')['xy'], pad('Q3', '5')['xy'], '#ff9f43', width='4')
        line(pad('Q3', '5')['xy'], pad('C8', '1')['xy'], '#ff9f43', width='4')
        # CC lines exiting left towards USB-C
        line(pad('U1', '17')['xy'], (45.0, pad('U1', '17')['xy'][1]), '#54a0ff', '5 4', width='2')
        line(pad('U1', '16')['xy'], (45.0, pad('U1', '16')['xy'][1]), '#54a0ff', '5 4', width='2')
        # Kelvin sense lines
        line(pad('R11', '1')['xy'], pad('U1', '1')['xy'], '#48dbfb', '3 3', width='1.5')
        line(pad('R11', '2')['xy'], pad('U1', '24')['xy'], '#48dbfb', '3 3', width='1.5')
        # Gate drive
        line(pad('U1', '23')['xy'], pad('R12', '1')['xy'], '#1dd1a1', width='2')
        line(pad('R12', '2')['xy'], pad('Q3', '2')['xy'], '#1dd1a1', width='2')
        # NTC thermal sensing
        line(pad('U1', '13')['xy'], pad('TH1', '2')['xy'], '#ff6b6b', '4 3', width='1.5')
        
        t = ET.SubElement(svg, 'text', x='16', y='685', fill='white', style='font: 13px sans-serif')
        t.text = 'Sarı/Turuncu: Güç yolu (USB_VBUS → R11 → Q3 → PD_VOUT → C8) | Mavi kesik: CC1/CC2 çıkış yönü | Camgöbeği: Kelvin algılama | Yeşil: Gate yolu | Kırmızı: NTC. Oklar planlanan koridorlardır.'
    
    ET.ElementTree(svg).write(here / ('after.svg' if after else 'before.svg'), encoding='unicode', xml_declaration=True)

draw(False)
draw(True)

print(json.dumps({
    k: out[k] for k in ('drc_before', 'drc_after', 'unconnected_before', 'unconnected_after', 'parity_after', 'tracks_unchanged')
}, ensure_ascii=False))
