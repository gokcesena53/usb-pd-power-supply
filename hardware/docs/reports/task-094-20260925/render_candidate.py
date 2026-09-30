from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4];D=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'.claude/skills/kicad-schematic/scripts'))
from kicadtools import run_cli
src=D/'candidate.kicad_pcb'
for side in ['top','left']:
 r=run_cli(['pcb','render','--output',str(D/('candidate-'+side+'.png')),'--width','1500','--height','1000','--background','opaque','--quality','basic','--side',side,str(src)],keep=src,check=False)
 print(side,r.returncode,r.stdout[-500:],r.stderr[-500:])
for side,layers in [('top','F.Cu,F.Silkscreen,F.Fab,Edge.Cuts'),('bottom','B.Cu,B.Silkscreen,B.Fab,Edge.Cuts')]:
 print(run_cli(['pcb','export','svg','--mode-single','--layers',layers,'--page-size-mode','2','--exclude-drawing-sheet','-o',str(D/('candidate-'+side+'.svg')),str(src)],keep=src).stdout)
for ref in ['J9','J3']:
 print(run_cli(['pcb','export','step','--force','--subst-models','--no-board-body','--component-filter',ref,'--user-origin','0x0mm','-o',str(D/(ref+'.step')),str(src)],keep=src).stdout)
