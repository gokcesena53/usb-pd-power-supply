from pathlib import Path
import sys,json,hashlib,math,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[4]; D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew,run_cli
p=ensure_pcbnew(); src=ROOT/'hardware/gopo.kicad_pcb'; b=p.LoadBoard(str(src))
def xy(v):return [round(v.x/1e6,6),round(v.y/1e6,6)]
fps={}
for f in b.GetFootprints():
 fps[f.GetReference()]={'value':f.GetValue(),'footprint':str(f.GetFPID().GetLibItemName()),'xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'layer':b.GetLayerName(f.GetLayer()),'pads':[{'n':v.GetNumber(),'xy':xy(v.GetPosition()),'net':v.GetNetname(),'uuid':str(v.m_Uuid.AsString())} for v in f.Pads()]}
(D/'board.json').write_text(json.dumps(fps,indent=2),encoding='utf-8')
run_cli(['sch','export','netlist','--format','kicadxml','-o',str(D/'netlist.xml'),str(ROOT/'hardware/gopo.kicad_sch')],keep=src)
tree=ET.parse(D/'netlist.xml'); sch={c.get('ref'):c.findtext('value') for c in tree.findall('./components/comp')}
nodes={}
for net in tree.findall('./nets/net'):
 for n in net.findall('node'):nodes[(n.get('ref'),n.get('pin'))]={'net':net.get('name'),'function':n.get('pinfunction')}
rows=[]; mismatch=[]
for ref,f in sorted(fps.items()):
 if not ref.startswith(('R','C')):continue
 if sch.get(ref)!=f['value']:mismatch.append([ref,'value',f['value'],sch.get(ref)])
 for pad in f['pads']:
  sn=nodes.get((ref,pad['n']))
  if not sn or sn['net']!=pad['net']:mismatch.append([ref,pad['n'],pad['net'],sn])
  pad['connections']=[]
  for tr,t in fps.items():
   if tr==ref or not tr.startswith(('U','Q','J','D','L','Y')):continue
   for tp in t['pads']:
    if tp['net'] and tp['net']==pad['net'] and tp['net']!='GND':
     pad['connections'].append({'ref':tr,'pin':tp['n'],'function':nodes.get((tr,tp['n']),{}).get('function'),'xy':tp['xy'],'mm':round(math.dist(pad['xy'],tp['xy']),3),'layer':t['layer']})
  pad['connections'].sort(key=lambda a:a['mm'])
 rows.append({'ref':ref,**f})
missing=[r for r in sch if r.startswith(('R','C')) and r not in fps]
(D/'rc_actual.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
summary={'hash':hashlib.sha256(src.read_bytes()).hexdigest(),'kicad':p.Version(),'count':len(rows),'R':sum(r['ref'].startswith('R') for r in rows),'C':sum(r['ref'].startswith('C') for r in rows),'mismatches':mismatch,'missing':missing}
(D/'verification.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary))
for r in rows:
 print(r['ref'],r['value'],r['xy'],r['layer'], '; '.join(v['n']+':'+v['net']+' -> '+','.join(c['ref']+'.'+c['pin']+'('+str(c['function'])+')='+str(c['mm']) for c in v['connections'][:4]) for v in r['pads']))
print(run_cli(['pcb','drc','--format','json','--schematic-parity','-o',str(D/'drc.json'),str(src)],keep=src,check=False).stdout)
