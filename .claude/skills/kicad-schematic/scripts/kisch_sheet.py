"""Sayfalar arasi islemler: blok tasima ve bos sayfa kaldirma.

Bir blogu baska sayfaya tasirken sembolun yalniz koordinati degil, ORNEK YOLU
(instances/path) da hedef sayfaninkiyle degismelidir; yoksa referans/annotation
bozulur. Eksik lib_symbols da kopyalanmalidir. move_block ikisini de yapar.

Kullanim (hardware/ dizininde):
    import sys; sys.path.insert(0, '../.claude/skills/kicad-schematic/scripts')
    import kisch_sheet as S
    # kaynak sayfadaki cerceveyi kapsayan kutu -> hedef sayfada (dx, dy) otelenmis
    S.move_block('powergeneration.kicad_sch', 'usb_pd_controller.kicad_sch',
                 (17, 33, 166, 122), dx=0, dy=200)
    # blok bosaldiktan sonra sayfayi ve sayfa sembolunu kaldir
    S.remove_sheet('powergeneration.kicad_sch', 'gopo.kicad_sch', 'gopo.kicad_pro')

DIKKAT: (dx, dy) 1.27'nin katı olmali. Gecici "park" icin bile: 200 mm otelersen
tum blok izgara disina kayar ve ERC 'endpoint_off_grid' yagar. Park etmen
gerekiyorsa 190.5 (150 x 1.27) gibi bir deger sec.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kisch as K  # noqa: E402
import kisch_edit as E  # noqa: E402
from kisch import f  # noqa: E402
from kicadtools import read_sheet, write_sheet  # noqa: E402

GRID = 1.27


def _on_grid(v):
    return abs(v / GRID - round(v / GRID)) < 1e-6


def shift_text(blk, dx, dy):
    """Bir ogenin metnindeki tum koordinatlari oteler (at / xy / start / end)."""
    def sh(m):
        return f'{m.group(1)}{f(float(m.group(2)) + dx)} {f(float(m.group(3)) + dy)}'
    return re.sub(r'(\((?:at|xy|start|end) )([-\d.]+) ([-\d.]+)', sh, blk)


def ensure_lib_symbol_from(dst, src, lib_id):
    """Hedef sayfanin lib_symbols onbellegine kaynaktaki sembol tanimini kopyalar."""
    if f'(symbol "{lib_id}"' in dst:
        return dst
    a, b = K.block_at(src, src.index(f'(symbol "{lib_id}"'))
    i = dst.index('(lib_symbols')
    _, lb = K.block_at(dst, i)
    return dst[:lb - 1] + src[a:b] + '\n\t' + dst[lb - 1:]


def move_block(src_fn, dst_fn, box, dx=0.0, dy=0.0, skip_refs=()):
    """Kaynak sayfadaki kutuda kalan TUM ogeleri hedef sayfaya tasir.

    Semboller + teller + etiketler + junction + no_connect + metin + cerceve
    birlikte gider; cizim bozulmaz. Sembollerde instances/path hedef sayfaninki
    ile degistirilir, eksik lib_symbols kopyalanir.

    box       : kaynak sayfadaki (x0, y0, x1, y1); cerceveyi ve etiket govdelerini
                kapsayacak kadar genis tut (etiket govdesi capa noktasinin
                disinda kalir, ama capa kutuda olmalidir).
    skip_refs : tasinmayacak sembol referanslari (ör. blokta kalacak konnektor).
    Donus     : tasinan sembol referanslari.

    Alt sayfa sembolleri (sheet) tasinmaz - onlari ayrica ele al.
    """
    assert _on_grid(dx) and _on_grid(dy), f'(dx, dy) 1.27 katı olmalı: {(dx, dy)}'
    st, scrlf = read_sheet(src_fn)
    dt, dcrlf = read_sheet(dst_fn)
    spath, dpath = E.path_of(st), E.path_of(dt)
    cut, add, moved = [], [], []
    for a, b, kind, blk in E.items(st):
        if not any(E.inside(p, box) for p in E.pos(kind, blk)):
            continue
        if kind == 'symbol':
            ref = E.ref_of(blk)
            if ref in skip_refs:
                continue
            lib = re.search(r'lib_id "([^"]+)"', blk).group(1)
            dt = ensure_lib_symbol_from(dt, st, lib)
            blk = blk.replace(f'(path "{spath}"', f'(path "{dpath}"')
            moved.append(ref)
        cut.append((a, b))
        add.append(shift_text(blk, dx, dy))
    for a, b in sorted(cut, reverse=True):
        st = st[:st.rindex('\n', 0, a)] + st[b:]
    dt = K.insert(dt, ''.join('\t' + x + '\n' for x in add))
    write_sheet(src_fn, st, scrlf)
    write_sheet(dst_fn, dt, dcrlf)
    return moved


def sheet_block(parent_text, child_fn):
    """Ust sayfadaki (sheet ...) blogunun (bas, son, uuid) degerleri."""
    for m in re.finditer(r'\n\t\(sheet\n', parent_text):
        a, b = K.block_at(parent_text, m.start() + 1)
        if f'"{child_fn}"' in parent_text[a:b]:
            return a, b, re.search(r'\(uuid "([0-9a-f-]+)"', parent_text[a:b]).group(1)
    return None


def is_empty(sheet_fn):
    """Sayfada cizim var mi? (lib_symbols ve alt sayfa sembolleri sayilmaz)"""
    t, _ = read_sheet(sheet_fn)
    return not E.items(t)


def remove_sheet(child_fn, parent_fn, project_fn=None, force=False):
    """Bos sayfayi siler: dosya + ust sayfadaki sembol + .kicad_pro kaydi.

    force=False iken sayfa bos degilse hata verir (icerik kaybini onler).
    Sayfa numaralari KiCad tarafindan yeniden atanir; render.py --list ile
    sayfa sirasini yeniden oku.
    """
    if not force and not is_empty(child_fn):
        raise ValueError(f'{child_fn} bos degil; once icerigini tasi')
    t, crlf = read_sheet(parent_fn)
    hit = sheet_block(t, child_fn)
    if not hit:
        raise KeyError(f'{child_fn} sayfa sembolu {parent_fn} icinde yok')
    a, b, uuid = hit
    write_sheet(parent_fn, t[:t.rindex('\n', 0, a)] + t[b:], crlf)
    os.remove(child_fn)
    if project_fn:
        pro = open(project_fn, encoding='utf-8').read()
        pro = re.sub(r'\s*\[\s*"%s",\s*"[^"]*"\s*\],?' % uuid, '', pro)
        pro = re.sub(r',(\s*\])', r'\1', pro)
        json.loads(pro)          # bozulmadigini dogrula
        open(project_fn, 'w', encoding='utf-8').write(pro)
    return uuid


def set_paper(sheet_fn, size):
    """Sayfa boyutunu degistirir ('A4', 'A3', 'A2'...). Donus: eski boyut."""
    t, crlf = read_sheet(sheet_fn)
    m = re.search(r'\(paper "([^"]+)"\)', t)
    old = m.group(1)
    write_sheet(sheet_fn, t[:m.start()] + f'(paper "{size}")' + t[m.end():], crlf)
    return old
