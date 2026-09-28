"""Read-only extraction for the 2026-09-28 placement plan. Run with KiCad Python."""
import hashlib
import json
from pathlib import Path
import pcbnew as p

root = Path('hardware/docs/reports/flow-space-plan-20260928')
root.mkdir(parents=True, exist_ok=True)
source = Path('hardware/gopo.kicad_pcb')
b = p.LoadBoard(str(source))
def xy(v): return [round(p.ToMM(v.x), 6), round(p.ToMM(v.y), 6)]
def polys(poly):
    return [[xy(poly.COutline(i).CPoint(j)) for j in range(poly.COutline(i).PointCount())]
            for i in range(poly.OutlineCount())]
def box(rect):
    return [p.ToMM(rect.GetX()), p.ToMM(rect.GetY()), p.ToMM(rect.GetRight()), p.ToMM(rect.GetBottom())]

data = {'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'footprints': [], 'groups': [], 'tracks': len(b.GetTracks()), 'zones': []}
outline = p.SHAPE_POLY_SET()
b.GetBoardPolygonOutlines(outline, False)
data['outline'] = polys(outline)
for fp in b.GetFootprints():
    item = {'ref': fp.GetReference(), 'value': fp.GetValue(), 'footprint': fp.GetFPIDAsString(),
            'xy': xy(fp.GetPosition()), 'rotation': fp.GetOrientationDegrees(), 'layer': fp.GetLayerName(),
            'courtyards': {}, 'pads': []}
    for layer in [p.F_CrtYd, p.B_CrtYd]:
        outline = fp.GetCourtyard(layer)
        if outline.OutlineCount(): item['courtyards'][b.GetLayerName(layer)] = polys(outline)
    for pad in fp.Pads():
        item['pads'].append({'number': pad.GetNumber(), 'net': pad.GetNetname(), 'xy': xy(pad.GetPosition()),
                             'size': xy(pad.GetSize()), 'angle': pad.GetOrientationDegrees(), 'shape': int(pad.GetShape()),
                             'bbox': box(pad.GetBoundingBox())})
    for zone in fp.Zones():
        data['zones'].append({'ref': fp.GetReference(), 'rule_area': zone.GetIsRuleArea(), 'outline': polys(zone.Outline()), 'layers': str(zone.GetLayerSet().FmtBin())})
    data['footprints'].append(item)
for group in b.Groups():
    data['groups'].append({'name': group.GetName(), 'refs': sorted(x.GetReference() for x in group.GetItems() if isinstance(x, p.FOOTPRINT))})
for zone in b.Zones():
    data['zones'].append({'ref': None, 'rule_area': zone.GetIsRuleArea(), 'net': zone.GetNetname(), 'outline': polys(zone.Outline())})
(root/'board-audit.json').write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
print('Board', data['sha256'], 'footprints', len(data['footprints']), 'tracks', data['tracks'], 'zones', len(data['zones']))
for group in data['groups']: print(group['name'], ','.join(group['refs']))
refs = {'J7','Q3','U11','L3','D4','U5','L1','Q5','U12','RShunt1','J4','U13','Q4','U6'}
for fp in data['footprints']:
    if fp['ref'] in refs:
        print(fp['ref'], fp['value'], fp['layer'], fp['xy'], [(x['number'],x['net']) for x in fp['pads'] if x['number']])
