from pathlib import Path
import sexpdata as s,xml.etree.ElementTree as E,hashlib,json,uuid
p=Path('powergeneration.kicad_sch');t=s.loads(p.read_text(encoding='utf8'))
for z in t:
 if not isinstance(z,list) or str(z[0])!='symbol':continue
 props={a[1]:a for a in z if isinstance(a,list) and str(a[0])=='property'};ref=props['Reference'][2]
 volts={'C12':'50V','C13':'50V','C14':'50V','C15':'10V','C16':'10V','C17':'16V','C18':'10V'}
 if ref in volts:
  z.append(s.loads(f'(property "Voltage" "{volts[ref]}" (at 0 0 0) (hide yes) (effects (font (size 1.27 1.27))))'))
for text,x,y in [('Cin: 50V X7R; effective bank >=10uF @28V',45.72,40.64),('Cout: 10V X7R; effective bank >=44uF @3.3V',175.26,63.5)]:
 t.append(s.loads(f'(text "{text}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) (justify left top)) (uuid "{uuid.uuid4()}"))'))
p.write_text('(kicad_sch\n'+'\n'.join(s.dumps(a) for a in t[1:])+'\n)\n',encoding='utf8')
r=E.parse('reports/buck-20260910/net.xml').getroot();nets={n.get('name'):{(a.get('ref'),a.get('pin')) for a in n} for n in r.find('nets')}
expected={'PD_VOUT':{('U5','9'),('C12','1'),('C13','1'),('C14','1')},'GND':{('U5','3'),('D2','2'),('C12','2'),('C13','2'),('C14','2'),('C15','2'),('C16','2'),('C18','2'),('C19','2'),('R38','2'),('R40','2'),('R42','2')},'+3.3V':{('L1','2'),('C15','1'),('C16','1'),('R39','1')},'/POWER GENERATION/LX_SW':{('U5','1'),('C17','2'),('D2','1'),('L1','1')},'Net-(U5-BST)':{('U5','2'),('C17','1')},'/POWER GENERATION/FB_3V3':{('U5','6'),('R39','2'),('R40','1')},'/POWER GENERATION/COMP_NODE':{('U5','5'),('R41','1')},'Net-(C19-Pad1)':{('R41','2'),('C19','1')},'/POWER GENERATION/FSW_SET':{('U5','4'),('R38','1')},'/POWER GENERATION/SS_RAMP':{('U5','7'),('C18','1')},'/POWER GENERATION/EN_CTRL':{('U5','8'),('R42','1')}}
for name,nodes in expected.items():assert nodes<=nets[name],(name,nodes-nets[name])
hashes=json.loads(Path('reports/buck-20260910/unrelated-hashes.json').read_text())
for f,h in hashes.items():assert hashlib.sha256(Path(f).read_bytes()).hexdigest()==h,f
print('PASS: 11 network assertions; unrelated schematic hashes unchanged.')
