#!/usr/bin/env python3
"""Sematigi PNG'ye render eder; bolgeye yakinlasmak icin mm cinsinden kirpar.

Gorsel yineleme dongusunun ayagidir: uret -> render -> BAK -> duzelt -> tekrar.

Kullanim:
    # tum sayfalari listele
    python render.py sema.kicad_sch --list

    # 10. sayfayi tam render et
    python render.py sema.kicad_sch --page 10 -o out

    # 10. sayfada (255,28)-(410,128) mm bolgesine yakinlas
    python render.py sema.kicad_sch --page 10 --crop 255 28 410 128 -o out

    # ayni PDF'ten baska bolge: --reuse ile yeniden export etme (hizli)
    python render.py sema.kicad_sch --page 12 --crop 170 34 358 122 -o out --reuse

    # proje footprint'ini onizle (ped/silk/fab/courtyard) - yeni footprint cizince
    python render.py --footprint libraries/Connector_FPC_Custom.pretty KLS_..._Horizontal -o out

Gereksinimler: kicad-cli; rasterlestirme icin PyMuPDF (tercih) veya pdftoppm.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kicadtools import kicad_cli, keep_file, project_file  # noqa: E402

try:
    import fitz  # PyMuPDF
except ImportError:  # pragma: no cover
    fitz = None

MM = 72 / 25.4


def export_pdf(sch, out_pdf):
    with keep_file(project_file(sch)):
        subprocess.run([kicad_cli(), 'sch', 'export', 'pdf', '-o', out_pdf, sch],
                       check=True, capture_output=True)
    return out_pdf


def list_pages(pdf):
    if fitz:
        texts = [p.get_text() for p in fitz.open(pdf)]
    else:
        texts = subprocess.run(['pdftotext', '-layout', pdf, '-'], check=True,
                               capture_output=True, text=True).stdout.split('\f')
    out = []
    for i, p in enumerate(texts, 1):
        m = re.search(r'Sheet:\s*(\S.*?)\s*$', p, re.M)
        if m:
            out.append((i, m.group(1)))
    return out


def render(pdf, page, out_prefix, dpi=200, crop=None):
    if fitz:
        pg = fitz.open(pdf)[page - 1]
        clip = fitz.Rect(*(v * MM for v in crop)) if crop else None
        path = f'{out_prefix}.png'
        pg.get_pixmap(dpi=dpi, clip=clip).save(path)
        return [path]
    if not shutil.which('pdftoppm'):
        raise FileNotFoundError('PyMuPDF (pip install pymupdf) veya pdftoppm gerekli')
    cmd = ['pdftoppm', '-f', str(page), '-l', str(page), '-r', str(dpi), '-png']
    if crop:
        x0, y0, x1, y1 = crop
        k = dpi / 25.4
        cmd += ['-x', str(int(x0 * k)), '-y', str(int(y0 * k)),
                '-W', str(int((x1 - x0) * k)), '-H', str(int((y1 - y0) * k))]
    cmd += [pdf, out_prefix]
    subprocess.run(cmd, check=True)
    d = os.path.dirname(out_prefix) or '.'
    base = os.path.basename(out_prefix)
    return sorted(os.path.join(d, x) for x in os.listdir(d)
                  if x.startswith(base) and x.endswith('.png'))


FP_LAYERS = 'F.Cu,F.SilkS,F.Fab,F.CrtYd'


def render_footprint(pretty, name, out, layers=FP_LAYERS, width=1000):
    """Footprint'i SVG'ye, varsa PNG'ye cevirir; olusan dosya yollarini dondurur.

    kicad-cli fp export svg cikti dizini YOKSA 'Error creating svg file' der
    ve cikis kodu 0 doner; dizin burada olusturulur. --layers verilmezse bos
    goruntu cikabilir. PNG icin PyMuPDF (SVG acabilir) veya cairosvg; ikisi de
    yoksa yalniz SVG doner. Silk'in pedin ustunden gectigi (DRC uyarisi) ve
    courtyard'in pedleri kapsamadigi durumlar bu goruntude hemen gorunur.
    """
    os.makedirs(out, exist_ok=True)
    subprocess.run([kicad_cli(), 'fp', 'export', 'svg', '--footprint', name,
                    '--layers', layers, '-o', out, pretty], check=True, capture_output=True)
    svg = os.path.join(out, name + '.svg')
    if not os.path.exists(svg):
        raise FileNotFoundError(f'SVG uretilemedi: {svg} (footprint adi / .pretty yolu?)')
    png = os.path.join(out, name + '.png')
    if fitz:
        doc = fitz.open(svg)
        pg = doc[0]
        pg.get_pixmap(dpi=int(72 * width / max(pg.rect.width, 1))).save(png)
        return [svg, png]
    try:
        import cairosvg
        cairosvg.svg2png(url=svg, write_to=png, output_width=width, background_color='white')
        return [svg, png]
    except ImportError:
        return [svg]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('schematic', nargs='?', help='kok .kicad_sch dosyasi')
    ap.add_argument('--footprint', nargs=2, metavar=('PRETTY', 'NAME'),
                    help='sema yerine footprint onizle')
    ap.add_argument('--page', type=int, help='PDF sayfa numarasi')
    ap.add_argument('--list', action='store_true', help='sayfalari listele')
    ap.add_argument('--crop', nargs=4, type=float, metavar=('X0', 'Y0', 'X1', 'Y1'),
                    help='mm cinsinden kirpma bolgesi')
    ap.add_argument('--dpi', type=int, default=None,
                    help='varsayilan: kirpmada 200, tam sayfada 110')
    ap.add_argument('--reuse', action='store_true',
                    help='cikti dizinindeki sch.pdf varsa yeniden export etme')
    ap.add_argument('-o', '--out', default=None, help='cikti dizini')
    a = ap.parse_args()

    out = a.out or tempfile.mkdtemp(prefix='kisch-render-')
    os.makedirs(out, exist_ok=True)
    if a.footprint:
        for p in render_footprint(a.footprint[0], a.footprint[1], out):
            print(p)
        return 0
    if not a.schematic:
        ap.error('schematic veya --footprint gerekli')
    pdf = os.path.join(out, 'sch.pdf')
    if not (a.reuse and os.path.exists(pdf)):
        export_pdf(a.schematic, pdf)

    if a.list or not a.page:
        for n, name in list_pages(pdf):
            print(f'  {n:3}  {name}')
        if not a.page:
            return 0

    dpi = a.dpi or (200 if a.crop else 110)
    tag = f'p{a.page}' + ('_' + '_'.join(str(int(v)) for v in a.crop) if a.crop else '')
    for p in render(pdf, a.page, os.path.join(out, tag), dpi, a.crop):
        print(p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
