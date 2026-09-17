from pathlib import Path
import re, uuid, copy
import sexpdata as s
p=Path('userinterface.kicad_sch')
raw=p.read_text(encoding='utf-8')
Path('.codex-encoder/userinterface.before.kicad_sch').write_text(raw,encoding='utf-8')
tree=s.loads(raw)
def items(t,k): return [v for v in t if isinstance(v,list) and v and str(v[0])==k]
def one(t,k): return items(t,k)[0]
def uid(): return str(uuid.uuid4())
def prop(t,k): return next(v for v in items(t,'property') if v[1]==k)
syms=items(tree,'symbol')
template=next(v for v in syms if prop(v,'Reference')[2]=='R29')
added=[]
def add(txt): added.append(txt)
def wire(x,y,a,b): add(f'(wire (pts (xy {x} {y}) (xy {a} {b})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
def label(n,x,y,angle=0):
 add(f'(global_label "{n}" (shape passive) (at {x} {y} {angle}) (effects (font (size 1.27 1.27)) (justify {"left" if angle==0 else "right"})) (uuid "{uid()}"))')
def resistor(ref,x,y):
 t=copy.deepcopy(template); old=one(t,'at'); dx=x-old[1];dy=y-old[2];old[1:]=[x,y,0]
 def walk(z):
  for a in z:
   if isinstance(a,list) and a:
    if str(a[0])=='uuid': a[1]=uid()
    else: walk(a)
 walk(t)
 for a in items(t,'property'):
  at=one(a,'at');at[1]+=dx;at[2]+=dy;at[3]=0
 prop(t,'Reference')[2]=ref;prop(t,'Value')[2]='10k'
 prop(t,'Footprint')[2]='Resistor_SMD:R_0603_1608Metric'
 one(one(one(t,'instances'),'project'),'path')[2][1]=ref
 added.append(s.dumps(t))
 wire(x,y-3.81,x,y-8.89);label('+3.3V',x,y-8.89)
 wire(x,y+3.81,x,y+8.89)
 return x,y+8.89
# Preserve the existing symbol and its pin/footprint mapping; annotate it.
raw=raw.replace('(property "Reference" "SW"','(property "Reference" "SW3"').replace('(reference "SW")','(reference "SW3")')
wire(216.535,93.345,203.2,93.345);label('ENCODER_A',203.2,93.345,180)
wire(216.535,103.505,203.2,103.505);label('ENCODER_B',203.2,103.505,180)
label('GND',216.535,98.425,180)
wire(239.395,97.155,250.19,97.155);label('ENCODER_SW',250.19,97.155)
wire(239.395,99.695,246.38,99.695);wire(246.38,99.695,246.38,110.49);label('GND',246.38,110.49)
for ref,x,net in [('R34',190.5,'ENCODER_A'),('R35',223.52,'ENCODER_B'),('R36',256.54,'ENCODER_SW')]:
 a,b=resistor(ref,x,137.16);label(net,a,b)
add(f'(text "ENCODER: A=GPIO22, B=GPIO23, SW=GPIO21\\n3.3V pull-ups; contacts close to GND.\\nFirmware: quadrature state decoding and switch debounce required." (at 182.88 158.75 0) (effects (font (size 1.27 1.27)) (justify left top)) (uuid "{uid()}"))')
raw=raw.rstrip();raw=raw[:-1]+'\n'+'\n'.join(added)+'\n)\n'
s.loads(raw)
p.write_text(raw,encoding='utf-8')
print('Connected SW3; added R34-R36.')

