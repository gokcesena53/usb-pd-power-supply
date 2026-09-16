from pathlib import Path
import math,json
exec(Path('reports/fixes-20260909/fix.py').read_text(encoding='utf8').split("pd=Sch(")[0])
changes=[]
def field(a,k,v):
 try:prop(a,k)[2]=v
 except StopIteration:
  x,y=one(a,'at')[1:3];a.append(s.loads(f'(property {s.dumps(k)} {s.dumps(v)} (at {x} {y} 0) (hide yes) (effects (font (size 1.27 1.27))))'))
def note(sch,text,x,y):sch.add(f'(text {s.dumps(text)} (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left top)) (uuid "{uid()}"))')
exceptions={'R11','RShunt','R43','R12','C3','C4','C5','C7','C8','C12','C13','C15','C16'}
for f in Path('.').glob('*.kicad_sch'):
 sch=Sch(f)
 for a in all(sch.t,'symbol'):
  ref=prop(a,'Reference')[2]
  if ref[0:1] in ['R','C'] and ref not in exceptions:
   old=prop(a,'Footprint')[2];new=('Resistor_SMD:R_' if ref.startswith('R') else 'Capacitor_SMD:C_')+'0402_1005Metric'
   if old!=new:field(a,'Footprint',new);changes.append([f.name,ref,'Footprint',old,new])
 # Signal direction refers to this sheet, not the arrow's facing direction.
 for a in all(sch.t,'global_label'):
  n=a[1];old=one(a,'shape')[1];typ='passive'
  if n.startswith('PD_I2C_') or n in ['USB_DP','USB_DN','USB_CC1','USB_CC2']:typ='bidirectional'
  if n in ['TFT_CS','TFT_DC','TFT_RST','TFT_MOSI','TFT_SCLK','TFT_BL_PWM']:typ='output' if f.name=='mcu.kicad_sch' else 'input'
  if n.startswith('ENCODER_'):typ='input' if f.name=='mcu.kicad_sch' else 'output'
  if n=='INA_ALERT':typ='output' if f.name=='powersensing.kicad_sch' else 'input'
  if n=='PD_INT_3V3':typ='output' if f.name=='usb_pd_controller.kicad_sch' else 'input'
  one(a,'shape')[1]=S(typ)
  if str(old)!=typ:changes.append([f.name,n,'Label direction',str(old),typ])
 if f.name=='mcu.kicad_sch':
  a=sch.sym('BT1');field(a,'Value','CR2032 holder');field(a,'MPN','L-KLS5-CR2032-05-R1');field(a,'Manufacturer','KLS Electronic');field(a,'Footprint','Power_Output_Custom:KLS_CR2032_05');field(a,'Supplier','Ozdisan 497433');field(a,'Datasheet','https://img.klsele.com/admin/product_upload/20250408144415L-KLS5-CR2032-05.pdf');field(a,'Battery','CR2032 3V PRIMARY; cell purchased separately; RTC trickle charge MUST be disabled')
  note(sch,'BT1: CR2032 holder, Ozdisan 497433.\nPrimary 3V cell: disable RTC trickle charging.\nPad 1 = +, pad 2 = GND.',182.88,22.86)
  changes.append([f.name,'BT1','Part','Unspecified battery','KLS CR2032 holder + project footprint'])
 if f.name=='userinterface.kicad_sch':
  # User replaced Q6 with Q5 AO3400A; preserve the chosen transistor.
  q=sch.sym('Q5');ld=next(z for z in one(sch.t,'lib_symbols')[1:] if z[1]==one(q,'lib_id')[1]);pin=next(z for z in walk(ld) if tag(z)=='pin' and one(z,'number')[1]=='3');pa=one(pin,'at');qa=one(q,'at');assert qa[3]==0;x=round(qa[1]+pa[1],6);y=round(qa[2]-pa[2],6)
  # Direct local label gives a deterministic connection without guessing old stub endpoints.
  sch.wire(x,y,x+5.08,y);sch.label('BL_SINK',x+5.08,y,True)
  a=sch.sym('J3');field(a,'Value','NHD-2.4-240320AF-CSXP');field(a,'MPN','54132-4062');field(a,'Manufacturer','Molex');field(a,'DisplayMPN','NHD-2.4-240320AF-CSXP')
  # TFT datasheet four-wire SPI wiring grounds unused parallel input pins 13..29.
  lid=next(z for z in one(sch.t,'lib_symbols')[1:] if z[1]==one(a,'lib_id')[1]);at=one(a,'at');assert at[3]==0
  for pin in [z for z in walk(lid) if tag(z)=='pin']:
   num=int(one(pin,'number')[1])
   if 13<=num<=29:
    p=one(pin,'at');px=round(at[1]+p[1],6);py=round(at[2]-p[2],6)
    for nc in list(all(sch.t,'no_connect')):
     if one(nc,'at')[1:3]==[px,py]:sch.t.remove(nc)
    sch.wire(px,py,px-10.16,py)
    if num>13:sch.wire(px-10.16,py-2.54,px-10.16,py)
    if 13<num<29:sch.add(f'(junction (at {px-10.16} {py}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))')
    if num==29:sch.label('GND',px-10.16,py,True)
  note(sch,'4-wire SPI: IM2/IM1/IM0 = 1/1/0.\nRDX and DB0..DB15 tied GND per TFT wiring diagram.\nBacklight needs regulated current (160mA typ, 200mA max).',175.26,182.88)
  changes.append([f.name,'J3.13..29','Connection','NC','GND per display SPI drawing'])
 sch.save()
# Rebuild the output sheet around the existing connector references.
o=Sch('poweroutput.kicad_sch');keep=[z for z in o.t if tag(z) in ['version','generator','generator_version','uuid','paper','lib_symbols']];symbols=[copy.deepcopy(o.sym(r)) for r in ['J4','J5','J6','J7']];o.t=[o.t[0]]+keep
def move(a,x,y):
 at=one(a,'at');dx=x-at[1];dy=y-at[2];at[1:]=[x,y,0]
 for p in all(a,'property'):
  v=one(p,'at');v[1]+=dx;v[2]+=dy
 o.t.append(a)
for a,(x,y) in zip(symbols,[(109.22,76.2),(203.2,63.5),(203.2,88.9),(203.2,114.3)]):
 move(a,x,y);ref=prop(a,'Reference')[2]
 if ref!='J4':
  mpn='108-0902-001' if ref=='J5' else '108-0903-001';field(a,'Value',mpn);field(a,'MPN',mpn);field(a,'Manufacturer','Cinch Johnson');field(a,'Footprint','Power_Output_Custom:Cinch_'+mpn+'_Panel');one(a,'on_board')[1]=S('no');field(a,'AssemblyNote','PANEL MOUNT, solder wire to J4; mechanical footprint is documentation only')
  for k,yy in [('Reference',y-5.08),('Value',y-2.54)]:one(prop(a,k),'at')[1:]=[x,yy,0]
def pinpos(a,num):
 d=next(z for z in one(o.t,'lib_symbols')[1:] if z[1]==one(a,'lib_id')[1]);p=next(z for z in walk(d) if tag(z)=='pin' and one(z,'number')[1]==num);v=one(p,'at');at=one(a,'at');return (round(at[1]+v[1],6),round(at[2]-v[2],6))
for ref,num,net in [('J4','1','OUT_POS'),('J4','2','GND')]:
 x,y=pinpos(o.sym(ref),num);o.wire(x,y,x-15.24,y);o.label(net,x-15.24,y,True,180)
for ref,net in [('J5','OUT_POS'),('J6','GND'),('J7','GND')]:
 x,y=pinpos(o.sym(ref),'1');o.wire(x,y,x-15.24,y);o.label(net,x-15.24,y,True,180)
note(o,'POWER OUTPUT — PD PASS-THROUGH / PANEL WIRING',38.1,27.94)
note(o,'PCB TERMINAL\nJ4.1 = OUT_POS (+)\nJ4.2 = GND (-)\nTwo solder legs per pole: 1/1 and 2/2.',63.5,101.6)
note(o,'PANEL JACKS (off-board)\nJ5 red: 108-0902-001\nJ6/J7 black: 108-0903-001\nWire both black terminals to J4.2.\nBlack output is GND, not protective earth.',175.26,139.7)
note(o,'Existing path: PD_VOUT -> 5mR shunt -> OUT_POS.\nThis block does not provide independent CV/CC regulation.\nOutput isolation, reverse-current protection and discharge remain design tasks.',38.1,157.48)
o.save();changes.append(['poweroutput.kicad_sch','J4/J5/J6/J7','Wiring','Unconnected','OUT_POS red; GND both black; off-board banana jacks'])
Path('reports/output-update/changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
print(len(changes),'changes; size exceptions',sorted(exceptions))
