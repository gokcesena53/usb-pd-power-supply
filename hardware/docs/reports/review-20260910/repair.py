from pathlib import Path
import math, json
exec(Path('reports/fixes-20260909/fix.py').read_text(encoding='utf8').split("pd=Sch(")[0])
b=Sch('powergeneration.kicad_sch'); pd=Sch('usb_pd_controller.kicad_sch'); ui=Sch('userinterface.kicad_sch'); sense=Sch('powersensing.kicad_sch')
# Use only the helper function definitions from the earlier builder, never its mutations.
src=Path('reports/buck-20260910/build.py').read_text(encoding='utf8')
t=b.t; lib=one(t,'lib_symbols'); u=b.sym('U5'); project=one(one(u,'instances'),'project')[1]; path=one(one(one(u,'instances'),'project'),'path')[1]
exec(src[src.index('def add('):src.index('capfoot=')])
pn=100
oldpower=power
def power(name,x,y):
 a=oldpower(name,x,y);e=one(prop(a,'Value'),'effects');e[:]=[v for v in e if tag(v)!='justify'];return a
for ref,val in [('R41','12.7kR 1%'),('C19','18nF / 16V')]:prop(b.sym(ref),'Value')[2]=val
for z in all(t,'text'):
 if 'EN requires' in z[1]: z[1]='VIN = EXPOSED PAD 9: PD_VOUT, NOT GND.\nEN: 2.495V shunt bias; R43 dissipation 0.65W at 28V.\nCOMP: Rc=12.7k, Cc=18nF; fc about 8.5..10kHz at Cout_eff=44uF.\nRF=100k: table 500kHz; equation 476.19kHz. Verify on prototype.'
 if 'L/D MPN' in z[1]:z[1]='L/D exact MPN and footprints require selection.\nL: Isat >=2A normal load, Irms >=1.5A.\nCout effective >=44uF; check DC-bias curves.'
component('Device:R','R43','1kR / 2W',243.84,120.65,foot='Resistor_SMD:R_2512_6332Metric',notes='Shunt feed: 0.651W at 28V. Select actual 2W-rated part; footprint alone is not a rating.')
label('PD_VOUT',243.84,110.49,True);wire(243.84,110.49,243.84,116.84);wire(243.84,124.46,243.84,135.89)
component('Reference_Voltage:TL431DBZ','U6','TL431BIDBZR',243.84,146.05,90,'Package_TO_SOT_SMD:SOT-23',notes='TI TL431 DBZ: K1 REF2 A3. REF tied K. No added capacitive load.')
# Rotation 90: cathode up, anode down, REF right.
wire(243.84,135.89,243.84,143.51);wire(243.84,135.89,251.46,135.89);wire(251.46,135.89,251.46,146.05);wire(251.46,146.05,246.38,146.05)
label('EN_CTRL',251.46,135.89);wire(243.84,148.59,243.84,153.67);power('GND',243.84,153.67)
add(f'(junction (at 243.84 135.89) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
for ref in ['C15','C16']:
 prop(b.sym(ref),'DesignNote')[2]='X7R; bank effective Cout >=44uF at 3.3V. Confirm exact MPN bias/ESR before manufacture.'
# Exact electrical gaps: endpoints obtained from KiCad ERC and pin/net export.
for v in [(115.57,74.93,127.635,74.93),(205.105,62.865,221.615,62.865),(207.01,33.02,223.52,33.02),(240.03,62.865,257.81,62.865),(241.935,33.02,259.715,33.02),(201.295,97.155,213.36,97.155)]:pd.wire(*v)
ui.wire(52.705,156.845,57.785,156.845)
# Valid package pad mapping, preserving gate/source/drain node positions.
libs=one(pd.t,'lib_symbols');orig=next(v for v in libs[1:] if v[1]=='Transistor_FET:Q_NMOS_GSD');d=copy.deepcopy(orig);d[1]='Power_Supply_Custom:IRF7855_SO8'
for v in all(d,'symbol'):v[1]=v[1].replace('Q_NMOS_GSD','IRF7855_SO8')
for v in all(d,'symbol'):
 for pin in list(all(v,'pin')):
  name=one(pin,'name')[1];numbers={'G':['4'],'S':['1','2','3'],'D':['5','6','7','8']}[name];one(pin,'number')[1]=numbers[0]
  for num in numbers[1:]:
   q=copy.deepcopy(pin);one(q,'number')[1]=num;q.append(S('hide'));v.append(q)
libs.append(d)
for ref in ['Q3','Q4']:
 a=pd.sym(ref);one(a,'lib_id')[1]=d[1];prop(a,'Footprint')[2]='Package_SO:SOIC-8_3.9x4.9mm_P1.27mm';a[:]=[v for v in a if tag(v)!='pin']
cp=Path('Power_Supply_Custom.kicad_sym');ct=s.loads(cp.read_text(encoding='utf8'));cl=copy.deepcopy(d);cl[1]='IRF7855_SO8';ct.append(cl);cp.write_text(s.dumps(ct),encoding='utf8')
for ref,val,foot in [('C3','1uF / 50V','C_0805_2012Metric'),('C8','10uF / 50V','C_1210_3225Metric'),('C4','1uF / 10V','C_0603_1608Metric')]:
 a=pd.sym(ref);prop(a,'Value')[2]=val;prop(a,'Footprint')[2]='Capacitor_SMD:'+foot
for a in [pd.sym('R11'),sense.sym('RShunt')]:
 prop(a,'Value')[2]='5mR / 1W';prop(a,'Footprint')[2]='Resistor_SMD:R_2512_6332Metric'
for sch in [b,pd,ui,sense]:sch.save()
print('Saved four sheets and custom MOSFET library. Backups in before/.')
