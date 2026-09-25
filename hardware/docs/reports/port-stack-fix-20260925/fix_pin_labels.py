from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli,kicad_open
p=ensure_pcbnew();D=Path(__file__).resolve().parent;src=ROOT/'hardware/gopo.kicad_pcb'
assert not kicad_open(str(ROOT/'hardware'),editors_only=True)
b=p.LoadBoard(str(src));changes=[]
labels={'1 A':104,'2 GND':108.2,'3 B':112.4,'4 SW':116.6,'5 GND':120.8}
for item in b.GetDrawings():
 if isinstance(item,p.PCB_TEXT) and item.GetText() in labels:
  txt=item.GetText();prev=[item.GetPosition().x/1e6,item.GetPosition().y/1e6]
  item.SetPosition(p.VECTOR2I(p.FromMM(61.0),p.FromMM(labels[txt])))
  item.SetTextAngle(p.EDA_ANGLE(0,p.DEGREES_T))
  changes.append({'text':txt,'before':prev,'after':[61,labels[txt]]})
print(json.dumps(changes,indent=2));assert len(changes)==5
p.SaveBoard(str(src),b)
(D/'pin-label-changes.json').write_text(json.dumps(changes,indent=2))
print(run_cli(['pcb','drc','--format','json','--schematic-parity','-o',str(D/'final-drc.json'),str(src)],keep=src,check=False).stdout)
v=json.loads((D/'verification.json').read_text(encoding='utf-8'))
dr=json.loads((D/'final-drc.json').read_text())
v['board_sha256']=hashlib.sha256(src.read_bytes()).hexdigest();v['pin_label_changes']=changes
v['final_errors']=sum(i['severity']=='error' for i in dr['violations']);v['warnings']=sum(i['severity']=='warning' for i in dr['violations'])
(D/'verification.json').write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
print('Final errors/warnings:',v['final_errors'],v['warnings'])
for side,layers in [('top','F.Cu,F.Silkscreen,F.Fab,Edge.Cuts'),('bottom','B.Cu,B.Silkscreen,B.Fab,Edge.Cuts')]:
 run_cli(['pcb','export','svg','--mode-single','--layers',layers,'--page-size-mode','2','--exclude-drawing-sheet','-o',str(D/('final-'+side+'.svg')),str(src)],keep=src)
