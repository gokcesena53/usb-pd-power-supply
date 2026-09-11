from pathlib import Path
import copy

exec(Path('reports/output-update/update_schematic.py').read_text(encoding='utf8').split('exceptions=')[0])

a = Sch('usb_c_input.kicad_sch')

# The 5.5 V TPD4E05U06 channels are retained for USB2 D+/D- only.
# CC1/CC2 must preserve the AP33772S 34 V short-to-VBUS tolerance, so remove
# the low-voltage shunts and use 28 V bidirectional TVS devices instead.
remove_uuids = {
    '0c0874f0-4125-4601-a07a-8ce18ce82723',
    '1012c9d2-5fbd-443c-b2a4-3a63f8c2b7be',
    'a4f165cf-2da2-445c-855d-dd8157360e6a',
    '2bd7de34-ec35-4474-853f-66c0a5b1c2e2',
}
a.t[:] = [z for z in a.t if not (isinstance(z, list) and any(tag(v) == 'uuid' and v[1] in remove_uuids for v in z if isinstance(v, list)))]

for x, y in [(200.66, 96.52), (200.66, 101.6)]:
    a.add(f'(no_connect (at {x} {y}) (uuid "{uid()}"))')

d3 = a.sym('D3')

def add_cc_tvs(ref, y, net):
    d = copy.deepcopy(d3)
    one(d, 'at')[1:] = [190.5, y, 0]
    for v in walk(d):
        if tag(v) == 'uuid':
            v[1] = uid()
        if tag(v) == 'reference':
            v[1] = ref
    field(d, 'Reference', ref)
    field(d, 'Value', 'AQ3130E-01ETG (bidirectional)')
    field(d, 'Description', f'28V bidirectional low-capacitance TVS diode for USB-C {net} ESD protection')
    field(d, 'DesignNote', f'Connect directly from {net} to GND at J1; shortest low-inductance return')
    one(prop(d, 'Reference'), 'at')[1:] = [195.58, y - 2.54, 0]
    one(prop(d, 'Value'), 'at')[1:] = [195.58, y + 2.54, 0]
    for p in all(d, 'property'):
        if p[1] not in ['Reference', 'Value']:
            one(p, 'at')[1:] = [195.58, y, 0]
    a.t.append(d)
    a.wire(179.07, y, 186.69, y)
    a.label(net, 179.07, y, True, 180)
    a.wire(194.31, y, 199.39, y)

add_cc_tvs('D4', 116.84, 'USB_CC1')
add_cc_tvs('D5', 124.46, 'USB_CC2')
a.wire(199.39, 116.84, 199.39, 129.54)

g = copy.deepcopy(next(z for z in all(a.t, 'symbol') if prop(z, 'Reference')[2] == '#PWR229'))
one(g, 'at')[1:] = [199.39, 129.54, 0]
for v in walk(g):
    if tag(v) == 'uuid':
        v[1] = uid()
    if tag(v) == 'reference':
        v[1] = '#PWR230'
field(g, 'Reference', '#PWR230')
a.t.append(g)

for z in all(a.t, 'text'):
    if 'USB PORT ESD' in z[1]:
        z[1] = ('USB PORT ESD\n'
                'U9: D+/D-; IEC 12kV contact, 15kV air.\n'
                'D4/D5: CC1/CC2, 28V VRWM; IEC 30kV contact/air.\n'
                'D3: 28V VBUS TVS; IEC 30kV contact/air.\n'
                'Place directly behind J1; shortest GND return.')
        one(z, 'at')[1:] = [182.88, 137.16, 0]
    if 'VBUS LIMIT' in z[1]:
        one(z, 'at')[1:] = [182.88, 160.02, 0]

a.save()
print('CC1/CC2 moved to 28 V TVS protection; U9 now protects USB2 D+/D- only')
