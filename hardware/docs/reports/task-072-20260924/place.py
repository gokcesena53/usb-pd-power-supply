"""TASK-072 relative placement; U11/D5 and their FB trace stay anchored."""
import pcbnew as p
from pathlib import Path

board_path = Path(__file__).resolve().parents[4] / 'hardware/gopo.kicad_pcb'
b = p.LoadBoard(str(board_path))
targets = {
    'L3': (69.55, 42.5, 180),
    'D4': (74.8, 49.0, 180),
    'C23': (72.0, 60.1, 180),
    'C24': (63.4, 62.3, 180),
    'C25': (59.5, 54.0, 180),
    'C26': (76.0, 51.7, 180),
    'C27': (75.8, 55.5, -90),
    'C28': (82.0, 64.0, 180),
    'C29': (59.5, 46.0, 180),
    'R47': (63.5, 54.0, 180),
    'R48': (60.2, 59.5, 180),
    'R49': (61.0, 62.3, 180),
    'R52': (66.5, 62.3, 180),
    'R53': (75.5, 60.1, 180),
}
for f in b.GetFootprints():
    if f.GetReference() in targets:
        x, y, a = targets[f.GetReference()]
        f.SetOrientationDegrees(a)
        f.SetPosition(p.VECTOR2I(p.FromMM(x), p.FromMM(y)))
        if f.GetReference() == 'R53':
            f.Reference().SetPosition(p.VECTOR2I(p.FromMM(75.5), p.FromMM(61.3)))
        if f.GetReference() == 'C27':
            f.Reference().SetPosition(p.VECTOR2I(p.FromMM(78.0), p.FromMM(58.7)))
p.SaveBoard(str(board_path), b)
