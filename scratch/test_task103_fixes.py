import shutil
import subprocess
import pcbnew

src_pcb = 'hardware/gopo.kicad_pcb'
test_pcb = 'scratch/cand_task103.kicad_pcb'
shutil.copyfile(src_pcb, test_pcb)
# Also copy dru and pro if needed
shutil.copyfile('hardware/gopo.kicad_dru', 'scratch/cand_task103.kicad_dru')
shutil.copyfile('hardware/gopo.kicad_pro', 'scratch/cand_task103.kicad_pro')

board = pcbnew.LoadBoard(test_pcb)

# 1. TP1-TP14: hide all references and remove TP5 graphical silkscreen text
for fp in board.GetFootprints():
    ref = fp.GetReference()
    if ref.startswith('TP'):
        fp.Reference().SetVisible(False)
        # Check graphical items in TP5
        items_to_remove = []
        for item in fp.GraphicalItems():
            if isinstance(item, pcbnew.PCB_TEXT) and 'Silk' in item.GetLayerName():
                items_to_remove.append(item)
        for item in items_to_remove:
            fp.Remove(item)

# 2. Resistors and Capacitors 0402 / 0603: hide references
# Check all R* and C* footprints
for fp in board.GetFootprints():
    ref = fp.GetReference()
    fpid = fp.GetFPIDAsString()
    # Check if 0402 or 0603 or small passive
    if (ref.startswith('R') or ref.startswith('C') or ref == 'TH1'):
        if '0402' in fpid or '0603' in fpid:
            fp.Reference().SetVisible(False)

# 3. For any remaining footprints with text height < 0.8mm or thickness < 0.08mm:
# e.g., U1, U3, U5, U6, Q1, Q2, D1, D2, SW1, SW2, J7
for fp in board.GetFootprints():
    ref_txt = fp.Reference()
    if ref_txt.IsVisible():
        h = pcbnew.ToMM(ref_txt.GetTextHeight())
        t = pcbnew.ToMM(ref_txt.GetTextThickness())
        if h < 0.80 or t < 0.08:
            print(f'Fixing size for {fp.GetReference()}: was ({h:.2f}, {t:.3f})')
            ref_txt.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.8), pcbnew.FromMM(0.8)))
            ref_txt.SetTextThickness(pcbnew.FromMM(0.12))

# 4. Fix U2 silkscreen lines clipping board edge (Y = 69.48mm)
u2 = board.FindFootprintByReference('U2')
for item in u2.GraphicalItems():
    if item.GetLayerName() == 'F.Silkscreen' and item.GetShapeStr() == 'Line':
        st_y = pcbnew.ToMM(item.GetStart().y)
        en_y = pcbnew.ToMM(item.GetEnd().y)
        # If line is completely above Y = 69.9mm, move it to Y = 70.0mm
        if st_y < 69.5 and en_y < 69.5:
            # horizontal top line: move to Y = 70.0mm
            item.SetStart(pcbnew.VECTOR2I(item.GetStart().x, pcbnew.FromMM(70.0)))
            item.SetEnd(pcbnew.VECTOR2I(item.GetEnd().x, pcbnew.FromMM(70.0)))
        elif st_y < 69.5:
            item.SetStart(pcbnew.VECTOR2I(item.GetStart().x, pcbnew.FromMM(70.0)))
        elif en_y < 69.5:
            item.SetEnd(pcbnew.VECTOR2I(item.GetEnd().x, pcbnew.FromMM(70.0)))

# 5. Fix C33:
c33 = board.FindFootprintByReference('C33')
# Move reference text away from board edge
c33.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(124.5), pcbnew.FromMM(75.0)))
# Fix polarity line in C33 touching R6 pad 1
# Let's inspect C33 graphical items and move the '+' sign lines
for item in c33.GraphicalItems():
    if item.GetLayerName() == 'B.Silkscreen' and item.GetShapeStr() == 'Line':
        # In local coords, start was (2.2, 3) to (4.2, 3), and (3.2, 4) to (3.2, 2)
        # In board coords, it was around (111.3, 78.0)
        st_x = pcbnew.ToMM(item.GetStart().x)
        st_y = pcbnew.ToMM(item.GetStart().y)
        if 110.0 <= st_x <= 113.0 and 77.0 <= st_y <= 79.5:
            # Shift by +3mm in X (away from R6 towards center of C33)
            item.SetStart(pcbnew.VECTOR2I(item.GetStart().x + pcbnew.FromMM(3.0), item.GetStart().y))
            item.SetEnd(pcbnew.VECTOR2I(item.GetEnd().x + pcbnew.FromMM(3.0), item.GetEnd().y))

# 6. Fix J8 rectangle on B.Silkscreen clipping J7 shield pad
j8 = board.FindFootprintByReference('J8')
for item in j8.GraphicalItems():
    if item.GetLayerName() == 'B.Silkscreen' and item.GetShapeStr() == 'Rect':
        # start was (-51.27, 20.01) -> board X=51.23.
        # Change local start X to -49.5 (board X=53.0)
        st = item.GetStart()
        en = item.GetEnd()
        print('J8 rect original:', pcbnew.ToMM(st.x), pcbnew.ToMM(st.y), pcbnew.ToMM(en.x), pcbnew.ToMM(en.y))
        item.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(-49.0), st.y))

# 7. Fix D8 and D9 reference positions:
d8 = board.FindFootprintByReference('D8')
d8.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(64.5), pcbnew.FromMM(92.0)))
d9 = board.FindFootprintByReference('D9')
d9.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(64.5), pcbnew.FromMM(94.5)))

# 8. Fix U13 reference position (overlapping pin 1 marker):
u13 = board.FindFootprintByReference('U13')
u13.Reference().SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(129.0), pcbnew.FromMM(128.5)))

board.Save(test_pcb)
print('Saved test PCB.')
