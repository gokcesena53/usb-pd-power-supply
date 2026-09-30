from pathlib import Path
import sys, json, shutil, hashlib
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew, run_cli
p=ensure_pcbnew()
D=Path(__file__).resolve().parent
src=ROOT/'hardware/gopo.kicad_pcb'
b=p.LoadBoard(str(src))
def xy(v): return [round(v.x/1e6,4),round(v.y/1e6,4)]
def box(v): return [round(x/1e6,4) for x in [v.GetX(),v.GetY(),v.GetRight(),v.GetBottom()]]
def inventory(board):
 return {f.GetReference():{'xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'side':board.GetLayerName(f.GetLayer()),'pads': [{'n':v.GetNumber(),'xy':xy(v.GetPosition()),'net':v.GetNetname(),'box':box(v.GetBoundingBox()),'drill':xy(v.GetDrillSize())} for v in f.Pads()]} for f in board.GetFootprints()}
inv=inventory(b)
(D/'before-inventory.json').write_text(json.dumps(inv,indent=2))
print(json.dumps({r:inv[r] for r in ['J7','J8','J9','H1','H3','TP14']},indent=2))
shutil.copy2(src,D/'before.kicad_pcb')
shutil.copy2(ROOT/'hardware/gopo.kicad_pro',D/'before.kicad_pro')
shutil.copy2(ROOT/'hardware/gopo.kicad_dru',D/'before.kicad_dru')
for ref,x,y,a in [('J7',53.975,88.5,-90),('J8',102.5,79.61,0),('J9',58,104,-90)]:
 f=b.FindFootprintByReference(ref);f.SetOrientationDegrees(a);f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
for f in b.GetFootprints():
 for m in f.Models():
  m.m_Filename=m.m_Filename.replace('${KIPRJMOD}',(ROOT/'hardware').as_posix())
p.SaveBoard(str(D/'candidate.kicad_pcb'),b)
shutil.copy2(ROOT/'hardware/gopo.kicad_pro',D/'candidate.kicad_pro')
shutil.copy2(ROOT/'hardware/gopo.kicad_dru',D/'candidate.kicad_dru')
print(run_cli(['pcb','drc','--format','json','-o',str(D/'candidate-drc.json'),str(D/'candidate.kicad_pcb')],keep=D/'candidate.kicad_pro',check=False).stdout)
data=json.loads((D/'candidate-drc.json').read_text())
print(json.dumps([v for v in data['violations'] if v['severity']=='error'],indent=2))
