from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[2]
report = Path(__file__).resolve().parent
new = ET.parse(report / 'after-final.xml')
old = ET.parse(report / 'before-final.xml')

def refs(tree):
    return {c.attrib['ref'] for c in tree.findall('.//components/comp')}

def groups(tree, keep):
    result = set()
    for net in tree.findall('.//nets/net'):
        nodes = frozenset((n.attrib['ref'], n.attrib['pin']) for n in net.findall('node') if n.attrib['ref'] in keep)
        if nodes:
            result.add(nodes)
    return result

old_refs = refs(old)
new_refs = refs(new)
assert new_refs - old_refs == {'D3', 'D4', 'D5', 'U9'}, (new_refs - old_refs)
assert old_refs - new_refs == set(), (old_refs - new_refs)
assert groups(old, old_refs) == groups(new, old_refs), 'Existing component connectivity changed'

pin_net = {}
for net in new.findall('.//nets/net'):
    name = net.attrib['name']
    for node in net.findall('node'):
        pin_net[(node.attrib['ref'], node.attrib['pin'])] = name

expected = {
    ('U9', '1'): 'USB_DP', ('U9', '2'): 'USB_DM',
    ('U9', '3'): 'GND', ('U9', '8'): 'GND',
    ('D3', '1'): 'GND', ('D3', '2'): 'USB_VBUS',
    ('D4', '1'): 'USB_CC1', ('D4', '2'): 'GND',
    ('D5', '1'): 'USB_CC2', ('D5', '2'): 'GND',
}
for key, value in expected.items():
    assert pin_net.get(key) == value, (key, pin_net.get(key), value)

for pin in ('4', '5', '6', '7', '9', '10'):
    assert pin_net.get(('U9', pin), '').startswith('unconnected-'), (pin, pin_net.get(('U9', pin)))

fp = (root / 'USB_ESD.pretty' / 'antmicro_tpd4e05u06qdqarq1.kicad_mod').read_text(encoding='utf8')
pads = sorted(set(re.findall(r'\(pad "(\d+)" ', fp)), key=int)
assert pads == [str(i) for i in range(1, 11)], pads

sym = (root / 'USB_ESD.kicad_sym').read_text(encoding='utf8')
for number, name in [('1','D1+'),('2','D1-'),('3','GND'),('4','D2+'),('5','D2-'),('6','NC'),('7','NC'),('8','GND'),('9','NC'),('10','NC')]:
    pattern = rf'\(name "{re.escape(name)}".*?\(number "{number}"'
    assert re.search(pattern, sym, re.S), (number, name)

erc = (report / 'erc-final.rpt').read_text(encoding='utf8')
assert '** ERC messages: 0  Errors 0  Warnings 0' in erc

print('PASS: Added refs D3/D4/D5/U9 only')
print('PASS: Existing component connectivity unchanged')
print('PASS: D+/D-, CC1/CC2 and VBUS ESD pin-to-net mapping')
print('PASS: U9 symbol pin table and 10-pad footprint')
print('PASS: ERC 0 errors, 0 warnings')
