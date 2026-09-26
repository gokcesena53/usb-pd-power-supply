from pathlib import Path
import json, itertools
import FreeCAD, Part
D=Path(__file__).resolve().parent
shapes={r:Part.read(str(D/(r+'.step'))) for r in ['J7','J8','J9']}
def bb(s):
 b=s.BoundBox
 return [round(v,4) for v in [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]]
out={'model_bounds':{r:bb(s) for r,s in shapes.items()},'pairs':{}}
for a,b in itertools.combinations(shapes,2):
 sa,sb=shapes[a],shapes[b]
 out['pairs'][a+'-'+b]={'distance_mm':sa.distToShape(sb)[0], 'intersection_volume_mm3':sa.common(sb).Volume}
out['J8_solids']=[bb(s) for s in shapes['J8'].Solids]
print(json.dumps(out,indent=2))
(D/'solid-check.json').write_text(json.dumps(out,indent=2))
