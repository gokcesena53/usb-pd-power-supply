"""Kartin ust ve alt yuzunu kart sinirina kirpilmis PNG olarak render eder.

Kullanim:
    sh $SK/kpy $PL/pcb_render.py hardware/gopo.kicad_pcb $T/cand [--crop x0 y0 x1 y1] [--dpi 220]
    -> $T/cand-top.png, $T/cand-bot.png (alt yuz aynalanmaz; koordinatlar ust gorunusle ayni)

Katmanlar: Edge.Cuts, X.Cu, X.Fab, X.Courtyard, User.Drawings (LCD/FPC izdusumleri).
kicad-cli PDF'i karti sayfada mutlak mm koordinatinda cizer; kirpma bu yuzden
dogrudan kart mm'si ile yapilir. Kirpma verilmezse Edge.Cuts'tan (+2 mm) bulunur.
Rasterlestirme: PyMuPDF varsa o, yoksa pdftoppm (Linux'ta pdftoppm ile dogrulandi).
pcbnew gerekmez; pcbnew'li python'da PyMuPDF olmayabilir.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'kicad-schematic', 'scripts'))
from kicadtools import run_cli  # noqa: E402

try:
    import fitz
except ImportError:
    fitz = None

LAYERS = {"top": "Edge.Cuts,F.Cu,F.Fab,F.Courtyard,User.Drawings",
          "bot": "Edge.Cuts,B.Cu,B.Fab,B.Courtyard,User.Drawings"}


def edge_bbox(board, margin=2.0):
    """Edge.Cuts cizimlerinin koordinatlarindan bbox (duz metin; pcbnew'siz)."""
    txt = open(board, encoding="utf-8").read()
    xs, ys = [], []
    for m in re.finditer(r'\(gr_\w+(?:(?!\n\t\(gr_|\n\t\(footprint).)*?\(layer "Edge\.Cuts"\)', txt, re.S):
        for x, y in re.findall(r'\((?:start|end|mid|center|xy) ([-\d.]+) ([-\d.]+)\)', m.group(0)):
            xs.append(float(x)); ys.append(float(y))
    if not xs:
        raise SystemExit("Edge.Cuts bulunamadi; --crop ver")
    return min(xs) - margin, min(ys) - margin, max(xs) + margin, max(ys) + margin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board"); ap.add_argument("out")
    ap.add_argument("--crop", nargs=4, type=float); ap.add_argument("--dpi", type=int, default=220)
    a = ap.parse_args()
    x0, y0, x1, y1 = a.crop or edge_bbox(a.board)
    for side, layers in LAYERS.items():
        pdf = f"{a.out}-{side}.pdf"; png = f"{a.out}-{side}.png"
        run_cli(["pcb", "export", "pdf", "--mode-single", "-l", layers, "-o", pdf, a.board])
        if fitz:
            pt = 72 / 25.4
            page = fitz.open(pdf)[0]
            page.get_pixmap(dpi=a.dpi, clip=fitz.Rect(x0 * pt, y0 * pt, x1 * pt, y1 * pt)).save(png)
        elif shutil.which("pdftoppm"):
            px = a.dpi / 25.4
            subprocess.run(["pdftoppm", "-png", "-r", str(a.dpi), "-x", str(int(x0 * px)), "-y", str(int(y0 * px)),
                            "-W", str(int((x1 - x0) * px)), "-H", str(int((y1 - y0) * px)), "-singlefile", pdf, png[:-4]], check=True)
        else:
            raise SystemExit("PyMuPDF veya pdftoppm gerekli")
        os.remove(pdf)
        print(png)


if __name__ == "__main__":
    main()
