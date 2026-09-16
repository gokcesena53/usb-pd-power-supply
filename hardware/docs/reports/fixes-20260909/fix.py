from pathlib import Path
import sexpdata as s,copy,uuid
S=s.Symbol
def tag(z):return str(z[0]) if isinstance(z,list) and z else ''
def all(z,k):return [a for a in z if tag(a)==k]
def one(z,k):return next(a for a in z if tag(a)==k)
def prop(z,k):return next(a for a in all(z,'property') if a[1]==k)
def uid():return str(uuid.uuid4())
def walk(z):
 yield z
 for a in z:
  if isinstance(a,list):yield from walk(a)
class Sch:
 def __init__(self,f):
  self.p=Path(f);self.raw=self.p.read_text(encoding='utf8');self.t=s.loads(self.raw);self.orig={id(a):s.dumps(a) for a in self.t if isinstance(a,list)}
 def sym(self,r):return next(a for a in all(self.t,'symbol') if prop(a,'Reference')[2]==r)
 def add(self,txt):self.t.append(s.loads(txt))
 def wire(self,x,y,a,b):
  if (x,y)!=(a,b):self.add(f'(wire (pts (xy {x} {y}) (xy {a} {b})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
 def label(self,n,x,y,global_=True,angle=0):self.add(f'({"global_label" if global_ else "label"} "{n}" '+('(shape passive) ' if global_ else '')+f'(at {x} {y} {angle}) (effects (font (size 1.27 1.27)) (justify {"left" if angle==0 else "right"})) (uuid "{uid()}"))')
 def save(self):
  # Preserve all unmodified top-level elements verbatim.
  spans=[];depth=0;quoted=False;escape=False;start=0
  for i,c in enumerate(self.raw):
   if quoted:
    if escape:escape=False
    elif c=='\\':escape=True
    elif c=='"':quoted=False
   elif c=='"':quoted=True
   elif c=='(':
    depth+=1
    if depth==2:start=i
   elif c==')':
    if depth==2:spans.append((start,i+1))
    depth-=1
  originals=list(self.orig);byid={id(a):a for a in self.t if isinstance(a,list)};raw=self.raw
  for ident,(a,b) in reversed(list(zip(originals,spans))):
   val=byid.get(ident);out='' if val is None else s.dumps(val)
   if out!=self.orig[ident]:raw=raw[:a]+out+raw[b:]
  extra=[s.dumps(a) for a in self.t if isinstance(a,list) and id(a) not in self.orig]
  if extra:raw=raw.rstrip()[:-1]+'\n'+'\n'.join(extra)+'\n)\n'
  s.loads(raw);self.p.write_text(raw,encoding='utf8')
pd=Sch('usb_pd_controller.kicad_sch');m=Sch('mcu.kicad_sch');ui=Sch('userinterface.kicad_sch');root=Sch('masaüstü güç kaynağı.kicad_sch')
# Use the project's existing global-net convention consistently.
for z in all(pd.t,'hierarchical_label'):
 n=z[1];at=one(z,'at');pd.t.remove(z);pd.label(n,64.77,64.77 if n=='USB_CC1' else 67.31,True,180)
for z in all(root.t,'sheet'):
 if prop(z,'Sheetfile')[2]=='usb_pd_controller.kicad_sch':
  z[:]=[a for a in z if tag(a)!='pin']
for z in all(pd.t,'global_label'):
 if z[1]=='TYPE-C KONNEKTÖRÜ':pd.t.remove(z)
pd.wire(223.52,97.155,235.585,97.155)
pd.wire(115.57,74.93,128.27,74.93)
for x,a,y in [(205.74,222.25,62.865),(240.03,257.81,62.865),(206.375,222.885,33.02),(241.935,259.715,33.02)]:pd.wire(x,y,a,y)
# LED pin polarity, preserve wire endpoints and field locations.
one(pd.sym('D1'),'at')[3]=180
for ref in ['R8','R9','R14']:prop(pd.sym(ref),'Footprint')[2]='Resistor_SMD:R_0603_1608Metric'
# RTC clock label was adjacent to, not on, the clock wire.
for z in all(m.t,'label'):
 if z[1]=='RTC_SCL' and one(z,'at')[1]>200:one(z,'at')[1:3]=[255.905,111.125]
 if z[1]=='':m.t.remove(z)
j=m.sym('J1');prop(j,'Reference')[2]='J2';prop(j,'Footprint')[2]='CONNFLY_DS1021-1X3SF11-B:CONNFLY_DS1021-1X3SF11-B'
for a in walk(j):
 if tag(a)=='reference':a[1]='J2'
ui.wire(57.785,156.845,67.945,156.845)
# GPIO8 must be high when GPIO9 is pulled low for download mode.
r=copy.deepcopy(m.sym('R23'));old=one(r,'at');dx=153.67-old[1];dy=98.425-old[2];old[1:]=[153.67,98.425,0]
for a in walk(r):
 if tag(a)=='uuid':a[1]=uid()
 if tag(a)=='reference':a[1]='R37'
for a in all(r,'property'):
 at=one(a,'at');at[1]+=dx;at[2]+=dy
prop(r,'Reference')[2]='R37';prop(r,'Value')[2]='10kR';prop(r,'Footprint')[2]='Resistor_SMD:R_0603_1608Metric';m.t.append(r)
m.wire(153.67,102.235,153.67,106.045)
# existing GPIO8 wire is split at the new branch junction.
for z in all(m.t,'wire'):
 pts=one(z,'pts');a,b=pts[1][1:],pts[2][1:]
 if a[1]==b[1]==106.045 and min(a[0],b[0])<153.67<max(a[0],b[0]):
  m.t.remove(z);m.wire(*a,153.67,106.045);m.wire(153.67,106.045,*b)
m.add(f'(junction (at 153.67 106.045) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
power=copy.deepcopy(m.sym('#PWR032'));a=one(power,'at');dx=153.67-a[1];dy=90.805-a[2];a[1:]=[153.67,90.805,0]
for z in walk(power):
 if tag(z)=='uuid':z[1]=uid()
 if tag(z)=='reference':z[1]='#PWR048'
for z in all(power,'property'):
 a=one(z,'at');a[1]+=dx;a[2]+=dy;a[3]=0
prop(power,'Reference')[2]='#PWR048';m.t.append(power);m.wire(153.67,90.805,153.67,94.615)
# Fix impractical placeholder packages without claiming a selected BOM.
prop(m.sym('C5'),'Footprint')[2]='Capacitor_SMD:C_0805_2012Metric'
for f in [pd,m,ui,root]:f.save()
print('Connectivity repairs saved.')
