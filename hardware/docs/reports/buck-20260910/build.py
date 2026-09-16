from pathlib import Path
import sexpdata as s,copy,uuid,hashlib,json,math
S=s.Symbol
def tag(z):return str(z[0]) if isinstance(z,list) and z else ''
def one(z,k):return next(a for a in z if tag(a)==k)
def prop(z,k):return next(a for a in z if tag(a)=='property' and a[1]==k)
def uid():return str(uuid.uuid4())
base=Path('reports/buck-20260910');p=Path('powergeneration.kicad_sch');raw=p.read_text(encoding='utf8');(base/'powergeneration.before.kicad_sch').write_text(raw,encoding='utf8')
hashes={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('.').glob('*.kicad_sch') if f!=p};(base/'unrelated-hashes.json').write_text(json.dumps(hashes),encoding='utf8')
old=s.loads(raw);libs=one(old,'lib_symbols');u=next(a for a in old if tag(a)=='symbol' and prop(a,'Reference')[2]=='U5');path=one(one(one(u,'instances'),'project'),'path')[1];project=one(one(u,'instances'),'project')[1]
t=[old[0]]+[copy.deepcopy(a) for a in old[1:] if tag(a) in ['version','generator','generator_version','uuid','paper']];t.append(copy.deepcopy(libs));lib=one(t,'lib_symbols')
def add(txt):a=s.loads(txt);t.append(a);return a
def ensure(id):
 for a in lib[1:]:
  if a[1]==id:return a
 file,name=id.split(':');lt=s.loads((Path('C:/Program Files/KiCad/10.0/share/kicad/symbols')/(file+'.kicad_sym')).read_text(encoding='utf8'));a=copy.deepcopy(next(z for z in lt if tag(z)=='symbol' and z[1]==name));a[1]=id;lib.append(a);return a
def component(id,ref,value,x,y,angle=0,foot='',notes=''):
 definition=ensure(id)
 text=f'(symbol (lib_id "{id}") (at {x} {y} {angle}) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid()}")'
 for name,val,px,py,hide in [('Reference',ref,x+3.81,y-1.27,False),('Value',value,x+3.81,y+1.27,False),('Footprint',foot,x,y,True),('DesignNote',notes,x,y,True)]:
  text+=f'(property "{name}" {s.dumps(val)} (at {px} {py} 0)'+(' (hide yes)' if hide else '')+' (effects (font (size 1.27 1.27)) (justify left)))'
 text+=f'(instances (project {s.dumps(project)} (path "{path}" (reference "{ref}") (unit 1)))))'
 return add(text)
def wire(x,y,a,b):
 if (x,y)!=(a,b):add(f'(wire (pts (xy {x} {y}) (xy {a} {b})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
def label(n,x,y,glob=False):add(f'({"global_label" if glob else "label"} "{n}" '+('(shape input)' if glob else '')+f' (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}"))')
pn=60
def power(name,x,y):
 global pn
 pn+=1;a=component('power:'+name,'#PWR0'+str(pn),name,x,y)
 prop(a,'Reference').append([S('hide'),S('yes')]);at=one(prop(a,'Value'),'at');at[1:]=[x,y+(3.81 if name=='GND' else -3.81),0];one(prop(a,'Value'),'effects')[-1]=[S('justify'),S('center')]
 return a
def note(text,x,y,size=1.27):add(f'(text {s.dumps(text)} (at {x} {y} 0) (effects (font (size {size} {size})) (justify left top)) (uuid "{uid()}"))')
capfoot='Capacitor_SMD:C_1210_3225Metric';rfoot='Resistor_SMD:R_0603_1608Metric'
u=copy.deepcopy(u);one(u,'at')[1:]=[127,76.2,0]
for a in [a for a in u if tag(a)=='property']:
 one(a,'at')[1:]=[127,63.5 if a[1]=='Reference' else 66.04,0]
t.append(u)
# Input decoupling bank and VIN exposed pad.
label('PD_VOUT',45.72,50.8,True)
for a,b in [(45.72,60.96),(60.96,78.74),(78.74,96.52),(96.52,110.49)]:wire(a,50.8,b,50.8)
for ref,x,val,foot in [('C12',60.96,'10uF / 50V',capfoot),('C13',78.74,'10uF / 50V',capfoot),('C14',96.52,'100nF / 50V','Capacitor_SMD:C_0603_1608Metric')]:
 component('Device:C',ref,val,x,60.96,foot=foot,notes='X7R; C12+C13 effective capacitance >=10uF at 28V; verify actual MPN')
 wire(x,50.8,x,57.15);wire(x,64.77,x,68.58);power('GND',x,68.58)
wire(110.49,50.8,110.49,71.12);wire(110.49,71.12,116.84,71.12)
# Compact switching loop.
component('Device:C','C17','100nF / 16V',147.32,71.12,90,'Capacitor_SMD:C_0603_1608Metric')
for k,py in [('Reference',66.04),('Value',68.58)]:one(prop(t[-1],k),'at')[1:]=[147.32,py,0]
wire(137.16,71.12,143.51,71.12);wire(151.13,71.12,158.75,71.12);wire(158.75,71.12,158.75,76.2)
wire(137.16,76.2,158.75,76.2);wire(158.75,76.2,167.64,76.2);label('LX_SW',153.67,76.2)
component('Device:L','L1','22uH',171.45,76.2,90,notes='Isat >=2A and Irms >=1.5A at max temperature; fault current capability UNRESOLVED')
for k,py in [('Reference',68.58),('Value',71.12)]:one(prop(t[-1],k),'at')[1:]=[171.45,py,0]
wire(175.26,76.2,195.58,76.2);wire(195.58,76.2,203.2,76.2);wire(203.2,76.2,218.44,76.2);power('+3.3V',218.44,76.2)
component('Device:D_Schottky','D2','60V / 2A',158.75,88.9,90,notes='Cathode LX; anode GND. VF/thermal/surge MPN qualification UNRESOLVED')
# Device:D_Schottky cathode starts at x=-3.81; 90deg puts cathode below.
one(t[-1],'at')[3]=270
wire(158.75,76.2,158.75,85.09);wire(158.75,92.71,158.75,99.06);power('GND',158.75,99.06)
for ref,x in [('C15',195.58),('C16',218.44)]:
 component('Device:C',ref,'47uF / 10V',x,88.9,foot=capfoot,notes='X7R; bank effective Cout >=44uF at 3.3V; actual C/ESR UNRESOLVED')
 wire(x,76.2,x,85.09);wire(x,92.71,x,99.06);power('GND',x,99.06)
wire(127,86.36,127,93.98);power('GND',127,93.98)
# Feedback senses the output, not LX.
wire(203.2,76.2,203.2,116.84)
component('Device:R','R39','10kR 0.1%',203.2,120.65,foot=rfoot)
wire(203.2,124.46,203.2,130.81);wire(203.2,130.81,203.2,134.62)
component('Device:R','R40','3.20kR 0.1%',203.2,138.43,foot=rfoot);wire(203.2,142.24,203.2,148.59);power('GND',203.2,148.59)
wire(137.16,81.28,142.24,81.28);wire(142.24,81.28,142.24,130.81);wire(142.24,130.81,203.2,130.81);label('FB_3V3',175.26,130.81)
# Low-current control functions use local labels for separation from LX.
for pin_y,net in [(73.66,'EN_CTRL'),(76.2,'SS_RAMP'),(78.74,'FSW_SET'),(81.28,'COMP_NODE')]:wire(116.84,pin_y,104.14,pin_y);label(net,104.14,pin_y)
for ref,id,val,x,y,net in [('R38','Device:R','100kR 1%',50.8,120.65,'FSW_SET'),('C18','Device:C','10nF',81.28,120.65,'SS_RAMP'),('R42','Device:R','100kR',111.76,120.65,'EN_CTRL')]:
 component(id,ref,val,x,y,foot=rfoot if id=='Device:R' else 'Capacitor_SMD:C_0603_1608Metric');wire(x,110.49,x,y-3.81);label(net,x,110.49);wire(x,y+3.81,x,132.08);power('GND',x,132.08)
component('Device:R','R41','UNRESOLVED',50.8,154.94,90,foot=rfoot)
for k,py in [('Reference',148.59),('Value',151.13)]:one(prop(t[-1],k),'at')[1:]=[46.99,py,0]
label('COMP_NODE',38.1,154.94);wire(38.1,154.94,46.99,154.94);wire(54.61,154.94,73.66,154.94)
component('Device:C','C19','UNRESOLVED',77.47,154.94,90,foot='Capacitor_SMD:C_0603_1608Metric')
for k,py in [('Reference',148.59),('Value',151.13)]:one(prop(t[-1],k),'at')[1:]=[73.66,py,0]
wire(81.28,154.94,93.98,154.94);power('GND',93.98,154.94)
note('INTERNAL 3.3V BUCK — 5..28V INPUT / 1A DESIGN LOAD',38.1,25.4,1.8)
note('VIN = EXPOSED PAD 9: PD_VOUT, NOT GND.\nEN requires independent 1.2..5V bias. DO NOT connect to PD_VOUT.\nCOMP values UNRESOLVED: datasheet GEA / Cc equations conflict.\nRF=100k: table 500kHz; equation 476.19kHz. Actual range UNRESOLVED.',38.1,172.72)
note('L/D MPN + footprints: UNRESOLVED\nIsat >=2A normal load; fault capability unverified\nCout effective >=44uF; DC bias must be checked',165.1,157.48)
# Explicit junctions on every branch, excluding simple bends.
pts={}
for z in t:
 if tag(z)=='wire':
  for a in one(z,'pts')[1:]:pts[tuple(a[1:])]=pts.get(tuple(a[1:]),0)+1
for (x,y),n in pts.items():
 if n>=3:add(f'(junction (at {x} {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
p.write_text('(kicad_sch\n'+'\n'.join(s.dumps(a) for a in t[1:])+'\n)\n',encoding='utf8')
assert all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in hashes.items())
print('Saved powergeneration only; other schematic hashes unchanged.')
