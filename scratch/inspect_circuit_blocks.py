import json
import math

with open('scratch/task104_detailed_passives.json', 'r') as f:
    data = json.load(f)

passives = data['passives']
ics = data['ics']
crtyds = data['courtyards']

# Define circuit blocks and their components
blocks = {
    'U1_AP33772S': {
        'ic': 'U1',
        'passives': ['C1', 'C2', 'C3', 'C4', 'C8', 'R8', 'R9', 'R11', 'R14', 'R21', 'R64', 'R65'],
        'layer': 'B.Cu'
    },
    'U2_ESP32_C6_DIGITAL': {
        'ic': 'U2',
        'passives': ['C5', 'C6', 'C7', 'C9', 'C10', 'C20', 'C21', 'C33', 'R4', 'R5', 'R6', 'R7', 'R10', 'R15', 'R16', 'R17', 'R37'],
        'layer': 'F.Cu & B.Cu'
    },
    'U11_BOOST': {
        'ic': 'U11',
        'passives': ['C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'R47', 'R48', 'R49', 'R50', 'R51', 'R52', 'R53'],
        'layer': 'B.Cu'
    },
    'U5_BUCK': {
        'ic': 'U5',
        'passives': ['C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C30', 'R38', 'R40', 'R41', 'R54'],
        'layer': 'B.Cu'
    },
    'U12_IDEAL_DIODE': {
        'ic': 'U12',
        'passives': ['C31', 'C32', 'R30', 'R31', 'R32', 'R33'],
        'layer': 'F.Cu'
    },
    'U3_INA226_OUTPUT': {
        'ic': 'U3',
        'passives': ['C11', 'R22', 'R23', 'R24', 'R25'],
        'layer': 'B.Cu'
    },
    'U13_LOGIC_DISCHARGE': {
        'ic': 'U13',
        'passives': ['C35', 'R55', 'R56', 'R57', 'R58', 'R59'],
        'layer': 'B.Cu'
    },
    'ENCODER_USB_UI': {
        'ic': 'U10',
        'passives': ['R1', 'R2', 'R3', 'R18', 'R19', 'R20', 'R26', 'R27', 'R28', 'R29', 'R34', 'R35', 'R36', 'R60', 'R61', 'R62', 'R63', 'C34'],
        'layer': 'Various'
    }
}

print("=== CIRCUIT BLOCK COMPONENT POSITIONS & ORIENTATIONS ===")
for bname, bdata in blocks.items():
    print(f"\n--- {bname} ---")
    u_ref = bdata['ic']
    if u_ref in ics:
        u_info = ics[u_ref]
        print(f"  IC {u_ref} ({u_info['layer']}) at {u_info['pos']} rot={u_info['rot']}")
    for r in sorted(bdata['passives']):
        if r in passives:
            p = passives[r]
            # check courtyard
            c_box = crtyds.get(r, {})
            c_w = c_box.get('width', '-')
            c_h = c_box.get('height', '-')
            print(f"  {r:6} {p['val']:10} {p['footprint']:25} {p['layer']:4} pos=({p['pos'][0]:6.3f}, {p['pos'][1]:6.3f}) rot={p['rot']:5.1f} crtyd=({c_w}x{c_h})")

