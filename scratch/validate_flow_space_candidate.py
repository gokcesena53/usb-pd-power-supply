import json, math, hashlib
from pathlib import Path
import pcbnew as p

out=Path('hardware/docs/reports/flow-space-plan-20260928')
source=Path('hardware/gopo.kicad_pcb')
boards=[p.LoadBoard(str(source)),p.LoadBoard(str(out/'candidate/gopo.kicad_pcb'))]
def topology(board):
    return sorted((fp.GetReference(),fp.GetValue(),fp.GetFPIDAsString(),
        tuple(sorted((pad.GetNumber(),pad.GetNetname()) for pad in fp.Pads()))) for fp in board.GetFootprints())
def dist(board,a,n,c,m):
    f={fp.GetReference():fp for fp in board.GetFootprints()}
    pad=lambda r,num:next(pad for pad in f[r].Pads() if pad.GetNumber()==str(num))
    va=pad(a,n).GetPosition();vb=pad(c,m).GetPosition()
    return round(math.hypot(p.ToMM(va.x-vb.x),p.ToMM(va.y-vb.y)),3)
pairs=[('D4',1,'C28',1),('U3',3,'U13',2),('U13',4,'Q4',1)]
result={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'topology_identical':topology(boards[0])==topology(boards[1]),
    'measurements':[{'from':f'{a}.{n}','to':f'{c}.{m}','before_mm':dist(boards[0],a,n,c,m),'candidate_mm':dist(boards[1],a,n,c,m)} for a,n,c,m in pairs]}
base=json.loads((out/'drc.json').read_text(encoding='utf-8'))
cand=json.loads((out/'candidate-drc.json').read_text(encoding='utf-8'))
def keys(report):
    return sorted((v['type'],v['description'],tuple(sorted(x['uuid'] for x in v['items']))) for v in report['violations'])
result['same_drc_violations']=keys(base)==keys(cand)
result['drc']={'baseline':len(base['violations']),'candidate':len(cand['violations']),'candidate_unconnected':len(cand['unconnected_items'])}
result['source_unchanged']=result['source_sha256']==json.loads((out/'board-audit.json').read_text(encoding='utf-8'))['sha256']
(out/'candidate-check.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
