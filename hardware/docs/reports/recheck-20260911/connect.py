from pathlib import Path
exec(Path('reports/output-update/update_schematic.py').read_text(encoding='utf8').split('exceptions=')[0])
p=Sch('usb_pd_controller.kicad_sch')
for x,y,a,b in [(115.57,74.93,127.635,74.93),(205.105,62.865,221.615,62.865),(207.01,33.02,223.52,33.02),(240.03,62.865,257.81,62.865),(241.935,33.02,259.715,33.02)]:p.wire(x,y,a,b)
lab=next(z for z in all(p.t,'global_label') if z[1]=='USB_VBUS' and one(z,'at')[2]==97.155)
print('VBUS label',one(lab,'at'))
for z in list(all(p.t,'wire')):
 a,b=one(z,'pts')[1:3]
 if a[2]==b[2]==97.155 and min(a[1],b[1])>=190 and max(a[1],b[1])<=229.235:p.t.remove(z)
p.wire(*one(lab,'at')[1:3],229.235,97.155);p.save()
sch=Sch('userinterface.kicad_sch')
src=Path('reports/output-update/update_schematic.py').read_text(encoding='utf8')
segment=src.split(" if f.name=='userinterface.kicad_sch':")[1].split(' sch.save()')[0]
exec('\n'.join(line[2:] for line in segment.splitlines()))
# Replace the newly added GND net label with an actual GND power symbol.
lab=next(z for z in all(sch.t,'global_label') if z[1]=='GND' and one(z,'at')[1]==127.635)
x,y=one(lab,'at')[1:3];sch.t.remove(lab)
pw=copy.deepcopy(next(z for z in all(sch.t,'symbol') if one(z,'lib_id')[1]=='power:GND'))
old=one(pw,'at');dx=x-old[1];dy=y+5.08-old[2];old[1:]=[x,y+5.08,0]
for z in walk(pw):
 if tag(z)=='uuid':z[1]=uid()
 if tag(z)=='reference':z[1]='#PWR218'
for z in all(pw,'property'):
 at=one(z,'at');at[1]+=dx;at[2]+=dy
prop(pw,'Reference')[2]='#PWR218';sch.t.append(pw);sch.wire(x,y,x,y+5.08)
for z in all(sch.t,'text'):
 if z[1].startswith('4-wire SPI:'):one(z,'at')[2]=167.64
sch.save()
