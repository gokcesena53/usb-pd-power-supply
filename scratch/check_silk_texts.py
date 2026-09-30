import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
small_passives = []
for fp in board.GetFootprints():
    ref = fp.GetReference()
    ref_txt = fp.Reference()
    sz = ref_txt.GetTextSize()
    th = ref_txt.GetTextThickness()
    visible = ref_txt.IsVisible()
    w = pcbnew.ToMM(sz.x)
    h = pcbnew.ToMM(sz.y)
    t = pcbnew.ToMM(th)
    if visible and (h < 0.80 or t < 0.08):
        small_passives.append((ref, fp.GetValue(), w, h, t, ref_txt.GetLayerName()))

print(f'Total footprint references with visible text < 0.8mm or thickness < 0.08mm: {len(small_passives)}')
for p in small_passives:
    print(f'{p[0]}: val={p[1]}, sz=({p[2]:.3f}, {p[3]:.3f}), th={p[4]:.3f}, layer={p[5]}')

for fp in board.GetFootprints():
    for item in fp.GraphicalItems():
        if isinstance(item, pcbnew.PCB_TEXT):
            sz = item.GetTextSize()
            th = item.GetTextThickness()
            w = pcbnew.ToMM(sz.x)
            h = pcbnew.ToMM(sz.y)
            t = pcbnew.ToMM(th)
            if item.IsVisible() and (h < 0.80 or t < 0.08):
                print(f'FP graphical text in {fp.GetReference()}: text={item.GetText()}, sz=({w:.3f},{h:.3f}), th={t:.3f}, layer={item.GetLayerName()}')

# Board drawings text
for item in board.GetDrawings():
    if isinstance(item, pcbnew.PCB_TEXT):
        sz = item.GetTextSize()
        th = item.GetTextThickness()
        w = pcbnew.ToMM(sz.x)
        h = pcbnew.ToMM(sz.y)
        t = pcbnew.ToMM(th)
        if item.IsVisible() and (h < 0.80 or t < 0.08):
            print(f'Board text: {item.GetText()}, sz=({w:.3f},{h:.3f}), th={t:.3f}, layer={item.GetLayerName()}')
