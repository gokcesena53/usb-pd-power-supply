import xml.etree.ElementTree as E
import json,collections
r=E.parse('reports/connectivity.xml').getroot()
cs={c.get('ref'):(c.findtext('value'),c.find('sheetpath').get('names')) for c in r.find('components')}
print('COMPONENTS',json.dumps(cs,ensure_ascii=False))
for n in r.find('nets'):
 print(n.get('name'), ' | '.join(f"{p.get('ref')}.{p.get('pin')}({p.get('pinfunction','')})" for p in n))
j=json.load(open('reports/erc.json',encoding='utf-8'))
print('ERC',collections.Counter((v['severity'],v['type']) for sh in j['sheets'] for v in sh['violations']))
