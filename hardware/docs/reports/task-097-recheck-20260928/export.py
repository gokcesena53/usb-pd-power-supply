from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import run_cli
src=D/'candidate.kicad_pcb'; board=json.loads((D/'board.json').read_text());refs=['C5','C6','C7','R1','R2','R3']
for side in ['top','bottom']:
 for which,pcb in [('actual',ROOT/'hardware/gopo.kicad_pcb'),('candidate',src)]:
  layers=('F' if side=='top' else 'B')+'.Cu,'+('F' if side=='top' else 'B')+'.Silkscreen,Edge.Cuts'
  run_cli(['pcb','export','svg','--mode-single','--layers',layers,'--page-size-mode','2','--exclude-drawing-sheet','-o',str(D/(which+'-'+side+'.svg')),str(pcb)],keep=pcb)
run_cli(['pcb','render','-o',str(D/'candidate-top.png'),'--width','1600','--height','1100','--background','opaque','--quality','basic','--side','top',str(src)],keep=src)
for ref in refs:
 run_cli(['pcb','export','step','--force','--subst-models','--no-board-body','--component-filter',ref,'--user-origin','0x0mm','-o',str(D/(ref+'.step')),str(src)],keep=src)
 print(ref,flush=True)
run_cli(['pcb','export','step','--force','--subst-models','--no-board-body','--component-filter',','.join(r for r in board if r not in refs),'--user-origin','0x0mm','-o',str(D/'stationary.step'),str(src)],keep=src)
