from pathlib import Path
import json,itertools
import FreeCAD as A,Part
D=Path(__file__).resolve().parent
data=json.loads((D/'placement.json').read_text());refs=[r for r in data['targets'] if not r.startswith('TP')]
moved={r:Part.read(str(D/(r+'.step'))) for r in refs}
stationary=Part.read(str(D/'stationary.step'))
envelopes={r:Part.read(str(D/(r+'.step'))) for r in ['J8','MECH_ENC','J9']}
envelopes['cable']=Part.makeBox(12.2,21,16.5,A.Vector(57.8,-123,-17))
out={'moved_vs_stationary':{},'pair_intersections':[],'clearances':{}}
for r,s in moved.items():
 candidates=[v for v in stationary.Solids if s.BoundBox.intersect(v.BoundBox)]
 vol=sum(s.common(v).Volume for v in candidates)
 out['moved_vs_stationary'][r]=vol
 out['clearances'][r]={q:{'distance_mm':s.distToShape(v)[0],'intersection_mm3':s.common(v).Volume if s.BoundBox.intersect(v.BoundBox) else 0.0} for q,v in envelopes.items()}
for (a,s),(b,t) in itertools.combinations(moved.items(),2):
 if s.BoundBox.intersect(t.BoundBox):
  vol=s.common(t).Volume
  if vol>1e-6:out['pair_intersections'].append({'a':a,'b':b,'volume':vol})
out['max_stationary_intersection']=max(out['moved_vs_stationary'].values())
out['minimum_cable_clearance']=min(v['cable']['distance_mm'] for v in out['clearances'].values())
out['minimum_encoder_clearance']=min(v['MECH_ENC']['distance_mm'] for v in out['clearances'].values())
(D/'solid-check.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k not in ['clearances','moved_vs_stationary']},indent=2))
assert out['max_stationary_intersection']<1e-6 and not out['pair_intersections']
assert all(v[q]['intersection_mm3']<1e-6 for v in out['clearances'].values() for q in envelopes)
