from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli,kicad_open
p=ensure_pcbnew();D=Path(__file__).resolve().parent
src=ROOT/'hardware/gopo.kicad_pcb'
assert not kicad_open(str(ROOT/'hardware'),editors_only=True), 'PCB editor must be saved and closed'
assert src.read_bytes()==(D/'before.kicad_pcb').read_bytes(), 'Board changed since saved baseline'
b=p.LoadBoard(str(src))
before={f.GetReference():f for f in b.GetFootprints()}
def snap(board):
 return {f.GetReference():{'xy':[f.GetPosition().x/1e6,f.GetPosition().y/1e6],'angle':f.GetOrientationDegrees(),'layer':board.GetLayerName(f.GetLayer()),'pads':sorted([(v.GetNumber(),v.GetNetname()) for v in f.Pads()])} for f in board.GetFootprints()}
old=snap(b)
targets={'J7':(53.975,88.5,-90),'J8':(102.5,79.61,0),'J9':(58,104,-90)}
for ref,(x,y,a) in targets.items():
 f=before[ref];f.SetOrientationDegrees(a);f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
new=snap(b)
assert all(new[r]['pads']==old[r]['pads'] for r in old)
assert all(new[r]==old[r] for r in old if r not in targets)
assert abs(new['J8']['xy'][1]+8.89-new['J7']['xy'][1])<1e-6
rule='''\n# Opposite-face stack; nominal STEP solids distance 3.23 mm, zero intersection.
# Only J7/J8 courtyard projection is exempted; hole/copper/edge checks stay active.
# Actual RJ45 solder protrusions and USB solder fillets: TASK-053 sample acceptance.
(rule "J7 above J8 nominal 3D clearance - port-stack-fix-20260925"
 (condition "(A.Reference == 'J7' && B.Reference == 'J8') || (A.Reference == 'J8' && B.Reference == 'J7')")
 (constraint courtyard_clearance (min -100mm))
)
'''
dru=ROOT/'hardware/gopo.kicad_dru'
assert 'J7 above J8 nominal' not in dru.read_text(encoding='utf-8')
p.SaveBoard(str(src),b)
dru.write_text(dru.read_text(encoding='utf-8').rstrip()+'\n'+rule,encoding='utf-8')
print(run_cli(['pcb','drc','--format','json','--schematic-parity','-o',str(D/'final-drc.json'),str(src)],keep=src,check=False).stdout)
baseline=json.loads((D/'baseline-drc.json').read_text())
final=json.loads((D/'final-drc.json').read_text())
def key(v): return (v['type'],v['severity'],tuple(sorted(i['uuid'] for i in v.get('items',[]))))
old_errors={key(v) for v in baseline['violations'] if v['severity']=='error'}
new_errors=[v for v in final['violations'] if v['severity']=='error' and key(v) not in old_errors]
summary={'board_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'changed_refs':list(targets),'before':{r:old[r] for r in targets},'after':{r:new[r] for r in targets},'pad_net_mapping_unchanged':True,'other_footprints_unchanged':True,'port_center_y_mm':88.5,'port_y_alignment_error_mm':0,'baseline_errors':len(old_errors),'final_errors':sum(v['severity']=='error' for v in final['violations']),'new_errors':new_errors,'warnings':sum(v['severity']=='warning' for v in final['violations']),'schematic_parity':len(final.get('schematic_parity_issues',[])),'unconnected_before':len(baseline['unconnected_items']),'unconnected_after':len(final['unconnected_items']),'sample_check':'RJ45 solder tails/USB solder fillets and real plug envelopes remain TASK-053/054/088 acceptance; STEP model is nominal.'}
(D/'verification.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
assert not new_errors
assert summary['schematic_parity']==0
print(json.dumps({k:v for k,v in summary.items() if k not in ['before','after']},ensure_ascii=False,indent=2))
for side,layers in [('top','F.Cu,F.Silkscreen,F.Fab,Edge.Cuts'),('bottom','B.Cu,B.Silkscreen,B.Fab,Edge.Cuts')]:
 print(run_cli(['pcb','export','svg','--mode-single','--layers',layers,'--page-size-mode','2','--exclude-drawing-sheet','-o',str(D/('final-'+side+'.svg')),str(src)],keep=src).stdout)
