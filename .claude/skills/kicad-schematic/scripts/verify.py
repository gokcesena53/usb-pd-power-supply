#!/usr/bin/env python3
"""ERC calistirir ve netlist'i referansla karsilastirir.

Sematik uretiminde deterministik dogrulama ayagi: goruntu temiz gorunse de
baglantilar dogru mu, bunu netlist soyler.

Kullanim:
    # ERC sayilari + netlist'i kaydet
    python3 verify.py sema.kicad_sch --save /tmp/base.net

    # degisiklikten sonra: ERC + hangi netler degisti
    python3 verify.py sema.kicad_sch --against /tmp/base.net

    # belirli netleri yazdir
    python3 verify.py sema.kicad_sch --show PD_VOUT V_PRE GND
"""
import argparse
import re
import subprocess
import sys
import tempfile


def erc(sch):
    with tempfile.NamedTemporaryFile(suffix='.rpt', delete=False) as fh:
        rpt = fh.name
    subprocess.run(['kicad-cli', 'sch', 'erc', '--severity-all', '-o', rpt, sch],
                   capture_output=True)
    body = open(rpt, encoding='utf-8').read()
    m = re.search(r'\*\* ERC messages: (\d+)\s+Errors (\d+)\s+Warnings (\d+)', body)
    kinds = re.findall(r'^\[(\w+)\]', body, re.M)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), kinds) if m else (0, 0, 0, [])


def netlist(sch, out=None):
    path = out or tempfile.mktemp(suffix='.net')
    subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '-o', path, sch],
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

    cur = netlist(a.schematic, a.save)
    d = parse(cur)
    print(f'netlist: {len(d)} net')

    if a.against:
        old = parse(a.against)
        changed = [k for k in set(old) | set(d) if old.get(k) != d.get(k)]
        if not changed:
            print('netlist farki: YOK')
        else:
            print(f'netlist farki: {len(changed)} net')
            for k in sorted(changed):
                print(f'\n  {k}')
                print(f'    once : {old.get(k, "(yok)")}')
                print(f'    sonra: {d.get(k, "(yok)")}')
    if a.show:
        for k in a.show:
            hit = [x for x in d if x == k or x.endswith('/' + k)]
            for h in hit or [k]:
                print(f'  {h}: {d.get(h, "(yok)")}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
