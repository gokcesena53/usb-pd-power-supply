from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import run_cli
src=D/'candidate.kicad_pcb';data=json.loads((D/'placement.json').read_text());targets=data['targets']
if '--final' in sys.argv:src=ROOT/'hardware/gopo.kicad_pcb'
for side in ['top','bottom']:
 r=run_cli(['pcb','render','-o',str(D/(side+'.png')),'--width','1600','--height','1100','--background','opaque','--quality','basic','--side',side,str(src)],keep=src)
 print(side,r.returncode)
 layers=('F' if side=='top' else 'B')+'.Cu,'+('F' if side=='top' else 'B')+'.Silkscreen,Edge.Cuts'
 run_cli(['pcb','export','svg','--mode-single','--layers',layers,'--page-size-mode','2','--exclude-drawing-sheet','-o',str(D/(side+'.svg')),str(src)],keep=src)
if '--images-only' in sys.argv:sys.exit(0)
for ref in [r for r in targets if not r.startswith('TP')]+['J8','MECH_ENC','J9']:
 run_cli(['pcb','export','step','--force','--subst-models','--no-board-body','--component-filter',ref,'--user-origin','0x0mm','-o',str(D/(ref+'.step')),str(src)],keep=src)
 print('STEP',ref,flush=True)
refs=','.join(r for r in data['before'] if r not in targets)
run_cli(['pcb','export','step','--force','--subst-models','--no-board-body','--component-filter',refs,'--user-origin','0x0mm','-o',str(D/'stationary.step'),str(src)],keep=src)
