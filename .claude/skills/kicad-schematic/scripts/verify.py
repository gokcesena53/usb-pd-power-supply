#!/usr/bin/env python3
"""ERC calistirir ve netlist'i referansla karsilastirir.

Sematik uretiminde deterministik dogrulama ayagi: goruntu temiz gorunse de
baglantilar dogru mu, bunu netlist soyler.

Kullanim:
    # ERC sayilari + netlist'i kaydet
    python verify.py sema.kicad_sch --save /tmp/base.net

    # degisiklikten sonra: ERC + hangi netler degisti
    python verify.py sema.kicad_sch --against /tmp/base.net

Yeniden yapilandirmada (blok baska sayfaya tasindi, global etiket yerel oldu)
net ADLARI degisir ama BAGLANTI ayni kalmalidir; --against ikisini ayri raporlar:
"baglanti farki: YOK; 9 net yeniden adlandi" kabul edilebilir sonuctur.

    # belirli netleri yazdir
    python verify.py sema.kicad_sch --show PD_VOUT V_PRE GND

Hedef: yerlesim/cizim duzenlemesinde "netlist farki: YOK" ve ERC sayisi degismemeli.
kicad-cli .kicad_pro'yu yeniden yazar; bu betik dosyayi bayt bayt geri koyar.
"""
import argparse
import re
import subprocess
import sys
import tempfile
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kicadtools import kicad_cli, keep_file, project_file  # noqa: E402


def erc(sch):
    with tempfile.NamedTemporaryFile(suffix='.rpt', delete=False) as fh:
        rpt = fh.name
    with keep_file(project_file(sch)):
        subprocess.run([kicad_cli(), 'sch', 'erc', '--severity-all', '-o', rpt, sch],
                       capture_output=True)
    body = open(rpt, encoding='utf-8').read()
    m = re.search(r'\*\* ERC messages: (\d+)\s+Errors (\d+)\s+Warnings (\d+)', body)
    kinds = re.findall(r'^\[(\w+)\]', body, re.M)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), kinds) if m else (0, 0, 0, [])


def netlist(sch, out=None):
    path = out or tempfile.mktemp(suffix='.net')
    with keep_file(project_file(sch)):
        subprocess.run([kicad_cli(), 'sch', 'export', 'netlist', '-o', path, sch],
                       check=True, capture_output=True)
    return path


def parse(path):
    t = open(path, encoding='utf-8').read()
    t = t[t.index('\t(nets'):]
    d = {}
    for b in re.split(r'\n\t\t\(net\b', t)[1:]:
        n = re.search(r'\(name "([^"]*)"\)', b)
        if n:
            d[n.group(1)] = sorted(
                f'{r}.{p}' for r, p in
                re.findall(r'\(ref "([^"]+)"\)\s*\n?\s*\(pin "([^"]+)"\)', b))
    return d


def signature(d):
    """Net adindan bagimsiz imza: {pin kumesi -> net adi}.

    Blok baska sayfaya tasindiginda net adi degisir (/POWER GENERATION/LX_SW ->
    /USB_PD_CONTROLLER/LX_SW) ama pin kumesi ayni kalir; boylece gercek baglanti
    kaybi ile yeniden adlandirma ayirt edilir.
    """
    return {frozenset(p): n for n, p in d.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('schematic')
    ap.add_argument('--save', metavar='NET', help='netlist dosyasini buraya kaydet')
    ap.add_argument('--against', metavar='NET', help='bu netlist ile karsilastir')
    ap.add_argument('--show', nargs='*', metavar='NET', help='bu netleri yazdir')
    a = ap.parse_args()

    n, e, w, kinds = erc(a.schematic)
    print(f'ERC: {n} ihlal  ({e} hata, {w} uyari)')
    from collections import Counter
    for k, c in Counter(kinds).most_common():
        print(f'   {c:3}  {k}')

    # onbellekte olmayan lib_id: ERC hata vermez ama pin ayri nete duser
    import glob
    import kisch_edit as E
    from kicadtools import read_sheet
    for sh in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(a.schematic)),
                                            '*.kicad_sch'))):
        miss = E.missing_lib_symbols(read_sheet(sh)[0])
        if miss:
            print(f'UYARI {os.path.basename(sh)}: lib_symbols onbelleginde yok: {miss} '
                  f'-> E.ensure_used_lib_symbols')

    cur = netlist(a.schematic, a.save)
    d = parse(cur)
    print(f'netlist: {len(d)} net')

    if a.against:
        old = parse(a.against)
        if all(old.get(k) == d.get(k) for k in set(old) | set(d)):
            print('netlist farki: YOK')
        else:
            so, sn = signature(old), signature(d)
            lost = sorted((so[k], sorted(k)) for k in so if k not in sn)
            gain = sorted((sn[k], sorted(k)) for k in sn if k not in so)
            ren = sorted((so[k], sn[k]) for k in so if k in sn and so[k] != sn[k])
            head = 'YOK' if not (lost or gain) else f'{len(lost)} kayip, {len(gain)} yeni'
            print(f'baglanti farki: {head}'
                  + (f'; {len(ren)} net yeniden adlandi' if ren else ''))
            for n, p in lost:
                print(f'  KAYIP {n}\n    {p}')
            for n, p in gain:
                print(f'  YENI  {n}\n    {p}')
            for x, y in ren:
                print(f'  AD    {x} -> {y}')
    if a.show:
        for k in a.show:
            hit = [x for x in d if x == k or x.endswith('/' + k)]
            for h in hit or [k]:
                print(f'  {h}: {d.get(h, "(yok)")}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
