#!/usr/bin/env python3
"""
TASK-105: Tum bilesenlerin TASK-104 IPC kurallarina ve estetik standartlarina uygunlugunu denetle
Script: scratch/audit_task104_compliance.py
KiCad Python: KiCad 10.0.5 pcbnew
"""

import os
import sys
import json
import math
import subprocess
import pcbnew

def run_compliance_audit(pcb_path='hardware/gopo.kicad_pcb', drc_rpt_path='scratch/task105_current_drc.rpt'):
    print(f"Loading PCB: {pcb_path}")
    board = pcbnew.LoadBoard(pcb_path)
    
    footprints = list(board.GetFootprints())
    total_fps = len(footprints)
    print(f"Total footprints found: {total_fps}")
    
    # 1. Categorization
    inventory = {
        'passives_rc': [],
        'r_shunt': [],
        'thermistors': [],
        'ics': [],
        'diodes': [],
        'transistors_fets': [],
        'inductors': [],
        'crystals': [],
        'test_points': [],
        'connectors': [],
        'switches': [],
        'mounting_holes': [],
        'mechanical': []
    }
    
    for fp in footprints:
        ref = str(fp.GetReference())
        pos = fp.GetPosition()
        x_mm = round(pcbnew.ToMM(pos.x), 3)
        y_mm = round(pcbnew.ToMM(pos.y), 3)
        rot = round(fp.GetOrientation().AsDegrees() % 360, 2)
        if rot == 360.0:
            rot = 0.0
        val = str(fp.GetValue())
        layer = str(fp.GetLayerName())
        fp_id = str(fp.GetFPID().GetLibItemName())
        
        info = {
            'ref': ref,
            'val': val,
            'x': x_mm,
            'y': y_mm,
            'rot': rot,
            'layer': layer,
            'footprint': fp_id
        }
        
        if ref.startswith('RShunt'):
            inventory['r_shunt'].append(info)
        elif ref.startswith('TH'):
            inventory['thermistors'].append(info)
        elif ref.startswith('R') or ref.startswith('C'):
            inventory['passives_rc'].append(info)
        elif ref.startswith('U'):
            inventory['ics'].append(info)
        elif ref.startswith('D'):
            inventory['diodes'].append(info)
        elif ref.startswith('Q'):
            inventory['transistors_fets'].append(info)
        elif ref.startswith('L'):
            inventory['inductors'].append(info)
        elif ref.startswith('Y'):
            inventory['crystals'].append(info)
        elif ref.startswith('TP'):
            inventory['test_points'].append(info)
        elif ref.startswith('J'):
            inventory['connectors'].append(info)
        elif ref.startswith('SW'):
            inventory['switches'].append(info)
        elif ref.startswith('H'):
            inventory['mounting_holes'].append(info)
        elif ref.startswith('MECH'):
            inventory['mechanical'].append(info)
        else:
            print(f"Uncategorized footprint: {ref}")

    print("\n--- INVENTORY SUMMARY ---")
    for cat, items in inventory.items():
        print(f"  {cat:20}: {len(items):3} items")
    
    # 2. AC #1: Courtyards & DRC Courtyard Overlap Check
    print("\n--- AC #1: IPC-7351 COURTYARD & CLEARANCE CHECK ---")
    courtyard_violations = []
    if os.path.exists(drc_rpt_path):
        with open(drc_rpt_path, 'r', encoding='utf-8') as f:
            drc_text = f.read()
        if 'courtyards_overlap' in drc_text:
            lines = [line for line in drc_text.splitlines() if 'courtyards_overlap' in line]
            courtyard_violations.extend(lines)
    
    ac1_pass = (len(courtyard_violations) == 0)
    print(f"Courtyard Overlap Violations: {len(courtyard_violations)} -> {'PASS' if ac1_pass else 'FAIL'}")

    # 3. AC #2: Grid Alignment of 85 Passives (R, C)
    print("\n--- AC #2: GRID ALIGNMENT (85 PASSIVES) ---")
    grid_050 = []
    grid_025 = []
    off_grid = []
    
    # Sort passives numerically by prefix and index
    def sort_key(item):
        r = item['ref']
        prefix = ''.join([c for c in r if c.isalpha()])
        num = int(''.join([c for c in r if c.isdigit()]))
        return (prefix, num)
    
    sorted_passives = sorted(inventory['passives_rc'], key=sort_key)
    
    for p in sorted_passives:
        x = p['x']
        y = p['y']
        
        rem_x_050 = round(abs(x % 0.50), 3)
        rem_y_050 = round(abs(y % 0.50), 3)
        is_050 = (rem_x_050 in (0.0, 0.50)) and (rem_y_050 in (0.0, 0.50))
        
        rem_x_025 = round(abs(x % 0.25), 3)
        rem_y_025 = round(abs(y % 0.25), 3)
        is_025 = (rem_x_025 in (0.0, 0.25)) and (rem_y_025 in (0.0, 0.25))
        
        if is_050:
            grid_type = "0.50mm"
            grid_050.append(p)
        elif is_025:
            grid_type = "0.25mm"
            grid_025.append(p)
        else:
            grid_type = "OFF_GRID"
            off_grid.append(p)
        p['grid_type'] = grid_type

    print(f"Total Passives: {len(sorted_passives)}")
    print(f"  Locked to 0.50 mm Grid: {len(grid_050)} ({len(grid_050)/len(sorted_passives)*100:.1f}%)")
    print(f"  Locked to 0.25 mm Grid: {len(grid_025)} ({len(grid_025)/len(sorted_passives)*100:.1f}%)")
    print(f"  Off-Grid Components:    {len(off_grid)} ({len(off_grid)/len(sorted_passives)*100:.1f}%)")
    ac2_pass = (len(sorted_passives) == 85 and len(off_grid) == 0)
    print(f"AC #2 Status: {'PASS' if ac2_pass else 'FAIL'}")

    # 4. AC #3: Linear Arrays and Center-Line Pitch Alignment
    print("\n--- AC #3: LINEAR ARRAYS & COMMON CENTER-LINES ---")
    rails = {}
    
    # AP33772S Rail (Y=125.50 mm)
    ap_refs = ['R21', 'R8', 'R64', 'R65', 'R9']
    ap_passives = [p for p in sorted_passives if p['ref'] in ap_refs]
    ap_passives.sort(key=lambda item: item['x'])
    ap_y_vals = [p['y'] for p in ap_passives]
    ap_pitches = [round(ap_passives[i+1]['x'] - ap_passives[i]['x'], 3) for i in range(len(ap_passives)-1)]
    rails['ap33772s_rail'] = {
        'refs': [p['ref'] for p in ap_passives],
        'y_coords': ap_y_vals,
        'common_y': 125.500,
        'y_aligned': all(y == 125.500 for y in ap_y_vals),
        'pitches': ap_pitches,
        'standard_pitch': 2.250,
        'pitch_uniform': all(p == 2.250 for p in ap_pitches)
    }
    print(f"AP33772S Rail: Refs={[p['ref'] for p in ap_passives]}, Y={ap_y_vals}, Pitches={ap_pitches}")

    # Active Discharge Rail (Y=107.50 mm)
    dis_refs = ['R55', 'R56', 'R58']
    dis_passives = [p for p in sorted_passives if p['ref'] in dis_refs]
    dis_passives.sort(key=lambda item: item['x'])
    dis_y_vals = [p['y'] for p in dis_passives]
    dis_pitches = [round(dis_passives[i+1]['x'] - dis_passives[i]['x'], 3) for i in range(len(dis_passives)-1)]
    rails['active_discharge_rail'] = {
        'refs': [p['ref'] for p in dis_passives],
        'y_coords': dis_y_vals,
        'common_y': 107.500,
        'y_aligned': all(y == 107.500 for y in dis_y_vals),
        'pitches': dis_pitches,
        'standard_pitch': 2.250,
        'pitch_uniform': all(p == 2.250 for p in dis_pitches)
    }
    print(f"Active Discharge Rail: Refs={[p['ref'] for p in dis_passives]}, Y={dis_y_vals}, Pitches={dis_pitches}")

    # Boost rails
    boost_fb = [p for p in sorted_passives if p['ref'] in ['R51', 'R50']]
    boost_fb.sort(key=lambda item: item['x'])
    rails['boost_feedback_rail'] = {
        'refs': [p['ref'] for p in boost_fb],
        'common_y': 108.000,
        'pitch': round(boost_fb[1]['x'] - boost_fb[0]['x'], 3) if len(boost_fb) == 2 else None
    }
    
    boost_comp = [p for p in sorted_passives if p['ref'] in ['R49', 'C24', 'R52']]
    boost_comp.sort(key=lambda item: item['x'])
    rails['boost_compensation_rail'] = {
        'refs': [p['ref'] for p in boost_comp],
        'common_y': 128.000,
        'pitches': [round(boost_comp[i+1]['x'] - boost_comp[i]['x'], 3) for i in range(len(boost_comp)-1)]
    }
    
    buck_in = [p for p in sorted_passives if p['ref'] in ['C13', 'C12']]
    buck_in.sort(key=lambda item: item['x'])
    rails['buck_input_rail'] = {
        'refs': [p['ref'] for p in buck_in],
        'common_y': 105.000,
        'pitch': round(buck_in[1]['x'] - buck_in[0]['x'], 3) if len(buck_in) == 2 else None
    }

    ac3_pass = rails['ap33772s_rail']['y_aligned'] and rails['ap33772s_rail']['pitch_uniform'] and \
               rails['active_discharge_rail']['y_aligned'] and rails['active_discharge_rail']['pitch_uniform']
    print(f"AC #3 Status: {'PASS' if ac3_pass else 'FAIL'}")

    # 5. AC #4: Rotations of all 144 Components
    print("\n--- AC #4: ORTHOGONAL ROTATION OF ALL 144 FOOTPRINTS ---")
    rot_histogram = {0.0: 0, 90.0: 0, 180.0: 0, 270.0: 0}
    non_orthogonal = []
    
    all_fps_info = []
    for cat in inventory.values():
        all_fps_info.extend(cat)
    
    for item in all_fps_info:
        r = item['rot']
        if r in rot_histogram:
            rot_histogram[r] += 1
        else:
            non_orthogonal.append(item)
    
    print(f"Total Components: {len(all_fps_info)}")
    print(f"Rotations Distribution: {rot_histogram}")
    print(f"Non-orthogonal Components: {len(non_orthogonal)}")
    
    # Pull-up matrices check
    pullups = {
        'i2c_3v3': ['R4', 'R7'],
        'i2c_5v': ['R5', 'R6'],
        'encoder_pullup': ['R34', 'R35', 'R36'],
        'usb_diff': ['R2', 'R3'],
        'cc_lines': ['R62', 'R63']
    }
    pullup_uniformity = {}
    for group_name, r_list in pullups.items():
        rots = [p['rot'] for p in sorted_passives if p['ref'] in r_list]
        pullup_uniformity[group_name] = {
            'refs': r_list,
            'rots': rots,
            'uniform': len(set(rots)) == 1
        }
    
    ac4_pass = (len(non_orthogonal) == 0 and all(v['uniform'] for v in pullup_uniformity.values()))
    print(f"AC #4 Status: {'PASS' if ac4_pass else 'FAIL'}")

    # 6. AC #5: Decoupling Loops and Pin Distances
    print("\n--- AC #5: DECOUPLING CAPACITORS & PIN DISTANCES ---")
    decoupling_targets = [
        ('U1', '10', 'Net-(U1-V18)', 'C1', '1', 'Net-(U1-V18)'),
        ('U1', '9', 'PD_INT_5V', 'C4', '1', 'PD_5V'),
        ('U1', '1', 'Net-(U1-IFB)', 'C2', '1', 'Net-(U1-IFB)'),
        ('U1', '19', 'PD_VOUT', 'C8', '1', 'PD_VOUT'),
        ('U2', '3', '+3.3V', 'C6', '1', '+3.3V'),
        ('U3', '1', '+3.3V', 'C11', '1', '+3.3V'),
        ('U4', '8', '+3.3V', 'C9', '1', '+3.3V'),
        ('U5', '2', 'V_PRE', 'C14', '1', 'V_PRE'),
        ('U5', '8', '/USB_PD_CONTROLLER/SS_RAMP', 'C18', '1', '/USB_PD_CONTROLLER/SS_RAMP'),
        ('U11', '2', 'PD_VOUT', 'C26', '1', 'PD_VOUT'),
        ('U11', '3', 'PD_VOUT', 'C27', '1', 'V_PRE'),
        ('U11', '6', 'Net-(U11-SS)', 'C23', '1', 'Net-(U11-SS)'),
        ('U12', '10', 'V_PRE', 'C32', '1', 'V_PRE'),
        ('U13', '5', '+3.3V', 'C35', '1', '+3.3V'),
        ('J3', '21', '+3.3V', 'C34', '1', '+3.3V'),
    ]
    
    decoupling_audit = []
    for ic_ref, ic_pin, ic_net, c_ref, c_pin, c_net in decoupling_targets:
        ic_fp = board.FindFootprintByReference(ic_ref)
        c_fp = board.FindFootprintByReference(c_ref)
        
        ic_pads = [p for p in ic_fp.Pads() if p.GetNumber() == ic_pin]
        c_pads = [p for p in c_fp.Pads() if p.GetNumber() == c_pin]
        
        if ic_pads and c_pads:
            ic_pad = ic_pads[0]
            c_pad = c_pads[0]
            
            ic_x = pcbnew.ToMM(ic_pad.GetPosition().x)
            ic_y = pcbnew.ToMM(ic_pad.GetPosition().y)
            c_x = pcbnew.ToMM(c_pad.GetPosition().x)
            c_y = pcbnew.ToMM(c_pad.GetPosition().y)
            
            euclid = round(math.hypot(c_x - ic_x, c_y - ic_y), 2)
            manhattan = round(abs(c_x - ic_x) + abs(c_y - ic_y), 2)
            
            ic_cx = round(pcbnew.ToMM(ic_fp.GetPosition().x), 2)
            ic_cy = round(pcbnew.ToMM(ic_fp.GetPosition().y), 2)
            c_cx = round(pcbnew.ToMM(c_fp.GetPosition().x), 2)
            c_cy = round(pcbnew.ToMM(c_fp.GetPosition().y), 2)
            center_dist = round(math.hypot(c_cx - ic_cx, c_cy - ic_cy), 2)
            
            row = {
                'ic': ic_ref,
                'ic_pin': ic_pin,
                'ic_net': ic_net,
                'cap': c_ref,
                'cap_pin': c_pin,
                'cap_net': c_net,
                'euclidean_mm': euclid,
                'manhattan_mm': manhattan,
                'center_dist_mm': center_dist,
                'status': 'PASS' if euclid <= 12.0 else 'WARN'
            }
            decoupling_audit.append(row)
            print(f"  {ic_ref:3} Pin {ic_pin:2} <-> {c_ref:3} Pin {c_pin:1}: Pad Dist={euclid:5.2f} mm (Center={center_dist:5.2f} mm) -> {row['status']}")

    ac5_pass = all(item['status'] == 'PASS' for item in decoupling_audit)
    print(f"AC #5 Status: {'PASS' if ac5_pass else 'FAIL'}")

    # 7. AC #6: Mechanical and RF Anchors
    print("\n--- AC #6: MECHANICAL & RF ANCHORS ---")
    anchors_nominal = {
        'H1': {'x': 54.300, 'y': 73.480, 'rot': 0.0, 'layer': 'F.Cu'},
        'H2': {'x': 145.700, 'y': 73.480, 'rot': 0.0, 'layer': 'F.Cu'},
        'H3': {'x': 54.300, 'y': 126.520, 'rot': 0.0, 'layer': 'F.Cu'},
        'H4': {'x': 145.700, 'y': 126.520, 'rot': 0.0, 'layer': 'F.Cu'},
        'J7': {'x': 52.975, 'y': 88.500, 'rot': 270.0, 'layer': 'F.Cu'},
        'J8': {'x': 102.500, 'y': 79.610, 'rot': 0.0, 'layer': 'B.Cu'},
        'J9': {'x': 61.500, 'y': 104.000, 'rot': 270.0, 'layer': 'F.Cu'},
        'J3': {'x': 98.000, 'y': 109.300, 'rot': 90.0, 'layer': 'F.Cu'},
        'J4': {'x': 146.000, 'y': 104.000, 'rot': 90.0, 'layer': 'B.Cu'},
        'MECH_ENC': {'x': 54.300, 'y': 112.400, 'rot': 0.0, 'layer': 'F.Cu'},
        'U2': {'x': 77.920, 'y': 75.065, 'rot': 0.0, 'layer': 'F.Cu'}
    }
    
    anchors_audit = []
    max_dev = 0.0
    for ref, nom in anchors_nominal.items():
        fp = board.FindFootprintByReference(ref)
        if fp:
            cur_x = round(pcbnew.ToMM(fp.GetPosition().x), 3)
            cur_y = round(pcbnew.ToMM(fp.GetPosition().y), 3)
            cur_rot = round(fp.GetOrientation().AsDegrees() % 360, 1)
            cur_layer = fp.GetLayerName()
            
            dx = round(abs(cur_x - nom['x']), 3)
            dy = round(abs(cur_y - nom['y']), 3)
            drot = round(abs(cur_rot - nom['rot']), 1)
            total_dev = math.hypot(dx, dy)
            if total_dev > max_dev:
                max_dev = total_dev
            
            row = {
                'ref': ref,
                'nom_x': nom['x'],
                'nom_y': nom['y'],
                'nom_rot': nom['rot'],
                'cur_x': cur_x,
                'cur_y': cur_y,
                'cur_rot': cur_rot,
                'dx': dx,
                'dy': dy,
                'drot': drot,
                'total_dev_mm': round(total_dev, 4),
                'match': (total_dev == 0.0 and drot == 0.0 and cur_layer == nom['layer'])
            }
            anchors_audit.append(row)
            print(f"  {ref:10}: Cur=({cur_x:.3f}, {cur_y:.3f}, rot={cur_rot}) Nom=({nom['x']:.3f}, {nom['y']:.3f}, rot={nom['rot']}) -> Dev={total_dev:.4f} mm")
        else:
            print(f"  {ref:10}: NOT FOUND!")
            anchors_audit.append({'ref': ref, 'match': False, 'error': 'Not found'})

    ac6_pass = all(item['match'] for item in anchors_audit)
    print(f"AC #6 Status: {'PASS' if ac6_pass else 'FAIL'} (Max deviation: {max_dev:.4f} mm)")

    # 8. AC #7: KiCad 10 DRC & Schematic Parity
    print("\n--- AC #7: KICAD 10 DRC & SCHEMATIC PARITY ---")
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    drc_cmd = [kicad_cli, "pcb", "drc", "--schematic-parity", "-o", drc_rpt_path, pcb_path]
    print(f"Running command: {' '.join(drc_cmd)}")
    drc_proc = subprocess.run(drc_cmd, capture_output=True, text=True)
    
    # Parse report
    drc_violations_count = None
    unconnected_count = None
    footprint_errors_count = None
    schematic_parity_count = 0
    
    with open(drc_rpt_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "Found" in line and "DRC violations" in line:
                drc_violations_count = int(line.split()[2])
            elif "Found" in line and "unconnected pads" in line:
                unconnected_count = int(line.split()[2])
            elif "Found" in line and "Footprint errors" in line:
                footprint_errors_count = int(line.split()[2])
            elif "schematic_parity" in line or "schematic parity" in line:
                schematic_parity_count += 1

    print(f"DRC Violations:      {drc_violations_count} (baseline <= 165)")
    print(f"Unconnected Pads:    {unconnected_count} (baseline == 360)")
    print(f"Footprint Errors:    {footprint_errors_count} (must be 0)")
    print(f"Schematic Parity:    {schematic_parity_count} (must be 0)")
    
    ac7_pass = (
        drc_violations_count is not None and drc_violations_count <= 165 and
        unconnected_count == 360 and
        footprint_errors_count == 0 and
        schematic_parity_count == 0
    )
    print(f"AC #7 Status: {'PASS' if ac7_pass else 'FAIL'}")

    # Summary of All ACs
    all_acs = {
        'AC1_IPC7351_Courtyard': ac1_pass,
        'AC2_Passives_Grid_Lock': ac2_pass,
        'AC3_Linear_Rails_Pitch': ac3_pass,
        'AC4_Orthogonal_Rotations': ac4_pass,
        'AC5_Decoupling_Loops': ac5_pass,
        'AC6_Mechanical_Anchors': ac6_pass,
        'AC7_KiCad10_DRC_Parity': ac7_pass
    }
    
    all_pass = all(all_acs.values())
    print("\n==========================================")
    print("TASK-105 OVERALL AUDIT RESULT:", "PASS" if all_pass else "FAIL")
    for k, v in all_acs.items():
        print(f"  {k:25}: {'PASS' if v else 'FAIL'}")
    print("==========================================\n")

    # Save to JSON
    audit_data = {
        'metadata': {
            'task_id': 'TASK-105',
            'date': '2026-09-28',
            'kicad_version': '10.0.5',
            'pcb_file': pcb_path,
            'total_footprints': total_fps,
            'overall_result': 'PASS' if all_pass else 'FAIL'
        },
        'acceptance_criteria': all_acs,
        'inventory_summary': {cat: len(items) for cat, items in inventory.items()},
        'grid_audit': {
            'total_passives': len(sorted_passives),
            'on_0_50mm_grid': len(grid_050),
            'on_0_25mm_grid': len(grid_025),
            'off_grid': len(off_grid),
            'passives_list': sorted_passives
        },
        'rails_audit': rails,
        'rotations_audit': {
            'distribution': rot_histogram,
            'non_orthogonal_count': len(non_orthogonal),
            'pullup_uniformity': pullup_uniformity
        },
        'decoupling_audit': decoupling_audit,
        'anchors_audit': anchors_audit,
        'drc_parity_audit': {
            'drc_violations': drc_violations_count,
            'unconnected_pads': unconnected_count,
            'footprint_errors': footprint_errors_count,
            'schematic_parity_issues': schematic_parity_count
        }
    }
    
    out_json = 'scratch/audit_task104_compliance.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(audit_data, f, indent=2)
    print(f"Audit JSON written to: {out_json}")
    
    return audit_data

if __name__ == '__main__':
    run_compliance_audit()
