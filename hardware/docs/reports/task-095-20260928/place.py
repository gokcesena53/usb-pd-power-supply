from pathlib import Path
import sys,json,shutil
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli
p=ensure_pcbnew();b=p.LoadBoard(str(D/'before.kicad_pcb'))
targets={'R11':(76.5,103),'Q3':(78.5,110),'C8':(82.7,116.9),'C3':(72.4,107),
'U1':(76.5,120.5),'C4':(72.5,118.5),'C2':(72,122.8),'C1':(73.5,125.5),
'R12':(77.5,115.5),'TH1':(73.5,111),'R13':(82.5,122.5),'R14':(81.2,120.5),'D1':(83.5,120.5),
'R21':(75.8,125.5),'R8':(78.2,125.5),'R64':(80.5,125.5),'R65':(82.8,125.5),'R9':(85.1,125.5),
'TP1':(71.5,101.3),'TP2':(82,102.5),'TP3':(90.8,103.6),'TP4':(70,127.5),'TP5':(74,113.5),
'R34':(62.5,125.5),'R35':(65,125.5),'R36':(67.5,125.5)}
def xy(v):return [v.x/1e6,v.y/1e6]
def snap(board):return {f.GetReference():{'xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'layer':board.GetLayerName(f.GetLayer()),'pads':sorted((v.GetNumber(),v.GetNetname()) for v in f.Pads())} for f in board.GetFootprints()}
before=snap(b)
for ref,(x,y) in targets.items():
 f=b.FindFootprintByReference(ref);f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
 if ref in ['R34','R35','R36']:f.SetOrientationDegrees(90)
 if ref=='C8':f.SetOrientationDegrees(0)
for group in b.Groups():
 if group.GetName() in ['AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR','ROTARY ENCODER']:
  for v in group.GetItems():
   if isinstance(v,p.PCB_TEXT):
    pos=(78,130) if group.GetName().startswith('AP') else (64,129)
    v.SetPosition(p.VECTOR2I(p.FromMM(pos[0]),p.FromMM(pos[1])))
after=snap(b)
for ref,pos in {'Q3':(80.3,114.8),'R11':(75,105.7),'J8':(85,98.5),'R64':(80.5,127),'R65':(82.8,128.2)}.items():
 b.FindFootprintByReference(ref).Reference().SetPosition(p.VECTOR2I(p.FromMM(pos[0]),p.FromMM(pos[1])))
b.FindFootprintByReference('R11').Reference().SetTextSize(p.VECTOR2I(p.FromMM(.8),p.FromMM(.8)))
b.FindFootprintByReference('R11').Reference().SetTextThickness(p.FromMM(.12))
assert all(before[r]==after[r] for r in before if r not in targets)
assert all(before[r]['pads']==after[r]['pads'] for r in before)
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(D/('before.'+ext),D/('candidate.'+ext))
(D/'fp-lib-table').write_text((ROOT/'hardware/fp-lib-table').read_text().replace('${KIPRJMOD}',(ROOT/'hardware').as_posix()))
src=D/'candidate.kicad_pcb';p.SaveBoard(str(src),b);src.write_text(src.read_text().replace('${KIPRJMOD}',(ROOT/'hardware').as_posix()))
(D/'placement.json').write_text(json.dumps({'before':before,'after':after,'targets':targets},indent=2))
print(run_cli(['pcb','drc','--format','json','-o',str(D/'candidate-drc.json'),str(src)],keep=src,check=False).stdout)
old=json.loads((D/'baseline-drc.json').read_text());new=json.loads((D/'candidate-drc.json').read_text())
def key(v):return (v['severity'],v['type'],tuple(sorted(i['uuid'] for i in v.get('items',[]))))
keys={key(v) for v in old['violations']}
added=[v for v in new['violations'] if key(v) not in keys]
print(json.dumps(added,indent=2));(D/'new-violations.json').write_text(json.dumps(added,indent=2))
