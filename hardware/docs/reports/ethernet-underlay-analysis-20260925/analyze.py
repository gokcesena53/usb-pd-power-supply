import json, sys, pathlib, hashlib
ROOT=next(d for d in pathlib.Path(__file__).resolve().parents if (d/'hardware/gopo.kicad_pcb').exists())
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew
p=ensure_pcbnew()
b=p.LoadBoard(str(ROOT/'hardware/gopo.kicad_pcb'))
def xy(v): return [round(v.x/1e6,4),round(v.y/1e6,4)]
def box(bb): return [round(v/1e6,4) for v in [bb.GetX(),bb.GetY(),bb.GetRight(),bb.GetBottom()]]
out={'scope':'Read-only geometry and net inventory; no placement or 3D/DRC validation','board_sha256':hashlib.sha256((ROOT/'hardware/gopo.kicad_pcb').read_bytes()).hexdigest(), 'footprints':{},'j8_shapes':[], 'j8_zones':[]}
for ref in ['J8','Q8','R17','C10','C20','C21','TP14','J3','J9','R16','R37','Q1','Q2','R4','R5','R6','R7','R34','R35','R36']:
 f=b.FindFootprintByReference(ref)
 out['footprints'][ref]={'xy':xy(f.GetPosition()),'angle':f.GetOrientationDegrees(),'side':b.GetLayerName(f.GetLayer()),'value':f.GetValue(),'footprint':str(f.GetFPID().GetLibItemName()),'pads':[{'n':s.GetNumber(),'xy':xy(s.GetPosition()),'net':s.GetNetname(),'size':xy(s.GetSize())} for s in f.Pads()]}
 if ref=='J8':
  for s in f.GraphicalItems():
   if isinstance(s,p.PCB_SHAPE) and s.GetLayer() in [p.B_Fab,p.B_CrtYd]:
    out['j8_shapes'].append({'layer':b.GetLayerName(s.GetLayer()),'shape':s.GetShapeStr(),'bbox':box(s.GetBoundingBox())})
  for z in f.Zones():
   out['j8_zones'].append({'bbox':box(z.GetBoundingBox()),'layers':[b.GetLayerName(i) for i in z.GetLayerSet().Seq()],'rule_area':z.GetIsRuleArea(),'no_footprints':z.GetDoNotAllowFootprints(),'no_tracks':z.GetDoNotAllowTracks(),'no_vias':z.GetDoNotAllowVias()})
out['groups']=[{'name':g.GetName(),'members':[v.GetReference() for v in g.GetItems() if isinstance(v,p.FOOTPRINT)]} for g in b.Groups()]
dst=ROOT/'hardware/docs/reports/ethernet-underlay-analysis-20260925'
dst.mkdir(parents=True,exist_ok=True)
(dst/'geometry.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'j8_shapes':out['j8_shapes'],'j8_zones':out['j8_zones'],'candidates':{k:{a:v[a] for a in ['xy','side','value','footprint']} for k,v in out['footprints'].items()}},ensure_ascii=False))
