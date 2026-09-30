from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
D=Path(__file__).resolve().parent
mesh=json.loads((D/'assembly-mesh.json').read_text())
colors={'encoder':'#b5bac2','board-body':'#347957','J7':'#e2b653','J8':'#599aca','J9':'#a66bc0','panel-world':'#c89562'}
fig,axes=plt.subplots(1,2,figsize=(14,7))
for ax,kind in zip(axes,['top','left']):
 tris=[]
 for name,data in mesh.items():
  v=np.array(data['vertices']);faces=np.array(data['faces']);xyz=v[faces]
  if kind=='top':
   uv=xyz[:,:,[0,1]].copy();uv[:,:,1]*=-1;depth=xyz[:,:,2].mean(axis=1)
  else:
   uv=xyz[:,:,[1,2]].copy();uv[:,:,0]*=-1;depth=-xyz[:,:,0].mean(axis=1)
  for poly,d in zip(uv,depth):tris.append((d,poly,colors[name],.25 if name=='panel-world' else 1))
 tris.sort(key=lambda t:t[0])
 ax.add_collection(PolyCollection([t[1] for t in tris],facecolors=[matplotlib.colors.to_rgba(t[2],t[3]) for t in tris],edgecolors='none'))
 ax.set_aspect('equal');ax.grid(alpha=.15);ax.set_axisbelow(True)
 if kind=='top':
  ax.set_xlim(33,74);ax.set_ylim(131,75);ax.set_xlabel('PCB X (mm)');ax.set_ylabel('PCB Y (mm)')
  ax.set_title('Üstten: sol kenar ve encoder')
  ax.annotate('Yeni sol kenar X=59,8',xy=(59.8,114),xytext=(62,126),arrowprops={'arrowstyle':'->'},fontsize=9)
  ax.annotate('Şaft ucu X=37,3',xy=(37.3,112.4),xytext=(34,103),arrowprops={'arrowstyle':'->'},fontsize=9)
  ax.text(62,110,'J9',fontsize=9)
 else:
  ax.set_xlim(76,124);ax.set_ylim(-21,14);ax.set_xlabel('Panel yatay konumu / PCB Y (mm)');ax.set_ylabel('STEP Z (mm)')
  ax.set_title('Sol panelden: şaft önden görülür')
  for z,color in [(3.325,'#c58916'),(-9.585,'#357dab'),(-3.13,'#b73740')]:ax.axhline(z,color=color,ls='--',lw=.9)
  ax.plot([88.5,88.5,112.4],[3.325,-9.585,-3.13],'o',color='#b73740',ms=3)
  ax.annotate('Şaft Z=-3,130',xy=(112.4,-3.13),xytext=(101,9),arrowprops={'arrowstyle':'->'},fontsize=10)
  ax.text(77,4.3,'USB merkezi +3,325',fontsize=9)
  ax.text(77,-12.5,'RJ45 merkezi -9,585',fontsize=9)
fig.suptitle('TASK-094 | 3 mm düz panel | şaft çıkıntısı 9,5 mm',fontsize=15)
fig.text(.5,.025,'RJ45 açıklığı mevcut yaklaşık modele dayanır. Panel kahverengi saydam gösterilir; fiziksel örnek kontrolü sürer.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.05,1,.94));fig.savefig(D/'mounting-review.png',dpi=180)
# Full working-area inventory, including parked blocks.
data=json.loads((D/'placement.json').read_text());fig,ax=plt.subplots(figsize=(10,8))
parked={r for g in data['parked_blocks'].values() for r in g['refs']}
for r,f in data['after'].items():
 x,y=f['xy'];c='#dc7633' if r in parked else '#2471a3';ax.plot(x,y,'.',color=c)
 if r in parked or r in ['J7','J8','J9','MECH_ENC']:ax.text(x+.3,y,r,fontsize=6,color=c)
outline=[(53.3,69.48),(146.7,69.48),(149.7,72.48),(149.7,127.52),(146.7,130.52),(53.3,130.52),(50.3,127.52),*list(reversed(data['new_left_edge']))[1:],(53.3,69.48)]
ax.plot(*zip(*outline),color='#347957')
ax.set_aspect('equal');ax.invert_yaxis();ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)');ax.grid(alpha=.2)
ax.set_title('26 komponent geçici park alanlarında; geri yerleşim TASK-095')
fig.tight_layout();fig.savefig(D/'parked-blocks.png',dpi=180)
