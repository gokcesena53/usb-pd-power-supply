#!/usr/bin/env python3
"""Headless "Update PCB from Schematic" (kicad-cli'da bu komut yok).

    python update_pcb.py hardware/gopo.kicad_pcb [--dry-run] [--keep-tracks]

Şemadan (PCB ile aynı adlı .kicad_sch) netlist üretir, footprint'leri
REFERANSLA eşler (sayfa taşıma UUID yolunu değiştirir), sonra:
  - şemada olmayan footprint'i siler, footprint kimliği değişeni aynı
    konum/yön/katmanda değiştirir, yenileri kart dışına ızgaraya dizer;
  - Value, yol, Sheetname/Sheetfile, DNP, tüm sembol alanlarını (gizli, Fab)
    eşitler; sembolde olmayan kullanıcı alanlarını siler;
  - pad netlerini yazar, kullanılmayan netleri siler.
Footprint'i boş sembol (TBD) atlanır ve raporlanır. İzler varsayılan olarak
silinir (footprint değişince eski pad'lere giden izler anlamsızlaşır);
--keep-tracks ile dokunulmaz. Doğrulama:
    kicad-cli pcb drc --schematic-parity --severity-all --format json ...
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

import pcbnew

FP_DIR = '/usr/share/kicad/footprints'
SKIP_PROPS = {'Sheetname', 'Sheetfile', 'dnp', 'ki_keywords', 'ki_fp_filters',
              'exclude_from_bom', 'exclude_from_board', 'exclude_from_pos_files'}


def parse(txt):
    stack = [[]]
    for m in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()"]+', txt):
        t = m.group()
        if t == '(':
            stack.append([])
        elif t == ')':
            x = stack.pop(); stack[-1].append(x)
        elif t[0] == '"':
            stack[-1].append(t[1:-1].replace('\\"', '"').replace('\\\\', '\\'))
        else:
            stack[-1].append(t)
    return stack[0][0]


def find(n, key):
    return [c for c in n[1:] if isinstance(c, list) and c and c[0] == key]


def one(n, key, default=None):
    r = find(n, key)
    return r[0] if r else default


def load_net(path):
    t = parse(open(path, encoding='utf-8').read())
    comps = {}
    for c in find(one(t, 'components'), 'comp'):
        sp = one(c, 'sheetpath')
        comps[one(c, 'ref')[1]] = {
            'value': one(c, 'value')[1],
            'fp': one(c, 'footprint', [0, ''])[1],
            'datasheet': one(c, 'datasheet', [0, ''])[1],
            'description': one(c, 'description', [0, ''])[1],
            'props': {p[1][1]: (p[2][1] if len(p) > 2 else '') for p in find(c, 'property')},
            'sheetnames': one(sp, 'names')[1], 'sheettst': one(sp, 'tstamps')[1],
            'tstamp': one(c, 'tstamps')[1]}
    nets = {one(n, 'name')[1]: [(one(x, 'ref')[1], one(x, 'pin')[1]) for x in find(n, 'node')]
            for n in find(one(t, 'nets'), 'net')}
    return comps, nets


def lib_table(prj):
    env = {'KIPRJMOD': prj, 'KICAD10_FOOTPRINT_DIR': os.environ.get('KICAD10_FOOTPRINT_DIR', FP_DIR)}
    libs = {}
    for tbl in (os.path.join(os.path.dirname(FP_DIR), 'template/fp-lib-table'), os.path.join(prj, 'fp-lib-table')):
        if not os.path.exists(tbl):
            continue
        for name, uri in re.findall(r'\(lib \(name "([^"]+)"\)\s*\(type "KiCad"\)\s*\(uri "([^"]+)"\)', open(tbl).read()):
            libs[name] = re.sub(r'\$\{(\w+)\}', lambda m: env[m.group(1)], uri)
    return libs


def natural(ref):
    return re.sub(r'\d', '', ref), int(re.sub(r'\D', '', ref) or 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pcb')
    ap.add_argument('--dry-run', action='store_true', help='yalnız değişiklikleri listele, kaydetme')
    ap.add_argument('--keep-tracks', action='store_true')
    a = ap.parse_args()
    pcb = os.path.abspath(a.pcb); prj = os.path.dirname(pcb)
    net = os.path.join(tempfile.mkdtemp(), 'board.net')
    subprocess.run(['kicad-cli', 'sch', 'export', 'netlist', '--format', 'kicadsexpr', '-o', net,
                    pcb[:-len('.kicad_pcb')] + '.kicad_sch'], check=True, capture_output=True)
    comps, nets = load_net(net)
    libs = lib_table(prj)
    io = pcbnew.PCB_IO_KICAD_SEXPR()

    def load_fp(fpid):
        lib, name = fpid.split(':', 1)
        fp = io.FootprintLoad(libs[lib], name)
        if not isinstance(fp, pcbnew.FOOTPRINT):
            sys.exit(f'footprint yüklenemedi: {fpid} ({libs.get(lib)})')
        fp.SetFPIDAsString(fpid)
        return fp

    b = pcbnew.LoadBoard(pcb)
    fps = {f.GetReference(): f for f in b.GetFootprints()}
    # KiCad 10 SWIG: kart düzenlendikten sonra FootprintLoad bazen çıplak
    # SwigPyObject döndürüyor -> hepsini önce yükle. Silinen nesneleri de
    # Python tarafında tut (keep), yoksa segfault riski.
    pre = {}
    for r, c in comps.items():
        if c['fp'] and (r not in fps or fps[r].GetFPIDAsString() != c['fp']):
            pre.setdefault(c['fp'], []).append(load_fp(c['fp']))
    keep, log = [], []

    for r in sorted(set(fps) - set(comps), key=natural):
        keep.append(fps.pop(r)); b.Remove(keep[-1]); log.append(f'SIL   {r}')

    for r in sorted(comps, key=natural):
        c, old = comps[r], fps.get(r)
        if not c['fp']:
            log.append(f'ATLA  {r}: şemada footprint yok')
        elif old is not None and old.GetFPIDAsString() != c['fp']:
            new = pre[c['fp']].pop()
            new.SetReference(r); b.Remove(old); keep.append(old); b.Add(new); fps[r] = new
            if old.GetLayer() == pcbnew.B_Cu:  # Flip yalnız karttaki footprint'te güvenli
                new.Flip(new.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
            new.SetPosition(old.GetPosition()); new.SetOrientation(old.GetOrientation())
            new.SetLocked(old.IsLocked())
            log.append(f'DEGIS {r}: {old.GetFPIDAsString()} -> {c["fp"]}')

    bb = b.GetBoardEdgesBoundingBox()
    x0 = bb.GetRight() + pcbnew.FromMM(10); x, y, rowh = x0, bb.GetTop(), 0
    for r in sorted(set(comps) - set(fps), key=natural):
        if not comps[r]['fp']:
            continue
        fp = pre[comps[r]['fp']].pop(); fp.SetReference(r); b.Add(fp)
        box = fp.GetBoundingBox(False)
        w, h = box.GetWidth() + pcbnew.FromMM(2), box.GetHeight() + pcbnew.FromMM(2)
        if x + w > x0 + pcbnew.FromMM(80):
            x, y, rowh = x0, y + rowh, 0
        fp.SetPosition(pcbnew.VECTOR2I(x + fp.GetPosition().x - box.GetLeft() + pcbnew.FromMM(1),
                                       y + fp.GetPosition().y - box.GetTop() + pcbnew.FromMM(1)))
        x += w; rowh = max(rowh, h)
        fps[r] = fp; log.append(f'EKLE  {r}: {comps[r]["fp"]}')

    netinfo = {}
    for name in (n for n, nodes in nets.items() if any(r in fps for r, _ in nodes)):
        ni = b.FindNet(name)
        if ni is None:
            ni = pcbnew.NETINFO_ITEM(b, name); b.Add(ni)
        netinfo[name] = ni
    padnet = {rp: n for n, nodes in nets.items() for rp in nodes}

    for r, c in comps.items():
        fp = fps.get(r)
        if fp is None:
            continue
        fp.SetValue(c['value'])
        fp.SetPath(pcbnew.KIID_PATH(c['sheettst'] + c['tstamp']))
        fp.SetSheetname(c['sheetnames']); fp.SetSheetfile(c['props'].get('Sheetfile', ''))
        fp.SetDNP('dnp' in c['props'])
        fp.SetExcludedFromBOM('exclude_from_bom' in c['props'])
        want = {k: v for k, v in c['props'].items() if k not in SKIP_PROPS}
        fp.GetField(pcbnew.FIELD_T_DATASHEET).SetText(c['datasheet'])
        fp.GetField(pcbnew.FIELD_T_DESCRIPTION).SetText(c['description'])
        for f in list(fp.GetFields()):
            if not f.IsMandatory() and f.GetName() not in want:
                fp.Remove(f); keep.append(f)
        fab = pcbnew.F_Fab if fp.GetLayer() == pcbnew.F_Cu else pcbnew.B_Fab
        for k, v in want.items():
            if fp.HasField(k):
                fp.GetField(k).SetText(v)
            else:
                f = pcbnew.PCB_FIELD(fp, pcbnew.FIELD_T_USER, k)
                f.SetText(v); f.SetVisible(False); f.SetLayer(fab); f.SetPosition(fp.GetPosition())
                fp.Add(f)
        for pad in fp.Pads():
            n = padnet.get((r, pad.GetNumber()))
            pad.SetNet(netinfo[n] if n in netinfo else b.GetNetInfo().OrphanedItem())

    if not a.keep_tracks:
        for t in list(b.GetTracks()):
            log.append(f'IZ SIL {t.GetNetname()} {pcbnew.ToMM(t.GetStart())}-{pcbnew.ToMM(t.GetEnd())}')
            keep.append(t); b.Remove(t)

    used = {p.GetNetname() for fp in b.GetFootprints() for p in fp.Pads()}
    used |= {t.GetNetname() for t in b.GetTracks()} | {z.GetNetname() for z in b.Zones()}
    for ni in list(b.GetNetInfo().NetsByName().values()):
        if ni.GetNetCode() > 0 and ni.GetNetname() not in used:
            b.Remove(ni); log.append(f'NET SIL {ni.GetNetname()}')

    print('\n'.join(log))
    if not a.dry_run:
        pcbnew.SaveBoard(pcb, b)


if __name__ == '__main__':
    main()
