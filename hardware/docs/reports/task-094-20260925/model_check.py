from pathlib import Path
import json
import FreeCAD as A, Part
D=Path(__file__).resolve().parent
ROOT=D.parents[3]
def bounds(s):
 b=s.BoundBox
 return [round(v,5) for v in (b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax)]
ports={r:Part.read(str(D/(r+'.step'))) for r in ['J7','J8']}
out={'coordinate_system':'KiCad STEP world: X right, Y negative PCB Y, Z up; all mm','ports':{r:{'bounds':bounds(s),'solids':[bounds(v) for v in s.Solids]} for r,s in ports.items()}}
# Model origin is shaft axis on rear body plane. +Z points toward shaft tip.
# Drawing p1: body 12 x 11.7 x 4.5; tabs overall 12.5; E bushing D7 x 5;
# F shaft L12.5, flat length4.5, across flat4.5; terminals reach -3.5.
pieces={'body':Part.makeBox(12,11.7,4.5,A.Vector(-6,-5.85,0)),
 'bushing':Part.makeCylinder(3.5,5,A.Vector(0,0,4.5)),
 'shaft':Part.makeCylinder(3,7.5,A.Vector(0,0,9.5))}
pieces['shaft']=pieces['shaft'].cut(Part.makeBox(10,5,4.5,A.Vector(-5,1.5,12.5)))
for side in [-1,1]:
 pieces['tab'+str(side)]=Part.makeBox(2,.4,7,A.Vector(-1,side*6.05-.2,-2.5))
for i,(x,y) in enumerate([(-7.5,-2.5),(-7.5,0),(-7.5,2.5),(7,-2.5),(7,2.5)],1):
 pieces['pin'+str(i)]=Part.makeBox(.3,.9,4.5,A.Vector(x-.15,y-.45,-3.5))
 # Simplified bent lead connection to housing; width from p1, thickness nominal.
 a,b=sorted([x,-6 if x<0 else 6])
 pieces['lead'+str(i)]=Part.makeBox(b-a+.15,.9,.3,A.Vector(a-.075,y-.45,.6))
model=Part.makeCompound(list(pieces.values()))
model.exportStep(str(D/'encoder-axis-origin.step'))
out['encoder']={'model':'encoder-axis-origin.step','bounds':bounds(model),'valid':model.isValid(),'parts':{k:bounds(v) for k,v in pieces.items()},'shaft_tip_from_body_front_mm':12.5,'bushing_length_mm':5,'panel_thickness_mm':3,'shaft_protrusion_from_panel_outer_when_body_front_seated_mm':9.5,'limitations':['Bushing thread not specified in drawing; thread and nut not claimed.','Lead thickness and frame details simplified; mechanical envelope only.','Exact circular shaft and F flat included; original STEP used stepped boxes and omitted flat.']}
usb_x=ports['J7'].BoundBox.XMin
out['axial_constraints']={'usb_mouth_x_mm':usb_x,'shaft_tip_x_mm':usb_x,'encoder_body_front_x_mm':usb_x+12.5,'encoder_body_rear_x_mm':usb_x+17,'encoder_terminal_rear_x_mm':usb_x+20.5,'panel_outer_x_if_seated_mm':usb_x+9.5,'panel_inner_x_if_seated_mm':usb_x+12.5,'required_setback_from_usb_mouth_mm':9.5,'note':'A flat common panel at USB mouth cannot also directly seat this encoder with its tip flush to the mouth; an internal support or stepped encoder panel region is required.'}
(D/'mechanical-analysis.json').write_text(json.dumps(out,indent=2))
# Updated user decision: flat external 3 mm panel; shaft may protrude.
usb_z=(3.025+3.625)/2 # Actual USB mouth cylindrical arc axes, not whole-body bbox.
rj_z=(-14.085-5.085)/2 # Explicit RJ45_port solid in project's simplified model.
zc=(usb_z+rj_z)/2
panel_inner=49.8; panel_outer=46.8; yc=112.4; rear=panel_inner+4.5
matrix=A.Matrix(0,0,-1,0, -1,0,0,0, 0,1,0,0, 0,0,0,1)
oriented=model.transformGeometry(matrix)
world=oriented.copy();world.translate(A.Vector(rear,-yc,zc))
local=oriented.copy();local.translate(A.Vector(0,0,zc-1.595))
lib=ROOT/'hardware/libraries/Mechanical_Custom.3dshapes';lib.mkdir(exist_ok=True)
local.exportStep(str(lib/'Encoder_Panel_EC1121S.step'))
world.exportStep(str(D/'encoder-world.step'))
panel=Part.makeBox(3,60,35,A.Vector(panel_outer,-135,-23))
panel=panel.cut(Part.makeCylinder(3.65,5,A.Vector(panel_outer-1,-yc,zc),A.Vector(1,0,0)))
# Oversized clear through apertures; actual plug overmould/latch need enclosure sample.
panel=panel.cut(Part.makeBox(5,12,6,A.Vector(panel_outer-1,-94.5,.325)))
panel=panel.cut(Part.makeBox(5,18,17,A.Vector(panel_outer-1,-97.5,-18.585)))
panel.exportStep(str(D/'panel-world.step'))
out['current_mount']={'decision':'Flat outer panel, shaft protrusion allowed; supersedes axial_constraints above','usb_opening_center_z':usb_z,'rj45_model_opening_center_z':rj_z,'shaft_center_z':zc,'pcb_top_z':1.595,'shaft_center_from_pcb_top':zc-1.595,'encoder_rear_axis_xy':[rear,yc],'panel_inner_x':panel_inner,'panel_outer_x':panel_outer,'board_to_panel_gap_mm':.5,'shaft_tip_x':panel_inner-12.5,'shaft_protrusion_mm':9.5,'bounds_world':bounds(world),'port_center_limitation':'RJ45 aperture model is approximate, sample validation remains TASK-053.','panel_location_assumption':'0.5 mm between original board left edge and panel inner face; 3 mm thickness per user.'}
out['current_pairs']={r:{'distance_mm':world.distToShape(s)[0],'intersection_mm3':world.common(s).Volume} for r,s in {**ports,'panel':panel}.items()}
(D/'mechanical-analysis.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'mount':out['current_mount'],'pairs':out['current_pairs']},indent=2))
