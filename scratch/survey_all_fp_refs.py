import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

footprints = board.GetFootprints()
print(f'Total footprints: {len(footprints)}')

by_prefix = {}
for fp in footprints:
    ref = fp.GetReference()
    prefix = ''.join([c for c in ref if not c.isdigit()])
    by_prefix.setdefault(prefix, []).append(fp)

for prefix, fps in sorted(by_prefix.items()):
    print(f'Prefix {prefix}: {len(fps)} components')
    for fp in sorted(fps, key=lambda x: int(''.join([c for c in x.GetReference() if c.isdigit()]) or 0)):
        r = fp.GetReference()
        ref_txt = fp.Reference()
        sz = (round(pcbnew.ToMM(ref_txt.GetTextSize().x), 2), round(pcbnew.ToMM(ref_txt.GetTextThickness()), 2))
        vis = ref_txt.IsVisible()
        layer = fp.GetLayerName()
        print(f'  {r:5s}: fpid={fp.GetFPIDAsString()[:30]}, layer={layer:6s}, vis={str(vis):5s}, size={sz}')
