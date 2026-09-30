import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here=Path(__file__).resolve().parent
root=here.parents[3]
b=p.LoadBoard(str(root/'hardware/gopo.kicad_pcb'))
baseline=json.loads((root/'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old={f['ref']:f for f in baseline['footprints']}
refs='J7 D3 D8 D9 R62 R63 U10'.split()
fs={f.GetReference():f for f in b.GetFootprints()}
groups={f.GetReference():g.GetName() for g in b.Groups() for f in g.GetItems() if isinstance(f,p.FOOTPRINT)}
mm=lambda v:tuple(round(x,6) for x in p.ToMM(v))
rows=[]
for ref in refs:
 f=fs[ref];box=f.GetBoundingBox(False,False)
 rows.append(dict(ref=ref,value=f.GetValue(),before_xy=old[ref]['xy'],before_angle=old[ref]['angle'],
     after_xy=mm(f.GetPosition()),after_angle=f.GetOrientationDegrees(),side=f.GetLayerName(),
     locked=f.IsLocked(),group=groups.get(ref),uuid=f.m_Uuid.AsString(),before_pads=old[ref]['pads'],
     after_pads=sorted((a.GetNumber(),a.GetNetname()) for a in f.Pads()),before_bbox=old[ref]['bbox'],
     after_bbox=[p.ToMM(box.GetLeft()),p.ToMM(box.GetTop()),p.ToMM(box.GetRight()),p.ToMM(box.GetBottom())]))

def pad(ref,num):
 a=next(a for a in fs[ref].Pads() if a.GetNumber()==str(num))
 return dict(net=a.GetNetname(),xy=mm(a.GetPosition()))
def measure(a,na,c,nc):
 pa,pb=pad(a,na),pad(c,nc)
 return dict(a=f'{a}.{na}',a_net=pa['net'],a_xy=pa['xy'],b=f'{c}.{nc}',b_net=pb['net'],
             b_xy=pb['xy'],straight_mm=round(math.dist(pa['xy'],pb['xy']),4))
measures=[measure(*x) for x in [('J7','B4','D3',1),('J7','A5','D8',1),('J7','B5','D9',1),
    ('J7','B7','U10',1),('J7','B6','U10',3),('D8',1,'R62',1),('D9',1,'R63',1),
    ('D3',1,'C3',1)]]
before_drc=json.loads((here/'drc-before.json').read_text(encoding='utf-8'))
after_drc=json.loads((here/'drc-after.json').read_text(encoding='utf-8'))
counts=lambda d:{k:sum(v['type']==k for v in d['violations']) for k in sorted({v['type'] for v in d['violations']})}
anchor_refs='J7 J3 J9 H1 H2 H3 H4 D5 U11'.split()
anchors={ref:dict(before_xy=old[ref]['xy'],after_xy=mm(fs[ref].GetPosition()),
                  before_angle=old[ref]['angle'],after_angle=fs[ref].GetOrientationDegrees(),
                  before_uuid=old[ref]['uuid'],after_uuid=fs[ref].m_Uuid.AsString(),
                  before_side=old[ref]['side'],after_side=fs[ref].GetLayerName()) for ref in anchor_refs}
track_ids={t.m_Uuid.AsString() for t in b.GetTracks()}
old_track_ids={t['uuid'] for t in baseline['tracks']}
out=dict(placements=rows,pad_distances=measures,anchors=anchors,
         u10_flow=dict(connector_side={'DM':pad('U10',1),'DP':pad('U10',3)},
                       system_side={'DM':pad('U10',6),'DP':pad('U10',4)},
                       gnd=pad('U10',2),rail=pad('U10',5)),
         drc_before=counts(before_drc),drc_after=counts(after_drc),
         unconnected_before=len(before_drc['unconnected_items']),unconnected_after=len(after_drc['unconnected_items']),
         parity_before=len(before_drc['schematic_parity']),parity_after=len(after_drc['schematic_parity']),
         tracks_before=len(old_track_ids),tracks_after=len(track_ids),tracks_unchanged=(track_ids==old_track_ids))
(here/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(rows)==7 and all(r['before_pads']==[list(x) for x in r['after_pads']] and
    r['group']=='USB-C GIRIS' and r['side']=='B.Cu' and r['uuid']==old[r['ref']]['uuid'] for r in rows)
assert all(v['before_xy']==list(v['after_xy']) and v['before_angle']==v['after_angle'] and
    v['before_uuid']==v['after_uuid'] and v['before_side']==v['after_side'] for v in anchors.values())
assert pad('U10',1)['net']==pad('U10',6)['net']=='USB_DM'
assert pad('U10',3)['net']==pad('U10',4)['net']=='USB_DP'
assert pad('U10',2)['net']=='GND' and pad('U10',5)['net']=='+3.3V'
assert track_ids==old_track_ids and len(before_drc['violations'])==len(after_drc['violations'])
assert out['unconnected_before']==out['unconnected_after'] and not out['parity_after']

def draw(after):
 svg=ET.Element('svg',xmlns='http://www.w3.org/2000/svg',width='1000',height='690',viewBox='0 0 1000 690')
 ET.SubElement(svg,'rect',x='0',y='0',width='1000',height='690',fill='#111827')
 t=ET.SubElement(svg,'text',x='20',y='30',fill='white',style='font: bold 20px sans-serif');t.text='TASK-070 | '+('Sonra: B.Cu yön koridorları' if after else 'Önce: B.Cu yerleşim')
 x0,y0,s=22,68,25
 def xy(x,y):return((x-x0)*s,(y-y0)*s)
 def line(a,c,color,dash=''):
  x1,y1=xy(*a);x2,y2=xy(*c)
  attrs=dict(x1=str(x1),y1=str(y1),x2=str(x2),y2=str(y2),stroke=color,**{'stroke-width':'3','marker-end':'url(#arr)'})
  if dash:attrs['stroke-dasharray']=dash
  ET.SubElement(svg,'line',**attrs)
 defs=ET.SubElement(svg,'defs');marker=ET.SubElement(defs,'marker',id='arr',markerWidth='8',markerHeight='8',refX='7',refY='4',orient='auto');ET.SubElement(marker,'path',d='M0,0 L8,4 L0,8',fill='#ffd166')
 for row in rows:
  bb=row['after_bbox' if after else 'before_bbox'];x,y=xy(bb[0],bb[1]);w=(bb[2]-bb[0])*s;h=(bb[3]-bb[1])*s
  color='#f59f64' if row['ref']=='J7' else '#80d5aa' if row['ref']=='U10' else '#8da9e9'
  ET.SubElement(svg,'rect',x=str(x),y=str(y),width=str(w),height=str(h),fill=color,**{'fill-opacity':'0.35','stroke':color,'stroke-width':'1.5'})
  t=ET.SubElement(svg,'text',x=str(x+w/2),y=str(y+h/2+5),fill='white',**{'text-anchor':'middle'},style='font: bold 13px sans-serif');t.text=row['ref']
 if after:
  line(pad('J7','B4')['xy'],pad('D3',1)['xy'],'#ffd166')
  line(pad('J7','A5')['xy'],pad('D8',1)['xy'],'#ffba66')
  line(pad('J7','B5')['xy'],pad('D9',1)['xy'],'#ffba66')
  line(pad('J7','B7')['xy'],pad('U10',1)['xy'],'#74dfef')
  line(pad('J7','B6')['xy'],pad('U10',3)['xy'],'#74dfef')
  line(pad('U10',6)['xy'],(27.6,76.35),'#74dfef','6 4')
  line(pad('U10',4)['xy'],(27.6,78.25),'#74dfef','6 4')
  line(pad('U10',2)['xy'],(35.1,77.3),'#87dca7','4 3')
  t=ET.SubElement(svg,'text',x='16',y='675',fill='white',style='font: 13px sans-serif');t.text='Sarı: VBUS  Turuncu: CC1/CC2  Mavi: D−/D+ akışı  Yeşil: ESD GND/via alanı. Oklar planlanan koridorlardır.'
 ET.ElementTree(svg).write(here/('after.svg' if after else 'before.svg'),encoding='unicode',xml_declaration=True)
draw(False);draw(True)
print(json.dumps({k:out[k] for k in ('drc_before','drc_after','unconnected_before','unconnected_after','parity_after','tracks_unchanged')},ensure_ascii=False))
