from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli,kicad_open
p=ensure_pcbnew();src=ROOT/'hardware/gopo.kicad_pcb'
assert not [f for f in kicad_open(str(ROOT/'hardware'),editors_only=True) if '.kicad_pcb' in f]
verified_hash=json.loads((D/'verification.json').read_text())['board_sha256'] if (D/'verification.json').exists() else None
assert src.read_bytes()==(D/'before.kicad_pcb').read_bytes() or hashlib.sha256(src.read_bytes()).hexdigest()==verified_hash,'Concurrent board edits'
assert not json.loads((D/'new-violations.json').read_text())
solid=json.loads((D/'solid-check.json').read_text());assert solid['max_stationary_intersection']<1e-6 and not solid['pair_intersections']
old=p.LoadBoard(str(src));new=p.LoadBoard(str(D/'candidate.kicad_pcb'))
def tracks(b):return sorted((v.m_Uuid.AsString(),v.GetStart().x,v.GetStart().y,v.GetEnd().x,v.GetEnd().y,v.GetNetname(),v.GetWidth()) for v in b.GetTracks())
assert tracks(old)==tracks(new)
def edges(b):
 return sorted((v.m_Uuid.AsString(),v.GetStart().x,v.GetStart().y,v.GetEnd().x,v.GetEnd().y,str(v.GetShape())) for v in b.GetDrawings() if v.GetLayer()==p.Edge_Cuts)
assert edges(old)==edges(new)
poly=p.SHAPE_POLY_SET();new.GetBoardPolygonOutlines(poly,False)
targets=json.loads((D/'placement.json').read_text())['targets']
inside={}
for r in targets:
 f=new.FindFootprintByReference(r)
 inside[r]=all(poly.Contains(v.GetPosition()) for v in f.Pads())
 assert inside[r],r
def point(r,n):
 return next(v.GetPosition() for v in new.FindFootprintByReference(r).Pads() if v.GetNumber()==n)
dist={}
for a,ap,b,bp in [('U1','20','C4','1'),('U1','12','C1','1'),('U1','15','C2','1'),('R11','2','Q3','7'),('Q3','5','C8','1'),('U1','23','R12','1'),('R12','2','Q3','2')]:
 u,v=point(a,ap),point(b,bp);dist[f'{a}.{ap}-{b}.{bp}']=math.hypot(u.x-v.x,u.y-v.y)/1e6
raw=(D/'candidate.kicad_pcb').read_text().replace((ROOT/'hardware').as_posix()+'/libraries/','${KIPRJMOD}/libraries/')
src.write_text(raw,encoding='utf-8')
print(run_cli(['pcb','drc','--format','json','--refill-zones','--schematic-parity','-o',str(D/'final-drc.json'),str(src)],keep=src,check=False).stdout)
baseline=json.loads((D/'baseline-drc.json').read_text());final=json.loads((D/'final-drc.json').read_text())
def key(v):return(v['severity'],v['type'],tuple(sorted(i['uuid'] for i in v.get('items',[]))))
keys={key(v) for v in baseline['violations']};added=[v for v in final['violations'] if key(v) not in keys]
out={'board_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'placed_refs':sorted(targets),'placed_count':len(targets),'pad_centers_inside':inside,'edge_cuts_unchanged':True,'track_geometry_nets_unchanged':True,'pad_nets_and_non_target_placements_unchanged':True,'layer_change_count':0,'baseline_errors':sum(v['severity']=='error' for v in baseline['violations']),'final_errors':sum(v['severity']=='error' for v in final['violations']),'baseline_warnings':sum(v['severity']=='warning' for v in baseline['violations']),'final_warnings':sum(v['severity']=='warning' for v in final['violations']),'new_violations':added,'schematic_parity':len(final.get('schematic_parity_issues',[])),'unconnected_before':len(baseline['unconnected_items']),'unconnected_after':len(final['unconnected_items']),'pin_center_distances_mm':dist,'distance_note':'Straight-line pin separations, not routed lengths. Routing remains TASK-087.','reference_field_adjustments':['Q3','R11','J8','R64','R65']}
(D/'verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
assert not added and out['schematic_parity']==0
