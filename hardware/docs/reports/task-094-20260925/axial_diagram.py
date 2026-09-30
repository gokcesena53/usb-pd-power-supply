from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
D=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(11,4.8))
ax.set_xlim(-3,23);ax.set_ylim(-6,8)
ax.add_patch(Rectangle((12.5,-2.6),4.5,5.2,facecolor='#374151'))
ax.add_patch(Rectangle((7.5,-1.6),5,3.2,facecolor='#94a3b8'))
ax.add_patch(Rectangle((0,-1),7.5,2,facecolor='#cbd5e1',edgecolor='#475569'))
ax.add_patch(Rectangle((9.5,-4),3,8,facecolor='#f59e0b',alpha=.35,hatch='//'))
ax.axvline(0,color='#2563eb',ls='--');ax.axhline(0,color='#64748b',lw=.7,ls=':')
ax.text(0,6.4,'USB giriş yüzü = şaft ucu',ha='center',color='#2563eb')
ax.text(11,4.4,'3 mm iç destek / kademeli panel',ha='center',color='#92400e')
ax.text(14.75,0,'Encoder\ngövdesi',ha='center',va='center',color='white')
ax.text(3.7,1.4,'Şaft',ha='center');ax.text(8.4,-2.2,'Burç',ha='center')
for a,b,y,t in [(0,12.5,-4.8,'12,5 mm'),(0,9.5,5.4,'9,5 mm içeride')]:
 ax.annotate('',xy=(a,y),xytext=(b,y),arrowprops={'arrowstyle':'<->','color':'#111827'})
 ax.text((a+b)/2,y+.2,t,ha='center')
ax.text(20,4,'Kutu içi →',ha='center');ax.text(-1,-2.8,'← Dış',ha='center')
ax.set_xlabel('USB giriş düzleminden içeri mesafe (mm)')
ax.set_yticks([]);ax.spines[['top','right','left']].set_visible(False)
fig.suptitle('TASK-094: şaft ucu hizası için gerekli montaj derinliği',fontsize=15)
fig.text(.5,.015,'Eksen kesiti; düşey boyutlar şematiktir. Dış kasa yüzeyinin yeri henüz belirlenmedi.',ha='center',fontsize=10)
fig.tight_layout(rect=(0,.045,1,.94));fig.savefig(D/'axial-mounting.png',dpi=170)
