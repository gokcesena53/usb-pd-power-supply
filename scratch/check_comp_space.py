import pcbnew

board = pcbnew.LoadBoard('scratch/cand_task103.kicad_pcb')

targets = ['D1', 'U6', 'U5', 'U1', 'U3', 'Q1', 'Q2', 'D2', 'SW1', 'SW2', 'U13']
for ref in targets:
    fp = board.FindFootprintByReference(ref)
    ref_txt = fp.Reference()
    pos = fp.GetPosition()
    txt_pos = ref_txt.GetPosition()
    layer = fp.GetLayerName()
    print(f'{ref} ({layer}): fp_at=({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f}), ref_at=({pcbnew.ToMM(txt_pos.x):.2f}, {pcbnew.ToMM(txt_pos.y):.2f})')
