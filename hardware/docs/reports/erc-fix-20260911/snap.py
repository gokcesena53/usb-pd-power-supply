from pathlib import Path
import math,json
exec(Path('reports/fixes-20260909/fix.py').read_text(encoding='utf8').split('pd=Sch(')[0])
def snap(v):return round(math.floor(float(v)/1.27+0.500001)*1.27,6)
log=[]
for f in Path('.').glob('*.kicad_sch'):
 a=Sch(f)
 for z in a.t:
  typ=tag(z)
  if typ=='symbol':
   at=one(z,'at');x,y=at[1:3];nx,ny=snap(x),snap(y);at[1:3]=[nx,ny]
   if (x,y)!=(nx,ny):
    log.append([f.name,prop(z,'Reference')[2],x,y,nx,ny])
    for p in all(z,'property'):
     at=one(p,'at');at[1]=round(at[1]+nx-x,6);at[2]=round(at[2]+ny-y,6)
  elif typ in ['wire','bus','junction','label','global_label','hierarchical_label','no_connect']:
   for b in walk(z):
    if tag(b) in ['at','xy']:b[1:3]=[snap(v) for v in b[1:3]]
 # Drop only zero-length or exactly duplicate wires introduced by quantization.
 seen=set()
 for z in list(all(a.t,'wire')):
  ps=[tuple(p[1:]) for p in one(z,'pts')[1:]];key=tuple(sorted(ps))
  if ps[0]==ps[1] or key in seen:a.t.remove(z)
  else:seen.add(key)
 a.save()
# Synchronize the actual reviewed encoder symbol into the project library.
u=Sch('userinterface.kicad_sch');ref=u.sym('SW3');lid=one(ref,'lib_id')[1];cached=copy.deepcopy(next(z for z in one(u.t,'lib_symbols')[1:] if z[1]==lid));name=lid.split(':',1)[1];cached[1]=name
p=Path('Power_Supply_Custom.kicad_sym');lib=s.loads(p.read_text(encoding='utf8'));old=next(z for z in all(lib,'symbol') if z[1]==name)
def pins(z):return sorted((one(a,'number')[1],one(a,'name')[1]) for a in walk(z) if tag(a)=='pin')
print('Encoder cached pins',pins(cached),'library pins',pins(old))
lib[lib.index(old)]=cached;p.write_text(s.dumps(lib)+'\n',encoding='utf8')
Path('reports/erc-fix-20260911/moved.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf8')
print('Moved symbols',len(log))
