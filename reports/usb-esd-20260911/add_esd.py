from pathlib import Path
import math, copy
exec(Path('reports/output-update/update_schematic.py').read_text(encoding='utf8').split('exceptions=')[0])

a=Sch('usb_c_input.kicad_sch')
source=Sch('powergeneration.kicad_sch')
ui=Sch('userinterface.kicad_sch')

def custom_array():
    pins=[
        ('1','D1+',-12.7,7.62,0,'bidirectional'),
        ('2','D1-',-12.7,2.54,0,'bidirectional'),
        ('4','D2+',-12.7,-2.54,0,'bidirectional'),
        ('5','D2-',-12.7,-7.62,0,'bidirectional'),
        ('3','GND',-2.54,-12.7,90,'power_in'),
        ('8','GND',2.54,-12.7,90,'power_in'),
        ('6','NC',12.7,-7.62,180,'no_connect'),
        ('7','NC',12.7,-2.54,180,'no_connect'),
        ('9','NC',12.7,2.54,180,'no_connect'),
        ('10','NC',12.7,7.62,180,'no_connect')]
    pin_text=''.join(f'(pin {typ} line (at {x} {y} {ang}) (length 2.54) (name "{name}" (effects (font (size 1.27 1.27)))) (number "{num}" (effects (font (size 1.27 1.27)))))' for num,name,x,y,ang,typ in pins)
    return s.loads('(symbol "USB_ESD:TPD4E05U06QDQARQ1" '
        '(pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes) '
        '(property "Reference" "U" (at 0 13.97 0) (effects (font (size 1.27 1.27)))) '
        '(property "Value" "TPD4E05U06QDQARQ1" (at 0 11.43 0) (effects (font (size 1.27 1.27)))) '
        '(property "Footprint" "USB_ESD:antmicro_tpd4e05u06qdqarq1" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27)))) '
        '(property "Datasheet" "https://www.ti.com/lit/ds/symlink/tpd4e05u06-q1.pdf" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27)))) '
        '(property "Description" "Four-channel ultra-low-capacitance ESD array; 5.5V VRWM; 0.5pF; IEC 12kV contact" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27)))) '
        '(property "MPN" "TPD4E05U06QDQARQ1" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27)))) '
        '(property "Manufacturer" "Texas Instruments" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27)))) '
        '(symbol "TPD4E05U06QDQARQ1_0_1" (rectangle (start -10.16 10.16) (end 10.16 -10.16) (stroke (width 0) (type default)) (fill (type background)))) '
        f'(symbol "TPD4E05U06QDQARQ1_1_1" {pin_text}))')

arr=custom_array()
one(a.t,'lib_symbols').append(copy.deepcopy(arr))

def new_symbol(lib_id,ref,value,x,y,footprint,datasheet,mpn,manufacturer):
    # Reuse a known symbol instance envelope, replacing cached lib and fields.
    z=copy.deepcopy(a.sym('J1'))
    one(z,'lib_id')[1]=lib_id
    one(z,'at')[1:]=[x,y,0]
    z[:]=[v for v in z if tag(v) not in ['instances','pin']]
    for v in walk(z):
        if tag(v)=='uuid':v[1]=uid()
        if tag(v)=='reference':v[1]=ref
    field(z,'Reference',ref);field(z,'Value',value);field(z,'Footprint',footprint)
    field(z,'Datasheet',datasheet);field(z,'MPN',mpn);field(z,'Manufacturer',manufacturer)
    for p in all(z,'property'):
        one(p,'at')[1:]=[x+13.97,y,0]
        if p[1] not in ['Reference','Value']:
            try:one(p,'hide')[1]=S('yes')
            except StopIteration:p.append([S('hide'),S('yes')])
    one(prop(z,'Reference'),'at')[1:]=[x-10.16,y-13.97,0]
    one(prop(z,'Value'),'at')[1:]=[x-10.16,y-11.43,0]
    a.t.append(z)
    return z

u=new_symbol('USB_ESD:TPD4E05U06QDQARQ1','U9','TPD4E05U06QDQARQ1',213.36,93.98,'USB_ESD:antmicro_tpd4e05u06qdqarq1','https://www.ti.com/lit/ds/symlink/tpd4e05u06-q1.pdf','TPD4E05U06QDQARQ1','Texas Instruments')

# Cache and instantiate the standard bidirectional-represented TVS symbol.
dev=Path('C:/Program Files/KiCad/10.0/share/kicad/symbols/Device.kicad_sym')
dt=s.loads(dev.read_text(encoding='utf8'))
dlib=copy.deepcopy(next(z for z in all(dt,'symbol') if z[1]=='D_TVS'))
dlib[1]='Device:D_TVS'
if not any(z[1]=='Device:D_TVS' for z in one(a.t,'lib_symbols')[1:]):one(a.t,'lib_symbols').append(dlib)
d=copy.deepcopy(source.sym('D2'));one(d,'lib_id')[1]='Device:D_TVS';one(d,'at')[1:]=[190.5,62.23,0]
for v in walk(d):
    if tag(v)=='uuid':v[1]=uid()
    if tag(v)=='reference':v[1]='D3'
field(d,'Reference','D3');field(d,'Value','AQ3130E-01ETG (bidirectional)');field(d,'Footprint','Diode_SMD:D_SOD-882')
field(d,'Datasheet','https://www.littelfuse.com/assetdocs/littelfuse-tvs-diode-array-aq3130e-01etg-datasheet?assetguid=f74c18ee-03bb-4555-9ff2-5486f45a66ee')
field(d,'MPN','AQ3130E-01ETG');field(d,'Manufacturer','Littelfuse')
for p in all(d,'property'):
    one(p,'at')[1:]=[195.58,62.23,0]
    if p[1] not in ['Reference','Value']:
        try:one(p,'hide')[1]=S('yes')
        except StopIteration:p.append([S('hide'),S('yes')])
one(prop(d,'Reference'),'at')[1:]=[195.58,59.69,0];one(prop(d,'Value'),'at')[1:]=[195.58,64.77,0]
a.t.append(d)

def pinpos(ref,num):
    z=next(x for x in all(a.t,'symbol') if prop(x,'Reference')[2]==ref)
    lib=next(x for x in one(a.t,'lib_symbols')[1:] if x[1]==one(z,'lib_id')[1])
    p=next(x for x in walk(lib) if tag(x)=='pin' and one(x,'number')[1]==str(num))
    px,py=one(p,'at')[1:3];sx,sy,ang=one(z,'at')[1:4];t=math.radians(ang)
    return round(sx+px*math.cos(t)+py*math.sin(t),6),round(sy-px*math.sin(t)-py*math.cos(t),6)

for num,net in [('1','USB_DP'),('2','USB_DM'),('4','USB_CC1'),('5','USB_CC2')]:
    x,y=pinpos('U9',num);a.wire(x-7.62,y,x,y);a.label(net,x-7.62,y,True,180)
for num in ['6','7','9','10']:
    x,y=pinpos('U9',num);a.add(f'(no_connect (at {x} {y}) (uuid "{uid()}"))')

# Both ground pins connect to a short common ground branch.
p3=pinpos('U9','3');p8=pinpos('U9','8');gx=(p3[0]+p8[0])/2;gy=p3[1]+5.08
a.wire(*p3,p3[0],gy);a.wire(*p8,p8[0],gy);a.wire(p3[0],gy,p8[0],gy)
g=copy.deepcopy(ui.sym('#PWR218'));one(g,'at')[1:]=[gx,gy,0]
for v in walk(g):
    if tag(v)=='uuid':v[1]=uid()
    if tag(v)=='reference':v[1]='#PWR228'
field(g,'Reference','#PWR228');a.t.append(g)

# VBUS TVS: pin 2 to USB_VBUS, pin 1 to GND (symbol orientation selected accordingly).
for num in ['1','2']:
    print('D3 pin',num,pinpos('D3',num))
p1=pinpos('D3','1');p2=pinpos('D3','2')
a.wire(*p2,p2[0],54.61);a.label('USB_VBUS',p2[0],54.61,True,90)
g2=copy.deepcopy(g);one(g2,'at')[1:]=[p1[0],p1[1]+5.08,0]
for v in walk(g2):
    if tag(v)=='uuid':v[1]=uid()
    if tag(v)=='reference':v[1]='#PWR229'
field(g2,'Reference','#PWR229');a.t.append(g2);a.wire(*p1,p1[0],p1[1]+5.08)

note(a,'USB PORT ESD\nU9: D+/D-/CC1/CC2; IEC 12kV contact, 15kV air.\nD3: 28V VBUS TVS; IEC 30kV contact/air.\nPlace both directly behind J1; shortest GND return.',182.88,129.54)
note(a,'VBUS LIMIT: AQ3130E clamps 39..44V @1A.\nAP33772 VCC abs max 34V and VOUT 31V.\nESD robustness improves, but surge immunity needs system test / surge stopper.',182.88,149.86)
a.save()

# Install project libraries for portability.
sym=Path('sym-lib-table');txt=sym.read_text(encoding='utf8')
if '(name "USB_ESD")' not in txt:txt=txt.rstrip()[:-1]+'\n\t(lib (name "USB_ESD") (type "KiCad") (uri "${KIPRJMOD}/USB_ESD.kicad_sym") (options "") (descr "USB ESD protection symbols"))\n)\n'
sym.write_text(txt,encoding='utf8')
fp=Path('fp-lib-table');txt=fp.read_text(encoding='utf8')
if '(name "USB_ESD")' not in txt:txt=txt.rstrip()[:-1]+' (lib (name "USB_ESD") (type "KiCad") (uri "${KIPRJMOD}/USB_ESD.pretty") (options "") (descr "Verified USB ESD footprint")))\n'
fp.write_text(txt,encoding='utf8')

# External symbol library mirrors the exact reviewed pin table.
ext=copy.deepcopy(arr);ext[1]='TPD4E05U06QDQARQ1'
Path('USB_ESD.kicad_sym').write_text(s.dumps([S('kicad_symbol_lib'),[S('version'),20231120],[S('generator'),'codex'],ext])+'\n',encoding='utf8')
print('Added U9 signal ESD and D3 VBUS ESD')
