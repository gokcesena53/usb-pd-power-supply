import pcbnew
import math
import json

pcb_path = r"hardware/gopo.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

def pt_dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def get_pad_info(pad):
    pos = pad.GetPosition()
    return {
        'num': pad.GetNumber(),
        'name': pad.GetName(),
        'net': pad.GetNetname(),
        'x': round(pcbnew.ToMM(pos.x), 3),
        'y': round(pcbnew.ToMM(pos.y), 3)
    }

def get_fp_dict(ref):
    fp = board.FindFootprintByReference(ref)
    if not fp:
        return None
    pos = fp.GetPosition()
    return {
        'ref': ref,
        'val': fp.GetValue(),
        'layer': fp.GetLayerName(),
        'x': round(pcbnew.ToMM(pos.x), 3),
        'y': round(pcbnew.ToMM(pos.y), 3),
        'rot': round(fp.GetOrientationDegrees(), 2),
        'fp_name': str(fp.GetFPID().GetLibItemName()),
        'pads': {str(pad.GetNumber()): get_pad_info(pad) for pad in fp.Pads()}
    }

# 1. Inspect Diodes D1-D10 and their relationships to ICs
diodes_to_audit = [f"D{i}" for i in range(1, 11)]
diodes_audit = {}
for ref in diodes_to_audit:
    fp = get_fp_dict(ref)
    diodes_audit[ref] = fp

# 2. Inspect Transistors Q1-Q8
qs_to_audit = [f"Q{i}" for i in range(1, 9)]
qs_audit = {}
for ref in qs_to_audit:
    fp = get_fp_dict(ref)
    qs_audit[ref] = fp

# 3. Inspect Inductors L1, L3
ls_to_audit = ['L1', 'L3']
ls_audit = {}
for ref in ls_to_audit:
    fp = get_fp_dict(ref)
    ls_audit[ref] = fp

# 4. Inspect Crystal Y1
ys_audit = {'Y1': get_fp_dict('Y1')}

# 5. Inspect ICs U1, U2, U3, U4, U5, U6, U10, U11, U12, U13
ics_to_audit = ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U10', 'U11', 'U12', 'U13']
ics_audit = {}
for ref in ics_to_audit:
    fp = get_fp_dict(ref)
    ics_audit[ref] = fp

# Let's calculate specific critical distances:
relations = []

# D1 -> U1 Pin 8 (via R14)
# Let's check R14
r14 = get_fp_dict('R14')
u1 = ics_audit['U1']
d1 = diodes_audit['D1']
relations.append({
    'name': 'D1 (LED) to U1 Pin 8 / R14',
    'd1_pos': (d1['x'], d1['y']),
    'd1_layer': d1['layer'],
    'u1_pos': (u1['x'], u1['y']),
    'u1_layer': u1['layer'],
    'u1_p8_pos': (u1['pads']['8']['x'], u1['pads']['8']['y']),
    'dist_d1_u1_p8': round(pt_dist((d1['x'], d1['y']), (u1['pads']['8']['x'], u1['pads']['8']['y'])), 3),
    'r14_pos': (r14['x'], r14['y']) if r14 else None,
    'r14_layer': r14['layer'] if r14 else None
})

# D2 (Catch Schottky) -> U5 Pin 1 (LX_SW)
u5 = ics_audit['U5']
d2 = diodes_audit['D2']
relations.append({
    'name': 'D2 (Catch Schottky) to U5 Pin 1 (LX_SW)',
    'd2_p1_pos': (d2['pads']['1']['x'], d2['pads']['1']['y']),
    'd2_layer': d2['layer'],
    'u5_p1_pos': (u5['pads']['1']['x'], u5['pads']['1']['y']),
    'u5_layer': u5['layer'],
    'dist_d2_p1_to_u5_p1': round(pt_dist((d2['pads']['1']['x'], d2['pads']['1']['y']), (u5['pads']['1']['x'], u5['pads']['1']['y'])), 3),
    'd2_center_to_u5_center': round(pt_dist((d2['x'], d2['y']), (u5['x'], u5['y'])), 3)
})

# D3 (VBUS TVS) -> J7 (USB-C) / U1
j7 = get_fp_dict('J7')
d3 = diodes_audit['D3']
relations.append({
    'name': 'D3 (VBUS TVS) to J7 (USB-C)',
    'd3_pos': (d3['x'], d3['y']),
    'd3_layer': d3['layer'],
    'j7_pos': (j7['x'], j7['y']) if j7 else None,
    'j7_layer': j7['layer'] if j7 else None,
    'dist_d3_j7': round(pt_dist((d3['x'], d3['y']), (j7['x'], j7['y'])), 3) if j7 else None
})

# D4 (Boost Schottky) -> U11 Pin 1,2 (SW) and C27/C28
u11 = ics_audit['U11']
d4 = diodes_audit['D4']
c27 = get_fp_dict('C27')
c28 = get_fp_dict('C28')
relations.append({
    'name': 'D4 (Boost Schottky) to U11 Pin 1,2 (BOOST_SW) & C27',
    'd4_p2_pos': (d4['pads']['2']['x'], d4['pads']['2']['y']),
    'd4_p1_pos': (d4['pads']['1']['x'], d4['pads']['1']['y']),
    'd4_layer': d4['layer'],
    'u11_p1_pos': (u11['pads']['1']['x'], u11['pads']['1']['y']),
    'u11_layer': u11['layer'],
    'dist_d4_p2_to_u11_p1': round(pt_dist((d4['pads']['2']['x'], d4['pads']['2']['y']), (u11['pads']['1']['x'], u11['pads']['1']['y'])), 3),
    'dist_d4_p1_to_c27': round(pt_dist((d4['pads']['1']['x'], d4['pads']['1']['y']), (c27['x'], c27['y'])), 3) if c27 else None,
    'dist_d4_center_to_u11_center': round(pt_dist((d4['x'], d4['y']), (u11['x'], u11['y'])), 3)
})

# D5 (Clamp Diode) -> U11 Pin 9 (BOOST_FB)
d5 = diodes_audit['D5']
relations.append({
    'name': 'D5 (FB Clamp Diode) to U11 Pin 9 (BOOST_FB)',
    'd5_p2_pos': (d5['pads']['2']['x'], d5['pads']['2']['y']),
    'd5_layer': d5['layer'],
    'u11_p9_pos': (u11['pads']['9']['x'], u11['pads']['9']['y']),
    'dist_d5_p2_to_u11_p9': round(pt_dist((d5['pads']['2']['x'], d5['pads']['2']['y']), (u11['pads']['9']['x'], u11['pads']['9']['y'])), 3),
    'dist_d5_center_to_u11_center': round(pt_dist((d5['x'], d5['y']), (u11['x'], u11['y'])), 3)
})

# D6 (Zener Clamp) -> U12 Pin 8 (GATE_DRV) & Pin 2/9 (SRC_COMMON)
u12 = ics_audit['U12']
d6 = diodes_audit['D6']
relations.append({
    'name': 'D6 (Gate-Source Clamp) to U12 Pin 8 (GATE_DRV)',
    'd6_p1_pos': (d6['pads']['1']['x'], d6['pads']['1']['y']),
    'd6_layer': d6['layer'],
    'u12_p8_pos': (u12['pads']['8']['x'], u12['pads']['8']['y']),
    'u12_layer': u12['layer'],
    'dist_d6_p1_to_u12_p8': round(pt_dist((d6['pads']['1']['x'], d6['pads']['1']['y']), (u12['pads']['8']['x'], u12['pads']['8']['y'])), 3),
    'dist_d6_center_to_u12_center': round(pt_dist((d6['x'], d6['y']), (u12['x'], u12['y'])), 3)
})

# D7 (Output TVS) -> U3 / OUT_POS
u3 = ics_audit['U3']
d7 = diodes_audit['D7']
relations.append({
    'name': 'D7 (Output TVS) to U3 Pin 8,9 (OUT_POS)',
    'd7_p1_pos': (d7['pads']['1']['x'], d7['pads']['1']['y']),
    'd7_layer': d7['layer'],
    'u3_p8_pos': (u3['pads']['8']['x'], u3['pads']['8']['y']),
    'u3_layer': u3['layer'],
    'dist_d7_p1_to_u3_p8': round(pt_dist((d7['pads']['1']['x'], d7['pads']['1']['y']), (u3['pads']['8']['x'], u3['pads']['8']['y'])), 3),
    'dist_d7_center_to_u3_center': round(pt_dist((d7['x'], d7['y']), (u3['x'], u3['y'])), 3)
})

# D8, D9 (CC1/CC2 TVS) -> J7 (USB-C) & U1
d8 = diodes_audit['D8']
d9 = diodes_audit['D9']
relations.append({
    'name': 'D8, D9 (CC TVS) to J7 and U1',
    'd8_pos': (d8['x'], d8['y']),
    'd9_pos': (d9['x'], d9['y']),
    'd8_layer': d8['layer'],
    'd9_layer': d9['layer'],
    'dist_d8_to_j7': round(pt_dist((d8['x'], d8['y']), (j7['x'], j7['y'])), 3) if j7 else None,
    'dist_d9_to_j7': round(pt_dist((d9['x'], d9['y']), (j7['x'], j7['y'])), 3) if j7 else None,
    'dist_d8_to_u1': round(pt_dist((d8['x'], d8['y']), (u1['x'], u1['y'])), 3),
    'dist_d9_to_u1': round(pt_dist((d9['x'], d9['y']), (u1['x'], u1['y'])), 3)
})

# D10 (Discharge Gate Zener) -> Q4 / Q6
q4 = qs_audit['Q4']
q6 = qs_audit['Q6']
d10 = diodes_audit['D10']
relations.append({
    'name': 'D10 (Discharge Gate Clamp) to Q4 & Q6',
    'd10_pos': (d10['x'], d10['y']),
    'd10_layer': d10['layer'],
    'q4_pos': (q4['x'], q4['y']),
    'q4_layer': q4['layer'],
    'q6_pos': (q6['x'], q6['y']),
    'q6_layer': q6['layer'],
    'dist_d10_to_q4': round(pt_dist((d10['x'], d10['y']), (q4['x'], q4['y'])), 3),
    'dist_d10_to_q6': round(pt_dist((d10['x'], d10['y']), (q6['x'], q6['y'])), 3)
})

# Q1, Q2 (I2C Level Shifters) -> U2 and U1
u2 = ics_audit['U2']
q1 = qs_audit['Q1']
q2 = qs_audit['Q2']
relations.append({
    'name': 'Q1, Q2 (I2C Level Shifters) to U2 (MCU) and U1 (PD)',
    'q1_pos': (q1['x'], q1['y']),
    'q1_layer': q1['layer'],
    'q2_pos': (q2['x'], q2['y']),
    'q2_layer': q2['layer'],
    'dist_q1_to_u2': round(pt_dist((q1['x'], q1['y']), (u2['x'], u2['y'])), 3),
    'dist_q2_to_u2': round(pt_dist((q2['x'], q2['y']), (u2['x'], u2['y'])), 3),
    'dist_q1_to_u1': round(pt_dist((q1['x'], q1['y']), (u1['x'], u1['y'])), 3),
    'dist_q2_to_u1': round(pt_dist((q2['x'], q2['y']), (u1['x'], u1['y'])), 3)
})

# Q3 (VBUS Dual FET) -> U1
q3 = qs_audit['Q3']
relations.append({
    'name': 'Q3 (VBUS Dual N-FET) to U1 (PD Sink Controller)',
    'q3_pos': (q3['x'], q3['y']),
    'q3_layer': q3['layer'],
    'dist_q3_to_u1': round(pt_dist((q3['x'], q3['y']), (u1['x'], u1['y'])), 3),
    'dist_q3_g_to_u1_p22_gate': round(pt_dist((q3['pads']['2']['x'], q3['pads']['2']['y']), (u1['pads']['22']['x'], u1['pads']['22']['y'])), 3)
})

# Q4, Q6 (Discharge FETs) & U13 (AND Gate)
u13 = ics_audit['U13']
relations.append({
    'name': 'Q4 (Inverter FET) to U13 (AND Gate)',
    'q4_p1_gate': (q4['pads']['1']['x'], q4['pads']['1']['y']),
    'u13_p4_out': (u13['pads']['4']['x'], u13['pads']['4']['y']),
    'dist_q4_gate_to_u13_out': round(pt_dist((q4['pads']['1']['x'], q4['pads']['1']['y']), (u13['pads']['4']['x'], u13['pads']['4']['y'])), 3),
    'dist_q4_center_to_u13_center': round(pt_dist((q4['x'], q4['y']), (u13['x'], u13['y'])), 3)
})

# Q5 (Dual Output Switch / Ideal Diode) -> U12
q5 = qs_audit['Q5']
relations.append({
    'name': 'Q5 (Dual Output FET) to U12 (LM74801)',
    'q5_pos': (q5['x'], q5['y']),
    'q5_layer': q5['layer'],
    'u12_pos': (u12['x'], u12['y']),
    'u12_layer': u12['layer'],
    'dist_q5_to_u12': round(pt_dist((q5['x'], q5['y']), (u12['x'], u12['y'])), 3),
    'dist_q5_dgate_to_u12_dgate': round(pt_dist((q5['pads']['4']['x'], q5['pads']['4']['y']), (u12['pads']['1']['x'], u12['pads']['1']['y'])), 3),
    'dist_q5_hgate_to_u12_hgate': round(pt_dist((q5['pads']['2']['x'], q5['pads']['2']['y']), (u12['pads']['8']['x'], u12['pads']['8']['y'])), 3),
    'dist_q5_src_to_u12_src': round(pt_dist((q5['pads']['1']['x'], q5['pads']['1']['y']), (u12['pads']['2']['x'], u12['pads']['2']['y'])), 3)
})

# Q8 (Ethernet Power Switch) -> J8 & U2
q8 = qs_audit['Q8']
j8 = get_fp_dict('J8')
relations.append({
    'name': 'Q8 (Ethernet Power FET) to J8 & U2',
    'q8_pos': (q8['x'], q8['y']),
    'q8_layer': q8['layer'],
    'j8_pos': (j8['x'], j8['y']) if j8 else None,
    'j8_layer': j8['layer'] if j8 else None,
    'dist_q8_to_j8': round(pt_dist((q8['x'], q8['y']), (j8['x'], j8['y'])), 3) if j8 else None,
    'dist_q8_gate_to_u2_p23': round(pt_dist((q8['pads']['3']['x'], q8['pads']['3']['y']), (u2['pads']['23']['x'], u2['pads']['23']['y'])), 3)
})

# L1 (Buck Inductor) -> U5 (Buck IC)
l1 = ls_audit['L1']
relations.append({
    'name': 'L1 (Buck Inductor) to U5 (AOZ1284PI)',
    'l1_pos': (l1['x'], l1['y']),
    'l1_layer': l1['layer'],
    'u5_pos': (u5['x'], u5['y']),
    'u5_layer': u5['layer'],
    'dist_l1_to_u5': round(pt_dist((l1['x'], l1['y']), (u5['x'], u5['y'])), 3),
    'dist_l1_p1_to_u5_lx': round(pt_dist((l1['pads']['1']['x'], l1['pads']['1']['y']), (u5['pads']['1']['x'], u5['pads']['1']['y'])), 3)
})

# L3 (Boost Inductor) -> U11 (Boost IC) & D4
l3 = ls_audit['L3']
relations.append({
    'name': 'L3 (Boost Inductor) to U11 (TPS55340) & D4',
    'l3_pos': (l3['x'], l3['y']),
    'l3_layer': l3['layer'],
    'u11_pos': (u11['x'], u11['y']),
    'u11_layer': u11['layer'],
    'dist_l3_to_u11': round(pt_dist((l3['x'], l3['y']), (u11['x'], u11['y'])), 3),
    'dist_l3_p1_to_u11_sw': round(pt_dist((l3['pads']['1']['x'], l3['pads']['1']['y']), (u11['pads']['1']['x'], u11['pads']['1']['y'])), 3),
    'dist_l3_p1_to_d4_p2': round(pt_dist((l3['pads']['1']['x'], l3['pads']['1']['y']), (d4['pads']['2']['x'], d4['pads']['2']['y'])), 3)
})

# Y1 (32.768kHz Crystal) -> U4 (BQ32000)
y1 = ys_audit['Y1']
u4 = ics_audit['U4']
relations.append({
    'name': 'Y1 (RTC Crystal) to U4 (BQ32000)',
    'y1_pos': (y1['x'], y1['y']),
    'y1_layer': y1['layer'],
    'u4_pos': (u4['x'], u4['y']),
    'u4_layer': u4['layer'],
    'dist_y1_to_u4': round(pt_dist((y1['x'], y1['y']), (u4['x'], u4['y'])), 3),
    'dist_y1_p1_to_u4_osci': round(pt_dist((y1['pads']['1']['x'], y1['pads']['1']['y']), (u4['pads']['1']['x'], u4['pads']['1']['y'])), 3),
    'dist_y1_p4_to_u4_osco': round(pt_dist((y1['pads']['4']['x'], y1['pads']['4']['y']), (u4['pads']['2']['x'], u4['pads']['2']['y'])), 3)
})

# Inter-IC distances:
inter_ic = [
    {
        'pair': 'U2 (ESP32-C6) <-> U1 (AP33772S)',
        'u2_pos': (u2['x'], u2['y']), 'u2_layer': u2['layer'],
        'u1_pos': (u1['x'], u1['y']), 'u1_layer': u1['layer'],
        'center_dist': round(pt_dist((u2['x'], u2['y']), (u1['x'], u1['y'])), 3)
    },
    {
        'pair': 'U2 (ESP32-C6) <-> U3 (INA226)',
        'u2_pos': (u2['x'], u2['y']), 'u2_layer': u2['layer'],
        'u3_pos': (u3['x'], u3['y']), 'u3_layer': u3['layer'],
        'center_dist': round(pt_dist((u2['x'], u2['y']), (u3['x'], u3['y'])), 3)
    },
    {
        'pair': 'U2 (ESP32-C6) <-> U4 (BQ32000)',
        'u2_pos': (u2['x'], u2['y']), 'u2_layer': u2['layer'],
        'u4_pos': (u4['x'], u4['y']), 'u4_layer': u4['layer'],
        'center_dist': round(pt_dist((u2['x'], u2['y']), (u4['x'], u4['y'])), 3)
    },
    {
        'pair': 'U3 (INA226) -> U13 (74LVC1G08)',
        'u3_pos': (u3['x'], u3['y']), 'u3_layer': u3['layer'],
        'u13_pos': (u13['x'], u13['y']), 'u13_layer': u13['layer'],
        'center_dist': round(pt_dist((u3['x'], u3['y']), (u13['x'], u13['y'])), 3),
        'ina_alert_pad_dist': round(pt_dist((u3['pads']['3']['x'], u3['pads']['3']['y']), (u13['pads']['2']['x'], u13['pads']['2']['y'])), 3)
    },
    {
        'pair': 'U13 (74LVC1G08) -> U12 (LM74801)',
        'u13_pos': (u13['x'], u13['y']), 'u13_layer': u13['layer'],
        'u12_pos': (u12['x'], u12['y']), 'u12_layer': u12['layer'],
        'center_dist': round(pt_dist((u13['x'], u13['y']), (u12['x'], u12['y'])), 3),
        'sw_en_pad_dist': round(pt_dist((u13['pads']['4']['x'], u13['pads']['4']['y']), (u12['pads']['6']['x'], u12['pads']['6']['y'])), 3)
    },
    {
        'pair': 'U13 (74LVC1G08) -> Q4 (Discharge Inverter FET)',
        'u13_pos': (u13['x'], u13['y']), 'u13_layer': u13['layer'],
        'q4_pos': (q4['x'], q4['y']), 'q4_layer': q4['layer'],
        'center_dist': round(pt_dist((u13['x'], u13['y']), (q4['x'], q4['y'])), 3),
        'sw_en_pad_dist': round(pt_dist((u13['pads']['4']['x'], u13['pads']['4']['y']), (q4['pads']['1']['x'], q4['pads']['1']['y'])), 3)
    }
]

audit_results = {
    'diodes': diodes_audit,
    'qs': qs_audit,
    'inductors': ls_audit,
    'crystal': ys_audit,
    'ics': ics_audit,
    'relations': relations,
    'inter_ic': inter_ic
}

with open("scratch/task099_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(audit_results, f, indent=2)

print("TASK-099 Audit Calculations Complete! Saved to scratch/task099_audit_results.json")
