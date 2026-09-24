import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
baseline = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in baseline['footprints']}
refs = 'RShunt1 U3 C11 R27 J4 D7 R59 U13 R61 C35'.split()
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

def measure(a, na, c, nc, desc=''):
    pa, pb = pad(a, na), pad(c, nc)
    return dict(
        desc=desc,
        a=f'{a}.{na}', a_net=pa['net'], a_xy=pa['xy'],
        b=f'{c}.{nc}', b_net=pb['net'], b_xy=pb['xy'],
        straight_mm=round(math.dist(pa['xy'], pb['xy']), 4)
    )

measures = [
    measure('U3', '10', 'RShunt1', '1', 'Kelvin IN+ (SW_OUT)'),
    measure('U3', '9', 'RShunt1', '2', 'Kelvin IN- (OUT_POS)'),
    measure('U3', '8', 'RShunt1', '2', 'VBUS voltage sense (OUT_POS)'),
    measure('U3', '6', 'C11', '1', 'U3 VS decoupling (+3.3V)'),
    measure('U3', '7', 'C11', '2', 'U3 GND decoupling'),
    measure('U13', '5', 'C35', '1', 'U13 VCC decoupling (+3.3V)'),
    measure('U13', '3', 'C35', '2', 'U13 GND decoupling'),
    measure('U3', '3', 'R27', '2', 'ALERT pull-up (INA_ALERT)'),
    measure('U3', '3', 'U13', '2', 'ALERT to U13 input'),
    measure('U13', '1', 'R61', '1', 'OUT_EN pull-down'),
    measure('RShunt1', '2', 'J4', '1', '3A Shunt to J4 Pin 1 (OUT_POS)'),
    measure('D7', '1', 'J4', '1', 'TVS D7 cathode to J4 Pin 1 (OUT_POS)'),
    measure('D7', '2', 'J4', '2', 'TVS D7 anode to J4 Pin 2 (GND)'),
    measure('R59', '1', 'J4', '1', 'Passive bleed to OUT_POS'),
    measure('R59', '2', 'J4', '2', 'Passive bleed to GND'),
]

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
    circuit_summary=dict(
        topology='INA226 Current/Power Monitor + Output Protection & Front-Panel Banana Jacks',
        kelvin_sensing=dict(
            shunt_resistor='RShunt1 (5m0 2512)',
            monitor_ic='U3 (INA226 TSSOP-10)',
            in_plus_distance_mm=measures[0]['straight_mm'],
            in_minus_distance_mm=measures[1]['straight_mm'],
            symmetry_verified=(measures[0]['straight_mm'] == measures[1]['straight_mm'])
        ),
        power_output=dict(
            connector='J4 (SolderWire-1.5sqmm_1x02_P7.8mm)',
            tvs_protection='D7 (SMBJ30A SMB 30V TVS)',
            passive_bleed='R59 (100k 0603)',
            max_continuous_current='3.0 A'
        ),
        protection_logic=dict(
            and_gate='U13 (74LVC1G08 SOT-23-5)',
            alert_pullup='R27 (10k 0402)',
            enable_pulldown='R61 (4k7 0402)',
            output_signal='SW_EN'
        )
    ),
    drc_before=counts(before_drc),
    drc_after=counts(after_drc),
    violations_before_total=len(before_drc['violations']),
    violations_after_total=len(after_drc['violations']),
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
    r['group'] == 'INA226 OLCUM + PANEL CIKISI' and
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
assert track_ids == old_track_ids
assert len(after_drc['violations']) <= len(before_drc['violations'])
assert out['unconnected_before'] == out['unconnected_after'] == 360
assert out['parity_after'] == 0

# Check 2D courtyard clearance
for i in range(len(rows)):
    for j in range(i+1, len(rows)):
        b1, b2 = rows[i]['after_bbox'], rows[j]['after_bbox']
        overlap_x = b1[0] < b2[2] and b2[0] < b1[2]
        overlap_y = b1[1] < b2[3] and b2[1] < b1[3]
        assert not (overlap_x and overlap_y), f"Overlap between {rows[i]['ref']} and {rows[j]['ref']}"

# SVG Generation
def draw(after):
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width='980', height='600', viewBox='0 0 980 600')
    ET.SubElement(svg, 'rect', x='0', y='0', width='980', height='600', fill='#111827')
    t = ET.SubElement(svg, 'text', x='20', y='30', fill='white', style='font: bold 20px sans-serif')
    t.text = 'TASK-075 | ' + ('Sonra: INA226 ve Panel Çıkışı Koridorları ve Yerleşim (B.Cu)' if after else 'Önce: Dağınık Yerleşim')
    x0, y0, s = 144, 46, 28
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
        color = '#f59f64' if row['ref'] == 'RShunt1' else '#54a0ff' if row['ref'] == 'U3' else '#e74c3c' if row['ref'] == 'D7' else '#ffd166' if row['ref'] == 'J4' else '#1dd1a1' if row['ref'] == 'U13' else '#a29bfe'
        ET.SubElement(svg, 'rect', x=str(x), y=str(y), width=str(w), height=str(h), fill=color, **{'fill-opacity': '0.35', 'stroke': color, 'stroke-width': '1.5'})
        t = ET.SubElement(svg, 'text', x=str(x + w / 2), y=str(y + h / 2 + 4), fill='white', **{'text-anchor': 'middle'}, style='font: bold 12px sans-serif')
        t.text = row['ref']
    
    if after:
        # High current 3A power path: SW_OUT (west) -> RShunt1.1 -> RShunt1.2 -> J4.1 (OUT_POS)
        line((146.0, pad('RShunt1', '1')['xy'][1]), pad('RShunt1', '1')['xy'], '#ffd166', width='4')
        line(pad('RShunt1', '1')['xy'], pad('RShunt1', '2')['xy'], '#ff9f43', width='4')
        line(pad('RShunt1', '2')['xy'], pad('J4', '1')['xy'], '#ffd166', width='4')
        line(pad('J4', '1')['xy'], pad('D7', '1')['xy'], '#e74c3c', width='2.5')
        line(pad('D7', '1')['xy'], pad('R59', '1')['xy'], '#a29bfe', width='1.5')
        # GND return
        line(pad('J4', '2')['xy'], pad('D7', '2')['xy'], '#8395a7', '3 3', width='2')
        line(pad('D7', '2')['xy'], pad('R59', '2')['xy'], '#8395a7', '3 3', width='2')
        # Symmetric Kelvin sensing pair: U3.10 -> RShunt1.1 (IN+), U3.9 -> RShunt1.2 (IN-)
        line(pad('U3', '10')['xy'], pad('RShunt1', '1')['xy'], '#00d2d3', width='2')
        line(pad('U3', '9')['xy'], pad('RShunt1', '2')['xy'], '#00d2d3', width='2')
        line(pad('U3', '8')['xy'], pad('RShunt1', '2')['xy'], '#54a0ff', '2 2', width='1.5')
        # Decoupling: U3.6 to C11.1, U13.5 to C35.1
        line(pad('U3', '6')['xy'], pad('C11', '1')['xy'], '#fed330', width='2')
        line(pad('U13', '5')['xy'], pad('C35', '1')['xy'], '#fed330', width='2')
        # Alert line: U3.3 -> R27.2 -> U13.2
        line(pad('U3', '3')['xy'], pad('R27', '2')['xy'], '#26de81', width='2')
        line(pad('R27', '2')['xy'], pad('U13', '2')['xy'], '#26de81', '3 3', width='1.5')
        # Enable: U13.1 to R61.1, U13.4 (SW_EN) output
        line(pad('R61', '1')['xy'], pad('U13', '1')['xy'], '#45aaf2', width='1.5')
        line(pad('U13', '4')['xy'], (pad('U13', '4')['xy'][0] + 5.0, pad('U13', '4')['xy'][1]), '#2bcbba', width='2')
        
        t = ET.SubElement(svg, 'text', x='20', y='580', fill='white', style='font: 13px sans-serif')
        t.text = 'Sarı/Turuncu: 3A Çıkış güç akışı (SW_OUT → RShunt1 → J4.1 OUT_POS) | Camgöbeği: Simetrik Kelvin diferansiyel çifti (IN+/IN-) | Yeşil: ALERT & Donanım kapatma mantığı | Sarı: +3.3V decoupling'
    
    ET.ElementTree(svg).write(here / ('after.svg' if after else 'before.svg'), encoding='unicode', xml_declaration=True)

draw(False)
draw(True)

print("Verification complete!")
print(json.dumps({
    k: out[k] for k in ('violations_before_total', 'violations_after_total', 'unconnected_before', 'unconnected_after', 'parity_after', 'tracks_unchanged')
}, ensure_ascii=False))
