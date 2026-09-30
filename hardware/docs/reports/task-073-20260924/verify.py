import json, math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here=Path(__file__).resolve().parent
root=here.parents[3]
b=p.LoadBoard(str(root/'hardware/gopo.kicad_pcb'))
old=json.loads((root/'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old={f['ref']:f for f in old['footprints']}
refs='U5 U6 L1 D2 C12 C13 C14 C15 C16 C17 C18 C19 R38 R39 R40 R41 R43 R50 R51'.split()
fs={f.GetReference():f for f in b.GetFootprints()}
groups={f.GetReference():g.GetName() for g in b.Groups() for f in g.GetItems() if isinstance(f,p.FOOTPRINT)}
mm=lambda v:tuple(round(x,6) for x in p.ToMM(v))
rows=[]
for ref in refs:
    f=fs[ref];box=f.GetBoundingBox(False,False)
    pads=sorted((a.GetNumber(),a.GetNetname()) for a in f.Pads())
    row=dict(ref=ref,before_xy=old[ref]['xy'],before_angle=old[ref]['angle'],
             after_xy=mm(f.GetPosition()),after_angle=f.GetOrientationDegrees(),side=f.GetLayerName(),
             group=groups.get(ref),uuid=f.m_Uuid.AsString(),locked=f.IsLocked(),
             before_pads=old[ref]['pads'],after_pads=pads,before_bbox=old[ref]['bbox'],
             after_bbox=[p.ToMM(box.GetLeft()),p.ToMM(box.GetTop()),p.ToMM(box.GetRight()),p.ToMM(box.GetBottom())])
    rows.append(row)

def pad(ref,num):
    a=next(a for a in fs[ref].Pads() if a.GetNumber()==str(num))
    return dict(net=a.GetNetname(),xy=mm(a.GetPosition()))
def measure(a,na,c,nc):
    pa,pb=pad(a,na),pad(c,nc)
    return dict(a=f'{a}.{na}',a_net=pa['net'],a_xy=pa['xy'],b=f'{c}.{nc}',b_net=pb['net'],b_xy=pb['xy'],straight_mm=round(math.dist(pa['xy'],pb['xy']),4))
measures=[measure(*x) for x in [('U5',1,'D2',1),('U5',1,'L1',1),('L1',2,'C16',1),
    ('C16',1,'C15',1),('U5',9,'C12',1),('U5',5,'R41',1),('U5',6,'R39',2),
    ('U6',1,'R51',1),('U6',1,'R50',2),('R51',1,'R50',2),
    ('D5',1,'U6',2),('C28',1,'R43',1),('C28',1,'C13',1)]]

fb_ids=['67174655-4b0a-418c-94ae-19de118917f4','bac123bf-3e8a-4a42-a3d9-e77dc0fb4f54',
        'ab6f190f-2a38-4051-afdd-29de0667dd97','dc31f985-bf69-4d4a-b183-b7bf2fcb8a73']
fb=[t for t in b.GetTracks() if t.m_Uuid.AsString() in fb_ids]
fb_length=sum(math.dist(mm(t.GetStart()),mm(t.GetEnd())) for t in fb)
before_drc=json.loads((here/'drc-before.json').read_text(encoding='utf-8'))
after_drc=json.loads((here/'drc-after.json').read_text(encoding='utf-8'))
counts=lambda d:{k:sum(v['type']==k for v in d['violations']) for k in sorted({v['type'] for v in d['violations']})}
out=dict(placements=rows,pad_distances=measures,
         u6_pin_nets={str(n):pad('U6',n)['net'] for n in (1,2,3)},
         boost_fb=dict(segment_uuids=[t.m_Uuid.AsString() for t in fb],length_mm=fb_length,
                       d5_anode=pad('D5',2),u11_fb=pad('U11',9),layers=sorted({t.GetLayerName() for t in fb})),
         drc_before=counts(before_drc),drc_after=counts(after_drc),
         unconnected_before=len(before_drc['unconnected_items']),unconnected_after=len(after_drc['unconnected_items']),
         parity_before=len(before_drc['schematic_parity']),parity_after=len(after_drc['schematic_parity']))
anchors='J3 J9 H1 H2 H3 H4 D5 U11'.split()
out['anchors']={ref:dict(before_xy=old[ref]['xy'],after_xy=mm(fs[ref].GetPosition()),
                         before_angle=old[ref]['angle'],after_angle=fs[ref].GetOrientationDegrees(),
                         before_side=old[ref]['side'],after_side=fs[ref].GetLayerName(),
                         before_uuid=old[ref]['uuid'],after_uuid=fs[ref].m_Uuid.AsString()) for ref in anchors}
(here/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
assert len(rows)==19
assert all(r['before_pads']==[list(x) for x in r['after_pads']] and r['side']=='B.Cu' and r['group']=='AOZ1284 3.3V BUCK' and r['uuid']==old[r['ref']]['uuid'] for r in rows)
assert out['u6_pin_nets']=={'1':'Net-(U6-REF)','2':'/USB_PD_CONTROLLER/EN_CTRL','3':'GND'}
assert len(fb)==4 and fb_length<10 and out['boost_fb']['layers']==['B.Cu']
assert all(v['before_xy']==list(v['after_xy']) and v['before_angle']==v['after_angle'] and
           v['before_side']==v['after_side'] and v['before_uuid']==v['after_uuid'] for v in out['anchors'].values())
assert len(before_drc['violations'])==len(after_drc['violations']) and not out['parity_after']

def draw(after):
    svg=ET.Element('svg',xmlns='http://www.w3.org/2000/svg',width='1100',height='720',viewBox='0 0 1100 720')
    ET.SubElement(svg,'rect',x='0',y='0',width='1100',height='720',fill='#101827')
    title=ET.SubElement(svg,'text',x='20',y='30',fill='white',style='font: bold 20px sans-serif')
    title.text='TASK-073 | '+('Sonra: B.Cu ve yön koridorları' if after else 'Önce: B.Cu yerleşim')
    x0,y0,s=62,34,17
    def xy(x,y): return ((x-x0)*s,(y-y0)*s)
    def line(a,c,color,dash=''):
        x1,y1=xy(*a);x2,y2=xy(*c)
        attrs=dict(x1=str(x1),y1=str(y1),x2=str(x2),y2=str(y2),stroke=color,**{'stroke-width':'3','marker-end':'url(#arrow)'})
        if dash:attrs['stroke-dasharray']=dash
        ET.SubElement(svg,'line',**attrs)
    defs=ET.SubElement(svg,'defs');marker=ET.SubElement(defs,'marker',id='arrow',markerWidth='8',markerHeight='8',refX='7',refY='4',orient='auto');ET.SubElement(marker,'path',d='M0,0 L8,4 L0,8',fill='#ffc857')
    for row in rows:
        bb=row['after_bbox' if after else 'before_bbox'];x,y=xy(bb[0],bb[1]);w=(bb[2]-bb[0])*s;h=(bb[3]-bb[1])*s
        color='#e68d5b' if row['ref'] in ('U5','L1','D2') else '#79cba8' if row['ref'].startswith('C') else '#85a9e8'
        ET.SubElement(svg,'rect',x=str(x),y=str(y),width=str(w),height=str(h),fill=color,**{'fill-opacity':'0.37','stroke':color,'stroke-width':'1.4'})
        t=ET.SubElement(svg,'text',x=str(x+w/2),y=str(y+h/2+4),fill='white',**{'text-anchor':'middle'},style='font: bold 12px sans-serif');t.text=row['ref']
    if after:
        line(pad('C12',1)['xy'],pad('U5',9)['xy'],'#ffc857')
        line(pad('U5',1)['xy'],pad('D2',1)['xy'],'#ff986b')
        line(pad('U5',1)['xy'],pad('L1',1)['xy'],'#ff986b')
        line(pad('L1',2)['xy'],pad('C16',1)['xy'],'#ffc857')
        line(pad('C16',1)['xy'],pad('C15',1)['xy'],'#ffc857')
        line(pad('U5',6)['xy'],pad('R39',2)['xy'],'#79dfff')
        line(pad('U5',5)['xy'],pad('R41',1)['xy'],'#79dfff')
        line(pad('D5',1)['xy'],pad('U6',2)['xy'],'#79dfff','6 4')
        line(pad('C28',1)['xy'],pad('R43',1)['xy'],'#ffc857','6 4')
        t=ET.SubElement(svg,'text',x='20',y='700',fill='#fff',style='font: 14px sans-serif');t.text='Sarı: V_PRE/+3.3V  Turuncu: LX/D2  Mavi: EN/FB/COMP  Kesik: grup sınırı; oklar planlanan koridor, bitmiş iz değil.'
    ET.ElementTree(svg).write(here/('after.svg' if after else 'before.svg'),encoding='unicode',xml_declaration=True)
draw(False);draw(True)
print(json.dumps({k:out[k] for k in ('u6_pin_nets','boost_fb','drc_before','drc_after','unconnected_before','unconnected_after','parity_after')},ensure_ascii=False))
