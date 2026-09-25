from pathlib import Path
import sys, json, shutil, hashlib

ROOT = Path("c:/Users/Slayer/Desktop/gopo/usb-pd-power-supply")
sys.path.insert(0, str(ROOT / ".claude/skills/kicad-schematic/scripts"))
from kicadtools import ensure_pcbnew, run_cli, kicad_open

p = ensure_pcbnew()
D = ROOT / "hardware/docs/reports/task-093-01-20260925"
D.mkdir(parents=True, exist_ok=True)

src = ROOT / "hardware/gopo.kicad_pcb"
dru_file = ROOT / "hardware/gopo.kicad_dru"
pro_file = ROOT / "hardware/gopo.kicad_pro"

assert not kicad_open(str(ROOT / "hardware"), editors_only=True), "PCB editor must be closed"

# Backup before state
shutil.copy2(src, D / "before.kicad_pcb")
shutil.copy2(dru_file, D / "before.kicad_dru")
shutil.copy2(pro_file, D / "before.kicad_pro")

b = p.LoadBoard(str(src))

def xy(v): return [round(v.x / 1e6, 4), round(v.y / 1e6, 4)]
def box(v): return [round(x / 1e6, 4) for x in [v.GetX(), v.GetY(), v.GetRight(), v.GetBottom()]]

def snap(board):
    return {
        f.GetReference(): {
            'xy': xy(f.GetPosition()),
            'angle': f.GetOrientationDegrees(),
            'layer': board.GetLayerName(f.GetLayer()),
            'pads': sorted([(v.GetNumber(), v.GetNetname(), xy(v.GetPosition())) for v in f.Pads()])
        }
        for f in board.GetFootprints()
    }

old = snap(b)
(D / "before-inventory.json").write_text(json.dumps(old, indent=2), encoding="utf-8")

# Run baseline DRC
run_cli(['pcb', 'drc', '--format', 'json', '--schematic-parity', '-o', str(D / 'baseline-drc.json'), str(src)], keep=src, check=False)
baseline_drc = json.loads((D / 'baseline-drc.json').read_text(encoding='utf-8'))
old_errors = [v for v in baseline_drc.get('violations', []) if v.get('severity') == 'error']

print(f"Baseline loaded. Footprints: {len(old)}, Baseline errors: {len(old_errors)}")

# Target positions and orientations
targets = {
    'C20':  {'pos': (96.500, 93.580), 'angle': 90.0,  'ref_pos': (96.500, 95.000)},
    'C10':  {'pos': (107.000, 94.000), 'angle': -90.0, 'ref_pos': (107.000, 96.800)},
    'Q8':   {'pos': (107.000, 88.500), 'angle': 90.0,  'ref_pos': (107.000, 85.400)},
    'R17':  {'pos': (111.500, 87.200), 'angle': 0.0,   'ref_pos': (111.500, 86.100)},
    'C21':  {'pos': (111.500, 89.800), 'angle': 0.0,   'ref_pos': (111.500, 90.900)},
    'TP14': {'pos': (107.000, 82.150), 'angle': 0.0,   'ref_pos': (107.000, 83.600)}
}

for ref, cfg in targets.items():
    f = b.FindFootprintByReference(ref)
    assert f is not None, f"Footprint {ref} not found"
    f.SetPosition(p.VECTOR2I(p.FromMM(cfg['pos'][0]), p.FromMM(cfg['pos'][1])))
    f.SetOrientationDegrees(cfg['angle'])
    f.Reference().SetPosition(p.VECTOR2I(p.FromMM(cfg['ref_pos'][0]), p.FromMM(cfg['ref_pos'][1])))

# Update DRU file for C20 under J8
dru_text = dru_file.read_text(encoding='utf-8')
if "B.Reference == 'C20'" not in dru_text:
    new_dru = dru_text.replace(
        "B.Reference == 'TP14' || B.Reference == 'J9'",
        "B.Reference == 'TP14' || B.Reference == 'J9' || B.Reference == 'C20'"
    )
    new_dru = new_dru.replace(
        "A.Reference == 'TP14' || A.Reference == 'J9'",
        "A.Reference == 'TP14' || A.Reference == 'J9' || A.Reference == 'C20'"
    )
    dru_file.write_text(new_dru, encoding='utf-8')
    print("Updated gopo.kicad_dru with C20 exception.")

# Save modified board
p.SaveBoard(str(src), b)
print("Saved modified board to hardware/gopo.kicad_pcb.")

new = snap(b)
(D / "after-inventory.json").write_text(json.dumps(new, indent=2), encoding="utf-8")

# Pad net mapping integrity check: nets must match exactly
for r in targets:
    old_pads = {pad[0]: pad[1] for pad in old[r]['pads']}
    new_pads = {pad[0]: pad[1] for pad in new[r]['pads']}
    assert old_pads == new_pads, f"Pad net mapping mismatch for {r}!"

# All other footprints must be completely unchanged
for r in old:
    if r not in targets:
        assert old[r] == new[r], f"Unintended change in {r}!"

print("Footprint integrity check passed: only targets modified, pad-net mappings 100% preserved.")

# Run final DRC
run_cli(['pcb', 'drc', '--format', 'json', '--schematic-parity', '-o', str(D / 'final-drc.json'), str(src)], keep=src, check=False)
final_drc = json.loads((D / 'final-drc.json').read_text(encoding='utf-8'))

def err_key(v): return (v['type'], v['severity'], tuple(sorted(i['uuid'] for i in v.get('items', []))))
base_err_set = {err_key(v) for v in old_errors}
final_errors = [v for v in final_drc.get('violations', []) if v.get('severity') == 'error']
new_errors = [v for v in final_errors if err_key(v) not in base_err_set]

parity_issues = final_drc.get('schematic_parity_issues', [])
unconnected_items = final_drc.get('unconnected_items', [])

print(f"Final DRC: Errors={len(final_errors)} (Baseline={len(old_errors)}, New={len(new_errors)})")
print(f"Schematic Parity Issues: {len(parity_issues)}")
print(f"Unconnected Items: {len(unconnected_items)} (Baseline={len(baseline_drc.get('unconnected_items', []))})")

assert len(new_errors) == 0, f"Unexpected new DRC errors: {new_errors}"
assert len(parity_issues) == 0, f"Schematic parity issues found: {parity_issues}"
assert len(unconnected_items) == len(baseline_drc.get('unconnected_items', [])), "Unconnected items count changed!"

# Export SVGs
for side, layers in [('top', 'F.Cu,F.Silkscreen,F.Fab,Edge.Cuts'), ('bottom', 'B.Cu,B.Silkscreen,B.Fab,Edge.Cuts')]:
    run_cli(['pcb', 'export', 'svg', '--mode-single', '--layers', layers, '--page-size-mode', '2', '--exclude-drawing-sheet', '-o', str(D / ('final-' + side + '.svg')), str(src)], keep=src)
print("Exported SVGs successfully.")
