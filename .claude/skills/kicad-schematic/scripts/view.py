#!/usr/bin/env python3
"""Datasheet / cizim / fotograf inceleme: PDF metni, PDF'te metin arama, PDF
bolgesi render, goruntu kirpip buyutme. Cikan PNG'yi Read ile ac.

Neden: Windows'ta pdftoppm yok, Read araci PDF sayfasi render edemiyor;
Linux'ta PyMuPDF olmayabilir. Bu betik PyMuPDF (fitz) varsa onu, yoksa
pdftotext/pdftoppm'i kullanir; goruntu icin PIL (yoksa fitz).

    SK=.claude/skills/kicad-schematic/scripts
    # PDF metni (Altium sema ciktisinda netlist de metin olarak cikar)
    sh $SK/kpy $SK/view.py hardware/datasheets/X.pdf --text > <scratch>/x.txt
    # metnin sayfa ve konumu (pt ve mm) -> --clip icin
    sh $SK/kpy $SK/view.py X.pdf --find P2 "Header 1"
    # sayfa bolgesi (pt, --mm ile mm), 500 dpi
    sh $SK/kpy $SK/view.py X.pdf --page 1 --clip 30 470 160 550 --dpi 500 -o <scratch>/p2.png
    # goruntu (webp/png/jpg) bolgesi piksel cinsinden, 3x buyut
    sh $SK/kpy $SK/view.py foto.webp --crop 820 520 915 835 --scale 3 -o <scratch>/hdr.png
    # goruntu boyutu
    sh $SK/kpy $SK/view.py foto.webp --info
"""
import argparse
import os
import shutil
import subprocess
import sys

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None
if os.environ.get('VIEW_NO_FITZ'):   # pdftoppm/pdftotext yedegini sinamak icin (selftest.sh)
    fitz = None

MM = 72 / 25.4
IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.tif', '.tiff')


def pdf_text(pdf, pages=None):
    """[(sayfa_no, metin)]. pages: 1 tabanli liste veya None (hepsi)."""
    if fitz:
        doc = fitz.open(pdf)
        idx = pages or range(1, doc.page_count + 1)
        return [(i, doc[i - 1].get_text()) for i in idx]
    if not shutil.which('pdftotext'):
        raise FileNotFoundError('PyMuPDF (pip install pymupdf) veya pdftotext gerekli')
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], check=True,
                         capture_output=True, text=True).stdout.split('\f')
    return [(i, t) for i, t in enumerate(txt, 1) if not pages or i in pages]


def pdf_find(pdf, words):
    """{kelime: [(sayfa, x0, y0, x1, y1 pt)]} - yalniz PyMuPDF."""
    if not fitz:
        raise RuntimeError('--find PyMuPDF ister')
    doc = fitz.open(pdf)
    return {w: [(i + 1, *tuple(r)) for i, pg in enumerate(doc) for r in pg.search_for(w)] for w in words}


def pdf_render(pdf, page, out, dpi=300, clip=None, mm=False):
    """Sayfayi (veya clip bolgesini, pt ya da mm) PNG'ye yazar; yolu dondurur."""
    if fitz:
        pg = fitz.open(pdf)[page - 1]
        rect = fitz.Rect(*(v * MM for v in clip)) if (clip and mm) else (fitz.Rect(*clip) if clip else None)
        pg.get_pixmap(dpi=dpi, clip=rect).save(out)
        return out
    if not shutil.which('pdftoppm'):
        raise FileNotFoundError('PyMuPDF veya pdftoppm gerekli')
    cmd = ['pdftoppm', '-f', str(page), '-l', str(page), '-r', str(dpi), '-png', '-singlefile']
    if clip:
        k = dpi / (25.4 if mm else 72)
        x0, y0, x1, y1 = clip
        cmd += ['-x', str(int(x0 * k)), '-y', str(int(y0 * k)),
                '-W', str(int((x1 - x0) * k)), '-H', str(int((y1 - y0) * k))]
    subprocess.run(cmd + [pdf, os.path.splitext(out)[0]], check=True)
    return out


def img_crop(path, out, box=None, scale=1.0):
    """Goruntu bolgesini (piksel x0 y0 x1 y1) kirpip scale kat buyutur."""
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError('goruntu icin PIL gerekli (pip install pillow)')
    im = Image.open(path).convert('RGB')
    if box:
        im = im.crop(tuple(int(v) for v in box))
    if scale != 1:
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    im.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('file')
    ap.add_argument('--text', action='store_true', help='PDF metnini yazdir')
    ap.add_argument('--pages', help='metin icin sayfa araligi, or. 3-5 veya 1,4')
    ap.add_argument('--find', nargs='+', metavar='METIN', help='PDF: metnin sayfa/konumu')
    ap.add_argument('--page', type=int, default=1, help='PDF render sayfasi (1 tabanli)')
    ap.add_argument('--clip', nargs=4, type=float, metavar=('X0', 'Y0', 'X1', 'Y1'), help='PDF bolgesi (pt)')
    ap.add_argument('--mm', action='store_true', help='--clip mm cinsinden')
    ap.add_argument('--dpi', type=int, default=300)
    ap.add_argument('--crop', nargs=4, type=float, metavar=('X0', 'Y0', 'X1', 'Y1'), help='goruntu bolgesi (px)')
    ap.add_argument('--scale', type=float, default=1.0, help='goruntu buyutme')
    ap.add_argument('--info', action='store_true', help='goruntu/PDF boyutu')
    ap.add_argument('-o', '--out', help='cikti PNG')
    a = ap.parse_args()

    is_img = a.file.lower().endswith(IMG_EXT)
    if a.info:
        if is_img:
            from PIL import Image
            print(Image.open(a.file).size)
        elif fitz:
            doc = fitz.open(a.file)
            print(doc.page_count, 'sayfa;', [tuple(round(v, 1) for v in p.rect) for p in doc][:5], 'pt')
        return 0
    if is_img:
        print(img_crop(a.file, a.out or os.path.splitext(a.file)[0] + '_crop.png', a.crop, a.scale))
        return 0
    if a.text:
        pages = None
        if a.pages:
            pages = []
            for part in a.pages.split(','):
                lo, _, hi = part.partition('-')
                pages += list(range(int(lo), int(hi or lo) + 1))
        for n, t in pdf_text(a.file, pages):
            print(f'--- sayfa {n}\n{t}')
        return 0
    if a.find:
        for w, hits in pdf_find(a.file, a.find).items():
            for p, x0, y0, x1, y1 in hits:
                print(f'{w!r}: s{p} pt ({x0:.1f},{y0:.1f})-({x1:.1f},{y1:.1f})  '
                      f'mm ({x0 / MM:.1f},{y0 / MM:.1f})-({x1 / MM:.1f},{y1 / MM:.1f})')
            if not hits:
                print(f'{w!r}: yok')
        return 0
    if not a.out:
        ap.error('-o gerekli')
    print(pdf_render(a.file, a.page, a.out, a.dpi, a.clip, a.mm))
    return 0


if __name__ == '__main__':
    sys.exit(main())
