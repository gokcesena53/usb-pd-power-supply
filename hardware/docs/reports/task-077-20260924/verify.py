import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
baseline = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in baseline['footprints']}
refs = 'U2 C5 C6 C7 R1 R2 R3 R10 R15 R16 R37 SW1 SW2 TP9 TP10'.split()
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
        a=f'{a}.{na}', a_net=pa['net'], a_xy=pa['xy'],
        b=f'{c}.{nc}', b_net=pb['net'], b_xy=pb['xy'],
        desc=desc,
        straight_mm=round(math.dist(pa['xy'], pb['xy']), 4)
    )

measures = [
    measure('C6', '1', 'U2', '3', '+3.3V high-frequency decoupling capacitor to VDD pin 3'),
    measure('C5', '1', 'U2', '3', '+3.3V bulk decoupling capacitor to VDD pin 3'),
    measure('C7', '2', 'U2', '8', 'EN reset timing capacitor (delay filter) to EN pin 8'),
    measure('R1', '2', 'U2', '8', 'EN pull-up resistor to EN pin 8'),
    measure('SW2', '2', 'U2', '8', 'RESET tactile switch to EN pin 8'),
    measure('R2', '1', 'U2', '17', 'USB_DM series damping resistor to IO12 pin 17'),
    measure('R3', '1', 'U2', '18', 'USB_DP series damping resistor to IO13 pin 18'),
    measure('R10', '1', 'U2', '23', 'IO9 boot strapping pull-up resistor to IO9 pin 23'),
    measure('SW1', '2', 'U2', '23', 'BOOT tactile switch to IO9 pin 23'),
    measure('R37', '1', 'U2', '22', 'IO8 pull-up resistor to IO8 pin 22'),
    measure('R15', '1', 'U2', '22', 'ETH_CFG0 series damping resistor to IO8 pin 22'),
    measure('R16', '2', 'U2', '12', 'IO0 / ETH_PWR_EN pull-down resistor to IO0 pin 12'),
    measure('TP9', '1', 'R15', '2', 'Test point TP9 on ETH_CFG0'),
    measure('TP10', '1', 'R16', '1', 'Test point TP10 on ETH_PWR_EN'),
    measure('C6', '2', 'U2', '1', 'GND return loop: C6.2 to U2 pin 1 (GND)'),
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

# Check antenna keepout zone compliance
KEEPOUT_X_MIN = 166.22
KEEPOUT_X_MAX = 186.62
KEEPOUT_Y_MIN = 72.00
KEEPOUT_Y_MAX = 115.20
EDGE_CUTS_X_MAX = 149.72

keepout_status = []
for row in rows:
    if row['ref'] == 'U2':
        continue
    bb = row['after_bbox']
    overlap_ko_x = bb[0] < KEEPOUT_X_MAX and bb[2] > KEEPOUT_X_MIN
    overlap_ko_y = bb[1] < KEEPOUT_Y_MAX and bb[3] > KEEPOUT_Y_MIN
    inside_keepout = overlap_ko_x and overlap_ko_y
    clearance_to_edge = round(bb[0] - EDGE_CUTS_X_MAX, 4)
    keepout_status.append(dict(
        ref=row['ref'],
        bbox=bb,
        inside_keepout=inside_keepout,
        edge_clearance_mm=clearance_to_edge
    ))

out = dict(
    placements=rows,
    pad_distances=measures,
    antenna_keepout_zone=dict(
        x_min=KEEPOUT_X_MIN, x_max=KEEPOUT_X_MAX,
        y_min=KEEPOUT_Y_MIN, y_max=KEEPOUT_Y_MAX,
        rule='Must be completely free of all traces, copper, vias, and components on all layers',
        peripherals_inside_keepout=sum(k['inside_keepout'] for k in keepout_status),
        peripherals_status=keepout_status
    ),
    anchors=anchors,
    circuit_summary=dict(
        module='ESP32-C6-MINI-1-H4 (U2)',
        layer='B.Cu',
        antenna_orientation='Facing EAST (towards board right edge)',
        power_decoupling='C6 (0402 100n bypass) placed 3.04 mm from VDD Pin 3; C5 (0805 22uF bulk) directly adjacent at 5.58 mm',
        reset_timing='C7 (0402 1uF) placed 3.03 mm from EN Pin 8; R1 (0402 10k pull-up) placed 3.45 mm from EN Pin 8',
        tactile_switches='SW2 (RESET) and SW1 (BOOT) placed in safe non-RF corridor at x=158.5 mm (8 mm away from antenna keepout)',
        west_column_signals='R2 (USB_DM 22R), R3 (USB_DP 22R), R16 (ETH_PWR_EN 10k), R10 (Boot 10k), R37 (IO8 10k), R15 (ETH_CFG0 22R) aligned at x=152.0 mm (>2.2 mm from Edge.Cuts)',
        test_points='TP9 (ETH_CFG0) at (152.0, 84.5) and TP10 (ETH_PWR_EN) at (152.0, 105.0) on B.Cu west column'
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
assert len(rows) == 15 and all(
    r['before_pads'] == [list(x) for x in r['after_pads']] and
    r['group'] == 'ESP32-C6-MINI-1-H4' and
    r['uuid'] == old[r['ref']]['uuid']
    for r in rows
)
# All 15 on B.Cu
assert all(fs[r].GetLayerName() == 'B.Cu' for r in refs)

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

# Check that NO peripheral overlaps antenna keepout
assert out['antenna_keepout_zone']['peripherals_inside_keepout'] == 0

# Check 2D courtyard clearance among all non-U2 pairs
non_u2_rows = [r for r in rows if r['ref'] != 'U2']
for i in range(len(non_u2_rows)):
    for j in range(i+1, len(non_u2_rows)):
        b1, b2 = non_u2_rows[i]['after_bbox'], non_u2_rows[j]['after_bbox']
        overlap_x = b1[0] < b2[2] and b2[0] < b1[2]
        overlap_y = b1[1] < b2[3] and b2[1] < b1[3]
        assert not (overlap_x and overlap_y), f"Overlap between {non_u2_rows[i]['ref']} and {non_u2_rows[j]['ref']}"

# SVG Generation
def draw(after):
    W, H = 1000, 850
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(W), height=str(H), viewBox=f'0 0 {W} {H}')
    ET.SubElement(svg, 'rect', x='0', y='0', width=str(W), height=str(H), fill='#0f172a')
    
    t = ET.SubElement(svg, 'text', x='25', y='35', fill='#f8fafc', style='font: bold 20px sans-serif')
    t.text = 'TASK-077 | ' + ('Sonra: ESP32-C6 RF Anten Keepout, Bypass ve Buton Koridorları' if after else 'Önce: Dağınık / Sıralı Başlangıç Yerleşimi')
    
    # Coordinate system: x in [146, 204], y in [70, 122]
    x0, y0, s = 146.0, 70.0, 16.0
    def xy(x, y): return ((x - x0) * s, (y - y0) * s)
    
    defs = ET.SubElement(svg, 'defs')
    marker = ET.SubElement(defs, 'marker', id='arr', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker, 'path', d='M0,0 L8,4 L0,8', fill='#38bdf8')

    # Draw Edge.Cuts line
    ec_x = (EDGE_CUTS_X_MAX - x0) * s
    ET.SubElement(svg, 'line', x1=str(ec_x), y1='50', x2=str(ec_x), y2=str(H - 40), stroke='#e11d48', **{'stroke-width': '2', 'stroke-dasharray': '6 4'})
    t_ec = ET.SubElement(svg, 'text', x=str(ec_x - 8), y='75', fill='#fb7185', **{'text-anchor': 'end'}, style='font: bold 12px sans-serif')
    t_ec.text = 'PCB Edge.Cuts (x=149.72)'
    
    # Draw Antenna Keepout Zone
    k_x, k_y = xy(KEEPOUT_X_MIN, KEEPOUT_Y_MIN)
    k_w = (KEEPOUT_X_MAX - KEEPOUT_X_MIN) * s
    k_h = (KEEPOUT_Y_MAX - KEEPOUT_Y_MIN) * s
    ET.SubElement(svg, 'rect', x=str(k_x), y=str(k_y), width=str(k_w), height=str(k_h),
                  fill='#dc2626', **{'fill-opacity': '0.15', 'stroke': '#ef4444', 'stroke-width': '2', 'stroke-dasharray': '5 5'})
    t_ko = ET.SubElement(svg, 'text', x=str(k_x + k_w/2), y=str(k_y + 25), fill='#f87171', **{'text-anchor': 'middle'}, style='font: bold 14px sans-serif')
    t_ko.text = 'ANTEN KEEPOUT BÖLGESİ (Tüm Katmanlar Yasak)'

    def line(a, c, color, dash='', width='2.5'):
        x1, y1 = xy(*a)
        x2, y2 = xy(*c)
        attrs = dict(x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2), stroke=color, **{'stroke-width': width, 'marker-end': 'url(#arr)'})
        if dash: attrs['stroke-dasharray'] = dash
        ET.SubElement(svg, 'line', **attrs)

    for row in rows:
        bb = row['after_bbox' if after else 'before_bbox']
        x, y = xy(bb[0], bb[1])
        w = (bb[2] - bb[0]) * s
        h = (bb[3] - bb[1]) * s
        
        ref = row['ref']
        if ref == 'U2':
            color = '#38bdf8'
        elif ref in ('C6', 'C5'):
            color = '#fbbf24'
        elif ref in ('C7', 'R1'):
            color = '#34d399'
        elif ref in ('SW1', 'SW2'):
            color = '#a855f7'
        elif ref in ('TP9', 'TP10'):
            color = '#ec4899'
        else:
            color = '#60a5fa'
            
        ET.SubElement(svg, 'rect', x=str(x), y=str(y), width=str(w), height=str(h), fill=color, **{'fill-opacity': '0.35', 'stroke': color, 'stroke-width': '1.5'})
        t = ET.SubElement(svg, 'text', x=str(x + w / 2), y=str(y + h / 2 + 4), fill='white', **{'text-anchor': 'middle'}, style='font: bold 11px sans-serif')
        t.text = ref

    if after:
        # VDD Power Decoupling lines: U2.3 -> C6.1 -> C5.1
        line(pad('U2', '3')['xy'], pad('C6', '1')['xy'], '#fbbf24', width='3')
        line(pad('C6', '1')['xy'], pad('C5', '1')['xy'], '#f59e0b', width='3')
        # GND return: C6.2 -> U2.1
        line(pad('C6', '2')['xy'], pad('U2', '1')['xy'], '#94a3b8', '3 3', width='2')
        # EN Reset Timing lines: U2.8 -> C7.2 -> R1.2 -> SW2.2
        line(pad('U2', '8')['xy'], pad('C7', '2')['xy'], '#34d399', width='2.5')
        line(pad('C7', '2')['xy'], pad('R1', '2')['xy'], '#10b981', width='2.5')
        line(pad('C7', '2')['xy'], pad('SW2', '2')['xy'], '#a855f7', width='2')
        # BOOT switch to IO9: U2.23 -> SW1.2
        line(pad('U2', '23')['xy'], pad('SW1', '2')['xy'], '#c084fc', width='2')
        # West Column signals to U2 pins
        line(pad('U2', '17')['xy'], pad('R2', '1')['xy'], '#60a5fa', width='2')
        line(pad('U2', '18')['xy'], pad('R3', '1')['xy'], '#60a5fa', width='2')
        line(pad('U2', '12')['xy'], pad('R16', '2')['xy'], '#60a5fa', width='2')
        line(pad('U2', '23')['xy'], pad('R10', '1')['xy'], '#60a5fa', width='2')
        line(pad('U2', '22')['xy'], pad('R37', '1')['xy'], '#60a5fa', width='2')
        line(pad('U2', '22')['xy'], pad('R15', '1')['xy'], '#60a5fa', width='2')
        # Test Points
        line(pad('R15', '2')['xy'], pad('TP9', '1')['xy'], '#ec4899', width='1.5')
        line(pad('R16', '1')['xy'], pad('TP10', '1')['xy'], '#ec4899', width='1.5')

        t_leg = ET.SubElement(svg, 'text', x='25', y=str(H - 18), fill='#cbd5e1', style='font: 12px sans-serif')
        t_leg.text = 'Sarı: VDD Decoupling (C6 100n, C5 22µ) | Yeşil: EN/Reset (C7, R1) | Mor: Butonlar (SW2 Reset, SW1 Boot) | Mavi: USB/Strapping Batı Kolonu | Pembe: TP9/TP10'

    ET.ElementTree(svg).write(here / ('after.svg' if after else 'before.svg'), encoding='unicode', xml_declaration=True)

draw(False)
draw(True)

print("Verification complete!")
print(json.dumps({
    k: out[k] for k in ('violations_before_total', 'violations_after_total', 'unconnected_before', 'unconnected_after', 'parity_after', 'tracks_unchanged')
}, ensure_ascii=False))
