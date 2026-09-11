from pathlib import Path
import csv
import json
import re
import xml.etree.ElementTree as ET

base = Path(__file__).resolve().parents[2]
out = Path(__file__).resolve().parent
tree = ET.parse(out / 'project-final.xml')

components = {c.attrib['ref']: c for c in tree.findall('.//components/comp')}
libparts = {}
for part in tree.findall('.//libparts/libpart'):
    key = (part.attrib.get('lib'), part.attrib.get('part'))
    libparts[key] = {
        p.attrib['num']: (p.attrib.get('name', ''), p.attrib.get('type', ''))
        for p in part.findall('./pins/pin')
    }

pin_net = {}
net_nodes = {}
for net in tree.findall('.//nets/net'):
    name = net.attrib['name']
    nodes = [(n.attrib['ref'], n.attrib['pin']) for n in net.findall('node')]
    net_nodes[name] = nodes
    for node in nodes:
        pin_net[node] = name

expected = {
    # USB-C and ESD
    ('J1','A4'):'USB_VBUS', ('J1','A9'):'USB_VBUS', ('J1','B4'):'USB_VBUS', ('J1','B9'):'USB_VBUS',
    ('J1','A5'):'USB_CC1', ('J1','B5'):'USB_CC2',
    ('J1','A6'):'USB_DP', ('J1','B6'):'USB_DP', ('J1','A7'):'USB_DM', ('J1','B7'):'USB_DM',
    ('U9','1'):'USB_DP', ('U9','2'):'USB_DM', ('U9','3'):'GND', ('U9','8'):'GND',
    ('D3','1'):'GND', ('D3','2'):'USB_VBUS', ('D4','1'):'USB_CC1', ('D4','2'):'GND',
    ('D5','1'):'USB_CC2', ('D5','2'):'GND',
    # PD controller and main power path
    ('U1','1'):'USB_VBUS', ('U1','24'):'PD_VBUS_SENSED', ('U1','16'):'USB_CC2', ('U1','17'):'USB_CC1',
    ('U1','22'):'Net-(U1-VOUT)', ('U1','23'):'Net-(U1-PWR_EN)', ('U1','3'):'GND', ('U1','25'):'GND',
    ('R11','1'):'USB_VBUS', ('R11','2'):'PD_VBUS_SENSED',
    ('Q4','5'):'PD_VBUS_SENSED', ('Q3','5'):'PD_VOUT', ('Q3','4'):'/USB_PD_CONTROLLER/PD_GATE', ('Q4','4'):'/USB_PD_CONTROLLER/PD_GATE',
    # 3.3 V buck
    ('U5','1'):'/POWER GENERATION/LX_SW', ('U5','2'):'Net-(U5-BST)', ('U5','3'):'GND',
    ('U5','4'):'/POWER GENERATION/FSW_SET', ('U5','5'):'/POWER GENERATION/COMP_NODE',
    ('U5','6'):'/POWER GENERATION/FB_3V3', ('U5','7'):'/POWER GENERATION/SS_RAMP',
    ('U5','8'):'/POWER GENERATION/EN_CTRL', ('U5','9'):'PD_VOUT',
    ('D2','1'):'/POWER GENERATION/LX_SW', ('D2','2'):'GND', ('L1','1'):'/POWER GENERATION/LX_SW', ('L1','2'):'+3.3V',
    # Current and voltage measurement
    ('RShunt','1'):'PD_VOUT', ('RShunt','2'):'OUT_POS',
    ('U3','10'):'PD_VOUT', ('U3','9'):'OUT_POS', ('U3','8'):'OUT_POS', ('U3','6'):'+3.3V', ('U3','7'):'GND',
    # MCU, RTC and encoder
    ('U2','2'):'+3.3V', ('U2','1'):'GND', ('U2','28'):'GND', ('U2','29'):'GND',
    ('U4','7'):'+3.3V', ('U4','5'):'GND', ('U4','6'):'Net-(U4-VBACKUP)',
    ('SW3','1'):'ENCODER_A', ('SW3','2'):'GND', ('SW3','3'):'ENCODER_B', ('SW3','4'):'ENCODER_SW', ('SW3','5'):'GND',
    # Backlight
    ('U7','2'):'+3.3V', ('U7','3'):'+3.3V', ('U7','4'):'GND',
    ('U7','5'):'/USER INTERFACE/BL_BOOST_SW', ('U7','6'):'BACKLIGHT_4V2',
    ('L2','1'):'+3.3V', ('L2','2'):'/USER INTERFACE/BL_BOOST_SW',
    ('R28','1'):'TFT_BL_PWM', ('R28','2'):'Net-(U8-EN_PWM)',
    ('R29','1'):'Net-(U8-EN_PWM)', ('R29','2'):'GND',
    ('U8','5'):'GND', ('U8','6'):'Net-(U8-EN_PWM)', ('U8','7'):'BACKLIGHT_4V2',
    ('J3','34'):'/USER INTERFACE/BL_K1', ('J3','35'):'/USER INTERFACE/BL_K2',
    ('J3','36'):'/USER INTERFACE/BL_K3', ('J3','37'):'/USER INTERFACE/BL_K4', ('J3','38'):'BACKLIGHT_4V2',
    # Output connectors
    ('J4','1'):'OUT_POS', ('J4','2'):'GND', ('J5','1'):'OUT_POS', ('J6','1'):'GND',
}

failures = []
for key, wanted in expected.items():
    actual = pin_net.get(key)
    if actual != wanted:
        failures.append({'pin': f'{key[0]}.{key[1]}', 'expected': wanted, 'actual': actual})

missing_pin_nets = []
rows = []
for ref, comp in sorted(components.items()):
    source = comp.find('libsource')
    key = (source.attrib.get('lib'), source.attrib.get('part'))
    sheet = comp.find('./sheetpath').attrib.get('names', '/')
    footprint = comp.findtext('footprint', '')
    for number, (name, etype) in sorted(libparts.get(key, {}).items(), key=lambda item: (len(item[0]), item[0])):
        net = pin_net.get((ref, number), '')
        if not net:
            missing_pin_nets.append(f'{ref}.{number}')
        rows.append([sheet, ref, comp.findtext('value',''), number, name, etype, net, footprint])

with (out / 'all-pin-connections.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['Sheet','Reference','Value','Pin','Pin name','Electrical type','Net','Footprint'])
    w.writerows(rows)

missing_footprints = []
for ref, comp in sorted(components.items()):
    if not comp.findtext('footprint', '').strip():
        missing_footprints.append({'ref': ref, 'value': comp.findtext('value','')})

single_node = [name for name, nodes in net_nodes.items() if len(nodes) == 1 and not name.startswith('unconnected-')]
unconnected = sorted((ref, pin, net) for (ref,pin),net in pin_net.items() if net.startswith('unconnected-'))

direction_rows = []
for path in sorted(base.glob('*.kicad_sch')):
    text = path.read_text(encoding='utf8')
    for name, shape in re.findall(r'\(global_label "([^"]+)"\s+\(shape ([^)]+)\)', text, re.S):
        direction_rows.append([path.name, name, shape])
with (out / 'global-label-directions.csv').open('w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f); w.writerow(['Sheet file','Global label','Direction']); w.writerows(direction_rows)

assert not failures, failures
assert not missing_pin_nets, missing_pin_nets
assert not single_node, single_node
assert components['RShunt'].findtext('footprint') == 'Resistor_SMD:R_2512_6332Metric'

result = {
    'component_count': len(components),
    'pin_count': len(rows),
    'net_count': len(net_nodes),
    'critical_pin_checks': len(expected),
    'critical_failures': failures,
    'pins_without_net': missing_pin_nets,
    'nonintentional_single_node_nets': single_node,
    'intentional_unconnected_pin_count': len(unconnected),
    'missing_footprints': missing_footprints,
    'global_label_instances_checked': len(direction_rows),
    'rshunt_footprint': components['RShunt'].findtext('footprint'),
}
(out / 'audit-summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf8')
print(json.dumps(result, indent=2, ensure_ascii=False))
