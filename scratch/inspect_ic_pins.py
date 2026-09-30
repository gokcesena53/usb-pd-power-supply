import pcbnew
import math

board = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')

def get_fp_pads(fp):
    res = {}
    fpos = fp.GetPosition()
    for p in fp.Pads():
        num = p.GetNumber()
        pos = p.GetPosition()
        res[num] = {
            'pos': (round(pcbnew.ToMM(pos.x), 3), round(pcbnew.ToMM(pos.y), 3)),
            'net': p.GetNetname()
        }
    return res

for u_ref in ['U1', 'U2', 'U3', 'U4', 'U5', 'U6', 'U10', 'U11', 'U12', 'U13']:
    fp = board.FindFootprintByReference(u_ref)
    fpos = fp.GetPosition()
    print(f"\n=======================================================")
    print(f"{u_ref}: {fp.GetValue()} at ({pcbnew.ToMM(fpos.x):.3f}, {pcbnew.ToMM(fpos.y):.3f}) rot={fp.GetOrientation().AsDegrees()%360:.1f} layer={fp.GetLayerName()}")
    print(f"Footprint: {fp.GetFPID().GetLibItemName()}")
    pads = get_fp_pads(fp)
    for pnum, pdata in pads.items():
        print(f"  pin {pnum:3}: at {pdata['pos']} net={pdata['net']}")
