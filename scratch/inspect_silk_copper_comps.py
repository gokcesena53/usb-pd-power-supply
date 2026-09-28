import pcbnew

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

for ref_name in ['D8', 'D9', 'R62', 'R63', 'J8']:
    fp = board.FindFootprintByReference(ref_name)
    ref = fp.Reference()
    print(f'=== {ref_name} ===')
    print(f'Pos: ({pcbnew.ToMM(fp.GetPosition().x):.2f}, {pcbnew.ToMM(fp.GetPosition().y):.2f}), Layer: {fp.GetLayerName()}')
    print(f'Ref: pos=({pcbnew.ToMM(ref.GetPosition().x):.2f}, {pcbnew.ToMM(ref.GetPosition().y):.2f}), size=({pcbnew.ToMM(ref.GetTextSize().x):.2f}, {pcbnew.ToMM(ref.GetTextSize().y):.2f}), visible={ref.IsVisible()}, layer={ref.GetLayerName()}')
    for p in fp.Pads():
        print(f'  Pad {p.GetName()} at ({pcbnew.ToMM(p.GetPosition().x):.2f}, {pcbnew.ToMM(p.GetPosition().y):.2f}), size=({pcbnew.ToMM(p.GetSize().x):.2f}, {pcbnew.ToMM(p.GetSize().y):.2f})')
    for item in fp.GraphicalItems():
        if 'Silk' in item.GetLayerName():
            st = item.GetStart()
            en = item.GetEnd() if hasattr(item, 'GetEnd') else ''
            print(f'  Silk item: {type(item).__name__}, {item.GetLayerName()}, start=({pcbnew.ToMM(st.x):.2f}, {pcbnew.ToMM(st.y):.2f})')
