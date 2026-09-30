"""TASK-073 relative placement in the temporary B.Cu group area."""
from pathlib import Path
import pcbnew as p

path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(path))
targets = {
    'U5': (98.2, 56.31, 180),
    'U6': (79.935, 56.0, -90),
    'L1': (98.495, 48.37, 90),
    'D2': (104.3, 54.5, 0),
    'C12': (92.3, 55.91, 90),
    'C13': (88.615, 55.91, 90),
    'C14': (99.4, 61.0, 90),
    'C15': (84.8, 47.7, 180),
    'C16': (91.5, 48.3, -90),
    'C17': (104.0, 58.5, 180),
    'C18': (93.3, 59.3, 180),
    'C19': (92.3, 63.5, 90),
    'R38': (102.5, 60.3, 0),
    'R39': (91.0, 60.5, 0),
    'R40': (88.0, 59.1, 180),
    'R41': (95.0, 61.2, -90),
    'R43': (88.0, 64.0, 90),
    'R50': (82.6, 59.0, 180),
    'R51': (79.7, 59.0, 180),
}
reference_positions = {
    'C12': (92.3, 52.5),
    'C13': (88.615, 52.5),
    'C16': (91.5, 52.0),
    'R51': (79.7, 60.8),
    'R43': (91.0, 66.5),
}
for f in b.GetFootprints():
    if f.GetReference() in targets:
        x,y,a=targets[f.GetReference()]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)))
        if f.GetReference() in reference_positions:
            rx,ry=reference_positions[f.GetReference()]
            f.Reference().SetPosition(p.VECTOR2I(p.FromMM(rx),p.FromMM(ry)))
p.SaveBoard(str(path),b)
