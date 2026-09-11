from pathlib import Path
exec(Path('reports/fixes-20260909/fix.py').read_text(encoding='utf8').split('pd=Sch(')[0])
edits={'mcu.kicad_sch':{((143.51,86.36),(168.91,86.36)):((161.29,86.36),(168.91,86.36)),((143.51,88.9),(168.91,88.9)):((161.29,88.9),(168.91,88.9)),((259.08,102.87),(259.08,111.76)):((259.08,102.87),(259.08,109.22))},'usb_pd_controller.kicad_sch':{((72.39,160.02),(72.39,162.56)):((72.39,160.02),(72.39,161.29)),((87.63,142.24),(87.63,144.78)):((87.63,142.24),(87.63,143.51)),((119.38,57.15),(133.35,57.15)):((119.38,57.15),(124.46,57.15))}}
for f,mapping in edits.items():
 a=Sch(f)
 for z in all(a.t,'wire'):
  pts=one(z,'pts');key=tuple(tuple(p[1:]) for p in pts[1:])
  if key in mapping:
   for p,xy in zip(pts[1:],mapping[key]):p[1:]=list(xy)
 a.save()
lib=s.loads(Path('C:/Program Files/KiCad/10.0/share/kicad/symbols/power.kicad_sym').read_text(encoding='utf8'))
flag=copy.deepcopy(next(z for z in all(lib,'symbol') if z[1]=='PWR_FLAG'));flag[1]='power:PWR_FLAG'
for f,ref,source,dest in [('usb_pd_controller.kicad_sch','#FLG01',(76.2,45.72),(69.85,45.72)),('usb_pd_controller.kicad_sch','#FLG02',(128.27,62.23),(135.89,62.23)),('usb_pd_controller.kicad_sch','#FLG03',(113.03,97.79),(106.68,97.79)),('powergeneration.kicad_sch','#FLG04',(195.58,76.2),(195.58,69.85)),('mcu.kicad_sch','#FLG05',(234.95,52.07),(234.95,45.72))]:
 a=Sch(f);ls=one(a.t,'lib_symbols')
 if not any(z[1]=='power:PWR_FLAG' for z in ls[1:]):ls.append(copy.deepcopy(flag))
 p=copy.deepcopy(next(z for z in all(a.t,'symbol') if one(z,'lib_id')[1]=='power:GND'))
 one(p,'lib_id')[1]='power:PWR_FLAG';one(p,'at')[1:]=[*dest,0];prop(p,'Reference')[2]=ref;prop(p,'Value')[2]='PWR_FLAG'
 for z in walk(p):
  if tag(z)=='uuid':z[1]=uid()
  if tag(z)=='reference':z[1]=ref
 for z in all(p,'property'):
  one(z,'at')[1:]=[dest[0],dest[1]-3.81,0]
 a.t.append(p);a.wire(*source,*dest)
 if not any(one(z,'at')[1:3]==list(source) for z in all(a.t,'junction')):a.add(f'(junction (at {source[0]} {source[1]}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
 a.save()
