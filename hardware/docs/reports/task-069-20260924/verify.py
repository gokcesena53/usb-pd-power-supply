"""Verification script for TASK-069: Manufacturer rules, anchors, and inventory validation."""
import json
from pathlib import Path
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]

b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))
inv = json.loads((here / 'inventory.json').read_text(encoding='utf-8'))

print("=== VERIFYING TASK-069 INVENTORY ===")

# 1. Total footprints count
fps = list(b.GetFootprints())
print(f"Total footprints in board: {len(fps)} (inventory: {inv['total_footprints']})")
assert len(fps) == 143, f"Expected 143 footprints, got {len(fps)}"
assert inv['total_footprints'] == 143

# 2. Total groups count and expected members
expected_groups = {
    'AOZ1284 3.3V BUCK': 19,
    'AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR': 23,
    'CIKIS DESARJI (R59 yerine aktif)': 5,
    'ESP32-C6-MINI-1-H4': 15,
    'ETHERNET MEZANIN (CH9121) + BESLEME ANAHTARI': 7,
    'I2C SEVIYE DONUSTURUCU 5V <-> 3.3V': 6,
    'INA226 OLCUM + PANEL CIKISI': 10,
    'LM74801 CIKIS ANAHTARI + IDEAL DIYOT': 10,
    'ROTARY ENCODER': 3,
    'RTC BQ32000 + 1F5 süper kapasitör': 5,
    'TEST NOKTALARI': 6,
    'TFT BACKLIGHT (3.3V + PWM)': 4,
    'TFT CONNECTOR J3': 1,
    'TPS55340 PRE-BOOST': 16,
    'USB-C GIRIS': 7
}

assert len(inv['groups']) == 15, f"Expected 15 groups, got {len(inv['groups'])}"
for gname, count in expected_groups.items():
    assert gname in inv['groups'], f"Missing group {gname}"
    actual_count = inv['groups'][gname]['count']
    assert actual_count == count, f"Group {gname}: expected {count} footprints, got {actual_count}"
    print(f"  OK Group '{gname}': {actual_count} footprints")

# 3. Ungrouped footprints
expected_ungrouped = sorted('H1 H2 H3 H4 J3 J9'.split())
assert sorted(inv['ungrouped_footprints']) == expected_ungrouped, f"Ungrouped mismatch: {inv['ungrouped_footprints']}"
print(f"  OK Ungrouped footprints (6): {' '.join(expected_ungrouped)}")

# 4. Anchors check
anchors = inv['anchors']
assert 'J7' in anchors and anchors['J7']['footprint'] == 'Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal'
assert 'J3' in anchors and anchors['J3']['locked'] == True and anchors['J3']['xy'] == [98.0, 109.3]
assert 'J9' in anchors
assert all(f'H{i}' in anchors for i in range(1, 5))
assert 'D5' in anchors and 'U11' in anchors
print("  OK All 9 critical anchors verified (J7, J3, J9, H1-H4, D5, U11)")

# 5. Pre-existing tracks (TASK-058 FB trace)
tracks = inv['pre_existing_tracks']
assert tracks['count'] == 4, f"Expected 4 track segments, got {tracks['count']}"
assert tracks['net'] == '/USB_PD_CONTROLLER/BOOST_FB'
assert abs(tracks['total_length_mm'] - 2.584607) < 0.001
print(f"  OK Pre-existing tracks: 4 segments on {tracks['net']}, length={tracks['total_length_mm']:.4f} mm")

# 6. DRC baseline
drc = inv['drc_baseline']
assert drc['total_violations'] == 145, f"Expected 145 violations, got {drc['total_violations']}"
assert drc['unconnected_items_count'] == 360, f"Expected 360 unconnected items, got {drc['unconnected_items_count']}"
assert drc['schematic_parity_issues_count'] == 0, f"Expected 0 parity issues, got {drc['schematic_parity_issues_count']}"
print(f"  OK DRC Baseline: {drc['total_violations']} violations, {drc['unconnected_items_count']} unconnected, {drc['schematic_parity_issues_count']} parity issues")

print("\nTASK-069 VERIFICATION SUCCESSFUL! All criteria verified.")
