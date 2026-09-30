from pathlib import Path
import sys,json,shutil
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli
p=ensure_pcbnew();src=ROOT/'hardware/gopo.kicad_pcb';b=p.LoadBoard(str(src))
for ext in ['kicad_pcb','kicad_pro','kicad_dru']:
 if not (D/('before.'+ext)).exists():shutil.copy2(ROOT/('hardware/gopo.'+ext),D/('before.'+ext))
def xy(v):return [v.x/1e6,v.y/1e6]
def box(v):return [v.GetX()/1e6,v.GetY()/1e6,v.GetRight()/1e6,v.GetBottom()/1e6]
out={}
for f in b.GetFootprints():
 shapes=[g for g in f.GraphicalItems() if g.GetLayer() in [p.F_CrtYd,p.B_CrtYd]]
 boxes=[box(g.GetBoundingBox()) for g in shapes]
 if boxes: bounds=[min(v[0] for v in boxes),min(v[1] for v in boxes),max(v[2] for v in boxes),max(v[3] for v in boxes)]
 else:bounds=box(f.GetBoundingBox(False,False))
 out[f.GetReference()]={'xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'layer':b.GetLayerName(f.GetLayer()),'courtyard':bounds,'pads':[{ 'n':v.GetNumber(),'xy':xy(v.GetPosition()),'net':v.GetNetname()} for v in f.Pads()]}
(D/'inventory.json').write_text(json.dumps(out,indent=2))
print(json.dumps({r:f for r,f in out.items() if 60<f['xy'][0]<104 and 98<f['xy'][1]<131},indent=2))
print(run_cli(['pcb','drc','--format','json','--schematic-parity','-o',str(D/'baseline-drc.json'),str(src)],keep=src,check=False).stdout)
