#!/usr/bin/env python3
"""
TASK-106: CRITICAL / Force Full-Pass Placement Optimization & Congestion Fix
Script: scratch/repack_engine.py
KiCad Python: KiCad 10.0.5 pcbnew
"""

import os
import sys
import json
import math
import shutil
import subprocess
from collections import defaultdict
import pcbnew

def ToMM(val):
    return pcbnew.ToMM(val)

def FromMM(val):
    return pcbnew.FromMM(val)

def get_fp_data(fp):
    pos = fp.GetPosition()
    rot = round(fp.GetOrientation().AsDegrees() % 360, 2)
    pads = []
    for p in fp.Pads():
        ppos = p.GetPosition()
        pads.append({
            'num': p.GetNumber(),
            'net': p.GetNetname(),
            'pos': (round(ToMM(ppos.x), 3), round(ToMM(ppos.y), 3))
        })
    return {
        'ref': fp.GetReference(),
        'val': fp.GetValue(),
        'layer': fp.GetLayerName(),
        'pos': (round(ToMM(pos.x), 3), round(ToMM(pos.y), 3)),
        'rot': rot,
        'pads': pads,
        'fpid': fp.GetFPID().GetLibItemName()
    }

def run_repack():
    pcb_path = 'hardware/gopo.kicad_pcb'
    print(f"Loading PCB from {pcb_path}")
    board = pcbnew.LoadBoard(pcb_path)
    
    # Target decoupling caps and their IC pins
    decoupling_definitions = [
        ('U1', '12', 'Net-(U1-V18)', 'C1', '1', 'U1 V18 Decoupling (1.8V Core)'),
        ('U1', '15', 'Net-(U1-IFB)', 'C2', '1', 'U1 IFB Filter / Decoupling'),
        ('U1', '20', 'PD_5V', 'C4', '1', 'U1 V5V Decoupling (5V Internal Rail)'),
        ('U1', '19', 'PD_VOUT', 'C8', '1', 'U1 VOUT Decoupling'),
        ('U2', '3', '+3.3V', 'C6', '1', 'U2 VDD Decoupling (+3.3V)'),
        ('U3', '6', '+3.3V', 'C11', '1', 'U3 VS Decoupling (+3.3V)'),
        ('U4', '8', '+3.3V', 'C9', '1', 'U4 VCC Decoupling (+3.3V)'),
        ('U5', '9', 'V_PRE', 'C14', '1', 'U5 VIN Decoupling (High Freq)'),
        ('U5', '7', '/USB_PD_CONTROLLER/SS_RAMP', 'C18', '1', 'U5 SS Decoupling / Ramp'),
        ('U11', '3', 'PD_VOUT', 'C26', '1', 'U11 VIN Decoupling'),
        ('U11', '5', 'Net-(U11-SS)', 'C23', '1', 'U11 SS Decoupling'),
        ('U12', '10', 'V_PRE', 'C32', '1', 'U12 V_PRE Decoupling'),
        ('U13', '5', '+3.3V', 'C35', '1', 'U13 VCC Decoupling (+3.3V)'),
    ]
    decoupling_map = {d[3]: d for d in decoupling_definitions}

    # Signal passives connected to ICs
    # We want to tightly repack passives to their ICs
    # Candidate moves based on precise geometric analysis
    
    repack_targets = {
        # --- U6 Block (TLV431 SOT-23 at 108.435, 105.000 B.Cu) ---
        # pin 1: Net-(U6-REF) at (107.485, 104.062)
        # pin 2: /USB_PD_CONTROLLER/EN_CTRL at (109.385, 104.062)
        # pin 3: GND at (108.435, 105.938)
        # R50 connects pin 2 & pin 1; R51 connects pin 1 & pin 3
        # North is open. R50 at (109.385, 102.500), R51 at (107.485, 102.500)
        'R50': {'x': 109.385, 'y': 102.500, 'rot': 180.0, 'ic': 'U6', 'pin': '2'},
        'R51': {'x': 107.485, 'y': 102.500, 'rot': 0.0, 'ic': 'U6', 'pin': '1'},
        
        # --- U4 Block (BQ32000 SOIC-8 at 143.000, 82.000 B.Cu) ---
        # pin 8: +3.3V at (140.525, 80.095)
        # pin 7: /MCU/RTC_INT at (140.525, 81.365)
        # C9 rot=0 at Y=78.800: center dist 1.295mm, pad1 dist 1.38mm.
        # Let's check west side or north side
        'C9': {'x': 140.525, 'y': 78.800, 'rot': 0.0, 'ic': 'U4', 'pin': '8'},
        'R24': {'x': 137.500, 'y': 81.365, 'rot': 0.0, 'ic': 'U4', 'pin': '7'},
        
        # --- U13 Block (74LVC1G08 SOT-23-5 at 129.000, 123.100 B.Cu) ---
        # pin 5: +3.3V at (130.137, 124.050)
        # pin 1: OUT_EN at (127.862, 124.050)
        'C35': {'x': 131.750, 'y': 124.050, 'rot': 180.0, 'ic': 'U13', 'pin': '5'},
        'R61': {'x': 126.250, 'y': 124.050, 'rot': 0.0, 'ic': 'U13', 'pin': '1'},
        
        # --- U3 Block (INA226 TSSOP-10 at 136.750, 112.100 B.Cu) ---
        # pin 6: +3.3V at (137.750, 114.250)
        # pin 3: INA_ALERT at (136.750, 109.950)
        'C11': {'x': 139.750, 'y': 114.250, 'rot': 180.0, 'ic': 'U3', 'pin': '6'},
        'R27': {'x': 136.750, 'y': 108.000, 'rot': 90.0, 'ic': 'U3', 'pin': '3'},
        
        # --- U12 Block (LM74801 WSON-12 at 135.500, 101.500 F.Cu) ---
        # pin 10: V_PRE at (136.938, 101.250)
        # pin 11: Net-(U12-CAP) at (136.938, 100.750)
        'C32': {'x': 138.500, 'y': 101.500, 'rot': 180.0, 'ic': 'U12', 'pin': '10'},
        'C31': {'x': 138.500, 'y': 100.000, 'rot': 180.0, 'ic': 'U12', 'pin': '11'},
        
        # --- U5 Block (AOZ1284PI SOIC-8-EP at 126.700, 105.310 B.Cu) ---
        # pin 2: BST at (129.202, 104.675)
        # pin 4: FSW_SET at (129.202, 107.215)
        # pin 7: SS_RAMP at (124.198, 104.675)
        # pin 5: COMP_NODE at (124.198, 107.215)
        # pin 6: FB_3V3 at (124.198, 105.945)
        'C17': {'x': 131.250, 'y': 104.675, 'rot': 180.0, 'ic': 'U5', 'pin': '2'},
        'R38': {'x': 131.250, 'y': 107.215, 'rot': 0.0, 'ic': 'U5', 'pin': '4'},
        'C18': {'x': 122.250, 'y': 104.675, 'rot': 180.0, 'ic': 'U5', 'pin': '7'},
        'R41': {'x': 122.250, 'y': 107.215, 'rot': 0.0, 'ic': 'U5', 'pin': '5'},
        
        # --- U11 Block (TPS55340 HTSSOP-14 at 98.000, 121.000 B.Cu) ---
        # pin 3: PD_VOUT at (100.862, 120.350)
        # pin 5: SS at (100.862, 121.650)
        # pin 8: COMP at (95.137, 122.950)
        # pin 10: FREQ at (95.137, 121.650)
        'C26': {'x': 102.750, 'y': 120.350, 'rot': 180.0, 'ic': 'U11', 'pin': '3'},
        'C23': {'x': 102.750, 'y': 122.000, 'rot': 180.0, 'ic': 'U11', 'pin': '5'},
        'R47': {'x': 93.250, 'y': 121.650, 'rot': 0.0, 'ic': 'U11', 'pin': '10'},
        'R52': {'x': 93.250, 'y': 123.000, 'rot': 0.0, 'ic': 'U11', 'pin': '8'},
        
        # --- U1 Block (AP33772S WQFN-24 at 76.500, 120.500 B.Cu) ---
        # pin 12: V18 at (75.250, 122.463)
        # pin 15: IFB at (74.537, 120.750)
        # pin 20: PD_5V at (75.750, 118.537)
        # pin 11: VSEL at (75.750, 122.463)
        # pin 23: PWR_EN at (77.250, 118.537)
        'C1': {'x': 75.250, 'y': 124.000, 'rot': 90.0, 'ic': 'U1', 'pin': '12'},
        'C2': {'x': 73.000, 'y': 120.750, 'rot': 0.0, 'ic': 'U1', 'pin': '15'},
        'C4': {'x': 75.750, 'y': 117.000, 'rot': 90.0, 'ic': 'U1', 'pin': '20'},
        'R21': {'x': 76.500, 'y': 124.000, 'rot': 90.0, 'ic': 'U1', 'pin': '11'},
        'R12': {'x': 77.250, 'y': 117.000, 'rot': 90.0, 'ic': 'U1', 'pin': '23'},
        
        # --- U10 Block (USBLC6-2SC6 SOT-23-6 at 61.500, 88.500 F.Cu) ---
        'R2': {'x': 64.000, 'y': 87.550, 'rot': 0.0, 'ic': 'U10', 'pin': '6'},
        'R3': {'x': 64.000, 'y': 89.450, 'rot': 0.0, 'ic': 'U10', 'pin': '4'},
    }
    
    return repack_targets

if __name__ == '__main__':
    repack_targets = run_repack()
    print(f"Total defined repack targets: {len(repack_targets)}")
    for ref, t in sorted(repack_targets.items()):
        print(f"  {t['ic']}-{ref:4} (pin {t['pin']:2}): -> ({t['x']:7.3f}, {t['y']:7.3f}) rot={t['rot']}")
