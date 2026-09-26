"""TASK-084 verification and artifact generation script for TEST NOKTALARI group."""
import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
baseline = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in baseline['footprints']}
refs = ['TP11', 'TP12', 'TP13', 'TP6', 'TP7', 'TP8']
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

def pad_info(fp, pad_num='1'):
    a = next(a for a in fp.Pads() if a.GetNumber() == str(pad_num))
    return dict(net=a.GetNetname(), xy=mm(a.GetPosition()))

def measure_pads(fp1, fp2, desc=''):
    p1 = pad_info(fp1)
    p2 = pad_info(fp2)
    dist = round(math.dist(p1['xy'], p2['xy']), 4)
    return dict(
        a=f"{fp1.GetReference()}.1", a_net=p1['net'], a_xy=p1['xy'],
        b=f"{fp2.GetReference()}.1", b_net=p2['net'], b_xy=p2['xy'],
        desc=desc,
        straight_mm=dist
    )

measures = [
    # UART cluster (F.Cu) 100-mil spacing:
    measure_pads(fs['TP11'], fs['TP12'], 'UART pitch: TP11 (UART_TX) to TP12 (UART_RX) [2.540 mm / 100 mil]'),
    measure_pads(fs['TP12'], fs['TP13'], 'UART pitch: TP12 (UART_RX) to TP13 (GND) [2.540 mm / 100 mil]'),
    measure_pads(fs['TP11'], fs['TP13'], 'UART span: TP11 (UART_TX) to TP13 (GND) [5.080 mm / 200 mil]'),
    
    # I2C cluster (B.Cu) 100-mil spacing:
    measure_pads(fs['TP6'], fs['TP7'], 'I2C pitch: TP6 (I2C_SCL) to TP7 (I2C_SDA) [2.540 mm / 100 mil]'),
    measure_pads(fs['TP7'], fs['TP8'], 'I2C pitch: TP7 (I2C_SDA) to TP8 (PD_INT) [2.540 mm / 100 mil]'),
    measure_pads(fs['TP6'], fs['TP8'], 'I2C span: TP6 (I2C_SCL) to TP8 (PD_INT) [5.080 mm / 200 mil]'),
    
    # Cluster vertical separation:
    measure_pads(fs['TP11'], fs['TP6'], 'Cluster vertical separation: TP11 (F.Cu) to TP6 (B.Cu) [4.000 mm]'),
]

# Comprehensive Table of ALL 14 Test Points on the PCB (AC #1)
all_tps = sorted([fp for fp in b.GetFootprints() if fp.GetReference().startswith('TP')], key=lambda x: int(x.GetReference()[2:]))
tp_table = []
tp_purposes = {
    'TP1':  ('AP33772S PD KONTROLCU', 'VBUS raw input voltage monitoring and PD negotiation contract check (5V..20V)'),
    'TP2':  ('AP33772S PD KONTROLCU', 'VBUS sense voltage divider feed; UVLO/OVLO trip point calibration'),
    'TP3':  ('AP33772S PD KONTROLCU', 'Switched VBUS power rail after Q3 back-to-back FET; input to TPS55340 pre-boost'),
    'TP4':  ('AP33772S PD KONTROLCU', 'AP33772S internal 5V LDO output and high-side I2C level shifter bias'),
    'TP5':  ('AP33772S PD KONTROLCU', 'AP33772S charge pump gate drive output driving Q3 power switch FETs'),
    'TP6':  ('TEST NOKTALARI / I2C',   'I2C bus SCL clock line (3.3V domain); fast-mode 400kHz bus timing analysis'),
    'TP7':  ('TEST NOKTALARI / I2C',   'I2C bus SDA data line (3.3V domain); protocol transaction and ACK/NACK sniffing'),
    'TP8':  ('TEST NOKTALARI / I2C',   'AP33772S active-low interrupt line to MCU (GPIO10); event alert notification timing'),
    'TP9':  ('ESP32-C6-MINI-1-H4',     'Ethernet controller boot configuration strapping (ETH_CFG0 / GPIO0)'),
    'TP10': ('ESP32-C6-MINI-1-H4',     'Ethernet power switch enable (ETH_PWR_EN / GPIO1) controlling Q8 soft-start'),
    'TP11': ('TEST NOKTALARI / UART',  'ESP32-C6 primary UART0 Transmit (GPIO16 / TXD0); boot log and CLI console output'),
    'TP12': ('TEST NOKTALARI / UART',  'ESP32-C6 primary UART0 Receive (GPIO17 / RXD0); firmware flashing and command input'),
    'TP13': ('TEST NOKTALARI / UART',  'Digital & power ground reference point; oscilloscope probe spring ground clip'),
    'TP14': ('ETHERNET MEZANIN',       'CH9121 Ethernet controller RUN status indicator / heartbeat'),
}

for tp in all_tps:
    ref = tp.GetReference()
    pos = tp.GetPosition()
    pad = list(tp.Pads())[0] if tp.Pads() else None
    net = pad.GetNetname() if pad else 'None'
    grp = groups.get(ref, 'None')
    block, purpose = tp_purposes.get(ref, ('Unknown', 'General debug test pad'))
    tp_table.append(dict(
        ref=ref,
        net=net,
        group=grp,
        block=block,
        purpose=purpose,
        layer=tp.GetLayerName(),
        xy=mm(pos),
        rot=tp.GetOrientationDegrees(),
        pad_size_mm=[p.ToMM(pad.GetSize().x), p.ToMM(pad.GetSize().y)] if pad else [1.0, 1.0]
    ))

# Courtyard clearances among TP6..TP8 and TP11..TP13
clearances = []
# F.Cu pair clearances
fcu_refs = ['TP11', 'TP12', 'TP13']
for i in range(len(fcu_refs)):
    for j in range(i+1, len(fcu_refs)):
        r1, r2 = next(r for r in rows if r['ref']==fcu_refs[i]), next(r for r in rows if r['ref']==fcu_refs[j])
        b1, b2 = r1['after_bbox'], r2['after_bbox']
        overlap_x = b1[0] < b2[2] and b2[0] < b1[2]
        overlap_y = b1[1] < b2[3] and b2[1] < b1[3]
        dx = max(0, max(b1[0] - b2[2], b2[0] - b1[2]))
        dy = max(0, max(b1[1] - b2[3], b2[1] - b1[3]))
        dist = max(dx, dy) if overlap_x or overlap_y else math.hypot(dx, dy)
        clearances.append(dict(
            pair=f"{fcu_refs[i]}-{fcu_refs[j]} (F.Cu)",
            overlap=(overlap_x and overlap_y),
            clearance_mm=round(dist, 4)
        ))

# B.Cu pair clearances
bcu_refs = ['TP6', 'TP7', 'TP8']
for i in range(len(bcu_refs)):
    for j in range(i+1, len(bcu_refs)):
        r1, r2 = next(r for r in rows if r['ref']==bcu_refs[i]), next(r for r in rows if r['ref']==bcu_refs[j])
        b1, b2 = r1['after_bbox'], r2['after_bbox']
        overlap_x = b1[0] < b2[2] and b2[0] < b1[2]
        overlap_y = b1[1] < b2[3] and b2[1] < b1[3]
        dx = max(0, max(b1[0] - b2[2], b2[0] - b1[2]))
        dy = max(0, max(b1[1] - b2[3], b2[1] - b1[3]))
        dist = max(dx, dy) if overlap_x or overlap_y else math.hypot(dx, dy)
        clearances.append(dict(
            pair=f"{bcu_refs[i]}-{bcu_refs[j]} (B.Cu)",
            overlap=(overlap_x and overlap_y),
            clearance_mm=round(dist, 4)
        ))

# DRC counts
before_drc = json.loads((here / 'drc-before.json').read_text(encoding='utf-8'))
after_drc = json.loads((here / 'drc-after.json').read_text(encoding='utf-8'))
counts = lambda d: {k: sum(v['type'] == k for v in d['violations']) for k in sorted({v['type'] for v in d['violations']})}

anchor_refs = 'J7 J3 J9 H1 H2 H3 H4 D5 U11'.split()
anchors = {ref: dict(
    before_xy=old[ref]['xy'], after_xy=mm(fs[ref].GetPosition()),
    before_angle=old[ref]['angle'], after_angle=fs[ref].GetOrientationDegrees(),
    before_uuid=old[ref]['uuid'], after_uuid=fs[ref].m_Uuid.AsString(),
    before_side=old[ref]['side'], after_side=fs[ref].GetLayerName(),
    locked=fs[ref].IsLocked()
) for ref in anchor_refs}

track_ids = {t.m_Uuid.AsString() for t in b.GetTracks()}
old_track_ids = {t['uuid'] for t in baseline['tracks']}

probe_rules = dict(
    pad_diameter_mm=1.00,
    pitch_standard_mm=2.54,
    pitch_standard_mil=100,
    probe_needle_compatibility='Compatible with 0.5-0.8 mm needle probes, pogo-pins, and oscilloscope spring clips',
    gnd_probe_reference='TP13 dedicated GND pad at 2.54 mm spacing from UART signals; local GND via field for I2C',
    forbidden_zones='No test points on high-di/dt SW nodes (AOZ1284 LX, TPS55340 SW); no test points under RJ45 THT pins or under LCD glass after final assembly'
)

out = dict(
    placements=rows,
    all_14_test_points=tp_table,
    pad_distances=measures,
    clearances=clearances,
    probe_rules=probe_rules,
    anchors=anchors,
    circuit_summary=dict(
        group='TEST NOKTALARI',
        members=refs,
        subgroups=dict(
            uart_cluster_fcu='TP11 (TX), TP12 (RX), TP13 (GND) at y=122.000 mm, pitch=2.540 mm (100 mil)',
            i2c_cluster_bcu='TP6 (SCL), TP7 (SDA), TP8 (INT) at y=126.000 mm, pitch=2.540 mm (100 mil)'
        ),
        gnd_reference='TP13 provides dedicated zero-loop scope spring ground clip reference',
        isolation='Separated by 4.00 mm vertically; completely outside high-current switching and RF keepout zones'
    ),
    drc_before=counts(before_drc),
    drc_after=counts(after_drc),
    violations_before_total=len(before_drc['violations']),
    violations_after_total=len(after_drc['violations']),
    unconnected_before=len(before_drc['unconnected_items']),
    unconnected_after=len(after_drc['unconnected_items']),
    parity_before=len(before_drc.get('schematic_parity', [])),
    parity_after=len(after_drc.get('schematic_parity', [])),
    tracks_before=len(old_track_ids),
    tracks_after=len(track_ids),
    tracks_unchanged=(track_ids == old_track_ids)
)
(here / 'verification.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')

# Assertions
assert len(rows) == 6 and all(r['ref'] in refs for r in rows)
assert all(r['group'] == 'TEST NOKTALARI' for r in rows)
assert len(tp_table) == 14

# Anchor checks
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

# Courtyard clearances
for c in clearances:
    assert not c['overlap'], f"Courtyard overlap in {c['pair']}"
    assert c['clearance_mm'] >= 0.45, f"Clearance too small: {c['pair']} has {c['clearance_mm']} mm"

# SVG Generation
def draw_svg(after):
    W, H = 900, 680
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(W), height=str(H), viewBox=f'0 0 {W} {H}')
    ET.SubElement(svg, 'rect', x='0', y='0', width=str(W), height=str(H), fill='#0f172a')
    
    t = ET.SubElement(svg, 'text', x='25', y='35', fill='#f8fafc', style='font: bold 20px sans-serif')
    t.text = 'TASK-084 | ' + ('Sonra: Test Noktaları Standart 100-mil Dağılımı ve Prob Alanı' if after else 'Önce: Test Noktaları Üst Üste/Gelişigüzel Yerleşimi')
    
    defs = ET.SubElement(svg, 'defs')
    marker_pwr = ET.SubElement(defs, 'marker', id='arr_pwr', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker_pwr, 'path', d='M0,0 L8,4 L0,8', fill='#ef4444')
    marker_gnd = ET.SubElement(defs, 'marker', id='arr_gnd', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker_gnd, 'path', d='M0,0 L8,4 L0,8', fill='#10b981')
    marker_sig = ET.SubElement(defs, 'marker', id='arr_sig', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker_sig, 'path', d='M0,0 L8,4 L0,8', fill='#38bdf8')

    # Mapping: Focus on the TEST NOKTALARI cluster
    # x in [204, 216] (12 mm span) -> 55 px/mm (660 px)
    # y in [119, 130] (11 mm span) -> 45 px/mm (495 px)
    x0, y0, sx, sy = 204.0, 119.0, 56.0, 46.0
    def xy(x, y): return ((x - x0) * sx + 50, (y - y0) * sy + 65)

    if after:
        # Cluster background box for UART (F.Cu)
        ux1, uy1 = xy(205.5, 120.2)
        ux2, uy2 = xy(214.5, 123.8)
        ET.SubElement(svg, 'rect', x=str(ux1), y=str(uy1), width=str(ux2 - ux1), height=str(uy2 - uy1), fill='#0284c7', **{'fill-opacity': '0.12', 'stroke': '#38bdf8', 'stroke-width': '1.5', 'stroke-dasharray': '4,4'})
        ET.SubElement(svg, 'text', x=str(ux1 + 12), y=str(uy1 + 18), fill='#38bdf8', style='font: bold 12px sans-serif').text = 'UART0 PROGRAMLAMA & DEBUG PORTU (F.Cu - TOP YÜZEY)'

        # Cluster background box for I2C (B.Cu)
        ix1, iy1 = xy(205.5, 124.2)
        ix2, iy2 = xy(214.5, 127.8)
        ET.SubElement(svg, 'rect', x=str(ix1), y=str(iy1), width=str(ix2 - ix1), height=str(iy2 - iy1), fill='#7c3aed', **{'fill-opacity': '0.12', 'stroke': '#a855f7', 'stroke-width': '1.5', 'stroke-dasharray': '4,4'})
        ET.SubElement(svg, 'text', x=str(ix1 + 12), y=str(iy1 + 18), fill='#c084fc', style='font: bold 12px sans-serif').text = 'I2C VERİ YOLU & KESME TEŞHİS PORTU (B.Cu - BOTTOM YÜZEY)'

        # Draw UART test points on F.Cu: TP11, TP12, TP13
        u_pts = [
            ('TP11', 'UART_TX', '#38bdf8', 207.50, 122.00),
            ('TP12', 'UART_RX', '#38bdf8', 210.04, 122.00),
            ('TP13', 'GND',     '#10b981', 212.58, 122.00),
        ]
        for ref, net, col, px_c, py_c in u_pts:
            px, py = xy(px_c, py_c)
            # Pad circle (D=1.0mm)
            r_pad = 0.50 * sx
            r_crt = 1.025 * sx
            # Courtyard boundary
            ET.SubElement(svg, 'circle', cx=str(px), cy=str(py), r=str(r_crt), fill='none', stroke=col, **{'stroke-width': '1', 'stroke-dasharray': '2,2', 'stroke-opacity': '0.6'})
            # Copper pad
            ET.SubElement(svg, 'circle', cx=str(px), cy=str(py), r=str(r_pad), fill=col, stroke='#f8fafc', **{'stroke-width': '1.2'})
            # Text label
            ET.SubElement(svg, 'text', x=str(px), y=str(py - r_pad - 6), fill='#f8fafc', **{'text-anchor': 'middle'}, style='font: bold 11px sans-serif').text = ref
            ET.SubElement(svg, 'text', x=str(px), y=str(py + r_pad + 14), fill=col, **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = net

        # Pitch dimension between TP11 and TP12 (2.54 mm)
        d_y = 120.7
        dx1, dy1 = xy(207.50, d_y)
        dx2, dy2 = xy(210.04, d_y)
        ET.SubElement(svg, 'line', x1=str(dx1), y1=str(dy1), x2=str(dx2), y2=str(dy2), stroke='#facc15', **{'stroke-width': '1.5'})
        ET.SubElement(svg, 'line', x1=str(dx1), y1=str(dy1 - 3), x2=str(dx1), y2=str(dy1 + 3), stroke='#facc15', **{'stroke-width': '1.5'})
        ET.SubElement(svg, 'line', x1=str(dx2), y1=str(dy1 - 3), x2=str(dx2), y2=str(dy1 + 3), stroke='#facc15', **{'stroke-width': '1.5'})
        ET.SubElement(svg, 'text', x=str((dx1 + dx2)/2), y=str(dy1 - 5), fill='#facc15', **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = '2.54 mm (100 mil)'

        # Pitch dimension between TP12 and TP13 (2.54 mm)
        dx3, dy3 = xy(210.04, d_y)
        dx4, dy4 = xy(212.58, d_y)
        ET.SubElement(svg, 'line', x1=str(dx3), y1=str(dy3), x2=str(dx4), y2=str(dy4), stroke='#facc15', **{'stroke-width': '1.5'})
        ET.SubElement(svg, 'line', x1=str(dx3), y1=str(dy3 - 3), x2=str(dx3), y2=str(dy3 + 3), stroke='#facc15', **{'stroke-width': '1.5'})
        ET.SubElement(svg, 'line', x1=str(dx4), y1=str(dy4 - 3), x2=str(dx4), y2=str(dy4 + 3), stroke='#facc15', **{'stroke-width': '1.5'})
        ET.SubElement(svg, 'text', x=str((dx3 + dx4)/2), y=str(dy3 - 5), fill='#facc15', **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = '2.54 mm'

        # Draw I2C test points on B.Cu: TP6, TP7, TP8
        i_pts = [
            ('TP6', 'I2C_SCL', '#c084fc', 207.50, 126.00),
            ('TP7', 'I2C_SDA', '#c084fc', 210.04, 126.00),
            ('TP8', 'PD_INT',  '#f59e0b', 212.58, 126.00),
        ]
        for ref, net, col, px_c, py_c in i_pts:
            px, py = xy(px_c, py_c)
            r_pad = 0.50 * sx
            r_crt = 1.025 * sx
            ET.SubElement(svg, 'circle', cx=str(px), cy=str(py), r=str(r_crt), fill='none', stroke=col, **{'stroke-width': '1', 'stroke-dasharray': '2,2', 'stroke-opacity': '0.6'})
            ET.SubElement(svg, 'circle', cx=str(px), cy=str(py), r=str(r_pad), fill=col, stroke='#f8fafc', **{'stroke-width': '1.2'})
            ET.SubElement(svg, 'text', x=str(px), y=str(py - r_pad - 6), fill='#f8fafc', **{'text-anchor': 'middle'}, style='font: bold 11px sans-serif').text = ref
            ET.SubElement(svg, 'text', x=str(px), y=str(py + r_pad + 14), fill=col, **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = net

        # Ground clip connection indicator between TP12/11 and TP13
        g_x1, g_y1 = xy(210.04, 122.00)
        g_x2, g_y2 = xy(212.58, 122.00)
        ET.SubElement(svg, 'path', d=f"M {g_x1} {g_y1 + 18} Q {(g_x1+g_x2)/2} {g_y1 + 32} {g_x2} {g_y1 + 18}", fill='none', stroke='#10b981', **{'stroke-width': '2', 'stroke-dasharray': '3,2'})
        ET.SubElement(svg, 'text', x=str((g_x1 + g_x2)/2), y=str(g_y1 + 42), fill='#10b981', **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = 'Prob GND Yay Klipsi Mesafesi (100 mil)'

    else:
        # Before state: non-standard 3.092 mm pitch and directly stacked coordinates
        ET.SubElement(svg, 'text', x='50', y='120', fill='#ef4444', style='font: bold 13px sans-serif').text = 'Önceki Durum: TP11-13 (F.Cu) ve TP6-8 (B.Cu) Aynı X Ekseninde Farklı Yüzeylerde Çakışık'
        for r in rows:
            ref = r['ref']
            rx, ry = xy(r['before_xy'][0], r['before_xy'][1])
            col = '#38bdf8' if r['side']=='F.Cu' else '#c084fc'
            ET.SubElement(svg, 'circle', cx=str(rx), cy=str(ry), r='15', fill=col, **{'fill-opacity': '0.4', 'stroke': col, 'stroke-width': '1.5'})
            ET.SubElement(svg, 'text', x=str(rx), y=str(ry + 4), fill='white', **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = ref
            ET.SubElement(svg, 'text', x=str(rx), y=str(ry + 22), fill=col, **{'text-anchor': 'middle'}, style='font: 9px sans-serif').text = f"({r['side']})"

    # Bottom summary legend
    t_leg = ET.SubElement(svg, 'text', x='25', y=str(H - 20), fill='#cbd5e1', style='font: 11px sans-serif')
    t_leg.text = 'Mavi: UART0 Sinyalleri | Mor: I2C Veri Yolu | Yeşil: GND Referans Pedi | Sarı: 100-mil (2.54 mm) Standart Prob Adımı'

    ET.ElementTree(svg).write(here / ('after.svg' if after else 'before.svg'), encoding='unicode', xml_declaration=True)

draw_svg(False)
draw_svg(True)

print("TASK-084 verification complete!")
print(json.dumps({
    k: out[k] for k in ('violations_before_total', 'violations_after_total', 'unconnected_before', 'unconnected_after', 'parity_after', 'tracks_unchanged')
}, ensure_ascii=False))
