import pcbnew
import sys
sys.path.append('scratch')
from force_repack_optimizer import analyze_ratsnest

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

# Apply the 4 repacks first
r50 = board.FindFootprintByReference('R50')
r51 = board.FindFootprintByReference('R51')
c9 = board.FindFootprintByReference('C9')
r27 = board.FindFootprintByReference('R27')

r50.SetPosition(pcbnew.VECTOR2I_MM(109.385, 102.300))
r50.SetOrientationDegrees(180.0)
r51.SetPosition(pcbnew.VECTOR2I_MM(107.485, 102.300))
r51.SetOrientationDegrees(0.0)
c9.SetPosition(pcbnew.VECTOR2I_MM(140.525, 78.800))
c9.SetOrientationDegrees(0.0)
r27.SetPosition(pcbnew.VECTOR2I_MM(136.750, 108.400))
r27.SetOrientationDegrees(0.0)

current_rn = analyze_ratsnest(board)
base_crossings = current_rn['crossings_count']
base_wl = current_rn['wirelength_mm']

print(f"Starting Crossings: {base_crossings}, Wirelength: {base_wl:.2f} mm")

# Find all passives (R, C)
passives = [fp for fp in board.GetFootprints() if (fp.GetReference().startswith('R') or fp.GetReference().startswith('C')) and not fp.GetReference().startswith('RShunt')]

beneficial_flips = []

for fp in passives:
    ref = fp.GetReference()
    orig_rot = fp.GetOrientation().AsDegrees() % 360
    
    # Try 180 degree flip
    flipped_rot = (orig_rot + 180.0) % 360
    fp.SetOrientationDegrees(flipped_rot)
    
    rn = analyze_ratsnest(board)
    new_crossings = rn['crossings_count']
    new_wl = rn['wirelength_mm']
    
    cross_diff = new_crossings - base_crossings
    wl_diff = new_wl - base_wl
    
    # Revert
    fp.SetOrientationDegrees(orig_rot)
    
    if cross_diff < 0 or (cross_diff == 0 and wl_diff < -0.2):
        print(f"Flip {ref:5} ({orig_rot:.1f} -> {flipped_rot:.1f}): Crossings delta={cross_diff:+2d}, Wirelength delta={wl_diff:+.2f} mm")
        beneficial_flips.append((ref, orig_rot, flipped_rot, cross_diff, wl_diff))

print(f"\nTotal beneficial 180 flips found: {len(beneficial_flips)}")
