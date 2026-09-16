from pathlib import Path
exec(Path('reports/output-update/update_schematic.py').read_text(encoding='utf8').split('exceptions=')[0])
u=Sch('userinterface.kicad_sch');field(u.sym('Q5'),'Footprint','Package_TO_SOT_SMD:SOT-23');field(u.sym('Q5'),'Datasheet','https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf')
# Join to existing BL_SINK wire, avoiding two overlapping label texts.
lab=next(z for z in all(u.t,'global_label') if z[1]=='BL_SINK' and one(z,'at')[3]==0)
x,y=one(lab,'at')[1:3];u.t.remove(lab);u.wire(x,y,x,156.845);u.wire(x,156.845,67.31,156.845)
pw=u.sym('#PWR218');old=one(pw,'at');dx=119.38-old[1];dy=100.965-old[2];old[1:]=[119.38,100.965,0]
for z in all(pw,'property'):
 a=one(z,'at');a[1]+=dx;a[2]+=dy
for z in list(all(u.t,'wire')):
 a,b=one(z,'pts')[1:3]
 if abs(a[1]-127.635)<.001 and abs(b[1]-127.635)<.001 and abs(a[2]-139.065)<.001 and abs(b[2]-144.145)<.001:u.t.remove(z)
u.wire(119.38,100.965,127.635,100.965)
u.save()
m=Sch('mcu.kicad_sch');note(m,'BT1: L-KLS5-CR2032-05-R1 holder.\nCR2032 primary cell: disable RTC trickle charge.\nPad 1 positive, pad 2 GND.',182.88,22.86);m.save()
