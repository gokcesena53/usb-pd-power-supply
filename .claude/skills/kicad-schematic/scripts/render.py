#!/usr/bin/env python3
"""Sematigi PNG'ye render eder; bolgeye yakinlasmak icin mm cinsinden kirpar.

Gorsel yineleme dongusunun ayagidir: uret -> render -> BAK -> duzelt -> tekrar.

Kullanim:
    # tum sayfalari listele
    python3 render.py sema.kicad_sch --list

    # 10. sayfayi tam render et
    python3 render.py sema.kicad_sch --page 10 -o /tmp/out

    # 10. sayfada (255,28)-(410,128) mm bolgesine yakinlas
    python3 render.py sema.kicad_sch --page 10 --crop 255 28 410 128 -o /tmp/out

Gereksinimler: kicad-cli, pdftoppm (poppler-utils)
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile


def export_pdf(sch, out_pdf):
    subprocess.run(['kicad-cli', 'sch', 'export', 'pdf', '-o', out_pdf, sch],
                   check=True, capture_output=True)
    return out_pdf


def list_pages(pdf):
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'],
                         check=True, capture_output=True, text=True).stdout
    pages = txt.split('\f')
    out = []
    for i, p in enumerate(pages, 1):
        m = re.search(r'Sheet:\s*(\S.*?)\s*$', p, re.M)
        if m:
            out.append((i, m.group(1)))
    return out


def render(pdf, page, out_prefix, dpi=200, crop=None):
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('schematic', help='kok .kicad_sch dosyasi')
    ap.add_argument('--page', type=int, help='PDF sayfa numarasi')
    ap.add_argument('--list', action='store_true', help='sayfalari listele')
    ap.add_argument('--crop', nargs=4, type=float, metavar=('X0', 'Y0', 'X1', 'Y1'),
                    help='mm cinsinden kirpma bolgesi')
    ap.add_argument('--dpi', type=int, default=200)
    ap.add_argument('-o', '--out', default=None, help='cikti dizini')
    a = ap.parse_args()

    out = a.out or tempfile.mkdtemp(prefix='kisch-render-')
    os.makedirs(out, exist_ok=True)
    pdf = export_pdf(a.schematic, os.path.join(out, 'sch.pdf'))

    if a.list or not a.page:
        for n, name in list_pages(pdf):
            print(f'  {n:3}  {name}')
        if not a.page:
            return 0

    files = render(pdf, a.page, os.path.join(out, f'p{a.page}'), a.dpi, a.crop)
    for p in files:
        print(p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
