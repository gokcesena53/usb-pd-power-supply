from pathlib import Path
import math,json
from KicadModTree import Footprint,FootprintType,Property,Text,Pad,Rectangle,Circle,Line,Arc,Model,KicadFileHandler
import cadquery as cq, ezdxf
lib=Path('Power_Output_Custom.pretty');lib.mkdir(exist_ok=True)
models=Path('Power_Output_Custom.3dshapes');models.mkdir(exist_ok=True)
spec={'battery':{'source':'L-KLS5-CR2032-05 drawing 2025-03-31','pad_centres':[[-14.55,0],[14.55,0]],'pad_size':[3.6,4.5],'polarity':['+','-'],'body':[28.5,16,5.5]},'terminal':{'pitch':5.08,'row_spacing':7.62,'drill':1.35,'pad_diameter_engineering_choice':2.35,'body':[12.7,14.1,13.4]},'banana':{'cutout_diameter':8.33,'across_flats':6.35,'head_diameter':11.13,'panel_max':8.8,'source':'User supplied Cinch 108-0904 family drawing; red/black product identities verified'}}
(lib/'dimensions.json').write_text(json.dumps(spec,indent=2))
def base(name,typ,description):
 f=Footprint(name,typ);f.setDescription(description);f.append(Property(name='Reference',text='REF**',at=[0,-10],layer='F.SilkS'));f.append(Property(name='Value',text=name,at=[0,11],layer='F.Fab'));return f
def rect(f,a,b,layer,w):f.append(Rectangle(start=a,end=b,layer=layer,width=w))
def save(f,folder=lib):KicadFileHandler(f).writeFile(str(folder/(f.name+'.kicad_mod')))
f=base('KLS_CR2032_05',FootprintType.SMD,'KLS L-KLS5-CR2032-05 family; pad1 positive left, pad2 negative right; 3.6x4.5 pads, 32.7 outer span; verify purchased R1 variant against drawing')
for number,x in [(1,-14.55),(2,14.55)]:f.append(Pad(number=number,type=Pad.TYPE_SMT,shape=Pad.SHAPE_RECT,at=[x,0],size=[3.6,4.5],layers=Pad.LAYERS_SMT))
rect(f,[-14.25,-8],[14.25,8],'F.Fab',.1);rect(f,[-16.6,-8.25],[16.6,8.25],'F.CrtYd',.05)
for y in [-8.12,8.12]:f.append(Line(start=[-14.25,y],end=[14.25,y],layer='F.SilkS',width=.12))
f.append(Text(text='+',at=[-11,-6],layer='F.SilkS'));f.append(Text(text='-',at=[11,-6],layer='F.SilkS'))
model=cq.Workplane('XY').box(28.5,16,5.5,centered=(True,True,False)).cut(cq.Workplane('XY').workplane(offset=1).circle(10.1).extrude(5));cq.exporters.export(model,str(models/'KLS_CR2032_05.step'));f.append(Model(filename='${KIPRJMOD}/Power_Output_Custom.3dshapes/KLS_CR2032_05.step'));save(f)
# Retain existing library identity while correcting the body origin/envelope.
name='DG142R-5.08-02P-14-00AH';f=base(name,FootprintType.THT,'Degson DG142R 2P: pitch5.08, rows7.62, drill1.35, body12.70x14.10, height13.4; pad diameter2.35 engineering choice')
for n,x in [(1,0),(2,5.08)]:
 for y in [0,7.62]:f.append(Pad(number=n,type=Pad.TYPE_THT,shape=Pad.SHAPE_RECT if (n==1 and y==0) else Pad.SHAPE_CIRCLE,at=[x,y],size=[2.35,2.35],drill=1.35,layers=Pad.LAYERS_THT))
rect(f,[-2.54,-1.75],[10.16,12.35],'F.Fab',.1);rect(f,[-2.66,-1.87],[10.28,12.47],'F.SilkS',.12);rect(f,[-3.04,-2.25],[10.66,12.85],'F.CrtYd',.05)
f.append(Text(text='1 +',at=[0,-3.4],layer='F.SilkS'));f.append(Text(text='2 -',at=[5.08,-3.4],layer='F.SilkS'))
shape=cq.Workplane('XY').box(12.7,14.1,13.4,centered=(False,False,False)).translate((-2.54,-12.35,0))
cq.exporters.export(shape,str(models/(name+'.step')));f.append(Model(filename='${KIPRJMOD}/Power_Output_Custom.3dshapes/'+name+'.step'));save(f,Path(name+'.pretty'))
# Panel-only document footprints, deliberately no copper pads or PCB edge cuts.
r=8.33/2;y=6.35/2;x=math.sqrt(r*r-y*y)
for code in ['108-0902-001','108-0903-001']:
 name='Cinch_'+code+'_Panel';f=base(name,FootprintType.UNSPECIFIED,'OFF-BOARD panel mount; double-D panel opening 8.33 diameter / 6.35 across flats. No electrical PCB pad. Wire solder lug to J4.')
 for layer in ['Dwgs.User','F.Fab']:
  f.append(Line(start=[-x,-y],end=[x,-y],layer=layer,width=.1));f.append(Line(start=[-x,y],end=[x,y],layer=layer,width=.1))
  f.append(Arc(start=[x,-y],mid=[r,0],end=[x,y],layer=layer,width=.1));f.append(Arc(start=[-x,y],mid=[-r,0],end=[-x,-y],layer=layer,width=.1))
 f.append(Circle(center=[0,0],radius=11.13/2,layer='F.Fab',width=.1));rect(f,[-6,-6],[6,6],'F.CrtYd',.05)
 f.append(Text(text='PANEL ONLY - NO PCB PAD',at=[0,7.5],layer='Dwgs.User',size=[.8,.8]))
 body=cq.Workplane('XY').circle(11.13/2).extrude(4.78).union(cq.Workplane('XY').circle(7.9375/2).extrude(-11.91)).cut(cq.Workplane('XY').circle(4.44/2).extrude(4.78))
 cq.exporters.export(body,str(models/(name+'.step')));f.append(Model(filename='${KIPRJMOD}/Power_Output_Custom.3dshapes/'+name+'.step'));save(f)
doc=ezdxf.new();ms=doc.modelspace();a=math.degrees(math.asin(y/r));ms.add_line((-x,y),(x,y));ms.add_line((-x,-y),(x,-y));ms.add_arc((0,0),r,360-a,a);ms.add_arc((0,0),r,180-a,180+a);doc.units=4;doc.saveas(str(lib/'Cinch_108_090x_doubleD_panel_cutout_mm.dxf'))
(models/'README.txt').write_text('STEP models are simplified clearance envelopes, not manufacturer detailed models. Terminal height 13.4 reference. Banana nut and solder lug omitted where complete dimensions are unavailable. Panel jack models must not be placed as electrically soldered PCB components. Battery cavity is illustrative; fit checks use dimensioned footprint and actual part.\n')
print('Created battery, terminal and two panel footprints; STEP envelope models and mm DXF.')
