from pathlib import Path
import json,math,collections,hashlib
D=Path(__file__).resolve().parent;ROOT=D.parents[3]
b=json.loads((D/'board.json').read_text());rc=json.loads((D/'rc_actual.json').read_text())
spec={}
def add(refs,role,source,targets):
 for r,t in zip(refs.split(),targets.split('|')):spec[r]={'role':role,'source':source,'targets':t.split()}
add('C1 C2 C3 C4 C8','AP33772S besleme/olcum kapasitörü','AP33772S s.3,18','1>U1.12|1>U1.24|1>U1.24|1>U1.20|1>Q3.5')
spec['C2']['targets']=['1>U1.15'];spec['C1']['role']='V18 100 nF dekuplaj';spec['C2']['role']='IFB 100 nF filtre';spec['C3']['role']='Sont sonrasi VBUS filtre';spec['C8']['role']='Q3 sonrasi PD_VOUT filtre'
add('C5 C6','U2 3V3 besleme','ESP32-C6-MINI-1 s.40','1>U2.3|1>U2.3')
add('C7','U2 EN/reset kapasitörü','ESP32-C6-MINI-1 s.40','2>U2.8')
add('C9','BQ32000 VCC dekuplaj','BQ32000 s.23','1>U4.8')
add('C10 C20','Ethernet modul besleme filtresi','CH9121 modul semasi; TASK-093.01','1>Q8.2|1>J8.14')
add('C11 C35','IC besleme dekuplaj','INA226 s.31; SN74LVC1G17 datasheet','1>U3.6|1>U13.5')
add('C12 C13 C14','Buck VIN giriş dekuplaji','AOZ1284 s.12','1>U5.9|1>U5.9|1>U5.9')
add('C15 C16','Buck 3V3 cikis filtresi','AOZ1284 s.12','1>L1.2|1>L1.2')
add('C17','Buck BST-LX bootstrap','AOZ1284 s.12','1>U5.2 2>U5.1')
add('C18','Buck SS ramp','AOZ1284','1>U5.7')
add('C19','Buck seri RC kompanzasyon','AOZ1284 s.12','1>R41.2')
add('C21','Ethernet MOSFET gate-source gecis filtresi','Devre netlisti / Q8','1>Q8.4 2>Q8.3')
add('C23','Boost soft start','TPS55340 s.28','1>U11.5')
add('C24','Boost seri RC kompanzasyon','TPS55340 s.28','1>R52.2')
add('C25 C26','Boost VIN besleme','TPS55340 s.28','1>U11.3|1>U11.3')
add('C27 C28','Boost cikis filtresi / sicak dongu','TPS55340 s.28','1>D4.1|1>D4.1')
add('C29','Boost bobin girisi bulk','TPS55340 s.28','1>L3.2')
add('C30','HGATE seri RC acilis filtresi','LM7480-Q1 s.35','1>R54.2')
add('C31','CAP-VS sarj pompasi','LM7480-Q1 s.35','1>U12.10 2>U12.11')
add('C32','VS-GND dekuplaj','LM7480-Q1 s.35','1>U12.10')
add('C33','RTC yedek enerji deposu','BQ32000 s.23','1>U4.3')
add('C34','LCD konnektor 3V3 dekuplaj','TFT032B018; netlist','1>J3.22')
add('R1','EN pull-up','ESP32-C6-MINI-1 s.40','2>U2.8')
add('R2 R3','USB seri sonlandirma','Espressif USB layout','1>U2.17|1>U2.18')
add('R4 R5 R6 R7','I2C seviye cevirici pull-up','Netlist; BSS138','1>Q1.2|2>Q1.3|2>Q2.3|2>Q2.2')
add('R8 R9 R64 R65','PD_INT 3V3 direnç bolucu zinciri','Netlist; TASK-043','2>R64.1|2>R65.1|1>R8.2|1>R9.2')
add('R10 R37','U2 strapping pull-up','ESP32-C6-MINI-1','1>U2.23|1>U2.22')
add('R11','Giriş akim sontu / Kelvin','AP33772S s.18','1>U1.1 2>U1.24')
add('R12','Q3 gate seri direnci','AP33772S s.18','1>U1.23 2>Q3.2')
add('R13','VOUT algilama seri direnci','AP33772S','1>U1.22')
add('R14','LED akim sinirlama','Netlist','2>D1.2')
add('R15','Ethernet CFG seri direnc','Netlist','1>U2.22')
add('R16','Ethernet gate kumanda seri direnci','Netlist','2>U2.12 1>Q8.3')
add('R17','Ethernet gate-source pull-up','Netlist','1>Q8.4 2>Q8.3')
add('R21','VSEL programlama','AP33772S','2>U1.11')
add('R24','RTC interrupt pull-up','BQ32000','2>U4.7')
add('R27','INA ALERT pull-up','INA226','2>U3.3')
add('R28 R29','Backlight gate seri / pull-down','Netlist; Q7','2>Q7.1|1>Q7.1')
add('R34 R35 R36','Encoder pull-up','Netlist; TASK-068','2>J9.1|2>J9.3|2>J9.4')
add('R38','Buck frekans ayari','AOZ1284','1>U5.4')
add('R39 R40','Buck FB bolucu','AOZ1284 s.12','2>U5.6|1>U5.6')
add('R41','Buck COMP seri RC','AOZ1284 s.12','1>U5.5 2>C19.1')
add('R43','EN_CTRL bias','Netlist','2>U5.8')
add('R47','Boost FREQ ayari','TPS55340','1>U11.10')
add('R48 R49','Boost FB bolucu','TPS55340 s.28','2>U11.9|1>U11.9')
add('R50 R51','TLV431 referans bolucu','TLV431; netlist','2>U6.1|1>U6.1')
add('R52','Boost COMP seri RC','TPS55340 s.28','1>U11.8 2>C24.1')
add('R53','Boost EN bias','TPS55340','2>U11.4')
add('R54','HGATE seri RC acilis','LM7480-Q1','2>C30.1 1>Q5.2')
add('R55 R56','OV algilama bolucu','LM7480-Q1 s.35','2>U12.5|1>U12.5')
add('R58','Cikis EN pull-down','Netlist','1>U12.6')
add('R59','Cikis pasif desarj','Netlist','1>J4.1')
add('R60','LCD backlight akim direnci','TFT032B018; netlist','2>J3.2')
add('R61','OUT_EN pull-down','Netlist; U13','1>U13.1')
add('R62 R63','USB CC Rd','AP33772S; USB-C','1>J7.A5|1>J7.B5')
add('R66','Desarj gate bias','Netlist','2>Q6.1')
add('R67','Aktif desarj guc direnci','Netlist','2>Q6.3')
add('RShunt1','Cikis akim sontu / Kelvin','INA226 s.31','1>U3.10 2>U3.9')
assert set(spec)=={r['ref'] for r in rc},(set(spec)^{r['ref'] for r in rc})
moves=set('C5 C6 C7 R1 R2 R3'.split())
conditional=set('C1 C2 C4 C9 C11 C12 C13 C14 C15 C16 C17 C19 C24 C25 C26 C27 C28 C30 C31 C32 C34 C35 R11 R12 R13 R28 R39 R40 R41 R48 R49 R50 R51 R52 R54 R55 R56 R62 R63 RShunt1'.split())
def measure(r,pn,t,tn):
 a=[x for x in b[r]['pads'] if x['n']==pn]; z=[x for x in b[t]['pads'] if x['n']==tn]
 assert a and z,(r,pn,t,tn)
 pairs=[(x,y) for x in a for y in z if x['net']==y['net'] and x['net']]
 assert pairs,('NET_MISMATCH',r,pn,t,tn)
 x,y=min(pairs,key=lambda pair:math.dist(pair[0]['xy'],pair[1]['xy']))
 return {'from':r+'.'+pn,'to':t+'.'+tn,'net':x['net'],'from_xy':x['xy'],'to_xy':y['xy'],'mm':round(math.dist(x['xy'],y['xy']),3)}
for r in rc:
 s=spec[r['ref']];r.update(s);r['verdict']='TASINMALI' if r['ref'] in moves else 'ROUTING_KOSULLU' if r['ref'] in conditional else 'UYGUN'
 r['measurements']=[]
 for target in s['targets']:
  pn,t=target.split('>');tr,tn=t.split('.');r['measurements'].append(measure(r['ref'],pn,tr,tn))
 r.pop('targets',None)
return_pairs=[('C14','2','U5','3'),('C12','2','U5','3'),('C26','2','U11','11'),('C27','2','U11','6'),('C28','2','U11','6'),('C32','2','U12','7'),('C11','2','U3','7')]
returns=[measure(*s) for s in return_pairs]
(D/'reviewed-rc.json').write_text(json.dumps(rc,ensure_ascii=False,indent=2),encoding='utf-8')
(D/'ground-returns.json').write_text(json.dumps(returns,indent=2))
print(json.dumps(collections.Counter(r['verdict'] for r in rc)));print(json.dumps(returns,indent=2))
v=json.loads((D/'verification.json').read_text());v['classification']=dict(collections.Counter(r['verdict'] for r in rc));v['measurement_count']=sum(len(r['measurements']) for r in rc);v['all_target_pads_exist_and_nets_match']=True
(D/'verification.json').write_text(json.dumps(v,indent=2))
