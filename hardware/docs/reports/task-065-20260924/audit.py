"""TASK-065: KiCad inventory and FreeCAD STEP-envelope measurement.

Run inventory with KiCad's Python; measure with FreeCAD's Python.
All paths in output are project-relative or KiCad variables.
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BOARD = ROOT / 'hardware/gopo.kicad_pcb'


def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def outline(board):
    import pcbnew as p
    return sorted([dict(uuid=g.m_Uuid.AsString(), shape=g.GetShapeStr(),
                        start=list(g.GetStart()), end=list(g.GetEnd()), width=g.GetWidth(),
                        mid=list(g.GetArcMid()) if g.GetShape()==p.SHAPE_T_ARC else None)
                   for g in board.GetDrawings() if g.GetLayer()==p.Edge_Cuts], key=lambda g:g['uuid'])


def inventory(label):
    import pcbnew as p
    b = p.LoadBoard(str(BOARD))
    groups = {i.GetReference(): g.GetName() for g in b.Groups()
              for i in g.GetItems() if isinstance(i, p.FOOTPRINT)}
    rows = []
    for f in sorted(b.GetFootprints(), key=lambda f: f.GetReference()):
        box = f.GetBoundingBox(False, False)
        rows.append(dict(ref=f.GetReference(), value=f.GetValue(), uuid=f.m_Uuid.AsString(),
                         footprint=str(f.GetFPID().GetLibItemName()), group=groups.get(f.GetReference(), ''),
                         side=f.GetLayerName(), xy=list(p.ToMM(f.GetPosition())),
                         angle=f.GetOrientationDegrees(), locked=f.IsLocked(),
                         bbox=[p.ToMM(box.GetLeft()), p.ToMM(box.GetTop()),
                               p.ToMM(box.GetRight()), p.ToMM(box.GetBottom())],
                         pads=sorted([(a.GetNumber(), a.GetNetname()) for a in f.Pads()]),
                         models=[dict(path=m.m_Filename,
                                      scale=[m.m_Scale.x, m.m_Scale.y, m.m_Scale.z],
                                      offset=[m.m_Offset.x, m.m_Offset.y, m.m_Offset.z],
                                      rotation=[m.m_Rotation.x, m.m_Rotation.y, m.m_Rotation.z])
                                 for m in f.Models()]))
    save(f'inventory-{label}.json', dict(sha256=hashlib.sha256(BOARD.read_bytes()).hexdigest(),
         thickness=p.ToMM(b.GetDesignSettings().GetBoardThickness()), footprints=rows,
         tracks=[dict(uuid=t.m_Uuid.AsString(), net=t.GetNetname(), side=t.GetLayerName(),
                      start=list(p.ToMM(t.GetStart())), end=list(p.ToMM(t.GetEnd())),
                      width=p.ToMM(t.GetWidth())) for t in b.GetTracks()],
         zones=len(list(b.Zones())), edge_cuts=outline(b)))
    print(f'{label}: {len(rows)} footprints')


def measure(label, model_dir):
    import FreeCAD
    import Part
    data = json.loads((HERE / f'inventory-{label}.json').read_text(encoding='utf-8'))
    rows, cache = [], {}
    lcd = [63.52, 72.28, 141.62, 127.72]  # TASK-064 envelope + 0.2 mm each edge
    for f in data['footprints']:
        boxes, missing = [], []
        for m in f['models']:
            path = m['path'].replace('${KIPRJMOD}', str(ROOT / 'hardware'))
            path = path.replace('${KICAD10_3DMODEL_DIR}', model_dir)
            assert m['rotation'] == [0, 0, 0], 'Add rotation handling before measuring rotated model'
            if path not in cache:
                if not Path(path).is_file():
                    missing.append(m['path'])
                    continue
                shape = Part.read(path)
                assert not shape.isNull(), path
                bb = shape.BoundBox
                cache[path] = [bb.XMin, bb.YMin, bb.ZMin, bb.XMax, bb.YMax, bb.ZMax]
            bb = cache[path]
            boxes.append([bb[i] * m['scale'][i % 3] + m['offset'][i % 3] for i in range(6)])
        h = max((bb[5] for bb in boxes), default=0)
        zmin = min((bb[2] for bb in boxes), default=0)
        # Map CAD y-up to footprint y-down, mirror local y on B.Cu, then rotate.
        xy = []
        a = math.radians(f['angle'])
        for bb in boxes:
            for x, y in itertools.product([bb[0], bb[3]], [bb[1], bb[4]]):
                y = -y if f['side'] == 'F.Cu' else y
                xy.append((f['xy'][0] + math.cos(a)*x + math.sin(a)*y,
                           f['xy'][1] - math.sin(a)*x + math.cos(a)*y))
        bounds = [min(x for x,y in xy), min(y for x,y in xy),
                  max(x for x,y in xy), max(y for x,y in xy)] if xy else f['bbox']
        overlap = bounds[0] <= lcd[2] and bounds[2] >= lcd[0] and bounds[1] <= lcd[3] and bounds[3] >= lcd[1]
        top = h if f['side'] == 'F.Cu' else max(0, -zmin-data['thickness'])
        no_model_ok = f['ref'].startswith(('TP', 'H'))
        if label == 'after':
            assert (boxes or no_model_ok) and not missing, f['ref']
        rows.append(dict(ref=f['ref'], value=f['value'], group=f['group'], side=f['side'],
                         height_mm=round(h, 4), model_zmin_mm=round(zmin,4),
                         top_projection_mm=round(top,4), model_xy_bbox=[round(v,4) for v in bounds],
                         lcd_overlap=overlap, models=[m['path'] for m in f['models']],
                         model_status='MISSING: '+str(missing) if missing else ('measured' if boxes else 'bare pad / mounting hole')))
    save(f'heights-{label}.json', rows)
    with (HERE / f'heights-{label}.csv').open('w',encoding='utf-8-sig',newline='') as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps(dict(footprints=len(rows), unique_models=len(cache),
          tall=[(r['ref'],r['height_mm'],r['side']) for r in rows if r['height_mm']>2.0001],
          lcd_top_violations=[r['ref'] for r in rows if r['lcd_overlap'] and r['top_projection_mm']>2.0001]), indent=2))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['inventory', 'measure'])
    ap.add_argument('label', choices=['before', 'after'])
    ap.add_argument('--model-dir', default='C:/Program Files/KiCad/10.0/share/kicad/3dmodels')
    args = ap.parse_args()
    if args.mode == 'inventory': inventory(args.label)
    else: measure(args.label, args.model_dir)
