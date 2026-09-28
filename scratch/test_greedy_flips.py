import pcbnew
import sys
sys.path.append('scratch')
from force_repack_optimizer import analyze_ratsnest

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

# Apply 4 repacks
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
best_crossings = current_rn['crossings_count']
best_wl = current_rn['wirelength_mm']

print(f"Initial: Crossings={best_crossings}, WL={best_wl:.2f} mm")

passives = [fp for fp in board.GetFootprints() if (fp.GetReference().startswith('R') or fp.GetReference().startswith('C')) and not fp.GetReference().startswith('RShunt')]

applied_flips = {}

# Priority 1: Flips that reduce crossings
for fp in passives:
    ref = fp.GetReference()
    orig_rot = fp.GetOrientation().AsDegrees() % 360
    new_rot = (orig_rot + 180.0) % 360
    
    fp.SetOrientationDegrees(new_rot)
    rn = analyze_ratsnest(board)
    
    # Cost function: crossings * 100 + wirelength
    cost_diff = (rn['crossings_count'] - best_crossings) * 100.0 + (rn['wirelength_mm'] - best_wl)
    
    if cost_diff < -0.1 and rn['crossings_count'] <= best_crossings:
        print(f"Accept flip {ref}: rot {orig_rot:.1f} -> {new_rot:.1f} (Cross: {rn['crossings_count']} vs {best_crossings}, WL: {rn['wirelength_mm']:.2f} vs {best_wl:.2f})")
        best_crossings = rn['crossings_count']
        best_wl = rn['wirelength_mm']
        applied_flips[ref] = (orig_rot, new_rot)
    else:
        # Revert
        fp.SetOrientationDegrees(orig_rot)

print(f"\nFinal: Crossings={best_crossings}, WL={best_wl:.2f} mm")
print(f"Total accepted flips: {len(applied_flips)}")
for ref, (o, n) in applied_flips.items():
    print(f"  {ref:5}: {o:5.1f} -> {n:5.1f}")
