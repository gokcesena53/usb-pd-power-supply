import pcbnew
import math

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

def to_mm(val):
    return round(pcbnew.ToMM(val), 3)

# Let's inspect decoupling for each IC
# 1. U1 (AP33772S, B.Cu)
# 2. U2 (ESP32-C6, F.Cu)
# 3. U3 (INA226, B.Cu)
# 4. U4 (BQ32000, B.Cu)
# 5. U5 (AOZ1284PI, B.Cu)
# 6. U6 (LM4040, B.Cu)
# 7. U10 (USBLC6, F.Cu)
# 8. U11 (TPS55340, B.Cu)
# 9. U12 (LM74801, F.Cu)
# 10. U13 (74LVC1G08, B.Cu)

pairs = [
    ('U1', ['C1', 'C2', 'C3', 'C4', 'C8']),
    ('U2', ['C5', 'C6', 'C7', 'C10', 'C20', 'C21']),
    ('U3', ['C11']),
    ('U4', ['C9']),
    ('U5', ['C12', 'C13', 'C14', 'C17', 'C18', 'C19']),
    ('U10', ['C6']), # C6 is on +3.3V near U10?
    ('U11', ['C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29']),
    ('U12', ['C31', 'C32']),
    ('U13', ['C35']),
]

for u_ref, c_list in pairs:
    u_fp = board.FindFootprintByReference(u_ref)
    if not u_fp:
        continue
    u_pos = (to_mm(u_fp.GetPosition().x), to_mm(u_fp.GetPosition().y))
    print(f"\n==========================================")
    print(f"IC {u_ref} ({u_fp.GetLayerName()}) at {u_pos} rot={round(u_fp.GetOrientation().AsDegrees()%360,1)}")
    print(f"==========================================")
    
    # Print IC pads
    u_pads = {}
    for p in u_fp.Pads():
        p_pos = (to_mm(p.GetPosition().x), to_mm(p.GetPosition().y))
        u_pads[p.GetNumber()] = {'net': p.GetNetname(), 'pos': p_pos}
    
    for c_ref in c_list:
        c_fp = board.FindFootprintByReference(c_ref)
        if not c_fp:
            continue
        c_pos = (to_mm(c_fp.GetPosition().x), to_mm(c_fp.GetPosition().y))
        c_layer = c_fp.GetLayerName()
        c_val = c_fp.GetValue()
        c_pads = []
        for p in c_fp.Pads():
            c_pads.append({
                'num': p.GetNumber(),
                'net': p.GetNetname(),
                'pos': (to_mm(p.GetPosition().x), to_mm(p.GetPosition().y))
            })
        
        # Calculate distance between common net pads
        min_pwr_dist = 999999.0
        min_gnd_dist = 999999.0
        pwr_info = None
        gnd_info = None
        
        for cp in c_pads:
            c_net = cp['net']
            is_gnd = 'GND' in c_net
            for up_num, up in u_pads.items():
                if up['net'] == c_net and c_net != '':
                    d = math.hypot(cp['pos'][0] - up['pos'][0], cp['pos'][1] - up['pos'][1])
                    if is_gnd:
                        if d < min_gnd_dist:
                            min_gnd_dist = d
                            gnd_info = (cp['num'], up_num, c_net, round(d, 2))
                    else:
                        if d < min_pwr_dist:
                            min_pwr_dist = d
                            pwr_info = (cp['num'], up_num, c_net, round(d, 2))
        
        center_dist = round(math.hypot(c_pos[0] - u_pos[0], c_pos[1] - u_pos[1]), 2)
        same_layer = (c_layer == u_fp.GetLayerName())
        print(f"  {c_ref:4} ({c_val:6}) {c_layer:4} at {c_pos} rot={round(c_fp.GetOrientation().AsDegrees()%360,1):5} | CenterDist: {center_dist:5.2f} mm | SameLayer: {same_layer}")
        if pwr_info:
            print(f"       PWR Net: '{pwr_info[2]}' Pad {c_ref}.{pwr_info[0]} -> {u_ref}.{pwr_info[1]}: {pwr_info[3]} mm")
        if gnd_info:
            print(f"       GND Net: '{gnd_info[2]}' Pad {c_ref}.{gnd_info[0]} -> {u_ref}.{gnd_info[1]}: {gnd_info[3]} mm")
