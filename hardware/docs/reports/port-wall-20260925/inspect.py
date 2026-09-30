from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import ensure_pcbnew
p=ensure_pcbnew()
b=p.LoadBoard(str(ROOT/'hardware/gopo.kicad_pcb'))
def xy(v): return [v.x/1e6,v.y/1e6]
def box(v): return [x/1e6 for x in [v.GetX(),v.GetY(),v.GetRight(),v.GetBottom()]]
for ref in ['J7','J8','J9','H1','H3','C20','Q8','U2']:
 f=b.FindFootprintByReference(ref)
 print(ref,xy(f.GetPosition()),f.GetOrientationDegrees(),b.GetLayerName(f.GetLayer()),f.GetFPID().GetLibItemName())
 if ref in ['J7','J8']:
  for pad in f.Pads(): print('pad',pad.GetNumber(),box(pad.GetBoundingBox()),xy(pad.GetDrillSize()))
  for g in f.GraphicalItems():
   if g.GetLayer() in [p.Edge_Cuts,p.F_Fab,p.B_Fab]:
    print('graphic',b.GetLayerName(g.GetLayer()),getattr(g,'GetText',lambda:'' )(),box(g.GetBoundingBox()))
  for m in f.Models(): print('model',m.m_Filename)
for g in b.GetDrawings():
 if g.GetLayer()==p.Edge_Cuts: print('edge',g.GetShapeStr(),xy(g.GetStart()),xy(g.GetEnd()))
