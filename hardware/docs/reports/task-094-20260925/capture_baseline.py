from pathlib import Path
import sys,json,shutil,hashlib
ROOT=Path(__file__).resolve().parents[4]
D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli
p=ensure_pcbnew(); src=ROOT/'hardware/gopo.kicad_pcb'; b=p.LoadBoard(str(src))
for ext in ['kicad_pcb','kicad_pro','kicad_dru']:
 out=D/('before.'+ext)
 if not out.exists(): shutil.copy2(ROOT/('hardware/gopo.'+ext),out)
def xy(v): return [v.x/1e6,v.y/1e6]
inv={f.GetReference():{'xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'layer':b.GetLayerName(f.GetLayer()),'models':[{'path':m.m_Filename,'offset':[m.m_Offset.x,m.m_Offset.y,m.m_Offset.z],'rotation':[m.m_Rotation.x,m.m_Rotation.y,m.m_Rotation.z]} for m in f.Models()],'pads':[(v.GetNumber(),v.GetNetname()) for v in f.Pads()]} for f in b.GetFootprints()}
groups={g.GetName():[getattr(v,'GetReference',lambda:str(v.m_Uuid))() for v in g.GetItems()] for g in b.Groups()}
(D/'inventory.json').write_text(json.dumps({'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'footprints':inv,'groups':groups},indent=2))
print(json.dumps({r:inv[r] for r in ['J7','J8','J9']},indent=2))
for ref in ['J7','J8']:
 print(run_cli(['pcb','export','step','--force','--subst-models','--no-board-body','--component-filter',ref,'--user-origin','0x0mm','-o',str(D/(ref+'.step')),str(src)],keep=src).stdout)
print(run_cli(['pcb','drc','--format','json','--schematic-parity','-o',str(D/'baseline-drc.json'),str(src)],keep=src,check=False).stdout)
