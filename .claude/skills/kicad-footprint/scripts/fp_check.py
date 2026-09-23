#!/usr/bin/env python3
"""Proje footprint'ini dogrula: KiCad ayristirmasi + 2D onizleme + (--3d) test
kartinda 3D render ve STEP disa aktarimi. Cikan PNG'lere Read ile BAK.

    SK=.claude/skills/kicad-schematic/scripts; FK=.claude/skills/kicad-footprint/scripts
    sh $SK/kpy $FK/fp_check.py hardware/libraries/Module_Custom.pretty Waveshare_2-CH_UART_TO_ETH \\
        -o <scratch>/fp --3d

Adimlar:
  1. `kicad-cli fp upgrade --force` ile kutuphaneyi gecici dizine yeniden yazar:
     KiCad dosyayi okuyamazsa burada patlar. Ped (THT/SMD/MP), keepout ve model
     sayilarini okunan dosyadan raporlar (yazdigin degil, KiCad'in anladigi).
     --force olmadan "Footprint library was not updated" deyip hicbir sey yazmaz.
  2. `render.py --footprint` ile F.Cu/SilkS/Fab/CrtYd PNG (silk ped ustunde mi,
     courtyard her seyi kapsiyor mu, pin 1 isareti dogru kosede mi).
  3. --3d: KiCad python'unda bos kart + footprint (+ kenar) kurar; modelin
     ${KIPRJMOD} yolu cozulsun diye referans verilen .3dshapes dizinini test
     kartinin yanina kopyalar; `pcb render` ust/on/izometrik + `pcb export step`.
     Model bulunamazsa KiCad sessizce modelsiz render eder -> once yolu denetler.
"""
import argparse
import glob
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kicad-schematic', 'scripts'))
from kicadtools import kicad_python, kicad_share, run_cli  # noqa: E402


def project_dir(pretty):
    """.pretty'den yukari cikip .kicad_pro bulunan dizin (${KIPRJMOD})."""
    d = os.path.abspath(pretty)
    while True:
        if glob.glob(os.path.join(d, '*.kicad_pro')):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            return os.path.dirname(os.path.abspath(pretty))
        d = nd


def resolve(path, prj):
    def sub(m):
        v = m.group(1)
        if v == 'KIPRJMOD':
            return prj
        if re.fullmatch(r'KICAD\d*_3DMODEL_DIR', v):
            return kicad_share('3dmodels')
        return os.environ.get(v, m.group(0))
    return re.sub(r'\$\{(\w+)\}', sub, path)


def parse_check(pretty, name, prj):
    tmp = tempfile.mkdtemp(prefix='fpchk-')
    out = os.path.join(tmp, 'x.pretty')
    run_cli(['fp', 'upgrade', '--force', '--output', out, pretty])
    fn = os.path.join(out, name + '.kicad_mod')
    if not os.path.exists(fn):
        sys.exit(f'KiCad footprint\'i okuyamadi / bulamadi: {name} ({pretty})')
    t = open(fn, encoding='utf-8').read()
    pads = re.findall(r'\(pad "([^"]*)" (\w+)', t)
    models = re.findall(r'\(model "([^"]+)"', t)
    rep = {'THT': sum(k == 'thru_hole' for _, k in pads), 'SMD': sum(k == 'smd' for _, k in pads),
           'NPTH': sum(k == 'np_thru_hole' for _, k in pads), 'MP': sum(n == 'MP' for n, _ in pads),
           'keepout': t.count('(keepout'), 'courtyard': t.count('"F.CrtYd"') + t.count('"B.CrtYd"'),
           'model': len(models)}
    print('KiCad okudu:', ', '.join(f'{k} {v}' for k, v in rep.items()))
    if not rep['courtyard']:
        print('UYARI: courtyard yok')
    for m in models:
        p = resolve(m, prj)
        print(f'model: {m}\n  -> {p} {"VAR" if os.path.exists(p) else "YOK (render modelsiz cikar)"}')
    return models


def check_3d(pretty, name, prj, models, out):
    tb = os.path.join(out, 'tb')
    shutil.rmtree(tb, ignore_errors=True)
    os.makedirs(tb)
    for m in models:                      # ${KIPRJMOD}/... -> test kartinin yanina
        if m.startswith('${KIPRJMOD}'):
            src = os.path.dirname(resolve(m, prj))
            dst = os.path.join(tb, os.path.relpath(src, prj))
            if not os.path.exists(dst):
                shutil.copytree(src, dst)
    board = os.path.join(tb, 'test.kicad_pcb')
    import subprocess
    r = subprocess.run([kicad_python(), os.path.abspath(__file__), '--_board', os.path.abspath(pretty),
                        name, board], capture_output=True, text=True, encoding='utf-8', errors='replace',
                       env=dict(os.environ, PYTHONIOENCODING='utf-8'))
    if r.returncode:
        sys.exit('test karti kurulamadi:\n' + r.stdout + r.stderr)
    views = {'top': ['--side', 'top'], 'front': ['--side', 'front'],
             'iso': ['--rotate', '-55,0,-30', '--zoom', '0.9']}
    for v, extra in views.items():
        png = os.path.join(out, f'{name}_3d_{v}.png')
        run_cli(['pcb', 'render', '-w', '1400', '--height', '900', *extra, '-o', png, board])
        print(png)
    step = os.path.join(tb, 'test.step')
    run_cli(['pcb', 'export', 'step', '-f', '-o', step, board])
    n = open(step, encoding='utf-8', errors='replace').read().count('MANIFOLD_SOLID_BREP')
    print(f'STEP disa aktarim: {n} kati (kart dahil) -> {step}')


def make_board(pretty, name, out):
    """KiCad python'unda calisir (pcbnew)."""
    import pcbnew
    b = pcbnew.BOARD()
    fp = pcbnew.PCB_IO_KICAD_SEXPR().FootprintLoad(pretty, name)
    fp.SetReference('REF')
    fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(100), pcbnew.FromMM(100)))
    b.Add(fp)
    bb = fp.GetBoundingBox(False)
    m = pcbnew.FromMM(3)
    x0, y0, x1, y1 = bb.GetLeft() - m, bb.GetTop() - m, bb.GetRight() + m, bb.GetBottom() + m
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    for i in range(4):
        s = pcbnew.PCB_SHAPE(b)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(*pts[i]))
        s.SetEnd(pcbnew.VECTOR2I(*pts[(i + 1) % 4]))
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        b.Add(s)
    b.Save(out)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--_board':
        make_board(*sys.argv[2:5])
        return 0
    sys.path.insert(0, os.path.join(HERE, '..', '..', 'kicad-schematic', 'scripts'))
    from render import render_footprint
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pretty')
    ap.add_argument('name')
    ap.add_argument('-o', '--out', default=None)
    ap.add_argument('--3d', dest='three_d', action='store_true', help='test kartinda 3D render + STEP')
    a = ap.parse_args()
    out = os.path.abspath(a.out or tempfile.mkdtemp(prefix='fpchk-'))
    os.makedirs(out, exist_ok=True)
    prj = project_dir(a.pretty)
    models = parse_check(a.pretty, a.name, prj)
    for p in render_footprint(a.pretty, a.name, out):
        print(p)
    if a.three_d:
        check_3d(a.pretty, a.name, prj, models, out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
