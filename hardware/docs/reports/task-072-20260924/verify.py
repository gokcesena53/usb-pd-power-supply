import json
import math
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
board = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
before = json.loads((root / 'hardware/docs/reports/task-065-20260924/inventory-after.json').read_text(encoding='utf-8'))
old = {f['ref']: f for f in before['footprints']}
refs = 'U11 L3 D4 D5 C23 C24 C25 C26 C27 C28 C29 R47 R48 R49 R52 R53'.split()
current = {f.GetReference(): f for f in board.GetFootprints()}
groups = {f.GetReference(): g.GetName() for g in board.Groups() for f in g.GetItems() if isinstance(f, p.FOOTPRINT)}
rows = []
for ref in refs:
    f = current[ref]
    box = f.GetBoundingBox(False, False)
    rows.append(dict(ref=ref, before_xy=old[ref]['xy'], before_angle=old[ref]['angle'],
                     after_xy=list(p.ToMM(f.GetPosition())), after_angle=f.GetOrientationDegrees(),
                     side=f.GetLayerName(), group=groups.get(ref), uuid=f.m_Uuid.AsString(),
                     before_pads=old[ref]['pads'], after_pads=sorted((a.GetNumber(), a.GetNetname()) for a in f.Pads()),
                     before_bbox=old[ref]['bbox'],
                     after_bbox=[p.ToMM(box.GetLeft()),p.ToMM(box.GetTop()),p.ToMM(box.GetRight()),p.ToMM(box.GetBottom())]))

net = '/USB_PD_CONTROLLER/BOOST_FB'
tracks = [t for t in board.GetTracks() if t.GetNetname() == net]
pad_a = next(a for a in current['D5'].Pads() if a.GetNumber() == '2')
pad_b = next(a for a in current['U11'].Pads() if a.GetNumber() == '9')
point = lambda v: tuple(round(n,6) for n in p.ToMM(v))
edges = [(point(t.GetStart()), point(t.GetEnd()), t) for t in tracks]
start, end = point(pad_a.GetPosition()), point(pad_b.GetPosition())
adj = {}
for a,b,t in edges:
    adj.setdefault(a,[]).append((b,t)); adj.setdefault(b,[]).append((a,t))
stack = [(start,[],0.0)]
visited = set(); found = None
while stack:
    v, path, length = stack.pop()
    if v == end:
        found=(path,length); break
    if v in visited: continue
    visited.add(v)
    for nxt,t in adj.get(v,[]):
        if nxt not in visited:
            stack.append((nxt,path+[t.m_Uuid.AsString()],length+math.dist(v,nxt)))

db = json.loads((here/'drc-before.json').read_text(encoding='utf-8'))
da = json.loads((here/'drc-after.json').read_text(encoding='utf-8'))
counts = lambda d: {k:sum(v['type']==k for v in d['violations']) for k in sorted({v['type'] for v in d['violations']})}
out = dict(placements=rows, boost_fb=dict(start=start,end=end,connected=found is not None,
       segment_uuids=found[0] if found else [],length_mm=found[1] if found else None,
       layer_names=sorted({t.GetLayerName() for t in tracks})),
       drc_before=counts(db),drc_after=counts(da),
       unconnected_before=len(db['unconnected_items']),unconnected_after=len(da['unconnected_items']),
       schematic_parity_before=len(db['schematic_parity']),schematic_parity_after=len(da['schematic_parity']))
(here/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
assert all(r['before_pads']==[list(x) for x in r['after_pads']] and r['side']=='B.Cu' and r['group']=='TPS55340 PRE-BOOST' for r in rows)
assert found and found[1] <= 10
assert len(db['violations']) == len(da['violations'])
assert not da['schematic_parity']

def draw(name, use_after):
    x0,y0,scale = 48,36,15
    svg = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width='900', height='540', viewBox='0 0 900 540')
    ET.SubElement(svg,'rect',x='0',y='0',width='900',height='540',fill='#101827')
    title=ET.SubElement(svg,'text',x='24',y='29',fill='#fff',style='font: bold 19px sans-serif');title.text=name
    def pt(x,y): return ((x-x0)*scale,(y-y0)*scale)
    def line(a,b,color,width=3,dash=None):
        x1,y1=pt(*a);x2,y2=pt(*b)
        attrs=dict(x1=str(x1),y1=str(y1),x2=str(x2),y2=str(y2),stroke=color,**{'stroke-width':str(width),'marker-end':'url(#arrow)'})
        if dash: attrs['stroke-dasharray']=dash
        ET.SubElement(svg,'line',**attrs)
    defs=ET.SubElement(svg,'defs'); marker=ET.SubElement(defs,'marker',id='arrow',markerWidth='8',markerHeight='8',refX='7',refY='4',orient='auto');ET.SubElement(marker,'path',d='M0,0 L8,4 L0,8',fill='#f9c74f')
    for row in rows:
        bb=row['after_bbox' if use_after else 'before_bbox'];x,y=pt(bb[0],bb[1]);w=(bb[2]-bb[0])*scale;h=(bb[3]-bb[1])*scale
        color='#e67e48' if row['ref'] in ('L3','D4','U11') else '#8cc6a1' if row['ref'].startswith('C') else '#83a7de'
        ET.SubElement(svg,'rect',x=str(x),y=str(y),width=str(w),height=str(h),fill=color,**{'fill-opacity':'0.38','stroke':color,'stroke-width':'1.5'})
        txt=ET.SubElement(svg,'text',x=str(x+w/2),y=str(y+h/2+4),fill='#fff',**{'text-anchor':'middle'},style='font: bold 12px sans-serif');txt.text=row['ref']
    if use_after:
        line((62,46),(66.35,42.5),'#f9c74f')
        line((72.75,42.5),(72.8,49),'#f9c74f')
        line((72.8,49),(72.712,53.39),'#f9c74f')
        line((76.8,49),(75.8,54.025),'#ff8f6b',2,'5 4')
        line((75.8,54.025),(83.475,64),'#ff8f6b',2,'5 4')
        line((64,58),(67,56.64),'#68d6ef',2)
        line((70,56),(70,59),'#6cb88a',2)
        line((63,62),(63,59),'#68d6ef',2)
        ET.SubElement(svg,'rect',x='470',y='390',width='420',height='140',fill='#1b2940')
        notes=['Sarı: PD_VOUT → L3 → SW (B.Cu)', 'Turuncu kesik: D4 → V_PRE/C27-C28 koridoru', 'Mavi: FB/COMP/EN_CTRL hassas çıkış', 'Yeşil: U11.15 ve bypass GND/via alanı', 'D5.2–U11.9 izi mevcut; yeni güç izi çizilmedi']
        for i,n in enumerate(notes):
            t=ET.SubElement(svg,'text',x='482',y=str(414+i*23),fill='#eef',style='font: 13px sans-serif');t.text=n
    ET.ElementTree(svg).write(here/('after.svg' if use_after else 'before.svg'),encoding='unicode',xml_declaration=True)
draw('TASK-072 | Önce',False)
draw('TASK-072 | Sonra: B.Cu yerleşim ve koridorlar',True)
print(json.dumps({k:out[k] for k in ('boost_fb','drc_before','drc_after','unconnected_before','unconnected_after','schematic_parity_after')},ensure_ascii=False))
