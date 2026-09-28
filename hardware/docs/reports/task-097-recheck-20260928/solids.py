from pathlib import Path
import json,itertools
import FreeCAD as A,Part
D=Path(__file__).resolve().parent
refs=['C5','C6','C7','R1','R2','R3'];shapes={r:Part.read(str(D/(r+'.step'))) for r in refs};fixed=Part.read(str(D/'stationary.step'))
out={'intersection_mm3':{},'pair_intersections':[],'note':'Candidate six MCU passives only. Nominal models; no physical assembly tolerance claim.'}
for r,s in shapes.items():
 out['intersection_mm3'][r]=sum(s.common(t).Volume for t in fixed.Solids if s.BoundBox.intersect(t.BoundBox))
for (r,s),(q,t) in itertools.combinations(shapes.items(),2):
 if s.BoundBox.intersect(t.BoundBox):
  v=s.common(t).Volume
  if v>1e-6:out['pair_intersections'].append([r,q,v])
out['passed']=max(out['intersection_mm3'].values())<1e-6 and not out['pair_intersections']
(D/'candidate-solid-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));assert out['passed']
