import json
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

out = Path('hardware/docs/reports/flow-space-plan-20260928')
d = json.loads((out/'board-audit.json').read_text(encoding='utf-8'))
fps = {f['ref']: f for f in d['footprints']}
colors = plt.get_cmap('tab20').colors
group_color = {r: colors[i % 20] for i,g in enumerate(d['groups']) for r in g['refs']}
fig, axes = plt.subplots(2, 1, figsize=(13, 16), constrained_layout=True)
labels = {r for r in fps if r.startswith(('U','Q','J','L','Y','H'))} | {'R43','RShunt1','R11','C28','C29','C12','C13','C16','C33','D4','D7','R67','MECH_ENC'}
for ax, side in zip(axes, ['F.Cu','B.Cu']):
    cy = 'F.Courtyard' if side == 'F.Cu' else 'B.Courtyard'
    for line in d['outline']:
        ax.add_patch(Polygon(line, closed=True, facecolor='#f6f8fa', edgecolor='#334155', linewidth=1))
    for f in d['footprints']:
        for poly in f['courtyards'].get(cy, []):
            ax.add_patch(Polygon(poly, closed=True, facecolor=group_color.get(f['ref'],'#777777'), edgecolor='#444', alpha=.45, lw=.6))
        if f['layer'] == side and f['ref'] in labels:
            x,y = f['xy']
            ax.text(x,y, f['ref'], fontsize=7, ha='center', va='center', weight='bold', bbox={'facecolor':'white','alpha':.75,'edgecolor':'none','pad':.7})
    if side == 'B.Cu':
        windows = [('A',106,109,8,12),('B',124,118.5,10,6)]
        for label,x,y,w,h in windows:
            ax.add_patch(Rectangle((x,y),w,h,facecolor='#bbf7d0',edgecolor='#15803d',ls='--',lw=1.5,alpha=.55))
            ax.text(x+w/2,y+.6,label,ha='center',va='top',fontsize=12,weight='bold',color='#166534')
        ax.annotate('', xy=(129,120.1),xytext=(129,123.1),arrowprops={'arrowstyle':'->','color':'#15803d','lw':2})
        ax.annotate('', xy=(107.5,118.75),xytext=(110,125),arrowprops={'arrowstyle':'->','color':'#15803d','lw':2})
        moves=json.loads((out/'candidate/moves.json').read_text(encoding='utf-8'))
        for move in moves:
            ref=move['ref']; old=move['before']; new=move['candidate']
            theta=math.radians(old[2]-new[2]); co=math.cos(theta); si=math.sin(theta)
            for poly in fps[ref]['courtyards'].get(cy,[]):
                pts=[(new[0]+co*(x-old[0])-si*(y-old[1]),new[1]+si*(x-old[0])+co*(y-old[1])) for x,y in poly]
                ax.add_patch(Polygon(pts,closed=True,fill=False,edgecolor='#1d4ed8',ls='--',lw=1.3))
    else:
        ax.add_patch(Rectangle((70,85),30,13,fill=False,edgecolor='#64748b',ls='--',lw=1.2))
        ax.text(85,91,'C: sinyal geçişi',ha='center',color='#475569',fontsize=10)
        ax.add_patch(Rectangle((105,88),35,8,fill=False,edgecolor='#ea580c',ls='--',lw=1.5))
        ax.text(123,92,'D: çıkış besleme koridoru',ha='center',color='#c2410c',fontsize=9)
    ax.set(xlim=(48,151),ylim=(131,65),aspect='equal',xlabel='X (mm)',ylabel='Y (mm)')
    ax.set_title(('Ön yüz — F.Cu' if side=='F.Cu' else 'Arka yüz — B.Cu')+' | KiCad koordinatları, aynalanmamış görünüm',loc='left',fontsize=13,pad=12)
    ax.set_xticks(range(50,151,10)); ax.set_yticks(range(70,131,10)); ax.grid(alpha=.14)
fig.suptitle('Güç akışı ve boş alan değerlendirme planı\nRenkli şekiller: mevcut avlular · Mavi kesik çizgiler: uygulanmamış adaylar',fontsize=15)
fig.savefig(out/'placement-plan.png',dpi=180)
plt.close(fig)

def pad(ref,num): return next(p for p in fps[ref]['pads'] if p['number']==str(num))
def distance(a,b): return math.dist(a['xy'],b['xy'])
pairs=[('U11',1,'D4',2),('D4',1,'C27',1),('D4',1,'C28',1),('U11',1,'L3',1),
       ('U5',9,'C12',1),('U5',3,'C12',2),('U5',9,'C14',1),('U5',6,'R39',2),
       ('U3',10,'RShunt1',1),('U3',9,'RShunt1',2),('U3',3,'U13',2),
       ('U13',4,'Q4',1),('R11',2,'Q5',7),('R11',2,'Q3',7),('Q5',5,'RShunt1',1)]
measurements=[]
for r1,n1,r2,n2 in pairs:
    x=pad(r1,n1); y=pad(r2,n2)
    item={'from':f'{r1}.{n1}','to':f'{r2}.{n2}','distance_mm':round(distance(x,y),3),'net':x['net'],'same_net':x['net']==y['net']}
    measurements.append(item)
    print(item)
(out/'measurements.json').write_text(json.dumps(measurements,indent=2),encoding='utf-8')
