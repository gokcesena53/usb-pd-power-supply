from pathlib import Path
import xml.etree.ElementTree as E, json, collections, re
r=E.parse('reports/review-20260910/after.xml').getroot();nets={}
for n in r.find('nets'):
 for p in n:nets[(p.get('ref'),p.get('pin'))]=n.get('name')
groups=[ [('U5','9'),('C12','1'),('C13','1'),('C14','1'),('R43','1')], [('U5','1'),('C17','2'),('D2','1'),('L1','1')], [('U5','2'),('C17','1')], [('L1','2'),('C15','1'),('C16','1'),('R39','1'),('U2','2'),('U3','6'),('U4','7')], [('U5','6'),('R39','2'),('R40','1')], [('U5','4'),('R38','1')], [('U5','7'),('C18','1')], [('U5','5'),('R41','1')], [('R41','2'),('C19','1')], [('U5','8'),('R42','1'),('R43','2'),('U6','1'),('U6','2')], [('U5','3'),('U6','3'),('D2','2'),('R38','2'),('R40','2'),('R42','2'),('C19','2')], [('R8','1'),('U1','9')], [('R11','1'),('J1','A4'),('U1','1')], [('R5','2'),('U1','5'),('Q1','3')], [('R6','2'),('U1','4'),('Q2','3')], [('R4','1'),('Q1','2'),('U2','16')], [('R7','2'),('Q2','2'),('U2','17')], [('Q6','3'),('R30','1'),('R31','1'),('R32','1'),('R33','1')]]
result=[]
for g in groups:
 ns={nets[p] for p in g};result.append({'pins':g,'nets':sorted(ns),'pass':len(ns)==1})
for ref in ['Q3','Q4']:
 for ps in [['1','2','3'],['5','6','7','8']]:
  ns={nets[(ref,p)] for p in ps};result.append({'pins':[(ref,p) for p in ps],'nets':sorted(ns),'pass':len(ns)==1})
Path('reports/review-20260910/net-checks.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps([v for v in result if not v['pass']],indent=2));print('PASS',sum(v['pass'] for v in result),'/',len(result))
stats={}
for st in ['before','after']:
 txt=Path(f'reports/review-20260910/{st}-erc.rpt').read_text(encoding='utf8');stats[st]={'errors':len(re.findall(r'; error',txt)),'warnings':len(re.findall(r'; warning',txt)),'types':dict(collections.Counter(re.findall(r'^\[([^]]+)\]',txt,re.M)))}
Path('reports/review-20260910/erc-summary.json').write_text(json.dumps(stats,indent=2),encoding='utf8');print(stats)
print('U5', {p:n for (a,p),n in nets.items() if a=='U5'})
import pymupdf
for f in Path('reports/review-20260910/svg').glob('*.svg'):
 d=pymupdf.open(f);q=pymupdf.open('pdf',d.convert_to_pdf());q[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(f.with_suffix('.png'))
