"""Create a review-only candidate; never write the working PCB."""
import json
from pathlib import Path
import pcbnew as p

out = Path('hardware/docs/reports/flow-space-plan-20260928/candidate')
out.mkdir(parents=True, exist_ok=True)
source = Path('hardware/gopo.kicad_pcb')
b = p.LoadBoard(str(source))
f = {x.GetReference():x for x in b.GetFootprints()}
moves = {'C28':(107.5,118.75,270), 'U13':(129,120.1,0), 'C35':(132.16,121,0), 'R61':(125.82,121,180)}
changes=[]
for ref,(x,y,angle) in moves.items():
    fp=f[ref]
    pos=fp.GetPosition()
    before=[p.ToMM(pos.x),p.ToMM(pos.y),fp.GetOrientationDegrees()]
    fp.SetOrientationDegrees(angle)
    fp.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
    changes.append({'ref':ref,'before':before,'candidate':[x,y,angle]})
p.SaveBoard(str(out/'gopo.kicad_pcb'),b)
for ext in ['kicad_pro','kicad_dru']:
    (out/f'gopo.{ext}').write_bytes(Path(f'hardware/gopo.{ext}').read_bytes())
lib=Path('hardware/fp-lib-table').read_text(encoding='utf-8')
lib=lib.replace('${KIPRJMOD}',Path('hardware').resolve().as_posix())
(out/'fp-lib-table').write_text(lib,encoding='utf-8')
(out/'moves.json').write_text(json.dumps(changes,indent=2),encoding='utf-8')
print(json.dumps(changes,indent=2))
