from pathlib import Path
exec(Path('reports/fixes-20260909/fix.py').read_text(encoding='utf8').split('pd=Sch(')[0])
a=Sch('usb_c_input.kicad_sch')
a.add(f'(junction (at 213.36 111.76) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
a.save()
