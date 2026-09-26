from pathlib import Path
import json
import FreeCAD as A,Part
D=Path(__file__).resolve().parent
def bb(s):
 b=s.BoundBox;return [round(v,6) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]
enc=Part.read(str(D/'MECH_ENC.step'))
expected=Part.read(str(D/'encoder-world.step'))
assert all(abs(a-b)<1e-5 for a,b in zip(bb(enc),bb(expected))), (bb(enc),bb(expected))
shapes={r:Part.read(str(D/(r+'.step'))) for r in ['board-body','J7','J8','J9','J3','panel-world']}
# Conservative full-height LCD XY prism, using earlier LCD tolerance envelope.
shapes['LCD_XY_envelope']=Part.makeBox(78.1,55.44,50,A.Vector(63.52,-127.72,-20))
out={'encoder_bounds':bb(enc),'encoder_model_matches_target':True,'pairs':{}}
for r,s in shapes.items():
 out['pairs'][r]={'distance_mm':enc.distToShape(s)[0],'intersection_mm3':enc.common(s).Volume}
 assert out['pairs'][r]['intersection_mm3']<1e-6,(r,out['pairs'][r])
# Reserve below-board service space for five flexible wires, not a production harness model.
cable=Part.makeBox(12.2,21,16.5,A.Vector(57.8,-123,-17))
out['cable_service_envelope']={'bounds':bb(cable),'description':'Below-board service envelope; 26-28 AWG wires, bend radius >=4.5 mm, stripped ends terminate on J9 pads. Final harness verified with sample.'}
out['cable_pairs']={r:{'intersection_mm3':cable.common(s).Volume,'distance_mm':cable.distToShape(s)[0]} for r,s in shapes.items() if r not in ['LCD_XY_envelope','J9']}
assert all(v['intersection_mm3']<1e-6 for v in out['cable_pairs'].values())
(D/'solid-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
Part.makeCompound([enc,*[s for r,s in shapes.items() if r!='LCD_XY_envelope']]).exportStep(str(D/'mechanical-review.step'))
# Meshes for reproducible, dimensioned orthographic review figures.
mesh={}
for r,s in {'encoder':enc,**{r:s for r,s in shapes.items() if r not in ['LCD_XY_envelope','J3']}}.items():
 verts,faces=s.tessellate(.12)
 mesh[r]={'vertices':[[v.x,v.y,v.z] for v in verts],'faces':faces}
(D/'assembly-mesh.json').write_text(json.dumps(mesh))
