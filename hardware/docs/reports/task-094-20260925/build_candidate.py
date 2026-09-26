from pathlib import Path
import sys,json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli
p=ensure_pcbnew();src=ROOT/'hardware/gopo.kicad_pcb'
assert src.read_bytes()==(D/'before.kicad_pcb').read_bytes(),'Source changed since baseline'
b=p.LoadBoard(str(src))
def vec(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def xy(v):return [round(v.x/1e6,6),round(v.y/1e6,6)]
def snap(board):
 return {f.GetReference():{'xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'layer':board.GetLayerName(f.GetLayer()),'pads':sorted((v.GetNumber(),v.GetNetname()) for v in f.Pads())} for f in board.GetFootprints()}
before=snap(b);park={}; moved=set()
for name,delta in [('AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR',(-45,50)),('ROTARY ENCODER',(-30,75))]:
 g=next(g for g in b.Groups() if g.GetName()==name)
 members=[v.GetReference() for v in g.GetItems() if isinstance(v,p.FOOTPRINT)]
 assert not {'J7','J8'}.intersection(members)
 g.Move(vec(*delta)); moved.update(members)
 park[name]={'translation':delta,'refs':members}
b.FindFootprintByReference('J9').SetPosition(vec(61.5,104))
# Keep J9 net labels close to pads but inside the new edge.
label_changes=[]
for g in b.GetDrawings():
 if isinstance(g,p.PCB_TEXT) and g.GetText() in ['1 A','2 GND','3 B','4 SW','5 GND']:
  old=xy(g.GetPosition());g.Move(vec(3.5,0));label_changes.append({'text':g.GetText(),'before':old,'after':xy(g.GetPosition())})
# Original left vertical only; retain all other outline items and mounting holes.
edge=next(g for g in b.GetDrawings() if g.GetLayer()==p.Edge_Cuts and g.GetShape()==p.SHAPE_T_SEGMENT and abs(g.GetStart().x/1e6-50.3)<1e-6 and abs(g.GetEnd().x/1e6-50.3)<1e-6)
old_edge=str(edge.m_Uuid.AsString());b.Remove(edge)
points=[(50.3,72.48),(50.3,101.5),(51.3,102.5),(58.8,102.5),(59.8,103.5),(59.8,121.3),(58.8,122.3),(51.3,122.3),(50.3,123.3),(50.3,127.52)]
for a,c in zip(points,points[1:]):
 g=p.PCB_SHAPE();g.SetShape(p.SHAPE_T_SEGMENT);g.SetLayer(p.Edge_Cuts);g.SetStart(vec(*a));g.SetEnd(vec(*c));g.SetWidth(p.FromMM(.05));b.Add(g)
# Mechanical-only panel part: no electrical pads, excluded from BOM/positions.
f=p.FOOTPRINT(b);f.SetReference('MECH_ENC');f.SetValue('PANEL EC1121S; J9 cable')
f.SetAttributes(p.FP_EXCLUDE_FROM_BOM|p.FP_EXCLUDE_FROM_POS_FILES|p.FP_BOARD_ONLY)
f.SetPosition(vec(54.3,112.4));f.Reference().SetVisible(False);f.Value().SetVisible(False)
m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/libraries/Mechanical_Custom.3dshapes/Encoder_Panel_EC1121S.step';f.Models().push_back(m)
b.Add(f)
after=snap(b)
assert all(before[r]['pads']==after[r]['pads'] for r in before)
assert all(before[r]==after[r] for r in before if r not in moved|{'J9'})
tracks=[{'uuid':t.m_Uuid.AsString(),'start':xy(t.GetStart()),'end':xy(t.GetEnd()),'net':t.GetNetname()} for t in b.GetTracks()]
original=p.LoadBoard(str(src));original_tracks=[{'uuid':t.m_Uuid.AsString(),'start':xy(t.GetStart()),'end':xy(t.GetEnd()),'net':t.GetNetname()} for t in original.GetTracks()]
assert tracks==original_tracks,'Unexpected track movement'
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(ROOT/('hardware/gopo.'+ext),D/('candidate.'+ext))
rules=(D/'candidate.kicad_dru').read_text();rules=rules.replace('(constraint edge_clearance (min 0.25mm))','(constraint edge_clearance (min 0.254mm))');(D/'candidate.kicad_dru').write_text(rules)
for footprint in b.GetFootprints():
 for model in footprint.Models():model.m_Filename=model.m_Filename.replace('${KIPRJMOD}',(ROOT/'hardware').as_posix())
p.SaveBoard(str(D/'candidate.kicad_pcb'),b)
candidate=D/'candidate.kicad_pcb'
candidate.write_text(candidate.read_text().replace('${KIPRJMOD}',(ROOT/'hardware').as_posix()))
(D/'fp-lib-table').write_text((ROOT/'hardware/fp-lib-table').read_text().replace('${KIPRJMOD}',(ROOT/'hardware').as_posix()))
verification={'before':before,'after':after,'parked_blocks':park,'j9_labels':label_changes,'other_footprints_preserved':True,'pad_nets_preserved':True,'tracks_preserved':tracks,'removed_edge_uuid':old_edge,'new_left_edge':points}
(D/'placement.json').write_text(json.dumps(verification,indent=2))
print(run_cli(['pcb','drc','--format','json','--refill-zones','-o',str(D/'candidate-drc.json'),str(D/'candidate.kicad_pcb')],keep=D/'candidate.kicad_pro',check=False).stdout)
for ref in ['MECH_ENC']:
 print(run_cli(['pcb','export','step','--force','--subst-models','--no-board-body','--component-filter',ref,'--user-origin','0x0mm','-o',str(D/(ref+'.step')),str(D/'candidate.kicad_pcb')],keep=D/'candidate.kicad_pro').stdout)
print(run_cli(['pcb','export','step','--force','--board-only','--user-origin','0x0mm','-o',str(D/'board-body.step'),str(D/'candidate.kicad_pcb')],keep=D/'candidate.kicad_pro').stdout)
print('Parked:',park)
