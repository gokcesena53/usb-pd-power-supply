"""TASK-070 relative B.Cu placement around the existing J7 anchor."""
from pathlib import Path
import pcbnew as p

path=Path(__file__).resolve().parents[4]/'hardware/gopo.kicad_pcb'
b=p.LoadBoard(str(path))
# J7 is a temporary mechanical anchor; TASK-063 will move the whole group to board edge.
targets={
 'D3': (40.0,87.0,-90),
 'D8': (33.0,74.0,180),
 'D9': (33.0,80.9,180),
 'R62': (29.0,74.0,180),
 'R63': (29.0,80.9,180),
 'U10': (32.7,77.3,180),
}
reference_positions={'D9':(33.0,83.7),'U10':(28.8,77.3)}
for f in b.GetFootprints():
 if f.GetReference() in targets:
  x,y,a=targets[f.GetReference()]
  f.SetOrientationDegrees(a)
  f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
  if f.GetReference() in reference_positions:
   rx,ry=reference_positions[f.GetReference()]
   f.Reference().SetPosition(p.VECTOR2I(p.FromMM(rx),p.FromMM(ry)))
p.SaveBoard(str(path),b)
