import re
import sys
import uuid
import shutil

sys.stdout.reconfigure(encoding='utf-8')

shutil.copyfile('hardware/gopo.kicad_pcb.bak', 'hardware/gopo.kicad_pcb')
print("Restored PCB from backup.")

UUIDS = {
    'tp15_sym': '54128f7d-08cf-43ba-97a1-c8b1bb7a1501',
    'tp15_pin': '54128f7d-08cf-43ba-97a1-c8b1bb7a1502',
    'tp15_gnd_sym': '54128f7d-08cf-43ba-97a1-c8b1bb7a1503',
    'tp15_gnd_pin': '54128f7d-08cf-43ba-97a1-c8b1bb7a1504',
    'tp15_wire': '54128f7d-08cf-43ba-97a1-c8b1bb7a1505',
    'tp15_fp': '54128f7d-08cf-43ba-97a1-c8b1bb7a1506',
    'tp15_ref': '54128f7d-08cf-43ba-97a1-c8b1bb7a1507',
    'tp15_val': '54128f7d-08cf-43ba-97a1-c8b1bb7a1508',
    'tp15_pad': '54128f7d-08cf-43ba-97a1-c8b1bb7a1509',
    'tp15_silk_c': '54128f7d-08cf-43ba-97a1-c8b1bb7a150a',
    'tp15_crtyd_c': '54128f7d-08cf-43ba-97a1-c8b1bb7a150b',

    'tp16_sym': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1601',
    'tp16_pin': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1602',
    'tp16_pwr_sym': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1603',
    'tp16_pwr_pin': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1604',
    'tp16_wire': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1605',
    'tp16_fp': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1606',
    'tp16_ref': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1607',
    'tp16_val': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1608',
    'tp16_pad': '67239a8e-19d0-44cb-a8b2-d9c2cc8b1609',
    'tp16_silk_c': '67239a8e-19d0-44cb-a8b2-d9c2cc8b160a',
    'tp16_crtyd_c': '67239a8e-19d0-44cb-a8b2-d9c2cc8b160b',

    'tp17_sym': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1701',
    'tp17_pin': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1702',
    'tp17_label': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1703',
    'tp17_wire': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1704',
    'tp17_fp': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1705',
    'tp17_ref': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1706',
    'tp17_val': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1707',
    'tp17_pad': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1708',
    'tp17_silk_c': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c1709',
    'tp17_crtyd_c': '7834ab9f-2ae1-45dc-b9c3-e0d3dd9c170a',

    'tp18_sym': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1801',
    'tp18_pin': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1802',
    'tp18_label': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1803',
    'tp18_wire': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1804',
    'tp18_fp': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1805',
    'tp18_ref': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1806',
    'tp18_val': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1807',
    'tp18_pad': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1808',
    'tp18_silk_c': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d1809',
    'tp18_crtyd_c': '8945bc0a-3bf2-46ed-cad4-f1e4ee0d180a',

    'tp19_sym': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1901',
    'tp19_pin': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1902',
    'tp19_label': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1903',
    'tp19_wire': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1904',
    'tp19_fp': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1905',
    'tp19_ref': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1906',
    'tp19_val': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1907',
    'tp19_pad': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1908',
    'tp19_silk_c': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e1909',
    'tp19_crtyd_c': '9a56cd1b-4c03-47fe-dbe5-02f5ff1e190a',
}

# --- 1. Update hardware/mcu.kicad_sch ---
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
\t\t(uuid "{UUIDS['tp15_wire']}")
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
\t\t(uuid "{UUIDS['tp15_gnd_sym']}")
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
\t\t\t(uuid "{UUIDS['tp15_gnd_pin']}")
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
\t\t(uuid "{UUIDS['tp15_sym']}")
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
\t\t\t(uuid "{UUIDS['tp15_pin']}")
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

last_paren = mcu_sch.rfind(')')
mcu_sch_updated = mcu_sch[:last_paren] + tp15_sch_snippet + mcu_sch[last_paren:]
with open('hardware/mcu.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(mcu_sch_updated)
print("1. Updated hardware/mcu.kicad_sch.")

# --- 2. Update hardware/usb_pd_controller.kicad_sch ---
with open('hardware/usb_pd_controller.kicad_sch', 'r', encoding='utf-8') as f:
    pd_sch = f.read()

def make_pd_sch_tp(ref, val_label, is_global, pwr_lib, at_x, at_y, sym_uuid, pin_uuid, conn_uuid, wire_uuid, ref_pwr="#PWR"):
    res = ""
    if pwr_lib:
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
\t\t\t(uuid "{pin_uuid}f")
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
pd_snippets += make_pd_sch_tp("TP16", "+3.3V", False, "power:+3.3V", 368.30, 215.90, UUIDS['tp16_sym'], UUIDS['tp16_pin'], UUIDS['tp16_pwr_sym'], UUIDS['tp16_wire'], ref_pwr="#PWR051")
# TP17 (V_PRE)
pd_snippets += make_pd_sch_tp("TP17", "V_PRE", True, None, 368.30, 226.06, UUIDS['tp17_sym'], UUIDS['tp17_pin'], UUIDS['tp17_label'], UUIDS['tp17_wire'])
# TP18 (OUT_POS)
pd_snippets += make_pd_sch_tp("TP18", "OUT_POS", True, None, 368.30, 236.22, UUIDS['tp18_sym'], UUIDS['tp18_pin'], UUIDS['tp18_label'], UUIDS['tp18_wire'])
# TP19 (SW_EN)
pd_snippets += make_pd_sch_tp("TP19", "SW_EN", False, None, 368.30, 246.38, UUIDS['tp19_sym'], UUIDS['tp19_pin'], UUIDS['tp19_label'], UUIDS['tp19_wire'])

last_paren = pd_sch.rfind(')')
pd_sch_updated = pd_sch[:last_paren] + pd_snippets + pd_sch[last_paren:]
with open('hardware/usb_pd_controller.kicad_sch', 'w', encoding='utf-8') as f:
    f.write(pd_sch_updated)
print("2. Updated hardware/usb_pd_controller.kicad_sch.")

# --- 3. Update hardware/gopo.kicad_pcb ---
with open('hardware/gopo.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb_lines = f.readlines()

def get_fp_range(lines, ref):
    for i, l in enumerate(lines):
        if f'(property "Reference" "{ref}"' in l:
            start = i
            while start >= 0 and not lines[start].startswith('\t(footprint '):
                start -= 1
            paren_count = 0
            end = i
            for j in range(start, len(lines)):
                paren_count += lines[j].count('(') - lines[j].count(')')
                if paren_count == 0:
                    end = j
                    break
            return start, end
    return None, None

# 3a. Modify TP9 -> B.Cu @ (107.50, 82.50)
s9, e9 = get_fp_range(pcb_lines, "TP9")
print(f"Modifying TP9 (lines {s9+1}-{e9+1})...")
for idx in range(s9, e9 + 1):
    l = pcb_lines[idx]
    if l.strip() == '(layer "F.Cu")':
        pcb_lines[idx] = '\t\t(layer "B.Cu")\n'
    elif l.strip().startswith('(at ') and idx == s9 + 3:
        pcb_lines[idx] = '\t\t(at 107.5 82.5)\n'
    elif '(layer "F.SilkS")' in l:
        pcb_lines[idx] = l.replace('"F.SilkS"', '"B.SilkS"')
    elif '(layer "F.Fab")' in l:
        pcb_lines[idx] = l.replace('"F.Fab"', '"B.Fab"')
    elif '(layer "F.CrtYd")' in l:
        pcb_lines[idx] = l.replace('"F.CrtYd"', '"B.CrtYd"')
    elif '(layers "F.Cu" "F.Mask")' in l:
        pcb_lines[idx] = l.replace('"F.Cu" "F.Mask"', '"B.Cu" "B.Mask"')
    elif idx < s9 + 25 and '(effects' in l:
        # Add (justify mirror) and hide yes if needed
        pcb_lines[idx] = '\t\t\t(hide yes)\n\t\t\t(effects\n\t\t\t\t(justify mirror)\n'

# 3b. Modify TP10 -> B.Cu @ (107.50, 79.50)
s10, e10 = get_fp_range(pcb_lines, "TP10")
print(f"Modifying TP10 (lines {s10+1}-{e10+1})...")
for idx in range(s10, e10 + 1):
    l = pcb_lines[idx]
    if l.strip() == '(layer "F.Cu")':
        pcb_lines[idx] = '\t\t(layer "B.Cu")\n'
    elif l.strip().startswith('(at ') and idx == s10 + 3:
        pcb_lines[idx] = '\t\t(at 107.5 79.5)\n'
    elif '(layer "F.SilkS")' in l:
        pcb_lines[idx] = l.replace('"F.SilkS"', '"B.SilkS"')
    elif '(layer "F.Fab")' in l:
        pcb_lines[idx] = l.replace('"F.Fab"', '"B.Fab"')
    elif '(layer "F.CrtYd")' in l:
        pcb_lines[idx] = l.replace('"F.CrtYd"', '"B.CrtYd"')
    elif '(layers "F.Cu" "F.Mask")' in l:
        pcb_lines[idx] = l.replace('"F.Cu" "F.Mask"', '"B.Cu" "B.Mask"')
    elif idx < s10 + 25 and '(effects' in l:
        pcb_lines[idx] = '\t\t\t(hide yes)\n\t\t\t(effects\n\t\t\t\t(justify mirror)\n'

# 3c. Modify TP11 -> F.Cu @ (133.00, 70.70)
s11, e11 = get_fp_range(pcb_lines, "TP11")
print(f"Modifying TP11 (lines {s11+1}-{e11+1})...")
for idx in range(s11, e11 + 1):
    l = pcb_lines[idx]
    if l.strip().startswith('(at ') and idx == s11 + 3:
        pcb_lines[idx] = '\t\t(at 133 70.7)\n'
    elif idx < s11 + 25 and '(effects' in l:
        pcb_lines[idx] = '\t\t\t(hide yes)\n\t\t\t(effects\n'

# 3d. Modify TP12 -> F.Cu @ (135.50, 70.70)
s12, e12 = get_fp_range(pcb_lines, "TP12")
print(f"Modifying TP12 (lines {s12+1}-{e12+1})...")
for idx in range(s12, e12 + 1):
    l = pcb_lines[idx]
    if l.strip().startswith('(at ') and idx == s12 + 3:
        pcb_lines[idx] = '\t\t(at 135.5 70.7)\n'
    elif idx < s12 + 25 and '(effects' in l:
        pcb_lines[idx] = '\t\t\t(hide yes)\n\t\t\t(effects\n'

# 3e. Modify TP13 -> F.Cu @ (138.00, 70.70)
s13, e13 = get_fp_range(pcb_lines, "TP13")
print(f"Modifying TP13 (lines {s13+1}-{e13+1})...")
for idx in range(s13, e13 + 1):
    l = pcb_lines[idx]
    if l.strip().startswith('(at ') and idx == s13 + 3:
        pcb_lines[idx] = '\t\t(at 138 70.7)\n'
    elif idx < s13 + 25 and '(effects' in l:
        pcb_lines[idx] = '\t\t\t(hide yes)\n\t\t\t(effects\n'

# 3f. Modify TP14 -> B.Cu @ (110.50, 82.50)
s14, e14 = get_fp_range(pcb_lines, "TP14")
print(f"Modifying TP14 (lines {s14+1}-{e14+1})...")
for idx in range(s14, e14 + 1):
    l = pcb_lines[idx]
    if l.strip().startswith('(at ') and idx == s14 + 3:
        pcb_lines[idx] = '\t\t(at 110.5 82.5)\n'
    elif idx < s14 + 25 and '(effects' in l:
        pcb_lines[idx] = '\t\t\t(hide yes)\n\t\t\t(effects\n'

# 3g. Insert new footprints TP15..TP19
def generate_new_fp_string(ref, net_name, layer, x, y, path, sheetname, sheetfile, fp_uuid, ref_uuid, val_uuid, pad_uuid, silk_uuid, crtyd_uuid):
    is_bottom = (layer == "B.Cu")
    silk_layer = "B.SilkS" if is_bottom else "F.SilkS"
    crtyd_layer = "B.CrtYd" if is_bottom else "F.CrtYd"
    fab_layer = "B.Fab" if is_bottom else "F.Fab"
    mask_layer = "B.Mask" if is_bottom else "F.Mask"
    mirror_clause = "\t\t\t\t(justify mirror)\n" if is_bottom else ""

    return f"""\t(footprint "TestPoint:TestPoint_Pad_D1.0mm"
\t\t(layer "{layer}")
\t\t(uuid "{fp_uuid}")
\t\t(at {x} {y})
\t\t(descr "SMD pad as test Point, diameter 1.0mm")
\t\t(tags "test point SMD pad")
\t\t(property "Reference" "{ref}"
\t\t\t(at 0 0 0)
\t\t\t(layer "{silk_layer}")
\t\t\t(hide yes)
\t\t\t(uuid "{ref_uuid}")
\t\t\t(effects
\t\t\t\t(font
\t\t\t\t\t(size 1 1)
\t\t\t\t\t(thickness 0.15)
\t\t\t\t)
{mirror_clause}\t\t\t)
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
{mirror_clause}\t\t\t)
\t\t)
\t\t(property "Datasheet" "~"
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
{mirror_clause}\t\t\t)
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
{mirror_clause}\t\t\t)
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

new_fps = []
# TP15 (GND, B.Cu, (71.0, 72.0))
new_fps.append(generate_new_fp_string("TP15", "GND", "B.Cu", 71.0, 72.0,
                                      f"/d73c21d5-7478-4a02-ac94-6607c580f283/{UUIDS['tp15_sym']}",
                                      "/MCU/", "mcu.kicad_sch",
                                      UUIDS['tp15_fp'], UUIDS['tp15_ref'], UUIDS['tp15_val'],
                                      UUIDS['tp15_pad'], UUIDS['tp15_silk_c'], UUIDS['tp15_crtyd_c']))

# TP16 (+3.3V, B.Cu, (125.0, 73.0))
new_fps.append(generate_new_fp_string("TP16", "+3.3V", "B.Cu", 125.0, 73.0,
                                      f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{UUIDS['tp16_sym']}",
                                      "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                                      UUIDS['tp16_fp'], UUIDS['tp16_ref'], UUIDS['tp16_val'],
                                      UUIDS['tp16_pad'], UUIDS['tp16_silk_c'], UUIDS['tp16_crtyd_c']))

# TP17 (V_PRE, B.Cu, (105.0, 101.0))
new_fps.append(generate_new_fp_string("TP17", "V_PRE", "B.Cu", 105.0, 101.0,
                                      f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{UUIDS['tp17_sym']}",
                                      "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                                      UUIDS['tp17_fp'], UUIDS['tp17_ref'], UUIDS['tp17_val'],
                                      UUIDS['tp17_pad'], UUIDS['tp17_silk_c'], UUIDS['tp17_crtyd_c']))

# TP18 (OUT_POS, B.Cu, (143.0, 107.0))
new_fps.append(generate_new_fp_string("TP18", "OUT_POS", "B.Cu", 143.0, 107.0,
                                      f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{UUIDS['tp18_sym']}",
                                      "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                                      UUIDS['tp18_fp'], UUIDS['tp18_ref'], UUIDS['tp18_val'],
                                      UUIDS['tp18_pad'], UUIDS['tp18_silk_c'], UUIDS['tp18_crtyd_c']))

# TP19 (SW_EN, B.Cu, (124.0, 121.0))
new_fps.append(generate_new_fp_string("TP19", "/USB_PD_CONTROLLER/SW_EN", "B.Cu", 124.0, 121.0,
                                      f"/ef9b8359-2233-4750-a469-a0efa9e391b0/{UUIDS['tp19_sym']}",
                                      "/USB_PD_CONTROLLER/", "usb_pd_controller.kicad_sch",
                                      UUIDS['tp19_fp'], UUIDS['tp19_ref'], UUIDS['tp19_val'],
                                      UUIDS['tp19_pad'], UUIDS['tp19_silk_c'], UUIDS['tp19_crtyd_c']))

# Find end of footprints
last_fp_start = -1
for i, l in enumerate(pcb_lines):
    if l.startswith('\t(footprint '):
        last_fp_start = i

paren_count = 0
last_fp_end = -1
for j in range(last_fp_start, len(pcb_lines)):
    paren_count += pcb_lines[j].count('(') - pcb_lines[j].count(')')
    if paren_count == 0:
        last_fp_end = j
        break

print(f"Inserting new footprints after line {last_fp_end+1}...")
pcb_lines[last_fp_end+1:last_fp_end+1] = [fp for fp in new_fps]

# Update group "TEST NOKTALARI" to include TP15
for i, l in enumerate(pcb_lines):
    if '(group "TEST NOKTALARI"' in l:
        for k in range(i, min(len(pcb_lines), i+10)):
            if '(members ' in pcb_lines[k]:
                pcb_lines[k] = pcb_lines[k].replace('(members ', f'(members "{UUIDS["tp15_fp"]}" ')
                print("Updated group 'TEST NOKTALARI' with TP15.")
                break
        break

with open('hardware/gopo.kicad_pcb', 'w', encoding='utf-8') as f:
    f.writelines(pcb_lines)
print("3. Successfully updated hardware/gopo.kicad_pcb.")
