import re
import sys
import shutil
import uuid

sys.stdout.reconfigure(encoding='utf-8')

# 1. Backups
shutil.copyfile('hardware/mcu.kicad_sch', 'hardware/mcu.kicad_sch.bak')
shutil.copyfile('hardware/usb_pd_controller.kicad_sch', 'hardware/usb_pd_controller.kicad_sch.bak')
shutil.copyfile('hardware/gopo.kicad_pcb', 'hardware/gopo.kicad_pcb.bak')
print("Backups created.")

# UUIDs
uuids = {
    # TP15
    'tp15_sym': str(uuid.uuid4()),
    'tp15_pin': str(uuid.uuid4()),
    'tp15_gnd_sym': str(uuid.uuid4()),
    'tp15_gnd_pin': str(uuid.uuid4()),
    'tp15_wire': str(uuid.uuid4()),
    'tp15_fp': str(uuid.uuid4()),
    'tp15_ref': str(uuid.uuid4()),
    'tp15_val': str(uuid.uuid4()),
    'tp15_pad': str(uuid.uuid4()),
    'tp15_silk_c': str(uuid.uuid4()),
    'tp15_crtyd_c': str(uuid.uuid4()),

    # TP16 (+3.3V)
    'tp16_sym': str(uuid.uuid4()),
    'tp16_pin': str(uuid.uuid4()),
    'tp16_pwr_sym': str(uuid.uuid4()),
    'tp16_pwr_pin': str(uuid.uuid4()),
    'tp16_wire': str(uuid.uuid4()),
    'tp16_fp': str(uuid.uuid4()),
    'tp16_ref': str(uuid.uuid4()),
    'tp16_val': str(uuid.uuid4()),
    'tp16_pad': str(uuid.uuid4()),
    'tp16_silk_c': str(uuid.uuid4()),
    'tp16_crtyd_c': str(uuid.uuid4()),

    # TP17 (V_PRE)
    'tp17_sym': str(uuid.uuid4()),
    'tp17_pin': str(uuid.uuid4()),
    'tp17_label': str(uuid.uuid4()),
    'tp17_wire': str(uuid.uuid4()),
    'tp17_fp': str(uuid.uuid4()),
    'tp17_ref': str(uuid.uuid4()),
    'tp17_val': str(uuid.uuid4()),
    'tp17_pad': str(uuid.uuid4()),
    'tp17_silk_c': str(uuid.uuid4()),
    'tp17_crtyd_c': str(uuid.uuid4()),

    # TP18 (OUT_POS)
    'tp18_sym': str(uuid.uuid4()),
    'tp18_pin': str(uuid.uuid4()),
    'tp18_label': str(uuid.uuid4()),
    'tp18_wire': str(uuid.uuid4()),
    'tp18_fp': str(uuid.uuid4()),
    'tp18_ref': str(uuid.uuid4()),
    'tp18_val': str(uuid.uuid4()),
    'tp18_pad': str(uuid.uuid4()),
    'tp18_silk_c': str(uuid.uuid4()),
    'tp18_crtyd_c': str(uuid.uuid4()),

    # TP19 (SW_EN)
    'tp19_sym': str(uuid.uuid4()),
    'tp19_pin': str(uuid.uuid4()),
    'tp19_label': str(uuid.uuid4()),
    'tp19_wire': str(uuid.uuid4()),
    'tp19_fp': str(uuid.uuid4()),
    'tp19_ref': str(uuid.uuid4()),
    'tp19_val': str(uuid.uuid4()),
    'tp19_pad': str(uuid.uuid4()),
    'tp19_silk_c': str(uuid.uuid4()),
    'tp19_crtyd_c': str(uuid.uuid4()),
}

# 2. Update hardware/mcu.kicad_sch: Add TP15 and GND
with open('hardware/mcu.kicad_sch', 'r', encoding='utf-8') as f:
    mcu_sch = f.read()

tp15_sch_snippet = f"""\t(wire
\t\t(pts
\t\t\t(xy 228.6 147.32) (xy 228.6 149.86)
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{uuids['tp15_wire']}")
\t)
\t(symbol
\t\t(lib_id "power:GND")
\t\t(at 228.6 149.86 0)
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(uuid "{uuids['tp15_gnd_sym']}")
\t\t(property "Reference" "#PWR050"
\t\t\t(at 231.14 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "GND"
\t\t\t(at 230.38 148.21 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at 228.6 149.86 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at 228.6 149.86 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at 228.6 149.86 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uuids['tp15_gnd_pin']}")
\t\t)
\t\t(instances
\t\t\t(project "gopo"
\t\t\t\t(path "/a43081a6-9aa2-4898-9347-bbcb5849dafd/d73c21d5-7478-4a02-ac94-6607c580f283"
\t\t\t\t\t(reference "#PWR050")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
\t(symbol
\t\t(lib_id "Connector:TestPoint")
\t\t(at 228.6 147.32 0)
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(fields_autoplaced yes)
\t\t(uuid "{uuids['tp15_sym']}")
\t\t(property "Reference" "TP15"
\t\t\t(at 229.87 143.51 0)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "TestPoint"
\t\t\t(at 229.87 145.415 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" "TestPoint:TestPoint_Pad_D1.0mm"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Description" "test point"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Category" "Test and Measurement"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Subcategory" "Test Points"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Manufacturer" "N/A"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "MPN" "N/A"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Package" "SMD Pad D1.0mm"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "MountingType" "Surface Mount"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Lifecycle" "N/A"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "RoHS" "N/A"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "OperatingTemp" "TBD"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Height" "TBD"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "DesignNote" "1.0 mm SMD test pedi; satin alinan parca degildir."
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "SelectionNote" "Özdisan (21.09.2026): Satın alınmaz. Kart üzerindeki pad; satın alınmaz."
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "AssemblyNote" "TBD"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "HardwareType" "Test Point"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "PadDiameter" "1.0mm"
\t\t\t(at 228.6 147.32 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{uuids['tp15_pin']}")
\t\t)
\t\t(instances
\t\t\t(project "gopo"
\t\t\t\t(path "/a43081a6-9aa2-4898-9347-bbcb5849dafd/d73c21d5-7478-4a02-ac94-6607c580f283"
\t\t\t\t\t(reference "TP15")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
"""

# Insert before the last closing paren of mcu_sch
last_paren_idx = mcu_sch.rfind(')')
mcu_sch_updated = mcu_sch[:last_paren_idx] + tp15_sch_snippet + mcu_sch[last_paren_idx:]
with open('hardware/mcu.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(mcu_sch_updated)
print("Updated hardware/mcu.kicad_sch.")

# 3. Update hardware/usb_pd_controller.kicad_sch: Add TP16 (+3.3V), TP17 (V_PRE), TP18 (OUT_POS), TP19 (SW_EN)
with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    pd_sch = f.read()

def create_sch_tp(ref, val_label, is_global, pwr_lib, at_x, at_y, sym_uuid, pin_uuid, conn_uuid, wire_uuid, ref_pwr="#PWR"):
    # at_x, at_y is pin location
    # TP symbol is placed at at_x, at_y
    res = ""
    if pwr_lib:
        # wire to power symbol above at_y - 2.54
        res += f"""\t(wire
\t\t(pts
\t\t\t(xy {at_x} {at_y}) (xy {at_x} {at_y - 2.54:.2f})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{wire_uuid}")
\t)
\t(symbol
\t\t(lib_id "{pwr_lib}")
\t\t(at {at_x} {at_y - 2.54:.2f} 0)
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(uuid "{conn_uuid}")
\t\t(property "Reference" "{ref_pwr}"
\t\t\t(at {at_x + 2.54:.2f} {at_y - 5.08:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "{val_label}"
\t\t\t(at {at_x + 1.78:.2f} {at_y - 4.19:.2f} 0)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" ""
\t\t\t(at {at_x} {at_y - 2.54:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {at_x} {at_y - 2.54:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Description" ""
\t\t\t(at {at_x} {at_y - 2.54:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{pin_uuid}_pwr")
\t\t)
\t\t(instances
\t\t\t(project "gopo"
\t\t\t\t(path "/a43081a6-9aa2-4898-9347-bbcb5849dafd/ef9b8359-2233-4750-a469-a0efa9e391b0"
\t\t\t\t\t(reference "{ref_pwr}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
"""
    elif is_global:
        # wire to global label
        res += f"""\t(wire
\t\t(pts
\t\t\t(xy {at_x} {at_y}) (xy {at_x - 5.08:.2f} {at_y})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{wire_uuid}")
\t)
\t(global_label "{val_label}"
\t\t(shape passive)
\t\t(at {at_x - 5.08:.2f} {at_y} 180)
\t\t(fields_autoplaced yes)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify right)
\t\t)
\t\t(uuid "{conn_uuid}")
\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"
\t\t\t(at {at_x - 5.08:.2f} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify right)
\t\t\t)
\t\t)
\t)
"""
    else:
        # local label
        res += f"""\t(wire
\t\t(pts
\t\t\t(xy {at_x} {at_y}) (xy {at_x - 5.08:.2f} {at_y})
\t\t)
\t\t(stroke
\t\t\t(width 0)
\t\t\t(type default)
\t\t)
\t\t(uuid "{wire_uuid}")
\t)
\t(label "{val_label}"
\t\t(at {at_x - 5.08:.2f} {at_y} 180)
\t\t(fields_autoplaced yes)
\t\t(effects
\t\t\t(font
\t\t\t\t(size 1.27 1.27)
\t\t\t)
\t\t\t(justify right)
\t\t)
\t\t(uuid "{conn_uuid}")
\t)
"""

    # TP symbol
    res += f"""\t(symbol
\t\t(lib_id "Connector:TestPoint")
\t\t(at {at_x} {at_y} 0)
\t\t(unit 1)
\t\t(body_style 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(in_pos_files yes)
\t\t(dnp no)
\t\t(fields_autoplaced yes)
\t\t(uuid "{sym_uuid}")
\t\t(property "Reference" "{ref}"
\t\t\t(at {at_x + 1.27:.2f} {at_y - 3.81:.2f} 0)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Value" "TestPoint"
\t\t\t(at {at_x + 1.27:.2f} {at_y - 1.905:.2f} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t\t(justify left)
\t\t\t)
\t\t)
\t\t(property "Footprint" "TestPoint:TestPoint_Pad_D1.0mm"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Description" "test point"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Category" "Test and Measurement"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Subcategory" "Test Points"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Manufacturer" "N/A"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "MPN" "N/A"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Package" "SMD Pad D1.0mm"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "MountingType" "Surface Mount"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Lifecycle" "N/A"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "RoHS" "N/A"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "OperatingTemp" "TBD"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Height" "TBD"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "DesignNote" "1.0 mm SMD test pedi; satin alinan parca degildir."
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "SelectionNote" "Özdisan (21.09.2026): Satın alınmaz. Kart üzerindeki pad; satın alınmaz."
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "AssemblyNote" "TBD"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "HardwareType" "Test Point"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "PadDiameter" "1.0mm"
\t\t\t(at {at_x} {at_y} 0)
\t\t\t(hide yes)
\t\t\t(show_name no)
\t\t\t(do_not_autoplace no)
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(pin "1"
\t\t\t(uuid "{pin_uuid}")
\t\t)
\t\t(instances
\t\t\t(project "gopo"
\t\t\t\t(path "/a43081a6-9aa2-4898-9347-bbcb5849dafd/ef9b8359-2233-4750-a469-a0efa9e391b0"
\t\t\t\t\t(reference "{ref}")
\t\t\t\t\t(unit 1)
\t\t\t\t)
\t\t\t)
\t\t)
\t)
"""
    return res

pd_snippets = ""
# TP16 (+3.3V)
pd_snippets += create_sch_tp("TP16", "+3.3V", False, "power:+3.3V", 368.30, 215.90, uuids['tp16_sym'], uuids['tp16_pin'], uuids['tp16_pwr_sym'], uuids['tp16_wire'], ref_pwr="#PWR051")
# TP17 (V_PRE)
pd_snippets += create_sch_tp("TP17", "V_PRE", True, None, 368.30, 226.06, uuids['tp17_sym'], uuids['tp17_pin'], uuids['tp17_label'], uuids['tp17_wire'])
# TP18 (OUT_POS)
pd_snippets += create_sch_tp("TP18", "OUT_POS", True, None, 368.30, 236.22, uuids['tp18_sym'], uuids['tp18_pin'], uuids['tp18_label'], uuids['tp18_wire'])
# TP19 (SW_EN)
pd_snippets += create_sch_tp("TP19", "SW_EN", False, None, 368.30, 246.38, uuids['tp19_sym'], uuids['tp19_pin'], uuids['tp19_label'], uuids['tp19_wire'])

last_paren_idx = pd_sch.rfind(')')
pd_sch_updated = pd_sch[:last_paren_idx] + pd_snippets + pd_sch[last_paren_idx:]
with open('hardware/usb_pd_controller.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(pd_sch_updated)
print("Updated hardware/usb_pd_controller.kicad_sch.")

# 4. Update hardware/gopo.kicad_pcb
with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

# Helper to generate a new footprint definition for KiCad PCB
def make_pcb_tp(ref, net_name, layer, x, y, path, sheetname, sheetfile, fp_uuid, ref_uuid, val_uuid, pad_uuid, silk_uuid, crtyd_uuid):
    is_bottom = (layer == "B.Cu")
    silk_layer = "B.SilkS" if is_bottom else "F.SilkS"
    crtyd_layer = "B.CrtYd" if is_bottom else "F.CrtYd"
    fab_layer = "B.Fab" if is_bottom else "F.Fab"
    mask_layer = "B.Mask" if is_bottom else "F.Mask"
    mirror_clause = "(justify mirror)" if is_bottom else ""

    return f"""\t(footprint "TestPoint:TestPoint_Pad_D1.0mm"
\t\t(layer "{layer}")
\t\t(uuid "{fp_uuid}")
\t\t(at {x} {y})
\t\t(descr "SMD pad as test Point, diameter 1.0mm")
\t\t(tags "test point SMD pad")
\t\t(property "Reference" "{ref}"
\t\t\t(at 1.129 0.381 270)
\t\t\t(layer "{silk_layer}")
\t\t\t(uuid "{ref_uuid}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 0.7 0.7)
\t\t\t\t\t(thickness 0.12)
\t\t\t\t)
\t\t\t\t{mirror_clause}
\t\t\t)
\t\t)
\t\t(property "Value" "TestPoint"
\t\t\t(at 0 -1.55 0)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{val_uuid}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t\t{mirror_clause}
\t\t\t)
\t\t)
\t\t(property "Datasheet" "TBD"
\t\t\t(at 0 0 180)
\t\t\t(unlocked yes)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t\t{mirror_clause}
\t\t\t)
\t\t)
\t\t(property "Description" "test point"
\t\t\t(at 0 0 180)
\t\t\t(unlocked yes)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t\t{mirror_clause}
\t\t\t)
\t\t)
\t\t(property "Category" "Test and Measurement"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Subcategory" "Test Points"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Manufacturer" "N/A"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "MPN" "N/A"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Package" "SMD Pad D1.0mm"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "MountingType" "Surface Mount"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Lifecycle" "N/A"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "RoHS" "N/A"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "OperatingTemp" "TBD"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "Height" "TBD"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "DesignNote" "1.0 mm SMD test pedi; satin alinan parca degildir."
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "SelectionNote" "Özdisan (21.09.2026): Satın alınmaz. Kart üzerindeki pad; satın alınmaz."
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "AssemblyNote" "TBD"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "HardwareType" "Test Point"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property "PadDiameter" "1.0mm"
\t\t\t(at 0 0 270)
\t\t\t(layer "{fab_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{uuid.uuid4()}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1.27 1.27)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
\t\t\t)
\t\t)
\t\t(property ki_fp_filters "Pin* Test*")
\t\t(path "{path}")
\t\t(sheetname "{sheetname}")
\t\t(sheetfile "{sheetfile}")
\t\t(units
\t\t\t(unit
\t\t\t\t(name "A")
\t\t\t\t(pins "1")
\t\t\t)
\t\t)
\t\t(duplicate_pad_numbers_are_jumpers no)
\t\t(fp_circle
\t\t\t(center 0 0)
\t\t\t(end 0 -0.7)
\t\t\t(stroke
\t\t\t\t(width 0.12)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(fill no)
\t\t\t(layer "{silk_layer}")
\t\t\t(uuid "{silk_uuid}")
\t\t)
\t\t(fp_circle
\t\t\t(center 0 0)
\t\t\t(end 1 0)
\t\t\t(stroke
\t\t\t\t(width 0.05)
\t\t\t\t(type solid)
\t\t\t)
\t\t\t(fill no)
\t\t\t(layer "{crtyd_layer}")
\t\t\t(uuid "{crtyd_uuid}")
\t\t)
\t\t(pad "1" smd circle
\t\t\t(at 0 0)
\t\t\t(size 1 1)
\t\t\t(layers "{layer}" "{mask_layer}")
\t\t\t(net "{net_name}")
\t\t\t(pinfunction "1_1")
\t\t\t(pintype "passive")
\t\t\t(uuid "{pad_uuid}")
\t\t)
\t\t(embedded_fonts no)
\t)
"""

# Modify TP9
# Replace TP9 block with B.Cu version at (107.5, 82.5)
tp9_old_m = re.search(r'\t\(footprint "TestPoint:TestPoint_Pad_D1.0mm"\s+\(layer "F.Cu"\).*?\(property "Reference" "TP9".*?\n\t\)', pcb, re.DOTALL)
if tp9_old_m:
    tp9_new = make_pcb_tp("TP9", "/MCU/ETH_CFG0", "B.Cu", 107.5, 82.5,
                          "/d73c21d5-7478-4a02-ac94-6607c580f283/0b58c7b7-3d73-470b-b8e8-13a4a0ab53e7",
                          "/MCU/", "mcu.kicad_sch",
                          "4e838c78-a8f7-4074-a921-175ffa74536e",
                          str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    pcb = pcb.replace(tp9_old_m.group(0), tp9_new.strip())
    print("Replaced TP9 in PCB.")

# Modify TP10
tp10_old_m = re.search(r'\t\(footprint "TestPoint:TestPoint_Pad_D1.0mm"\s+\(layer "F.Cu"\).*?\(property "Reference" "TP10".*?\n\t\)', pcb, re.DOTALL)
if tp10_old_m:
    tp10_new = make_pcb_tp("TP10", "/MCU/ETH_PWR_EN", "B.Cu", 107.5, 85.5,
                           "/d73c21d5-7478-4a02-ac94-6607c580f283/5c4265c5-c940-4753-8483-ec86034dac41",
                           "/MCU/", "mcu.kicad_sch",
                           "2f2ccc8e-f9c6-4a10-8913-f7cbd0db94db",
                           str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    pcb = pcb.replace(tp10_old_m.group(0), tp10_new.strip())
    print("Replaced TP10 in PCB.")

# Modify TP11
tp11_old_m = re.search(r'\t\(footprint "TestPoint:TestPoint_Pad_D1.0mm"\s+\(layer "F.Cu"\).*?\(property "Reference" "TP11".*?\n\t\)', pcb, re.DOTALL)
if tp11_old_m:
    tp11_new = make_pcb_tp("TP11", "/MCU/UART_TX", "F.Cu", 133.0, 70.7,
                           "/d73c21d5-7478-4a02-ac94-6607c580f283/134b54a3-35ef-4ef3-80a1-50ed4ed14842",
                           "/MCU/", "mcu.kicad_sch",
                           "d1369d44-b041-46b0-895f-84f110bda202",
                           str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    pcb = pcb.replace(tp11_old_m.group(0), tp11_new.strip())
    print("Replaced TP11 in PCB.")

# Modify TP12
tp12_old_m = re.search(r'\t\(footprint "TestPoint:TestPoint_Pad_D1.0mm"\s+\(layer "F.Cu"\).*?\(property "Reference" "TP12".*?\n\t\)', pcb, re.DOTALL)
if tp12_old_m:
    tp12_new = make_pcb_tp("TP12", "/MCU/UART_RX", "F.Cu", 135.5, 70.7,
                           "/d73c21d5-7478-4a02-ac94-6607c580f283/79449fc5-556a-4e5c-8194-18c56e45bcbf",
                           "/MCU/", "mcu.kicad_sch",
                           "6ec3984b-ea40-439b-9261-0c47021b381e",
                           str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    pcb = pcb.replace(tp12_old_m.group(0), tp12_new.strip())
    print("Replaced TP12 in PCB.")

# Modify TP13
tp13_old_m = re.search(r'\t\(footprint "TestPoint:TestPoint_Pad_D1.0mm"\s+\(layer "F.Cu"\).*?\(property "Reference" "TP13".*?\n\t\)', pcb, re.DOTALL)
if tp13_old_m:
    tp13_new = make_pcb_tp("TP13", "GND", "F.Cu", 138.0, 70.7,
                           "/d73c21d5-7478-4a02-ac94-6607c580f283/72e77b9b-6ebd-4727-8258-8f50f3e12ca1",
                           "/MCU/", "mcu.kicad_sch",
                           "e9b04ec4-e15d-4ae3-b51a-a732bd5be394",
                           str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    pcb = pcb.replace(tp13_old_m.group(0), tp13_new.strip())
    print("Replaced TP13 in PCB.")

# Modify TP14
tp14_old_m = re.search(r'\t\(footprint "TestPoint:TestPoint_Pad_D1.0mm"\s+\(layer "B.Cu"\).*?\(property "Reference" "TP14".*?\n\t\)', pcb, re.DOTALL)
if tp14_old_m:
    tp14_new = make_pcb_tp("TP14", "/MCU/ETH_RUN", "B.Cu", 110.5, 82.5,
                           "/d73c21d5-7478-4a02-ac94-6607c580f283/a5229aa7-5fa6-419d-855b-874837da92e4",
                           "/MCU/", "mcu.kicad_sch",
                           "91e77a5f-c449-4697-a441-c462cec5f893",
                           str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    pcb = pcb.replace(tp14_old_m.group(0), tp14_new.strip())
    print("Replaced TP14 in PCB.")

# Append new test points TP15, TP16, TP17, TP18, TP19
new_pcb_fps = ""
# TP15 (GND)
new_pcb_fps += make_pcb_tp("TP15", "GND", "B.Cu", 71.0, 72.0,
                           f"/d73c21d5-7478-4a02-ac94-6607c580f283/{uuids['tp15_sym']}",
                           "/MCU/", "mcu.kicad_sch",
                           uuids['tp15_fp'], uuids['tp15_ref'], uuids['tp15_val'], uuids['tp15_pad'], uuids['tp15_silk_c'], uuids['tp15_crtyd_c'])
# TP16 (+3.3V)
new_pcb_fps += make_pcb_tp("TP16", "+3.3V", "B.Cu", 131.0, 97.0,
                           f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{uuids['tp16_sym']}",
                           "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                           uuids['tp16_fp'], uuids['tp16_ref'], uuids['tp16_val'], uuids['tp16_pad'], uuids['tp16_silk_c'], uuids['tp16_crtyd_c'])
# TP17 (V_PRE)
new_pcb_fps += make_pcb_tp("TP17", "V_PRE", "B.Cu", 117.0, 101.5,
                           f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{uuids['tp17_sym']}",
                           "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                           uuids['tp17_fp'], uuids['tp17_ref'], uuids['tp17_val'], uuids['tp17_pad'], uuids['tp17_silk_c'], uuids['tp17_crtyd_c'])
# TP18 (OUT_POS)
new_pcb_fps += make_pcb_tp("TP18", "OUT_POS", "B.Cu", 143.0, 107.0,
                           f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{uuids['tp18_sym']}",
                           "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                           uuids['tp18_fp'], uuids['tp18_ref'], uuids['tp18_val'], uuids['tp18_pad'], uuids['tp18_silk_c'], uuids['tp18_crtyd_c'])
# TP19 (SW_EN)
new_pcb_fps += make_pcb_tp("TP19", "/USB_PD_CONTROLLER/SW_EN", "B.Cu", 124.0, 121.0,
                           f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{uuids['tp19_sym']}",
                           "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                           uuids['tp19_fp'], uuids['tp19_ref'], uuids['tp19_val'], uuids['tp19_pad'], uuids['tp19_silk_c'], uuids['tp19_crtyd_c'])

last_paren_idx = pcb.rfind(')')
pcb_updated = pcb[:last_paren_idx] + new_pcb_fps + pcb[last_paren_idx:]
with open('hardware/gopo.kicad_pcb', 'w', encoding='utf-8') as f:
    f.write(pcb_updated)
print("Updated hardware/gopo.kicad_pcb with all TP modifications and additions.")
