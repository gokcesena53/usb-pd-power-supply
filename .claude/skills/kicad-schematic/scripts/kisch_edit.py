"""Mevcut bir sayfadaki blogu yeniden yerlestirme yardimcilari (kisch.py uzerine).

Is akisi "temizle -> tasi -> yeniden tel ciz":
  1. strip_region  : bolgedeki tel/etiket/junction/no_connect/metin/cerceve ve
                     GUC sembollerini siler; #PWR/#FLG referanslarini geri verir.
                     Normal semboller (R, C, U...) SILINMEZ.
  2. place         : mevcut sembolu tasir. uuid, footprint, MPN, instance korunur;
                     sembolu silip yeniden olusturmaktan her zaman iyidir.
  3. sym_pin       : tasinmis sembolun pin konumunu okur (ayna destekli).
  4. kisch.wire/label/power ile yeniden ciz, Pool ile #PWR'leri geri kullan.
  5. lint          : kesisen teller, eksik junction, cakisan teller.

Ornek (hardware/ dizininde):
    import sys; sys.path.insert(0, '../.claude/skills/kicad-schematic/scripts')
    import kisch as K, kisch_edit as E
    from kicadtools import read_sheet, write_sheet
    t, crlf = read_sheet('poweroutput.kicad_sch')
    path = E.path_of(t)
    t, freed = E.strip_region(t, (174, 36, 356, 125))
    pool = E.Pool(freed, K.next_power_ref())
    t = E.place(t, 'Q6', 294.64, 60.96, ang=90, mirror='y',
                ref_at=(-5.08, -10.16), val_at=(-5.08, -7.62))
    g = K.wire(E.sym_pin(t, 'Q6', '2'), (284.48, 58.42))
    g += K.power('GND', pool.pwr(), 289.56, 88.9, path)
    t = K.insert(t, g)
    print(E.lint(t, (174, 36, 356, 125)))
    write_sheet('poweroutput.kicad_sch', t, crlf)

Betik tekrar calistirilabilir olmali: strip_region yeni cizimi de siler, place
mutlak konum yazar. Bolge disina tasinan ogeler icin tek-seferlik korumayi
(or. "eski konum hala dosyada mi?") kendin koy.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kisch as K  # noqa: E402
from kisch import f  # noqa: E402
from kicadtools import read_sheet, write_sheet  # noqa: E402

KINDS = ('symbol', 'wire', 'label', 'global_label', 'hierarchical_label',
         'junction', 'no_connect', 'text', 'rectangle')


# ------------------------------------------------------------- okuma

def items(t):
    """Ust seviye ogeler: [(bas, son, tur, blok)] (lib_symbols haric)."""
    _, le = K.block_at(t, t.index('(lib_symbols'))
    out, i = [], le
    pat = re.compile(r'\n\t\((%s)\b' % '|'.join(KINDS))
    while True:
        m = pat.search(t, i)
        if not m:
            break
        a, b = K.block_at(t, m.start() + 2)
        out.append((a, b, m.group(1), t[a:b]))
        i = b
    return out


def pos(kind, blk):
    if kind == 'wire':
        return [tuple(map(float, p)) for p in
                re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)', blk)]
    m = re.search(r'\((?:at|start) ([-\d.]+) ([-\d.]+)', blk)
    return [(float(m.group(1)), float(m.group(2)))]


def inside(p, box):
    return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]


def ref_of(blk):
    m = re.search(r'property "Reference" "([^"]+)"', blk)
    return m.group(1) if m else None


def path_of(t):
    """Sayfadaki sembol orneklerinin hiyerarsik yolu (yeni guc sembolleri icin)."""
    return re.search(r'\(path "(/[0-9a-f-]+/[0-9a-f-]+)"', t).group(1)


def dump(t, box):
    """Bolgedeki ogeleri insan-okur listeler (yeniden yerlesim oncesi envanter)."""
    lines = []
    for _, _, kind, blk in items(t):
        ps = pos(kind, blk)
        if not any(inside(p, box) for p in ps):
            continue
        if kind == 'symbol':
            lib = re.search(r'lib_id "([^"]+)"', blk).group(1)
            at = re.search(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)', blk).groups()
            val = re.search(r'property "Value" "([^"]*)"', blk).group(1)
            mir = re.search(r'\(mirror (\w)\)', blk)
            lines.append(f'SYM {ref_of(blk)} {lib} "{val}" at={at}'
                         + (f' mirror={mir.group(1)}' if mir else ''))
        elif kind == 'wire':
            col = re.search(r'color (\d+ \d+ \d+)', blk)
            lines.append(f'WIRE {ps}' + (f' rgb={col.group(1)}' if col else ''))
        else:
            nm = re.search(r'\(\w+ "([^"]*)"', blk)
            lines.append(f'{kind.upper()} {nm.group(1) if nm else ""} {ps[0]}')
    return '\n'.join(lines)


# ------------------------------------------------------------- degistirme

def strip_region(t, box):
    """Bolgedeki cizimi ve guc sembollerini siler.
    Donus: (yeni metin, serbest kalan #PWR/#FLG referanslari)."""
    freed, cut = [], []
    for a, b, kind, blk in items(t):
        if not any(inside(p, box) for p in pos(kind, blk)):
            continue
        if kind == 'symbol':
            r = ref_of(blk)
            if r and r.startswith('#'):
                freed.append(r)
                cut.append((a, b))
            continue
        cut.append((a, b))
    for a, b in sorted(cut, reverse=True):
        a2 = t.rindex('\n', 0, a)
        t = t[:a2] + t[b:]
    return t, freed


def translate_region(t, box, dx, dy=0):
    """Bolgedeki TUM ogeleri (semboller ve alanlari dahil) oteler.
    Blok cercevesine tasan komsu gruplari kenara cekmek icin."""
    edits = []
    for a, b, kind, blk in items(t):
        if not any(inside(p, box) for p in pos(kind, blk)):
            continue

        def sh(m):
            return f'{m.group(1)}{f(float(m.group(2)) + dx)} {f(float(m.group(3)) + dy)}'
        edits.append((a, b, re.sub(r'(\((?:at|xy|start|end) )([-\d.]+) ([-\d.]+)', sh, blk)))
    for a, b, nb in sorted(edits, reverse=True):
        t = t[:a] + nb + t[b:]
    return t


def _sym_span(t, ref):
    for a, b, kind, blk in items(t):
        if kind == 'symbol' and ref_of(blk) == ref:
            return a, b, blk
    raise KeyError(ref)


def _set_prop(blk, name, x, y, rot=0, just='left', hide=False):
    a, b = K.block_at(blk, blk.index(f'(property "{name}"'))
    p = blk[a:b]
    p = re.sub(r'\(at [-\d.]+ [-\d.]+ [-\d.]+\)', f'(at {f(x)} {f(y)} {rot})', p, count=1)
    p = re.sub(r'\n\t\t\t\(hide yes\)', '', p)
    if hide:
        p = p.replace('\n\t\t\t(show_name', '\n\t\t\t(hide yes)\n\t\t\t(show_name', 1)
    p = re.sub(r'\n\t\t\t\t\(justify [^)]*\)', '', p)
    if just:
        p = re.sub(r'(\n\t\t\t\t\(font\n\t\t\t\t\t\(size [^)]*\)\n'
                   r'(?:\t\t\t\t\t\(bold yes\)\n)?\t\t\t\t\))',
                   r'\1' + f'\n\t\t\t\t(justify {just})', p, count=1)
    return blk[:a] + p + blk[b:]


def place(t, ref, x, y, ang=0, mirror=None, ref_at=None, val_at=None,
          just='left', prop_rot=None, hide_val=False):
    """Mevcut sembolu (x, y, ang, mirror) konumuna tasir.

    ref_at / val_at : sembol merkezine gore (dx, dy) veya (dx, dy, justify).
                      justify None -> ortali (sembolun ustune ortali yazi).
    prop_rot        : verilmezse 90/270'te 90 (metin yatay kalir).
    Gizli alanlar (Footprint, Datasheet...) sembolle birlikte tasinir.
    """
    a, b, blk = _sym_span(t, ref)
    blk = re.sub(r'\(at [-\d.]+ [-\d.]+ [-\d.]+\)', f'(at {f(x)} {f(y)} {ang})', blk, count=1)
    blk = re.sub(r'\n\t\t\(mirror \w\)', '', blk)
    if mirror:
        blk = blk.replace('\n\t\t(unit ', f'\n\t\t(mirror {mirror})\n\t\t(unit ', 1)
    pr = prop_rot if prop_rot is not None else (90 if ang in (90, 270) else 0)
    for name, o in (('Reference', ref_at), ('Value', val_at)):
        if o is None:
            continue
        j = o[2] if len(o) > 2 else just
        blk = _set_prop(blk, name, x + o[0], y + o[1], pr, j,
                        hide=(hide_val and name == 'Value'))
    for m in list(re.finditer(r'\(property "([^"]+)"', blk))[::-1]:
        if m.group(1) in ('Reference', 'Value'):
            continue
        pa, pb = K.block_at(blk, m.start())
        p = re.sub(r'\(at [-\d.]+ [-\d.]+ ([-\d.]+)\)',
                   lambda mm: f'(at {f(x)} {f(y)} {mm.group(1)})', blk[pa:pb], count=1)
        blk = blk[:pa] + p + blk[pb:]
    return t[:a] + blk + t[b:]


def sym_pin(t, ref, num):
    """Yerlestirilmis sembolun pininin mutlak konumu (aci + ayna)."""
    _, _, blk = _sym_span(t, ref)
    lib = re.search(r'lib_id "([^"]+)"', blk).group(1)
    x, y, ang = map(float, re.search(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)', blk).groups())
    m = re.search(r'\(mirror (\w)\)', blk)
    return K.xf((x, y), int(ang), K.lib_pins(t, lib)[num], m.group(1) if m else None)


class Pool:
    """Silinen #PWR/#FLG referanslarini yeniden kullanir; yetmezse yenisini verir.
    Referanslar korunursa diff kucuk kalir ve annotation bozulmaz."""

    def __init__(self, freed, nxt):
        self.free = sorted((r for r in freed if r.startswith('#PWR')), key=lambda r: int(r[4:]))
        self.flg = sorted((r for r in freed if r.startswith('#FLG')), key=lambda r: int(r[4:]))
        self.nxt = nxt

    def _new(self, pfx):
        self.nxt += 1
        return f'{pfx}{self.nxt - 1:03d}'

    def pwr(self):
        return self.free.pop(0) if self.free else self._new('#PWR')

    def flag(self):
        return self.flg.pop(0) if self.flg else self._new('#FLG')


# ------------------------------------------------------------- kutuphane

def edit_lib_symbol(fn, lib_path, sheet_paths, sym_name, lib_nick):
    """Sembol degisikligini .kicad_sym dosyasina VE onu kullanan her sayfanin
    lib_symbols onbellegine ayni sekilde uygular. Yalniz birine uygularsan ERC
    lib_symbol_mismatch verir.

    fn(sembol_blogu) -> yeni_blok. Sembol blogu '(symbol "AD"' ile baslar.
    Donus: degisen dosyalar.
    """
    changed = []
    for path, name in [(lib_path, sym_name)] + [(p, f'{lib_nick}:{sym_name}') for p in sheet_paths]:
        t, crlf = read_sheet(path)
        key = f'(symbol "{name}"'
        if key not in t:
            continue
        a, b = K.block_at(t, t.index(key))
        nb = fn(t[a:b])
        if nb != t[a:b]:
            write_sheet(path, t[:a] + nb + t[b:], crlf)
            changed.append(path)
    return changed


def _indent_after(blk):
    m = re.match(r'\(symbol "[^"]+"\n(\t*)', blk)
    return m.group(1) if m else '\t\t'


def hide_pin_texts(blk, numbers=True, names=True):
    """Iki pinli semboller (TVS, diyot) icin pin numarasi/adi gizle.
    A1/A2 gibi adlar govdenin ustune biner."""
    ind = _indent_after(blk)
    head = blk.index('\n') + 1
    add = ''
    if numbers and '(pin_numbers' not in blk:
        add += f'{ind}(pin_numbers\n{ind}\t(hide yes)\n{ind})\n'
    if names and '(pin_names' not in blk:
        add += f'{ind}(pin_names\n{ind}\t(offset 1.016)\n{ind}\t(hide yes)\n{ind})\n'
    return blk[:head] + add + blk[head:]


def hide_stacked_pins(blk, numbers):
    """Ayni noktaya istiflenmis pinlerden verilenleri passive + gizli yapar
    (numaralar ust uste binmesin). Bir tanesini power_in ve gorunur BIRAK.
    Gizli power_in pinleri ada gore ayri nete baglanir - asla onlari gizleme."""
    def fix(m):
        pin = m.group(0)
        num = re.search(r'\(number "([^"]+)"', pin).group(1)
        if num in numbers and 'hide yes' not in pin:
            pin = re.sub(r'\(pin power_in ', '(pin passive ', pin, count=1)
            pin = re.sub(r'(\(length [\d.]+\))(\s*)', r'\1\2(hide yes)\2', pin, count=1)
        return pin
    return re.sub(r'\(pin \w+ \w+[\s\S]*?\(number "[^"]+"', fix, blk)


# ------------------------------------------------------------- denetim

def _segs(t, box):
    out = []
    for _, _, kind, blk in items(t):
        if kind == 'wire':
            p = pos(kind, blk)
            if any(inside(q, box) for q in p):
                out.append((p[0], p[1]))
    return out


def lint(t, box, grid=1.27):
    """Bolgedeki telleri denetler. Donus: bulgu listesi (bos = temiz).

    - izgara disi koordinat
    - kesisen teller (baglanti YOK; bilincli degilse yeniden yerlestir)
    - baska telin ortasina degen uc ama junction yok
    - uc uca degil, ust uste binen teller
    - capraz tel
    """
    eps = 1e-3
    junc = {tuple(round(v, 2) for v in pos(k, b)[0])
            for _, _, k, b in items(t) if k == 'junction'}
    segs = _segs(t, box)
    out = []

    def on_grid(v):
        return abs(v / grid - round(v / grid)) < 1e-3

    def interior(s, p):
        (x0, y0), (x1, y1) = s
        if abs(x0 - x1) < eps and abs(p[0] - x0) < eps:
            return min(y0, y1) + eps < p[1] < max(y0, y1) - eps
        if abs(y0 - y1) < eps and abs(p[1] - y0) < eps:
            return min(x0, x1) + eps < p[0] < max(x0, x1) - eps
        return False

    for s in segs:
        (x0, y0), (x1, y1) = s
        if not all(on_grid(v) for v in (x0, y0, x1, y1)):
            out.append(f'izgara disi: {s}')
        if abs(x0 - x1) > eps and abs(y0 - y1) > eps:
            out.append(f'capraz tel: {s}')
    for i, a in enumerate(segs):
        for b in segs[i + 1:]:
            for s, o in ((a, b), (b, a)):
                for p in o:
                    if interior(s, p) and tuple(round(v, 2) for v in p) not in junc:
                        out.append(f'T baglanti junction yok: {p}')
            av = abs(a[0][0] - a[1][0]) < eps
            bv = abs(b[0][0] - b[1][0]) < eps
            if av != bv:
                v, h = (a, b) if av else (b, a)
                p = (v[0][0], h[0][1])
                if interior(v, p) and interior(h, p):
                    tag = 'junction VAR (iki gecen tel)' if tuple(round(x, 2) for x in p) in junc \
                        else 'baglantisiz'
                    out.append(f'kesisme {tag}: {p}')
            elif av and bv and abs(a[0][0] - b[0][0]) < eps:
                lo = max(min(a[0][1], a[1][1]), min(b[0][1], b[1][1]))
                hi = min(max(a[0][1], a[1][1]), max(b[0][1], b[1][1]))
                if hi - lo > eps:
                    out.append(f'ust uste dikey tel: x={a[0][0]} y={lo}..{hi}')
            elif not av and not bv and abs(a[0][1] - b[0][1]) < eps:
                lo = max(min(a[0][0], a[1][0]), min(b[0][0], b[1][0]))
                hi = min(max(a[0][0], a[1][0]), max(b[0][0], b[1][0]))
                if hi - lo > eps:
                    out.append(f'ust uste yatay tel: y={a[0][1]} x={lo}..{hi}')
    return sorted(set(out))
