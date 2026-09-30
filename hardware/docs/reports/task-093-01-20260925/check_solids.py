from pathlib import Path
import json, itertools
import FreeCAD, Part

ROOT = Path("c:/Users/Slayer/Desktop/gopo/usb-pd-power-supply")
D = ROOT / "hardware/docs/reports/task-093-01-20260925"

KICAD_3D = Path(r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels")
MOD_3D = ROOT / "hardware/libraries/Module_Custom.3dshapes"

# Footprint placements on board (x, y, angle, layer)
# Note on KiCad bottom layer placement:
# Board thickness = 1.6 mm.
# Top surface is Z = 0, Bottom surface is Z = -1.6 mm.
# When a footprint is on B.Cu:
# It is mirrored in X relative to footprint local origin, or flipped around Y axis.
# In KiCad board coordinates:
# J8 is at pos=(102.500, 79.610), angle 0, B.Cu.
# The J8 STEP model header pins are at (0,0), spacer is from Z=0 to +2.50 mm (extending into -Z space from B.Cu).
# Let's place the solids accurately in board space:
# For B.Cu, components sit at Z = -1.6 mm and extend towards -Z (or if relative to B.Cu, B.Cu is Z=0 and components extend in +Z).
# For relative distance check between J8 and components on B.Cu, we can define B.Cu surface as Z=0.
# On B.Cu, J8 sits at (102.500, 79.610).
# J8 header spacer is from Z=0 to Z=2.50 mm (module PCB is at Z=2.50 to 4.10 mm).
# Any SMD component on B.Cu sits on Z=0 and extends to Z = Height.

models = {
    'J8': {
        'path': MOD_3D / "Waveshare_2-CH_UART_TO_ETH.step",
        'pos': (102.500, 79.610),
        'angle': 0.0,
        'layer': 'B.Cu'
    },
    'C20': {
        'path': KICAD_3D / "Capacitor_SMD.3dshapes/C_0402_1005Metric.step",
        'pos': (96.500, 93.580),
        'angle': 90.0,
        'layer': 'B.Cu'
    },
    'C10': {
        'path': KICAD_3D / "Capacitor_SMD.3dshapes/C_0805_2012Metric.step",
        'pos': (107.000, 94.000),
        'angle': -90.0,
        'layer': 'B.Cu'
    },
    'Q8': {
        'path': KICAD_3D / "Package_TO_SOT_SMD.3dshapes/SOT-23-6.step",
        'pos': (107.000, 88.500),
        'angle': 90.0,
        'layer': 'B.Cu'
    },
    'R17': {
        'path': KICAD_3D / "Resistor_SMD.3dshapes/R_0402_1005Metric.step",
        'pos': (111.500, 87.200),
        'angle': 0.0,
        'layer': 'B.Cu'
    },
    'C21': {
        'path': KICAD_3D / "Capacitor_SMD.3dshapes/C_0402_1005Metric.step",
        'pos': (111.500, 89.800),
        'angle': 0.0,
        'layer': 'B.Cu'
    }
}

shapes = {}
for name, cfg in models.items():
    raw_shape = Part.read(str(cfg['path']))
    # Apply rotation and translation
    # In KiCad B.Cu: footprints are placed on bottom layer.
    # Rotation angle is counter-clockwise or clockwise around Z:
    # Rotate around Z by cfg['angle'], then translate by (pos.x, pos.y, 0)
    sh = raw_shape.copy()
    if cfg['angle'] != 0.0:
        sh.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,0,1), cfg['angle'])
    sh.translate(FreeCAD.Vector(cfg['pos'][0], cfg['pos'][1], 0))
    shapes[name] = sh

def bb(s):
    b = s.BoundBox
    return [round(v, 4) for v in [b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax]]

out = {
    'model_bounds': {r: bb(s) for r, s in shapes.items()},
    'pairs_to_J8': {}
}

# Distance and collision checks to J8
for ref in ['C20', 'C10', 'Q8', 'R17', 'C21']:
    s_ref = shapes[ref]
    s_j8 = shapes['J8']
    dist, pts, _ = s_ref.distToShape(s_j8)
    common = s_ref.common(s_j8)
    out['pairs_to_J8'][f"{ref}-J8"] = {
        'distance_mm': round(dist, 4),
        'intersection_volume_mm3': round(common.Volume, 6),
        'status': 'PASSED (no collision)' if common.Volume < 1e-5 else 'COLLISION'
    }

# Check pairs among the placed components
out['inter_component_pairs'] = {}
for a, b in itertools.combinations(['C20', 'C10', 'Q8', 'R17', 'C21'], 2):
    sa, sb = shapes[a], shapes[b]
    dist, _, _ = sa.distToShape(sb)
    common = sa.common(sb)
    out['inter_component_pairs'][f"{a}-{b}"] = {
        'distance_mm': round(dist, 4),
        'intersection_volume_mm3': round(common.Volume, 6)
    }

print(json.dumps(out, indent=2))
(D / "solid-check.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("Saved solid-check.json successfully.")
