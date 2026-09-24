import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
baseline = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in baseline['footprints']}
refs = 'R67 Q6 D10 R66 Q4'.split()
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
    ('R67', '2', 'Q6', '3'),     # Net-(Q6-D): Resistor to MOSFET Drain
    ('Q6', '1', 'D10', '1'),     # DISCH_G: Q6 Gate to D10 Cathode
    ('D10', '1', 'R66', '2'),    # DISCH_G: D10 Cathode to R66 pull-up
    ('Q4', '3', 'Q6', '1'),      # DISCH_G: Inverter Drain to Q6 Gate
    ('Q6', '2', 'D10', '2'),     # GND: Q6 Source to D10 Anode
    ('Q4', '2', 'D10', '2'),     # GND: Q4 Source to D10 Anode
    ('R67', '1', 'Q6', '2'),     # OUT_POS to GND discharge path
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
    circuit_summary=dict(
        topology='Active Output Discharge (R59 passive bleed replacement)',
        r67_power_resistor=dict(
            ref='R67', value='1k', package='2512', rating='2W',
            continuous_power_28v='0.781 W (39% rating)',
            continuous_power_30v4='0.920 W (46% rating)',
            pad_1_net=pad('R67', '1')['net'],
            pad_2_net=pad('R67', '2')['net']
        ),
        q6_discharge_switch=dict(
            ref='Q6', value='BSS138P', package='SOT-23', layer='F.Cu',
            gate_drive='DISCH_G clamped to 12V max by D10'
        ),
        d10_gate_clamp=dict(
            ref='D10', value='BZT52C12', package='SOD-123', layer='F.Cu',
            vz='12V', polarity='Cathode on DISCH_G, Anode on GND'
        ),
        r66_pullup=dict(
            ref='R66', value='100k', package='0603', layer='F.Cu',
            input_rail='SW_OUT'
        ),
        q4_inverter=dict(
            ref='Q4', value='BSS138P', package='SOT-23', layer='B.Cu',
            control_input='SW_EN from U13 (B.Cu)'
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
assert len(rows) == 5 and all(
    r['before_pads'] == [list(x) for x in r['after_pads']] and
    r['group'] == 'CIKIS DESARJI (R59 yerine aktif)' and
    r['uuid'] == old[r['ref']]['uuid']
    for r in rows
)
# Ensure sides match TASK-065 inventory-after
assert fs['Q4'].GetLayerName() == 'B.Cu'
assert all(fs[r].GetLayerName() == 'F.Cu' for r in ['R67', 'Q6', 'D10', 'R66'])

assert all(
    v['before_xy'] == list(v['after_xy']) and
    v['before_angle'] == v['after_angle'] and
    v['before_uuid'] == v['after_uuid'] and
    v['before_side'] == v['after_side']
    for v in anchors.values()
)
assert track_ids == old_track_ids
# DRC violations should be <= baseline (145 <= 146)
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
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width='950', height='550', viewBox='0 0 950 550')
    ET.SubElement(svg, 'rect', x='0', y='0', width='950', height='550', fill='#111827')
    t = ET.SubElement(svg, 'text', x='20', y='30', fill='white', style='font: bold 20px sans-serif')
    t.text = 'TASK-076 | ' + ('Sonra: CIKIS DESARJI Koridorları ve Yerleşim' if after else 'Önce: Dağınık Yerleşim')
    x0, y0, s = 178, 53, 40
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
        color = '#f59f64' if row['ref'] == 'R67' else '#54a0ff' if row['ref'] == 'Q6' else '#e74c3c' if row['ref'] == 'D10' else '#a29bfe' if row['ref'] == 'R66' else '#1dd1a1'
        layer_text = ' [B.Cu]' if row['side'] == 'B.Cu' else ' [F.Cu]'
        ET.SubElement(svg, 'rect', x=str(x), y=str(y), width=str(w), height=str(h), fill=color, **{'fill-opacity': '0.35', 'stroke': color, 'stroke-width': '1.5'})
        t = ET.SubElement(svg, 'text', x=str(x + w / 2), y=str(y + h / 2 + 4), fill='white', **{'text-anchor': 'middle'}, style='font: bold 12px sans-serif')
        t.text = row['ref'] + layer_text
    
    if after:
        # High power discharge path: OUT_POS -> R67.1 -> R67.2 -> Q6.3 -> Q6.2 -> GND
        line((179.0, pad('R67', '1')['xy'][1]), pad('R67', '1')['xy'], '#ffd166', width='4')
        line(pad('R67', '2')['xy'], pad('Q6', '3')['xy'], '#ff9f43', width='4')
        line(pad('Q6', '2')['xy'], (pad('Q6', '2')['xy'][0], pad('Q6', '2')['xy'][1] - 3.0), '#8395a7', '3 3', width='2')
        # DISCH_G control node: Q6.1 <-> D10.1 <-> R66.2
        line(pad('Q6', '1')['xy'], pad('D10', '1')['xy'], '#54a0ff', width='2')
        line(pad('D10', '1')['xy'], pad('R66', '2')['xy'], '#54a0ff', width='2')
        # GND node: Q6.2 to D10.2
        line(pad('Q6', '2')['xy'], pad('D10', '2')['xy'], '#8395a7', '3 3', width='2')
        # SW_OUT pull-up input to R66.1
        line((pad('R66', '1')['xy'][0], pad('R66', '1')['xy'][1] - 3.0), pad('R66', '1')['xy'], '#a29bfe', width='2')
        # Q4 on B.Cu: SW_EN input from west, DISCH_G pull-down to via
        line((188.0, pad('Q4', '1')['xy'][1]), pad('Q4', '1')['xy'], '#1dd1a1', width='2')
        line(pad('Q4', '3')['xy'], (pad('Q4', '3')['xy'][0], pad('Q4', '3')['xy'][1] - 3.5), '#54a0ff', '4 3', width='2')
        
        t = ET.SubElement(svg, 'text', x='20', y='525', fill='white', style='font: 13px sans-serif')
        t.text = 'Sarı/Turuncu: OUT_POS deşarj güç koridoru (2512 2W R67 → Q6.3) | Mavi: DISCH_G kenet/sürme düğümü | Yeşil: SW_EN tersleyici girişi (B.Cu) | Kesikli Gri: GND'
    
    ET.ElementTree(svg).write(here / ('after.svg' if after else 'before.svg'), encoding='unicode', xml_declaration=True)

draw(False)
draw(True)

print("Verification complete!")
print(json.dumps({
    k: out[k] for k in ('violations_before_total', 'violations_after_total', 'unconnected_before', 'unconnected_after', 'parity_after', 'tracks_unchanged')
}, ensure_ascii=False))
