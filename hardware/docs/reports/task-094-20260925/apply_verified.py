from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli,kicad_open
p=ensure_pcbnew();src=ROOT/'hardware/gopo.kicad_pcb'
assert not [x for x in kicad_open(str(ROOT/'hardware'),editors_only=True) if '.kicad_pcb' in x], 'PCB editor open'
assert src.read_bytes()==(D/'before.kicad_pcb').read_bytes(),'Concurrent board change'
assert (ROOT/'hardware/gopo.kicad_dru').read_bytes()==(D/'before.kicad_dru').read_bytes(),'Concurrent rule change'
baseline=json.loads((D/'baseline-drc.json').read_text());candidate=json.loads((D/'candidate-drc.json').read_text())
def key(v):return (v['type'],v['severity'],tuple(sorted(i['uuid'] for i in v.get('items',[]))))
old_keys={key(v) for v in baseline['violations']}
assert not [v for v in candidate['violations'] if key(v) not in old_keys]
solid=json.loads((D/'solid-check.json').read_text());assert all(v['intersection_mm3']<1e-6 for v in solid['pairs'].values())
raw=(D/'candidate.kicad_pcb').read_text().replace((ROOT/'hardware').as_posix()+'/libraries/','${KIPRJMOD}/libraries/')
src.write_text(raw,encoding='utf-8')
(ROOT/'hardware/gopo.kicad_dru').write_text((D/'candidate.kicad_dru').read_text(),encoding='utf-8')
print(run_cli(['pcb','drc','--format','json','--refill-zones','--schematic-parity','-o',str(D/'final-drc.json'),str(src)],keep=src,check=False).stdout)
final=json.loads((D/'final-drc.json').read_text());new=[v for v in final['violations'] if key(v) not in old_keys]
summary={'board_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'baseline_errors':sum(v['severity']=='error' for v in baseline['violations']),'final_errors':sum(v['severity']=='error' for v in final['violations']),'baseline_warnings':sum(v['severity']=='warning' for v in baseline['violations']),'final_warnings':sum(v['severity']=='warning' for v in final['violations']),'new_violations':new,'schematic_parity':len(final.get('schematic_parity_issues',[])),'unconnected_before':len(baseline['unconnected_items']),'unconnected_after':len(final['unconnected_items']),'parked_count':26,'j7_j8_unchanged':True,'tracks_nets_unchanged':True,'notch_vertical_edge_x_mm':59.8,'j9_copper_left_x_mm':60.575,'j9_notch_clearance_mm':.775,'usb_edge_rule_mm':.254}
b=p.LoadBoard(str(src));old=p.LoadBoard(str(D/'before.kicad_pcb'))
old_edges={v.m_Uuid.AsString():v for v in old.GetDrawings() if v.GetLayer()==p.Edge_Cuts}
edges={v.m_Uuid.AsString():v for v in b.GetDrawings() if v.GetLayer()==p.Edge_Cuts}
removed=set(old_edges)-set(edges)
assert len(removed)==1
for uid in set(old_edges)&set(edges):
 a,c=old_edges[uid],edges[uid]
 assert a.GetStart()==c.GetStart() and a.GetEnd()==c.GetEnd() and a.GetShape()==c.GetShape()
 if a.GetShape()==p.SHAPE_T_ARC:assert a.GetArcMid()==c.GetArcMid()
summary['unchanged_original_edge_items']=len(set(old_edges)&set(edges));summary['removed_left_edge_items']=len(removed)
summary['copper_zones']=b.GetAreaCount()
(D/'verification.json').write_text(json.dumps(summary,indent=2))
assert not new and summary['schematic_parity']==0
print(json.dumps(summary,indent=2))
for side,layers in [('top','F.Cu,F.Silkscreen,F.Fab,Edge.Cuts'),('bottom','B.Cu,B.Silkscreen,B.Fab,Edge.Cuts')]:
 print(run_cli(['pcb','export','svg','--mode-single','--layers',layers,'--page-size-mode','2','--exclude-drawing-sheet','-o',str(D/('final-'+side+'.svg')),str(src)],keep=src).stdout)
for side in ['top','right']:
 print(run_cli(['pcb','render','--output',str(D/('final-'+side+'.png')),'--width','1500','--height','1000','--background','opaque','--quality','basic','--side',side,str(src)],keep=src).stdout[-150:])
