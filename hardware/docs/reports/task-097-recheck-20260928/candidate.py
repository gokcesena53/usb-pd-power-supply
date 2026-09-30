from pathlib import Path
import sys,json,shutil,math
ROOT=Path(__file__).resolve().parents[4]; D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli
p=ensure_pcbnew(); src=ROOT/'hardware/gopo.kicad_pcb'; b=p.LoadBoard(str(src)); fs={f.GetReference():f for f in b.GetFootprints()}
targets={'C5':(66.8,72.7,180),'C6':(70.1,72.665,180),'C7':(70.1,76.665,0),'R1':(67.8,76.665,0),'R2':(77.1,82.3,-90),'R3':(78.5,82.3,-90)}
for r,(x,y,a) in targets.items():fs[r].SetPosition(p.VECTOR2I(round(x*1e6),round(y*1e6)));fs[r].SetOrientationDegrees(a)
fs['U2'].Reference().SetPosition(p.VECTOR2I(90000000,80500000))
out=D/'candidate.kicad_pcb';p.SaveBoard(str(out),b)
for ext in ['kicad_pro','kicad_dru']:shutil.copy2(ROOT/('hardware/gopo.'+ext),D/('candidate.'+ext))
(D/'fp-lib-table').write_text((ROOT/'hardware/fp-lib-table').read_text().replace('${KIPRJMOD}',str(ROOT/'hardware').replace('\\','/')))
out.write_text(out.read_text().replace('${KIPRJMOD}',str(ROOT/'hardware').replace('\\','/')))
print(run_cli(['pcb','drc','--format','json','-o',str(D/'candidate-drc.json'),str(out)],keep=out,check=False).stdout)
base=json.loads((D/'drc.json').read_text());new=json.loads((D/'candidate-drc.json').read_text())
def key(v):return v['type'],v['severity'],tuple(sorted(i['uuid'] for i in v.get('items',[])))
keys={key(v) for v in base['violations']}; fresh=[v for v in new['violations'] if key(v) not in keys]
(D/'candidate-new-drc.json').write_text(json.dumps(fresh,indent=2)); print(json.dumps(fresh,indent=2))
spec=[('C5','1','U2','3'),('C6','1','U2','3'),('C7','2','U2','8'),('R1','2','U2','8'),('R2','1','U2','17'),('R3','1','U2','18')]
old=p.LoadBoard(str(src));ofs={f.GetReference():f for f in old.GetFootprints()}
def dist(fs,r,pn,t,tn):
 a=[v for v in fs[r].Pads() if v.GetNumber()==pn];z=[v for v in fs[t].Pads() if v.GetNumber()==tn]
 assert a and z
 return round(min(math.hypot(v.GetPosition().x-w.GetPosition().x,v.GetPosition().y-w.GetPosition().y)/1e6 for v in a for w in z),3)
measure=[{'ref':r,'pin':pn,'target':t+'.'+tn,'before':dist(ofs,r,pn,t,tn),'candidate':dist(fs,r,pn,t,tn),'xyz':targets[r]} for r,pn,t,tn in spec]
(D/'candidate-measures.json').write_text(json.dumps(measure,indent=2));print(json.dumps(measure,indent=2))

