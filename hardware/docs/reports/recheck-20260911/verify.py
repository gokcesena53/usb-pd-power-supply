from pathlib import Path
import json,xml.etree.ElementTree as E,collections,re,hashlib
import pymupdf as fitz,pcbnew
base=Path('reports/recheck-20260911');root=E.parse(base/'after.xml').getroot()
n={(p.get('ref'),p.get('pin')):net.get('name') for net in root.find('nets') for p in net}
checks=json.loads(Path('reports/output-update/net-checks.json').read_text())
for pins,expected in [([['U4','3'],['U2','7']],'/MCU/RTC_SCL'),([['U4','4'],['U2','6']],'/MCU/RTC_SDA'),([['U5','1'],['C17','2'],['D2','1'],['L1','1']],'/POWER GENERATION/LX_SW'),([['U5','2'],['C17','1']],'Net-(U5-BST)'),([['L1','2'],['C15','1'],['C16','1'],['R39','1']],'+3.3V')]:checks.append(dict(pins=pins,expected=expected))
for t in checks:
 t['pins']=[p for p in t['pins'] if p[0]!='J7'];t['actual']=sorted(set(n.get(tuple(p),'MISSING') for p in t['pins']));t['pass']=t['actual']==[t['expected']]
(base/'net-checks.json').write_text(json.dumps(checks,indent=2));print('NET CHECKS',sum(c['pass'] for c in checks),'/',len(checks))
assert all(c['pass'] for c in checks)
for f in (base/'svg').glob('*.svg'):
 d=fitz.open(f);d=fitz.open('pdf',d.convert_to_pdf());d[0].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(str(f.with_suffix('.png')))
fp=[]
for folder in ['Power_Output_Custom.pretty','DG142R-5.08-02P-14-00AH.pretty']:
 for f in Path(folder).glob('*.kicad_mod'):
  obj=pcbnew.FootprintLoad(str(f.parent.resolve()),f.stem);assert obj
  pads=[{'number':p.GetNumber(),'x_mm':pcbnew.ToMM(p.GetPosition().x),'y_mm':pcbnew.ToMM(p.GetPosition().y),'drill_mm':pcbnew.ToMM(p.GetDrillSize().x)} for p in obj.Pads()]
  fp.append(dict(file=str(f),pads=pads));print(f.name,pads)
(base/'footprint-checks.json').write_text(json.dumps(fp,indent=2))
s=(base/'erc.rpt').read_text(encoding='utf8');counts=collections.Counter(re.findall(r'^\[([^]]+)\]',s,re.M));print('ERC',s.count('; error'),s.count('; warning'),dict(counts))
(base/'erc-summary.json').write_text(json.dumps(dict(errors=s.count('; error'),warnings=s.count('; warning'),categories=counts),indent=2))
manifest={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in Path('.').glob('*.kicad_sch')};(base/'schematic-sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
