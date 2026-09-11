from pathlib import Path
import math,json
exec(Path('reports/output-update/update_schematic.py').read_text(encoding='utf8').split('exceptions=')[0])
a=Sch('userinterface.kicad_sch');templates={r:copy.deepcopy(a.sym(r)) for r in ['R28','R29','#PWR017']};pg=Sch('powergeneration.kicad_sch')
templates['C']=copy.deepcopy(pg.sym('C14'));templates['L']=copy.deepcopy(pg.sym('L1'))
sheet_instances=copy.deepcopy(one(a.sym('R34'),'instances'))
# Remove only the superseded backlight circuit; leave SPI/encoder unchanged.
remove={'Q5','R28','R29','R30','R31','R32','R33','#PWR017','#PWR036'}
for z in list(a.t):
 typ=tag(z)
 if typ=='symbol' and prop(z,'Reference')[2] in remove:a.t.remove(z)
 elif typ in ['wire','junction','global_label','label']:
  points=[p[1:3] for p in walk(z) if tag(p) in ['at','xy']]
  if points and min(p[1] for p in points)>=152.4 and max(p[0] for p in points)<140:
   # Retain J3 pin39 GND and the anode wire, modifying its net separately.
   if typ=='wire' and min(p[1] for p in points) in [162.56,165.1]:continue
   if typ=='global_label' and z[1]=='BACKLIGHT_3V0':z[1]='BACKLIGHT_4V2';continue
   a.t.remove(z)
for z in list(all(a.t,'text')):
 if 'Backlight needs regulated current' in z[1]:z[1]='4-wire SPI: IM2/IM1/IM0 = 1/1/0.\nRDX and DB0..DB15 tied GND per TFT wiring diagram.'

def custom(name,pins,width=7.62):
 body=f'(symbol "{name}_0_1" (rectangle (start {-width} 10.16) (end {width} -10.16) (stroke (width 0) (type default)) (fill (type background))))'
 pintext=''
 for num,n,x,y,ang,typ in pins:
  pintext+=f'(pin {typ} line (at {x} {y} {ang}) (length 2.54) (name "{n}" (effects (font (size 1.27 1.27)))) (number "{num}" (effects (font (size 1.27 1.27)))))'
 return s.loads(f'(symbol "{name}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes) (property "Reference" "U" (at 0 13.97 0) (effects (font (size 1.27 1.27)))) (property "Value" "{name}" (at 0 11.43 0) (effects (font (size 1.27 1.27)))) {body}(symbol "{name}_1_1" {pintext}))')
u7pins=[('1','FB',10.16,-5.08,180,'input'),('2','EN',-10.16,0,0,'input'),('3','VIN',-10.16,5.08,0,'power_in'),('4','GND',0,-12.7,90,'power_in'),('5','SW',0,12.7,270,'passive'),('6','VOUT',10.16,5.08,180,'power_out')]
u8pins=[('1','LED1',12.7,7.62,180,'passive'),('2','LED2',12.7,2.54,180,'passive'),('3','LED3',12.7,-2.54,180,'passive'),('4','LED4',12.7,-7.62,180,'passive'),('5','GND',0,-12.7,90,'power_in'),('6','EN_PWM',-12.7,2.54,0,'input'),('7','VIN',0,12.7,270,'power_in'),('8','RSET',-12.7,-5.08,0,'passive')]
libs=[custom('TPS61023DRLR',u7pins),custom('CAT4104V-GT3',u8pins,10.16)]
lp=Path('Power_Supply_Custom.kicad_sym');lt=s.loads(lp.read_text(encoding='utf8'))
for z in libs:
 lt.append(copy.deepcopy(z));z[1]='Power_Supply_Custom:'+z[1];one(a.t,'lib_symbols').append(z)
lp.write_text(s.dumps(lt)+'\n',encoding='utf8')

def put(ref,value,x,y,angle,template,footprint=None,libid=None,fields=None):
 z=copy.deepcopy(templates[template]);one(z,'at')[1:]=[x,y,angle]
 if libid:one(z,'lib_id')[1]=libid
 z[:]=[v for v in z if tag(v) not in ['instances','pin']];z.append(copy.deepcopy(sheet_instances))
 for v in walk(z):
  if tag(v)=='uuid':v[1]=uid()
  if tag(v)=='reference':v[1]=ref
 prop(z,'Reference')[2]=ref;prop(z,'Value')[2]=value
 for p in all(z,'property'):one(p,'at')[1:]=[x+3.81,y,0]
 one(prop(z,'Reference'),'at')[1:]=[x+3.81,y-2.54,0]
 if angle in [90,270]:
  one(prop(z,'Reference'),'at')[1:]=[x,y-5.08,90];one(prop(z,'Value'),'at')[1:]=[x,y-2.54,90]
 if ref.startswith('U'):
  one(prop(z,'Reference'),'at')[1:]=[x+5.08,y-17.78,0];one(prop(z,'Value'),'at')[1:]=[x+5.08,y-15.24,0]
 if footprint:field(z,'Footprint',footprint)
 for k,v in (fields or {}).items():field(z,k,v)
 # Copy the source standard library symbol if not already cached.
 lid=one(z,'lib_id')[1]
 if not any(b[1]==lid for b in one(a.t,'lib_symbols')[1:]):one(a.t,'lib_symbols').append(copy.deepcopy(next(b for b in one(pg.t,'lib_symbols')[1:] if b[1]==lid)))
 a.t.append(z);return z
def pin(ref,num):
 z=a.sym(ref);lib=next(b for b in one(a.t,'lib_symbols')[1:] if b[1]==one(z,'lib_id')[1]);p=next(p for p in walk(lib) if tag(p)=='pin' and one(p,'number')[1]==str(num));x,y=one(p,'at')[1:3];at=one(z,'at');t=math.radians(at[3]);return (round(at[1]+x*math.cos(t)+y*math.sin(t),6),round(at[2]-x*math.sin(t)-y*math.cos(t),6))
def wire(p,q):a.wire(*p,*q)
def chain(*ps):
 for p,q in zip(ps,ps[1:]):wire(p,q)
def ground(x,y,ref):
 z=put(ref,'GND',x,y,0,'#PWR017');one(prop(z,'Value'),'at')[1:]=[x,y+3.81,0]
def gl(n,x,y):a.label(n,x,y,True,0)
def loc(n,x,y):a.label(n,x,y,False,0)
put('U7','TPS61023DRLR',63.5,50.8,0,'R29','Package_TO_SOT_SMD:SOT-563','Power_Supply_Custom:TPS61023DRLR',{'MPN':'TPS61023DRLR','Manufacturer':'Texas Instruments','Datasheet':'https://www.ti.com/lit/ds/symlink/tps61023.pdf'})
put('U8','CAT4104V-GT3',66.04,125.73,0,'R29','Package_SO:SOIC-8_3.9x4.9mm_P1.27mm','Power_Supply_Custom:CAT4104V-GT3',{'MPN':'CAT4104V-GT3','Manufacturer':'onsemi','Datasheet':'https://www.onsemi.com/download/data-sheet/pdf/cat4104-d.pdf'})
put('L2','2.2uH',58.42,25.4,90,'L','Inductor_SMD:L_Wuerth_MAPI-4030',fields={'MPN':'74438357022','Manufacturer':'Wurth Elektronik','Datasheet':'https://www.we-online.com/components/products/datasheet/74438357022.pdf'})
for ref,x,y in [('C20',35.56,53.34),('C21',86.36,53.34)]:put(ref,'22uF / 16V X7R',x,y,0,'C','Capacitor_SMD:C_1206_3216Metric',fields={'EffectiveCapacitance':'>=10uF at 3.3V' if ref=='C20' else '4uF..30uF at 4.3V','SelectionNote':'Verify DC-bias curve for final capacitor MPN'})
put('C22','100nF / 16V',86.36,102.87,0,'C','Capacitor_SMD:C_0402_1005Metric')
for ref,val,x,y,ang in [('R44','604kR 0.1%',99.06,53.34,0),('R45','100kR 0.1%',99.06,71.12,0),('R46','3.24kR 0.1%',53.34,153.67,0),('R28','100R',38.1,123.19,90),('R29','100kR',48.26,135.89,0)]:put(ref,val,x,y,ang,'R29','Resistor_SMD:R_0402_1005Metric')
# Boost power path and feedback.
wire(pin('L2',1),(40.64,25.4));chain((40.64,25.4),(40.64,45.72),pin('U7',3));chain(pin('L2',2),(63.5,25.4),pin('U7',5))
chain(pin('C20',1),(35.56,45.72),(40.64,45.72));chain(pin('U7',2),(40.64,50.8),(40.64,45.72))
plus=copy.deepcopy(next(z for z in all(a.t,'symbol') if one(z,'lib_id')[1]=='power:+3.3V'));templates['plus']=plus
z=put('#PWR219','+3.3V',40.64,20.32,0,'plus');one(prop(z,'Value'),'at')[1:]=[40.64,16.51,0];wire((40.64,20.32),(40.64,25.4))
chain(pin('U7',6),(86.36,45.72),(99.06,45.72),(111.76,45.72));gl('BACKLIGHT_4V2',111.76,45.72)
chain(pin('C21',1),(86.36,45.72));chain(pin('R44',1),(99.06,45.72));chain(pin('R44',2),(99.06,63.5),pin('R45',1));chain(pin('U7',1),(78.74,55.88),(78.74,63.5),(99.06,63.5));loc('BL_BOOST_FB',99.06,63.5)
for ref,num,dest,pwr in [('C20',2,(35.56,63.5),'#PWR220'),('C21',2,(86.36,60.96),'#PWR221'),('U7',4,(63.5,68.58),'#PWR222'),('R45',2,(99.06,80.01),'#PWR223')]:wire(pin(ref,num),dest);ground(*dest,pwr)
loc('BL_BOOST_SW',63.5,30.48)
# Four independently regulated cathodes, controlled by existing PWM.
chain(pin('U8',7),(66.04,93.98),(86.36,93.98),pin('C22',1));gl('BACKLIGHT_4V2',66.04,93.98)
wire(pin('C22',2),(86.36,111.76));ground(86.36,111.76,'#PWR224')
wire(pin('U8',5),(66.04,143.51));ground(66.04,143.51,'#PWR225')
chain(pin('U8',8),(53.34,146.05),pin('R46',1));wire(pin('R46',2),(53.34,162.56));ground(53.34,162.56,'#PWR226')
chain(pin('R28',1),(24.13,123.19));gl('TFT_BL_PWM',24.13,123.19)
one(next(z for z in all(a.t,'global_label') if z[1]=='TFT_BL_PWM'),'shape')[1]=S('input')
chain(pin('R28',2),(48.26,123.19),pin('U8',6));chain((48.26,123.19),pin('R29',1));wire(pin('R29',2),(48.26,144.78));ground(48.26,144.78,'#PWR227')
for i in range(1,5):
 p=pin('U8',i);wire(p,(86.36,p[1]));loc('BL_K'+str(i),86.36,p[1]);q=pin('J3',33+i);wire(q,(125.73,q[1]));loc('BL_K'+str(i),125.73,q[1])
note(a,'BACKLIGHT: 4 x ~40mA constant-current sinks.\nR46 from CAT4104 nonlinear RSET equation.\nPWM: 1kHz recommended; duty 0 or >=1%.',20.32,180.34)
note(a,'BOOST: +3.3V -> ~4.2V; 0.20A output design.\nC20 effective >=10uF; C21 effective 4..30uF.\nR/C 0402 except boost bulk C20/C21 (1206).',20.32,7.62)
# Junction dots at actual multi-way wire meetings.
for x,y in [(40.64,25.4),(40.64,45.72),(86.36,45.72),(99.06,45.72),(99.06,63.5),(48.26,123.19)]:a.add(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
a.save()
print('Added U7/U8/L2/C20..22/R44..46; reused R28/R29; removed Q5/R30..33')
