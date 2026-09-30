import pcbnew as p
from pathlib import Path
b=p.LoadBoard(str(Path(__file__).resolve().parents[4]/'hardware/gopo.kicad_pcb'))
for ref in 'J7 D3 D8 D9 R62 R63 U10 C3 U1'.split():
 f=next(f for f in b.GetFootprints() if f.GetReference()==ref)
 print(ref,f.GetValue(),tuple(round(v,3) for v in p.ToMM(f.GetPosition())),f.GetOrientationDegrees(),f.GetLayerName())
 for a in f.Pads():print(' ',a.GetNumber(),a.GetNetname(),tuple(round(v,3) for v in p.ToMM(a.GetPosition())))
