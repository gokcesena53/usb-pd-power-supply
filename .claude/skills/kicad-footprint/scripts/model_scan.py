"""PCB'deki 3D model atamalarini tara: modelsiz footprint ve dosyasi bulunmayan model.

KiCad model dosyasini bulamazsa render/STEP'te parcayi SESSIZCE modelsiz
cizer. KiCad 10 standart footprint'lerinin bir kismi kurulumda olmayan modele
isaret ediyor (L_7.3x7.3_H4.5, WSON-12 3x3, ESP32-C6-MINI-1, ABS25, SolderWire,
SOIC-8-1EP EP2.71x3.7). PCB kopyasinda model yoksa kutuphanedeki footprint'e
bakar (update_pcb --refresh oncesi durumu gorur).

    sh .claude/skills/kicad-schematic/scripts/kpy \\
       .claude/skills/kicad-footprint/scripts/model_scan.py hardware/gopo.kicad_pcb
Cikis kodu: kirik model varsa 1.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'kicad-schematic', 'scripts'))
import kicadtools as kt  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pcb')
    ap.add_argument('--ignore', default='TestPoint:', help='modelsiz sayilmayacak FPID oneki')
    a = ap.parse_args()
    prj = os.path.dirname(os.path.abspath(a.pcb))
    share3d = kt.kicad_share('3dmodels')
    env = {'KIPRJMOD': prj, 'KISYS3DMOD': share3d}
    env.update({f'KICAD{v}_3DMODEL_DIR': share3d for v in range(6, 12)})

    def res(p):
        return re.sub(r'\$\{(\w+)\}', lambda m: env.get(m.group(1), m.group(0)), p)
    table = os.path.join(prj, 'fp-lib-table')
    libs = dict(re.findall(r'\(name "([^"]+)"\).*?\(uri "([^"]+)"\)', open(table).read())) \
        if os.path.exists(table) else {}
    s = open(a.pcb, encoding='utf-8').read()
    parts = re.split(r'\n\t\(footprint ', s)[1:]
    nomodel, missing, ok = [], [], 0
    for p in parts:
        fpid = p.split('"')[1]
        ref = re.search(r'\(property "Reference" "([^"]+)"', p).group(1)
        models, src = re.findall(r'\(model "([^"]+)"', p), 'pcb'
        if not models:
            lib, name = fpid.split(':', 1)
            path = os.path.join(res(libs[lib]), name + '.kicad_mod') if lib in libs else \
                os.path.join(kt.kicad_share('footprints'), lib + '.pretty', name + '.kicad_mod')
            if os.path.exists(path):
                models, src = re.findall(r'\(model "([^"]+)"', open(path, encoding='utf-8').read()), 'lib'
        if not models:
            if not fpid.startswith(a.ignore):
                nomodel.append(f'{ref} {fpid}')
            continue
        for m in models:
            base = os.path.splitext(res(m))[0]
            if any(os.path.isfile(base + e) for e in ('.step', '.stp', '.wrl')):
                ok += 1
            else:
                missing.append(f'{ref} [{src}] {m}')
    print(f'{len(parts)} footprint; cozulen model {ok}')
    print(f'modelsiz ({a.ignore} haric): {len(nomodel)}')
    for x in sorted(nomodel):
        print('  ', x)
    print(f'dosyasi yok: {len(missing)}')
    for x in sorted(missing):
        print('  ', x)
    sys.exit(1 if missing or nomodel else 0)


if __name__ == '__main__':
    main()
