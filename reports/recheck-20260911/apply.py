from pathlib import Path
import json, xml.etree.ElementTree as E
src=Path('reports/output-update/update_schematic.py').read_text(encoding='utf8')
# Reuse field/package/direction helpers, excluding the old layout rebuild.
src=src.split(" if f.name=='userinterface.kicad_sch':")[0]
src=src.replace("  note(sch,'BT1:","  # note(sch,'BT1:")
src+='\n sch.save()\n'
exec(src)
m=Sch('mcu.kicad_sch');field(m.sym('C7'),'Footprint','Capacitor_SMD:C_0603_1608Metric');m.save()
p=Sch('usb_pd_controller.kicad_sch');field(p.sym('R12'),'Footprint','Resistor_SMD:R_0603_1608Metric');p.save()
o=Sch('poweroutput.kicad_sch')
for ref,mpn in [('J5','108-0902-001'),('J6','108-0903-001')]:
 a=o.sym(ref)
 for k,v in {'Value':mpn,'MPN':mpn,'Manufacturer':'Cinch Johnson','Footprint':'Power_Output_Custom:Cinch_'+mpn+'_Panel','AssemblyNote':'PANEL MOUNT; wire to J4; mechanical footprint only'}.items():field(a,k,v)
 one(a,'on_board')[1]=S('no')
assert not any(prop(a,'Reference')[2]=='J7' for a in all(o.t,'symbol'))
note(o,'PANEL: J5 red (+), J6 black (GND).\nJ4.1 = OUT_POS; J4.2 = GND.\nPanel-mount jacks: wire to PCB terminal.',114.3,137.16)
o.save()
u=Sch('userinterface.kicad_sch');a=u.sym('J3')
for k,v in {'Value':'NHD-2.4-240320AF-CSXP','MPN':'54132-4062','Manufacturer':'Molex','DisplayMPN':'NHD-2.4-240320AF-CSXP'}.items():field(a,k,v)
u.save()
Path('reports/recheck-20260911/changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),encoding='utf8')
r=E.parse('reports/recheck-20260911/before.xml').getroot()
n={(p.get('ref'),p.get('pin')):net.get('name') for net in r.find('nets') for p in net}
for ref in ['R4','R5','R6','R7','R8','R11','Q5','J3','U5','BT1']:
 print(ref,{p:net for (a,p),net in n.items() if a==ref})
