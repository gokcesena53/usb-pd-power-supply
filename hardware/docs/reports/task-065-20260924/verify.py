"""Verify saved TASK-065 board against the pre-change snapshot (KiCad Python)."""
import json
import hashlib
from collections import Counter
import pcbnew as p
from audit import HERE, BOARD, save, outline

before = json.loads((HERE/'inventory-before.json').read_text(encoding='utf-8'))
after = json.loads((HERE/'inventory-after.json').read_text(encoding='utf-8'))
assert hashlib.sha256(BOARD.read_bytes()).hexdigest()==after['sha256'], 'Refresh saved-board inventory first'
old = {f['ref']: f for f in before['footprints']}
new = {f['ref']: f for f in after['footprints']}
assert old.keys() == new.keys()
for ref in old:
    for field in ['uuid','pads','group','locked','value','footprint']:
        assert old[ref][field] == new[ref][field], (ref, field)
for ref in ['J3', 'J9', 'H1', 'H2', 'H3', 'H4']:
    for field in ['xy','angle','side','locked']:
        assert old[ref][field] == new[ref][field], (ref, field)
assert 'SW3' not in new and 'BT1' not in new
assert before['zones'] == after['zones'] == 0
assert {t['uuid'] for t in before['tracks']} == {t['uuid'] for t in after['tracks']}
for t in after['tracks']:
    prev = next(v for v in before['tracks'] if v['uuid'] == t['uuid'])
    assert t['net'] == prev['net'] and t['width'] == prev['width']
    assert t['side'] == 'B.Cu'

heights = json.loads((HERE/'heights-after.json').read_text(encoding='utf-8'))
assert all(not r['model_status'].startswith('MISSING') for r in heights)
assert not [r for r in heights if r['lcd_overlap'] and r['top_projection_mm']>2.0001]
assert not [r for r in heights if r['lcd_overlap'] and r['ref']!='J3' and r['top_projection_mm']>1.8001]
assert [r['ref'] for r in heights if r['side']=='F.Cu' and r['height_mm']>2.0001] == ['J9']
assert next(r for r in heights if r['ref']=='J9')['lcd_overlap'] is False

blocks = {}
for name, side in [('TPS55340 PRE-BOOST','B.Cu'), ('AOZ1284 3.3V BUCK','B.Cu'),
                   ('TFT BACKLIGHT (3.3V + PWM)','F.Cu')]:
    members = [r['ref'] for r in after['footprints'] if r['group']==name]
    assert members and all(new[ref]['side']==side for ref in members)
    blocks[name] = dict(side=side, refs=members)

b = p.LoadBoard(str(BOARD))
assert outline(b) == before['edge_cuts'] == after['edge_cuts']
fps = {f.GetReference():f for f in b.GetFootprints()}
getpad = lambda ref,num: next(a for a in fps[ref].Pads() if a.GetNumber()==num)
start,end = getpad('D5','2'),getpad('U11','9')
edges = {}
for t in b.GetTracks():
    assert t.GetNetname()==start.GetNetname()==end.GetNetname()
    a,c = tuple(t.GetStart()),tuple(t.GetEnd())
    edges.setdefault(a,[]).append(c);edges.setdefault(c,[]).append(a)
seen,queue = set(),[tuple(start.GetPosition())]
while queue:
    q=queue.pop()
    if q in seen: continue
    seen.add(q);queue.extend(edges.get(q,[]))
assert tuple(end.GetPosition()) in seen
fb_length = sum(p.ToMM(t.GetLength()) for t in b.GetTracks())
assert fb_length<=10

dr0=json.loads((HERE/'drc-before.json').read_text())
dr1=json.loads((HERE/'drc-after.json').read_text())
key=lambda x:(x['type'],tuple(sorted(i['uuid'] for i in x.get('items',[]))))
added=set(map(key,dr1['violations']))-set(map(key,dr0['violations']))
assert not added, added
assert not dr1['schematic_parity']
counts=Counter(v['type'] for v in dr1['violations'])
assert not any(counts[k] for k in ['courtyards_overlap','clearance','shorting_items'])
result=dict(footprints=len(new), flipped=sum(old[r]['side']!=new[r]['side'] for r in old),
    models=sum(bool(r['models']) for r in heights), bare_pads_or_holes=sum(not r['models'] for r in heights),
    missing_models=0, lcd_tall_top_bodies=0, lcd_top_pin_conflicts=0,
    anchors_preserved=['J3','J9','H1','H2','H3','H4'], groups_and_pad_nets_preserved=True,
    edge_cuts_preserved=True, blocks=blocks, fb_continuity=True, fb_layer='B.Cu', fb_length_mm=fb_length,
    new_drc_violations=0, drc_before=len(dr0['violations']), drc_after=len(dr1['violations']),
    drc_counts_after=dict(counts), unconnected_before=len(dr0['unconnected_items']),
    unconnected_after=len(dr1['unconnected_items']), schematic_parity=0,
    note='Staging placement; repeat height/pin audit after final placement and routing.')
save('verification.json',result)
print(json.dumps(result,ensure_ascii=True,indent=2))
