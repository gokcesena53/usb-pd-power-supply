import pcbnew
import math

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

# Define each subcircuit block and the exact (IC, ic_pin, passive_ref, is_decoupling, passive_pin)
subcircuits = [
    # U6 Block
    {'ic': 'U6', 'pin': '2', 'ref': 'R50', 'decoupling': False, 'desc': 'U6 Cathode / EN_CTRL resistor'},
    {'ic': 'U6', 'pin': '1', 'ref': 'R51', 'decoupling': False, 'desc': 'U6 REF to GND resistor'},
    
    # U4 Block
    {'ic': 'U4', 'pin': '8', 'ref': 'C9', 'decoupling': True, 'c_pin': '1', 'desc': 'U4 VCC decoupling capacitor'},
    {'ic': 'U4', 'pin': '7', 'ref': 'R24', 'decoupling': False, 'desc': 'U4 RTC_INT pullup'},
    
    # U13 Block
    {'ic': 'U13', 'pin': '5', 'ref': 'C35', 'decoupling': True, 'c_pin': '1', 'desc': 'U13 VCC decoupling capacitor'},
    {'ic': 'U13', 'pin': '1', 'ref': 'R61', 'decoupling': False, 'desc': 'U13 OUT_EN pulldown'},
    
    # U3 Block
    {'ic': 'U3', 'pin': '6', 'ref': 'C11', 'decoupling': True, 'c_pin': '1', 'desc': 'U3 VS decoupling capacitor'},
    {'ic': 'U3', 'pin': '3', 'ref': 'R27', 'decoupling': False, 'desc': 'U3 INA_ALERT pullup'},
    
    # U12 Block
    {'ic': 'U12', 'pin': '10', 'ref': 'C32', 'decoupling': True, 'c_pin': '1', 'desc': 'U12 V_PRE decoupling capacitor'},
    {'ic': 'U12', 'pin': '11', 'ref': 'C31', 'decoupling': False, 'desc': 'U12 Charge pump CAP'},
    {'ic': 'U12', 'pin': '8', 'ref': 'R54', 'decoupling': False, 'desc': 'U12 GATE series resistor'},
    {'ic': 'U12', 'pin': '5', 'ref': 'R55', 'decoupling': False, 'desc': 'U12 OV_SENSE divider high'},
    {'ic': 'U12', 'pin': '5', 'ref': 'R56', 'decoupling': False, 'desc': 'U12 OV_SENSE divider low'},
    {'ic': 'U12', 'pin': '6', 'ref': 'R58', 'decoupling': False, 'desc': 'U12 SW_EN pulldown'},
    
    # U5 Block
    {'ic': 'U5', 'pin': '9', 'ref': 'C14', 'decoupling': True, 'c_pin': '1', 'desc': 'U5 VIN decoupling capacitor'},
    {'ic': 'U5', 'pin': '2', 'ref': 'C17', 'decoupling': False, 'desc': 'U5 BST bootstrap capacitor'},
    {'ic': 'U5', 'pin': '7', 'ref': 'C18', 'decoupling': True, 'c_pin': '1', 'desc': 'U5 SS soft start capacitor'},
    {'ic': 'U5', 'pin': '4', 'ref': 'R38', 'decoupling': False, 'desc': 'U5 FSW_SET resistor'},
    {'ic': 'U5', 'pin': '5', 'ref': 'R41', 'decoupling': False, 'desc': 'U5 COMP resistor'},
    {'ic': 'U5', 'pin': '6', 'ref': 'R39', 'decoupling': False, 'desc': 'U5 FB divider high'},
    {'ic': 'U5', 'pin': '6', 'ref': 'R40', 'decoupling': False, 'desc': 'U5 FB divider low'},
    
    # U11 Block
    {'ic': 'U11', 'pin': '3', 'ref': 'C26', 'decoupling': True, 'c_pin': '1', 'desc': 'U11 VIN decoupling capacitor'},
    {'ic': 'U11', 'pin': '5', 'ref': 'C23', 'decoupling': True, 'c_pin': '1', 'desc': 'U11 SS soft start capacitor'},
    {'ic': 'U11', 'pin': '10', 'ref': 'R47', 'decoupling': False, 'desc': 'U11 FREQ resistor'},
    {'ic': 'U11', 'pin': '8', 'ref': 'R52', 'decoupling': False, 'desc': 'U11 COMP resistor'},
    {'ic': 'U11', 'pin': '9', 'ref': 'R48', 'decoupling': False, 'desc': 'U11 FB divider high'},
    {'ic': 'U11', 'pin': '9', 'ref': 'R49', 'decoupling': False, 'desc': 'U11 FB divider low'},
    {'ic': 'U11', 'pin': '4', 'ref': 'R53', 'decoupling': False, 'desc': 'U11 EN pullup'},
    
    # U1 Block
    {'ic': 'U1', 'pin': '12', 'ref': 'C1', 'decoupling': True, 'c_pin': '1', 'desc': 'U1 V18 decoupling cap'},
    {'ic': 'U1', 'pin': '15', 'ref': 'C2', 'decoupling': True, 'c_pin': '1', 'desc': 'U1 IFB filter/decoupling cap'},
    {'ic': 'U1', 'pin': '20', 'ref': 'C4', 'decoupling': True, 'c_pin': '1', 'desc': 'U1 PD_5V decoupling cap'},
    {'ic': 'U1', 'pin': '22', 'ref': 'C8', 'decoupling': True, 'c_pin': '1', 'desc': 'U1 PD_VOUT decoupling cap'},
    {'ic': 'U1', 'pin': '11', 'ref': 'R21', 'decoupling': False, 'desc': 'U1 VSEL resistor'},
    {'ic': 'U1', 'pin': '8', 'ref': 'R14', 'decoupling': False, 'desc': 'U1 LED resistor'},
    {'ic': 'U1', 'pin': '23', 'ref': 'R12', 'decoupling': False, 'desc': 'U1 PWR_EN resistor'},
    {'ic': 'U1', 'pin': '22', 'ref': 'R13', 'decoupling': False, 'desc': 'U1 VOUT sense resistor'},
    {'ic': 'U1', 'pin': '9', 'ref': 'R8', 'decoupling': False, 'desc': 'U1 PD_INT_5V pullup'},
    
    # U10 Block
    {'ic': 'U10', 'pin': '6', 'ref': 'R2', 'decoupling': False, 'desc': 'USB DM series'},
    {'ic': 'U10', 'pin': '4', 'ref': 'R3', 'decoupling': False, 'desc': 'USB DP series'},
    
    # U2 Block
    {'ic': 'U2', 'pin': '3', 'ref': 'C6', 'decoupling': True, 'c_pin': '1', 'desc': 'U2 +3.3V decoupling cap'},
    {'ic': 'U2', 'pin': '8', 'ref': 'C7', 'decoupling': False, 'desc': 'U2 EN delay cap'},
    {'ic': 'U2', 'pin': '8', 'ref': 'R1', 'decoupling': False, 'desc': 'U2 EN pullup'},
    {'ic': 'U2', 'pin': '23', 'ref': 'R10', 'decoupling': False, 'desc': 'U2 IO9 boot pullup'},
    {'ic': 'U2', 'pin': '22', 'ref': 'R15', 'decoupling': False, 'desc': 'U2 IO8 CFG0 series'},
    {'ic': 'U2', 'pin': '12', 'ref': 'R16', 'decoupling': False, 'desc': 'U2 IO0 ETH_PWR_EN series'},
    {'ic': 'U2', 'pin': '22', 'ref': 'R37', 'decoupling': False, 'desc': 'U2 IO8 pullup'},
]

print("Scanning subcircuits...")
results = []
for sc in subcircuits:
    ic_ref = sc['ic']
    ic_pin = sc['pin']
    p_ref = sc['ref']
    is_dec = sc['decoupling']
    
    u_fp = board.FindFootprintByReference(ic_ref)
    p_fp = board.FindFootprintByReference(p_ref)
    
    u_pad = [p for p in u_fp.Pads() if p.GetNumber() == ic_pin][0]
    ux = pcbnew.ToMM(u_pad.GetPosition().x)
    uy = pcbnew.ToMM(u_pad.GetPosition().y)
    
    px = pcbnew.ToMM(p_fp.GetPosition().x)
    py = pcbnew.ToMM(p_fp.GetPosition().y)
    prot = p_fp.GetOrientation().AsDegrees() % 360
    
    center_dist = math.hypot(px - ux, py - uy)
    
    # pad dist
    pad_dists = []
    for pad in p_fp.Pads():
        pax = pcbnew.ToMM(pad.GetPosition().x)
        pay = pcbnew.ToMM(pad.GetPosition().y)
        d = math.hypot(pax - ux, pay - uy)
        pad_dists.append((pad.GetNumber(), d, pad.GetNetname()))
        
    pad_dists.sort(key=lambda x: x[1])
    min_pad_dist = pad_dists[0][1]
    closest_pad_num = pad_dists[0][0]
    
    violation = False
    reasons = []
    if center_dist > 2.0:
        violation = True
        reasons.append(f"center_dist={center_dist:.3f}mm > 2.0mm")
    if is_dec and min_pad_dist > 1.2:
        violation = True
        reasons.append(f"decoupling pad_dist={min_pad_dist:.3f}mm > 1.2mm")
        
    row = {
        'block': ic_ref,
        'ic_pin': ic_pin,
        'passive': p_ref,
        'decoupling': is_dec,
        'center_dist': round(center_dist, 3),
        'min_pad_dist': round(min_pad_dist, 3),
        'closest_pad': closest_pad_num,
        'pos': (round(px, 3), round(py, 3)),
        'ic_pos': (round(ux, 3), round(uy, 3)),
        'rot': prot,
        'layer': p_fp.GetLayerName(),
        'violation': violation,
        'reasons': reasons,
        'desc': sc['desc']
    }
    results.append(row)
    
print(f"Total surveyed: {len(results)}")
violations = [r for r in results if r['violation']]
print(f"Total violations: {len(violations)}")
for v in violations:
    print(f"  {v['block']}-{v['passive']:4} (pin {v['ic_pin']:2}): {', '.join(v['reasons'])} [cur pos {v['pos']}]")
