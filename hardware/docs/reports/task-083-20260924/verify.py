"""TASK-083 verification and artifact generation script for PANEL ENCODER / J9 + PULL-UP group."""
import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
baseline = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in baseline['footprints']}
refs = ['R34', 'R35', 'R36']
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

def pad_info(fp, pad_num):
    a = next(a for a in fp.Pads() if a.GetNumber() == str(pad_num))
    return dict(net=a.GetNetname(), xy=mm(a.GetPosition()))

def measure_pads(fp1, num1, fp2, num2, desc=''):
    p1 = pad_info(fp1, num1)
    p2 = pad_info(fp2, num2)
    dist = round(math.dist(p1['xy'], p2['xy']), 4)
    return dict(
        a=f"{fp1.GetReference()}.{num1}", a_net=p1['net'], a_xy=p1['xy'],
        b=f"{fp2.GetReference()}.{num2}", b_net=p2['net'], b_xy=p2['xy'],
        desc=desc,
        straight_mm=dist
    )

j9 = fs['J9']
r34 = fs['R34']
r35 = fs['R35']
r36 = fs['R36']

measures = [
    # Pull-up array alignment & spacing:
    measure_pads(r34, '1', r35, '1', '+3.3V bus pitch: R34.1 to R35.1 (2.000 mm pitch, 0.000 mm Y offset)'),
    measure_pads(r35, '1', r36, '1', '+3.3V bus pitch: R35.1 to R36.1 (2.000 mm pitch, 0.000 mm Y offset)'),
    measure_pads(r34, '2', r35, '2', 'Signal bus pitch: R34.2 (ENC_A) to R35.2 (ENC_B)'),
    measure_pads(r35, '2', r36, '2', 'Signal bus pitch: R35.2 (ENC_B) to R36.2 (ENC_SW)'),
    
    # J9 pad pitches:
    measure_pads(j9, '1', j9, '2', 'J9 pin pitch: Pin 1 (ENC_A) to Pin 2 (GND) [4.200 mm]'),
    measure_pads(j9, '2', j9, '3', 'J9 pin pitch: Pin 2 (GND) to Pin 3 (ENC_B) [4.200 mm]'),
    measure_pads(j9, '3', j9, '4', 'J9 pin pitch: Pin 3 (ENC_B) to Pin 4 (ENC_SW) [4.200 mm]'),
    measure_pads(j9, '4', j9, '5', 'J9 pin pitch: Pin 4 (ENC_SW) to Pin 5 (GND) [4.200 mm]'),
]

# J9 mechanical position and clearance measurements:
j9_pad1 = pad_info(j9, '1')['xy']
j9_pad5 = pad_info(j9, '5')['xy']
lcd_left_edge_x = 63.72
lcd_tol_left_edge_x = 63.52
pcb_left_edge_x = 50.275

j9_mechanical = dict(
    ref='J9',
    footprint='Connector_Wire:SolderWire-0.25sqmm_1x05_P4.2mm_D0.65mm_OD1.7mm',
    pad_type='Through-Hole (THT, all copper layers)',
    position=mm(j9.GetPosition()),
    orientation_deg=j9.GetOrientationDegrees(),
    pad_pitch_mm=4.200,
    total_pad_span_mm=round(abs(j9_pad5[1] - j9_pad1[1]), 3),
    clearance_to_lcd_nominal_mm=round(lcd_left_edge_x - j9_pad1[0], 3),
    clearance_to_lcd_worst_case_mm=round(lcd_tol_left_edge_x - j9_pad1[0], 3),
    clearance_to_pcb_edge_mm=round(j9_pad1[0] - pcb_left_edge_x, 3),
    soldering_iron_angle_clearance='45-60 deg vertical clearance unobstructed outside LCD bezel',
    wire_gauge_spec='26-28 AWG (0.14 mm2), max OD 1.50 mm, max length 150 mm',
    min_bend_radius_mm=4.50,
    bend_envelope_depth_mm=6.00
)

# Courtyard clearances among R34, R35, R36
clearances = []
for i in range(len(rows)):
    for j in range(i+1, len(rows)):
        b1, b2 = rows[i]['after_bbox'], rows[j]['after_bbox']
        overlap_x = b1[0] < b2[2] and b2[0] < b1[2]
        overlap_y = b1[1] < b2[3] and b2[1] < b1[3]
        dx = max(0, max(b1[0] - b2[2], b2[0] - b1[2]))
        dy = max(0, max(b1[1] - b2[3], b2[1] - b1[3]))
        dist = max(dx, dy) if overlap_x or overlap_y else math.hypot(dx, dy)
        clearances.append(dict(
            pair=f"{rows[i]['ref']}-{rows[j]['ref']}",
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

# Slot and Mechanical Handoff to TASK-063 (AC #5 & AC #6)
handoff_to_task063 = dict(
    authority='TASK-063 is the sole authority for final board placement of J7 (USB-C), J8 (Ethernet), U2 (ESP32-C6), and J9',
    j9_current_status='THT wire solder pad array at (58.000, 91.600, rot -90.0, F.Cu), fully outside LCD projection',
    slot_type_decision=dict(
        recorded_decision='Open board keepout corridor (Option B) is recommended; physical slot (Option A) fully specified if required by chassis',
        option_A_physical_slot=dict(
            type='Milled slot in Edge.Cuts',
            width_mm=2.50,
            length_mm=22.00,
            corner_radius_mm=1.25,
            router_bit_diameter_mm=2.00,
            copper_clearance_mm=0.50,
            min_pcb_margin_mm=3.00,
            note='Requires Edge.Cuts update by TASK-063 if chosen'
        ),
        option_B_open_keepout_corridor=dict(
            type='3D mechanical keepout corridor (no PCB cutout)',
            keepout_area_mm='X in [52.00, 58.00], Y in [88.00, 112.00]',
            vertical_clearance_mm='Z >= 8.00 mm above PCB',
            strain_relief='Chassis boss / zip-tie anchor within 15 mm of J9 on front panel',
            note='Edge.Cuts remains unmodified; preserves GND plane integrity'
        )
    ),
    cable_exit_options=[
        dict(
            option='Option A (West Direct Exit)',
            direction='-X towards front panel',
            length_mm='< 60 mm',
            noise_profile='Safest: moves directly away from LCD, buck (AOZ1284), boost (TPS55340), and RF'
        ),
        dict(
            option='Option B (North-West Exit Along Left Edge)',
            direction='Along X ~ 52..55 mm towards upper chassis',
            length_mm='< 80 mm',
            noise_profile='Bypasses RJ45 mezzanine connector to the North'
        ),
        dict(
            option='Option C (Bottom Solder Pass-Through)',
            direction='Soldered from B.Cu, routes through notch/slot to panel',
            length_mm='< 70 mm',
            noise_profile='Requires slot or edge notch if chosen by TASK-063'
        )
    ],
    mandatory_isolation_rules=[
        'Cable harness MUST NOT cross within 15 mm of ESP32-C6 (U2) PCB antenna keepout',
        'Cable harness MUST NOT route over or adjacent to L1/D2/LX (AOZ1284) or L3/D4/SW (TPS55340) switching nodes',
        'Strain relief clamp on chassis wall mandatory to prevent mechanical fatigue on solder joints'
    ]
)

out = dict(
    placements=rows,
    j9_mechanical=j9_mechanical,
    pad_distances=measures,
    clearances=clearances,
    anchors=anchors,
    handoff_to_task063=handoff_to_task063,
    circuit_summary=dict(
        group='ROTARY ENCODER',
        members=['R34', 'R35', 'R36'],
        associated_anchor='J9 (5-pin solder wire THT connector)',
        topology='3x 10k 0402 pull-up resistors to +3.3V with unified 90 deg rotation; parallel signal breakout to MCU (GPIO21, 22, 23)',
        pin_map='J9.1=ENC_A, J9.2=GND, J9.3=ENC_B, J9.4=ENC_SW, J9.5=GND',
        sch_notes='Debounce handled in firmware; no RC/TVS in schematic; ESD protection via insulated knob and enclosed chassis'
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
assert len(rows) == 3 and all(r['ref'] in refs for r in rows)
assert all(r['group'] == 'ROTARY ENCODER' for r in rows)
assert all(r['side'] == 'B.Cu' for r in rows)
assert all(r['after_angle'] == 90.0 for r in rows)
assert rows[0]['after_xy'] == (40.7, 116.2)
assert rows[1]['after_xy'] == (42.7, 116.2)
assert rows[2]['after_xy'] == (44.7, 116.2)

# Anchor checks
assert all(
    v['before_xy'] == list(v['after_xy']) and
    v['before_angle'] == v['after_angle'] and
    v['before_uuid'] == v['after_uuid'] and
    v['before_side'] == v['after_side']
    for v in anchors.values()
)
assert anchors['J9']['after_xy'] == (58.0, 91.6)
assert anchors['J9']['after_angle'] == -90.0

assert track_ids == old_track_ids
assert len(after_drc['violations']) <= len(before_drc['violations'])
assert out['unconnected_before'] == out['unconnected_after'] == 360
assert out['parity_after'] == 0

# Courtyard clearances
for c in clearances:
    assert not c['overlap'], f"Courtyard overlap in {c['pair']}"
    assert c['clearance_mm'] >= 0.50, f"Courtyard clearance too small: {c['pair']} has {c['clearance_mm']} mm"

# SVG Generation
def draw_svg(after):
    W, H = 950, 720
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(W), height=str(H), viewBox=f'0 0 {W} {H}')
    ET.SubElement(svg, 'rect', x='0', y='0', width=str(W), height=str(H), fill='#0f172a')
    
    t = ET.SubElement(svg, 'text', x='25', y='35', fill='#f8fafc', style='font: bold 20px sans-serif')
    t.text = 'TASK-083 | ' + ('Sonra: Panel Enkoder J9 ve R34-R36 Pull-Up Düzeni & Koridorları' if after else 'Önce: R34-R36 Dağınık Yerleşimi')
    
    defs = ET.SubElement(svg, 'defs')
    marker_pwr = ET.SubElement(defs, 'marker', id='arr_pwr', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker_pwr, 'path', d='M0,0 L8,4 L0,8', fill='#ef4444')
    marker_gnd = ET.SubElement(defs, 'marker', id='arr_gnd', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker_gnd, 'path', d='M0,0 L8,4 L0,8', fill='#10b981')
    marker_sig = ET.SubElement(defs, 'marker', id='arr_sig', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker_sig, 'path', d='M0,0 L8,4 L0,8', fill='#38bdf8')
    marker_opt = ET.SubElement(defs, 'marker', id='arr_opt', markerWidth='8', markerHeight='8', refX='7', refY='4', orient='auto')
    ET.SubElement(marker_opt, 'path', d='M0,0 L8,4 L0,8', fill='#f59e0b')

    # Coordinate mapping:
    # We display two key zones:
    # 1. Left side of SVG: Staging area with R34, R35, R36 (x ~ 38..48, y ~ 113..120)
    # 2. Right side of SVG: J9 connection, LCD edge, PCB edge, cable exit options (x ~ 48..75, y ~ 85..120)
    
    # Let's map real PCB coordinates: x in [35, 75], y in [85, 125]
    # W=950, H=720
    # x_range = 40 mm -> scale_x = 20 px/mm (800 px)
    # y_range = 40 mm -> scale_y = 15 px/mm (600 px)
    x0, y0, sx, sy = 35.0, 85.0, 21.0, 14.5
    def xy(x, y): return ((x - x0) * sx + 45, (y - y0) * sy + 65)

    # 1. PCB Edge line at x=50.275
    pcb_x1, pcb_y1 = xy(50.275, 87.0)
    pcb_x2, pcb_y2 = xy(50.275, 123.0)
    ET.SubElement(svg, 'line', x1=str(pcb_x1), y1=str(pcb_y1), x2=str(pcb_x2), y2=str(pcb_y2), stroke='#38bdf8', **{'stroke-width': '2.5', 'stroke-dasharray': '6,4'})
    ET.SubElement(svg, 'text', x=str(pcb_x1 - 8), y=str(pcb_y1 + 20), fill='#38bdf8', **{'text-anchor': 'end'}, style='font: bold 12px sans-serif').text = 'KART KENARI (X=50.28)'

    # Staging zone label on the left (x < 50.28)
    stg_x1, stg_y1 = xy(37.0, 112.0)
    stg_x2, stg_y2 = xy(48.5, 121.0)
    ET.SubElement(svg, 'rect', x=str(stg_x1), y=str(stg_y1), width=str(stg_x2 - stg_x1), height=str(stg_y2 - stg_y1), fill='#1e293b', **{'fill-opacity': '0.5', 'stroke': '#64748b', 'stroke-width': '1', 'stroke-dasharray': '3,3'})
    ET.SubElement(svg, 'text', x=str(stg_x1 + 10), y=str(stg_y1 + 18), fill='#94a3b8', style='font: bold 11px sans-serif').text = 'R34-R36 PULL-UP HÜCRESİ (B.Cu)'

    # 2. LCD Boundary on the right (x >= 63.72)
    lcd_x1, lcd_y1 = xy(63.72, 87.0)
    lcd_x2, lcd_y2 = xy(74.0, 123.0)
    ET.SubElement(svg, 'rect', x=str(lcd_x1), y=str(lcd_y1), width=str(lcd_x2 - lcd_x1), height=str(lcd_y2 - lcd_y1), fill='#3b82f6', **{'fill-opacity': '0.12', 'stroke': '#60a5fa', 'stroke-width': '1.5'})
    ET.SubElement(svg, 'text', x=str(lcd_x1 + 12), y=str(lcd_y1 + 25), fill='#93c5fd', style='font: bold 13px sans-serif').text = 'LCD MODÜL ALANI (TFT032B018)'
    ET.SubElement(svg, 'text', x=str(lcd_x1 + 12), y=str(lcd_y1 + 42), fill='#bfdbfe', style='font: 11px sans-serif').text = 'Sol Kenar: X = 63.72 mm'
    ET.SubElement(svg, 'text', x=str(lcd_x1 + 12), y=str(lcd_y1 + 60), fill='#ef4444', style='font: bold 11px sans-serif').text = 'LEHİM YASAKLI BÖLGE'

    # LCD Margin indicator (58.0 to 63.72 mm = 5.72 mm)
    dim_y = 89.0
    dx1, dy1 = xy(58.0, dim_y)
    dx2, dy2 = xy(63.72, dim_y)
    ET.SubElement(svg, 'line', x1=str(dx1), y1=str(dy1), x2=str(dx2), y2=str(dy2), stroke='#facc15', **{'stroke-width': '1.5'})
    ET.SubElement(svg, 'line', x1=str(dx1), y1=str(dy1 - 4), x2=str(dx1), y2=str(dy1 + 4), stroke='#facc15', **{'stroke-width': '1.5'})
    ET.SubElement(svg, 'line', x1=str(dx2), y1=str(dy1 - 4), x2=str(dx2), y2=str(dy2 + 4), stroke='#facc15', **{'stroke-width': '1.5'})
    ET.SubElement(svg, 'text', x=str((dx1 + dx2)/2), y=str(dy1 - 6), fill='#facc15', **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = '5.72 mm Boşluk'

    # Draw J9 footprint (THT 5-pin)
    j9_pins = [
        (1, 'ENCODER_A', '#38bdf8', 91.60),
        (2, 'GND',       '#10b981', 95.80),
        (3, 'ENCODER_B', '#38bdf8', 100.00),
        (4, 'ENCODER_SW','#38bdf8', 104.20),
        (5, 'GND',       '#10b981', 108.40),
    ]

    for p_num, p_net, p_col, p_y in j9_pins:
        px, py = xy(58.00, p_y)
        # Pad outer ring (OD 1.7mm)
        r_out = 1.7 * sx / 2
        r_hole = 0.85 * sx / 2
        if p_num == 1:
            # Pin 1 is square
            ET.SubElement(svg, 'rect', x=str(px - r_out), y=str(py - r_out), width=str(2*r_out), height=str(2*r_out), fill=p_col, stroke='#f8fafc', **{'stroke-width': '1'})
        else:
            ET.SubElement(svg, 'circle', cx=str(px), cy=str(py), r=str(r_out), fill=p_col, stroke='#f8fafc', **{'stroke-width': '1'})
        # Drill hole
        ET.SubElement(svg, 'circle', cx=str(px), cy=str(py), r=str(r_hole), fill='#0f172a')
        # Pin label
        ET.SubElement(svg, 'text', x=str(px + r_out + 8), y=str(py + 4), fill='#f8fafc', style='font: bold 11px sans-serif').text = f"J9.{p_num} ({p_net})"

    # J9 Title
    j9_title_x, j9_title_y = xy(58.00, 88.00)
    ET.SubElement(svg, 'text', x=str(j9_title_x), y=str(j9_title_y), fill='#f8fafc', **{'text-anchor': 'middle'}, style='font: bold 13px sans-serif').text = 'J9 ENKODER KABLO PEDLERİ (P=4.2mm)'

    # Draw R34, R35, R36
    for r in rows:
        rx, ry = xy(r['after_xy'][0] if after else r['before_xy'][0], r['after_xy'][1] if after else r['before_xy'][1])
        ref = r['ref']
        # Resistor body
        ET.SubElement(svg, 'rect', x=str(rx - 8), y=str(ry - 12), width='16', height='24', fill='#a855f7', **{'fill-opacity': '0.7', 'stroke': '#c084fc', 'stroke-width': '1.5'})
        ET.SubElement(svg, 'text', x=str(rx), y=str(ry + 3), fill='white', **{'text-anchor': 'middle'}, style='font: bold 9px sans-serif').text = ref

        if after:
            # Pad 1 (+3.3V) at North or South: in our script rot=90 -> p1 is at y=116.71 (higher y, south)
            p1_x, p1_y = xy(r['after_xy'][0], 116.71)
            ET.SubElement(svg, 'circle', cx=str(p1_x), cy=str(p1_y), r='3.5', fill='#ef4444')
            # Pad 2 (Signal) at y=115.69 (lower y, north)
            p2_x, p2_y = xy(r['after_xy'][0], 115.69)
            ET.SubElement(svg, 'circle', cx=str(p2_x), cy=str(p2_y), r='3.5', fill='#38bdf8')
        else:
            # Before: R36 was inverted
            if ref == 'R36':
                p1_x, p1_y = xy(r['before_xy'][0], 115.70)
                p2_x, p2_y = xy(r['before_xy'][0], 116.72)
                ET.SubElement(svg, 'circle', cx=str(p1_x), cy=str(p1_y), r='3.5', fill='#ef4444')
                ET.SubElement(svg, 'circle', cx=str(p2_x), cy=str(p2_y), r='3.5', fill='#38bdf8')
                ET.SubElement(svg, 'text', x=str(rx), y=str(ry + 25), fill='#ef4444', **{'text-anchor': 'middle'}, style='font: bold 9px sans-serif').text = '(Ters rot!)'

    if after:
        # Common +3.3V bus line across R34.1, R35.1, R36.1
        b_x1, b_y1 = xy(39.5, 116.71)
        b_x2, b_y2 = xy(46.0, 116.71)
        ET.SubElement(svg, 'line', x1=str(b_x1), y1=str(b_y1), x2=str(b_x2), y2=str(b_y2), stroke='#ef4444', **{'stroke-width': '3', 'marker-end': 'url(#arr_pwr)'})
        ET.SubElement(svg, 'text', x=str(b_x2 + 8), y=str(b_y2 + 4), fill='#ef4444', style='font: bold 10px sans-serif').text = '+3.3V GÜÇ BARASI'

        # Signal lines exiting North towards MCU
        for rx_c, net_name in [(40.7, 'ENC_A'), (42.7, 'ENC_B'), (44.7, 'ENC_SW')]:
            sx1, sy1 = xy(rx_c, 115.69)
            sx2, sy2 = xy(rx_c, 113.50)
            ET.SubElement(svg, 'line', x1=str(sx1), y1=str(sy1), x2=str(sx2), y2=str(sy2), stroke='#38bdf8', **{'stroke-width': '2.5', 'marker-end': 'url(#arr_sig)'})
        ET.SubElement(svg, 'text', x=str(xy(42.7, 113.0)[0]), y=str(xy(42.7, 113.0)[1]), fill='#38bdf8', **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = 'MCU (GPIO21-23)'

        # Draw Keepout & Cable Exit Corridors between PCB edge and J9
        kp_x1, kp_y1 = xy(51.5, 90.0)
        kp_x2, kp_y2 = xy(56.5, 110.0)
        ET.SubElement(svg, 'rect', x=str(kp_x1), y=str(kp_y1), width=str(kp_x2 - kp_x1), height=str(kp_y2 - kp_y1), fill='#10b981', **{'fill-opacity': '0.12', 'stroke': '#10b981', 'stroke-width': '1.5', 'stroke-dasharray': '4,4'})
        ET.SubElement(svg, 'text', x=str((kp_x1 + kp_x2)/2), y=str(kp_y1 + 45), fill='#34d399', **{'text-anchor': 'middle'}, style='font: bold 11px sans-serif').text = 'KABLO & LEHİM'
        ET.SubElement(svg, 'text', x=str((kp_x1 + kp_x2)/2), y=str(kp_y1 + 60), fill='#34d399', **{'text-anchor': 'middle'}, style='font: bold 11px sans-serif').text = 'KORİDORU'
        ET.SubElement(svg, 'text', x=str((kp_x1 + kp_x2)/2), y=str(kp_y1 + 75), fill='#6ee7b7', **{'text-anchor': 'middle'}, style='font: 10px sans-serif').text = '(Z >= 8mm)'

        # Cable Exit Option A: Westward direct to Front Panel
        c_ax1, c_ay1 = xy(58.0, 100.0)
        c_ax2, c_ay2 = xy(48.0, 100.0)
        ET.SubElement(svg, 'line', x1=str(c_ax1), y1=str(c_ay1), x2=str(c_ax2), y2=str(c_ay2), stroke='#f59e0b', **{'stroke-width': '3', 'stroke-dasharray': '5,3', 'marker-end': 'url(#arr_opt)'})
        ET.SubElement(svg, 'text', x=str(c_ax2 - 10), y=str(c_ay2 + 4), fill='#f59e0b', **{'text-anchor': 'end'}, style='font: bold 11px sans-serif').text = 'SEÇENEK A: Ön Panele Doğrudan Batı Çıkışı (<60mm)'

        # Cable Exit Option B: North-West exit
        c_bx1, c_by1 = xy(58.0, 93.0)
        c_bx2, c_by2 = xy(52.0, 86.0)
        ET.SubElement(svg, 'line', x1=str(c_bx1), y1=str(c_by1), x2=str(c_bx2), y2=str(c_by2), stroke='#a855f7', **{'stroke-width': '2.5', 'stroke-dasharray': '5,3', 'marker-end': 'url(#arr_opt)'})
        ET.SubElement(svg, 'text', x=str(c_bx2), y=str(c_by2 - 6), fill='#c084fc', **{'text-anchor': 'middle'}, style='font: bold 10px sans-serif').text = 'SEÇENEK B: Kuzey-Batı Çıkışı'

        # Strain Relief Symbol
        sr_x, sr_y = xy(49.0, 100.0)
        ET.SubElement(svg, 'rect', x=str(sr_x - 6), y=str(sr_y - 12), width='12', height='24', fill='#f59e0b', stroke='#ffffff', **{'stroke-width': '1.5'})
        ET.SubElement(svg, 'text', x=str(sr_x), y=str(sr_y + 4), fill='#0f172a', **{'text-anchor': 'middle'}, style='font: bold 8px sans-serif').text = 'SR'

    t_leg = ET.SubElement(svg, 'text', x='25', y=str(H - 20), fill='#cbd5e1', style='font: 11px sans-serif')
    t_leg.text = 'Mavi: Enkoder Faz/Buton Sinyalleri | Kırmızı: +3.3V Pull-Up Barası | Yeşil: GND | Sarı: Kablo Çıkış Güzergâhı & Gerilim Alma (SR)'

    ET.ElementTree(svg).write(here / ('after.svg' if after else 'before.svg'), encoding='unicode', xml_declaration=True)

draw_svg(False)
draw_svg(True)

print("TASK-083 verification script completed successfully!")
print(json.dumps({
    k: out[k] for k in ('violations_before_total', 'violations_after_total', 'unconnected_before', 'unconnected_after', 'parity_after', 'tracks_unchanged')
}, ensure_ascii=False))
