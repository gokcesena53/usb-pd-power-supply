"""KiCad 10 sematik uretim yardimcilari.

S-expression seviyesinde sembol yerlestirme, tel cizme, etiketleme.
Tum koordinatlar milimetre. KiCad izgarasi 1.27 mm'nin katlaridir.

Kullanim:
    import sys; sys.path.insert(0, '.claude/skills/kicad-schematic/scripts')
    import kisch as K
    t = open('sheet.kicad_sch').read()
    t = K.ensure_lib_symbol(t, 'libs/My.kicad_sym', 'MYPART', 'My')
    pins = K.lib_pins(t, 'My:MYPART')
    p = K.xf((100, 100), 0, pins['1'])      # pin 1'in mutlak konumu
"""
import re
import uuid

__all__ = ['block_at', 'f', 'uid', 'lib_pins', 'xf', 'sym', 'power', 'wire',
           'wires', 'no_connect', 'label', 'junction', 'rect', 'text', 'insert',
           'ensure_lib_symbol', 'next_power_ref', 'sheet_path', 'text_width']


# ---------------------------------------------------------------- temel

def block_at(text, i):
    """i konumundaki '(' ile baslayan dengeli s-expression'in (bas, son) indisi."""
    depth = 0
    in_str = False
    j = i
    while j < len(text):
        c = text[j]
        if in_str:
            if c == '\\':
                j += 2
                continue
            if c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    raise ValueError('dengesiz parantez')


def f(v):
    """KiCad'in yazdigi gibi sayi bicimle: gereksiz sifirlar atilir."""
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    return s if s else '0'


def uid():
    return str(uuid.uuid4())


def text_width(s, size=1.27):
    """Metnin yaklasik genisligi (mm), carpisma hesabi icin (hafif fazla tahmin).

    Render'dan olculdu (1.27 mm font): "ESP32-C6-WROOM-1" 21.4 mm (~1.34/karakter),
    "47uF 50V" 8.9 mm. Buyuk harf/rakam kucuk harften belirgin genis; tek bir
    karakter basi deger (1.11) buyuk harfli etiketlerde ~%20 eksik kalir.
    """
    w = 0.0
    for c in s:
        if c.isupper() or c.isdigit():
            w += 1.1
        elif c == ' ':
            w += 0.6
        else:
            w += 0.8
    return w * size


# ------------------------------------------------------- sembol geometrisi

def lib_pins(sheet, lib_id):
    """Sayfanin lib_symbols onbellegindeki sembolun pinleri -> {numara: (x, y)}."""
    a, b = block_at(sheet, sheet.index(f'(symbol "{lib_id}"'))
    out = {}
    pat = (r'\(pin \w+ \w+\s*\n\s*\(at (-?[\d.]+) (-?[\d.]+) (-?[\d.]+)\)'
           r'[\s\S]{0,400}?\(number "([^"]+)"')
    for m in re.finditer(pat, sheet[a:b]):
        out[m.group(4)] = (float(m.group(1)), float(m.group(2)))
    return out


def xf(inst, ang, p, mirror=None):
    """Kutuphane pin koordinatini sema koordinatina cevirir.

    KiCad'de kutuphane Y ekseni terstir. Donusumler bu projede U6 (TL431,
    aci 90) ve D2 (D_Schottky, aci 270) uzerinden ampirik dogrulanmistir.

    mirror: KiCad'in (mirror x|y) alani. Ayna DONMEDEN SONRA, sema ekseninde
    uygulanir: 'y' -> yatay cevirme (dx = -dx), 'x' -> dikey cevirme (dy = -dy).
    Q_NMOS_GSD aci 90 + mirror y ile ampirik dogrulandi (REV_C Blok B, Q6).
    Kutuphane koordinatinda cevirip sonra dondurmek 90/270'te YANLIS sonuc verir.
    """
    x, y = inst
    px, py = p
    if ang == 0:
        dx, dy = px, -py
    elif ang == 90:
        dx, dy = -py, -px
    elif ang == 180:
        dx, dy = -px, py
    elif ang == 270:
        dx, dy = py, px
    else:
        raise ValueError(f'gecersiz aci: {ang}')
    if mirror == 'y':
        dx = -dx
    elif mirror == 'x':
        dy = -dy
    return (round(x + dx, 4), round(y + dy, 4))


# ------------------------------------------------------------- ogeler

def _prop(name, val, x, y, hide=False, just=None, rot=0):
    return (f'\t\t(property "{name}" "{val}"\n\t\t\t(at {f(x)} {f(y)} {rot})\n'
            + ('\t\t\t(hide yes)\n' if hide else '')
            + '\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n'
              '\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n'
            + (f'\t\t\t\t(justify {just})\n' if just else '')
            + '\t\t\t)\n\t\t)\n')


def sym(lib_id, ref, value, x, y, path, npins, fp=None, ang=0,
        ref_off=(2.54, -2.54), val_off=(2.54, 2.54),
        hide_ref=False, hide_val=False, prop_rot=0, extra=()):
    """Sembol ornegi yerlestirir.

    ref_off / val_off : referans ve deger metninin sembol merkezine gore ofseti.
                        Buyuk IC'lerde govdenin disina cikacak sekilde verin.
    hide_ref          : guc sembollerinde True (#PWR### gorunmemeli).
    hide_val          : GND gibi grafigi kendini anlatan sembollerde True.
    prop_rot          : dondurulmus sembollerde metin de doner; 90/270 ile geri alin.
    """
    s = (f'\t(symbol\n\t\t(lib_id "{lib_id}")\n\t\t(at {f(x)} {f(y)} {ang})\n'
         '\t\t(unit 1)\n\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n'
         '\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n'
         f'\t\t(dnp no)\n\t\t(fields_autoplaced no)\n\t\t(uuid "{uid()}")\n')
    s += _prop('Reference', ref, x + ref_off[0], y + ref_off[1],
               hide=hide_ref, just='left', rot=prop_rot)
    s += _prop('Value', value, x + val_off[0], y + val_off[1],
               hide=hide_val, just='left', rot=prop_rot)
    s += _prop('Footprint', fp if fp is not None else '', x, y, hide=True)
    s += _prop('Datasheet', '~', x, y, hide=True)
    for n, v in extra:
        s += _prop(n, v, x, y, hide=True)
    for i in range(1, npins + 1):
        s += f'\t\t(pin "{i}"\n\t\t\t(uuid "{uid()}")\n\t\t)\n'
    s += (f'\t\t(instances\n\t\t\t(project "gopo"\n\t\t\t\t(path "{path}"\n'
          f'\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n'
          '\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')
    return s


def power(kind, ref, x, y, path, val_off=(1.78, -1.65)):
    """GND / +3.3V gibi guc sembolu. GND asagi, pozitif raylar yukari bakar.

    kind: 'GND', '+3.3V', 'PWR_FLAG' ...  (power: kutuphanesindeki sembol adi)
    Referans daima gizli; deger GND ve PWR_FLAG disinda gorunur.
    """
    hide_val = kind in ('GND', 'PWR_FLAG')
    return sym(f'power:{kind}', ref, kind, x, y, path, 1,
               hide_ref=True, hide_val=hide_val, val_off=val_off)


def wire(p1, p2, rgb=None):
    """Tel. rgb verilirse net renklendirilir (ilgili netleri ayirmak icin)."""
    col = f'\n\t\t\t(color {rgb[0]} {rgb[1]} {rgb[2]} 1)' if rgb else ''
    return (f'\t(wire\n\t\t(pts\n\t\t\t(xy {f(p1[0])} {f(p1[1])}) '
            f'(xy {f(p2[0])} {f(p2[1])})\n\t\t)\n'
            f'\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default){col}\n\t\t)\n'
            f'\t\t(uuid "{uid()}")\n\t)\n')


def label(txt, x, y, rot=0, glob=False, just=None, shape='passive'):
    """Etiket. DIKKAT: tam olarak bir telin uzerinde olmali, yaninda degil.

    0.64 mm kayma bile ERC'de label_dangling verir.

    Global etiket yonu: baglanti noktasi (x, y)'dir ve govde oradan uzar.
      rot=0   -> govde SAGA uzar: telin SAG ucunda kullan (ray sonu, SW_OUT)
      rot=180 -> govde SOLA uzar: telin SOL ucunda kullan (ray basi, PD_VOUT)
    Yanlis yon secilirse tel etiketin govdesinin altindan gecer (ERC temiz,
    cizim bozuk).
    """
    if just is None:
        just = 'right' if rot == 180 else 'left'
    if glob:
        return (f'\t(global_label "{txt}"\n\t\t(shape {shape})\n'
                f'\t\t(at {f(x)} {f(y)} {rot})\n\t\t(fields_autoplaced yes)\n'
                f'\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n'
                f'\t\t\t(justify {just})\n\t\t)\n\t\t(uuid "{uid()}")\n'
                f'\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"\n'
                f'\t\t\t(at {f(x)} {f(y)} 0)\n\t\t\t(hide yes)\n\t\t\t(show_name no)\n'
                f'\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n'
                f'\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify {just})\n'
                f'\t\t\t)\n\t\t)\n\t)\n')
    return (f'\t(label "{txt}"\n\t\t(at {f(x)} {f(y)} {rot})\n'
            f'\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n'
            f'\t\t\t(justify {just} bottom)\n\t\t)\n\t\t(uuid "{uid()}")\n\t)\n')


def wires(pts, rgb=None):
    """Kirik cizgi: ardisik noktalar arasina tel. [(x0,y0), (x1,y0), (x1,y1)]"""
    return ''.join(wire(pts[i], pts[i + 1], rgb) for i in range(len(pts) - 1))


def no_connect(x, y):
    """Bos pin isareti (x). Pinin tam ucuna konur."""
    return f'\t(no_connect\n\t\t(at {f(x)} {f(y)})\n\t\t(uuid "{uid()}")\n\t)\n'


def junction(x, y):
    """Uc veya daha fazla telin bulustugu noktaya gerekir."""
    return (f'\t(junction\n\t\t(at {f(x)} {f(y)})\n\t\t(diameter 0)\n'
            f'\t\t(color 0 0 0 0)\n\t\t(uuid "{uid()}")\n\t)\n')


def rect(x1, y1, x2, y2, rgb=(72, 120, 180)):
    """Alt devreyi cerceveleyen kesikli dikdortgen."""
    r, g, b = rgb
    return (f'\t(rectangle\n\t\t(start {f(x1)} {f(y1)})\n\t\t(end {f(x2)} {f(y2)})\n'
            f'\t\t(stroke\n\t\t\t(width 0.254)\n\t\t\t(type dash)\n'
            f'\t\t\t(color {r} {g} {b} 1)\n\t\t)\n'
            f'\t\t(fill\n\t\t\t(type none)\n\t\t)\n\t\t(uuid "{uid()}")\n\t)\n')


def text(s, x, y, size=2.0, rgb=(72, 120, 180), bold=True):
    """Serbest metin (blok basligi, tasarim notu)."""
    r, g, b = rgb
    return (f'\t(text "{s}"\n\t\t(exclude_from_sim no)\n\t\t(at {f(x)} {f(y)} 0)\n'
            f'\t\t(effects\n\t\t\t(font\n\t\t\t\t(size {f(size)} {f(size)})\n'
            + ('\t\t\t\t(bold yes)\n' if bold else '')
            + f'\t\t\t\t(color {r} {g} {b} 1)\n\t\t\t)\n'
              f'\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "{uid()}")\n\t)\n')


# ------------------------------------------------------------- sayfa islemleri

def insert(sheet, chunk):
    """Uretilen ogeleri sayfanin en dis kapanis parantezinden once ekler."""
    i = sheet.rindex('\n)')
    return sheet[:i + 1] + chunk + sheet[i + 1:]


def ensure_lib_symbol(sheet, lib_path, sym_name, lib_nick):
    """Harici kutuphanedeki sembol tanimini sayfanin lib_symbols onbellegine kopyalar.

    Sembol baska bir sembolden turuyorsa (extends) once bagimsiz hale getirin,
    aksi halde KiCad kutuphaneyi yukleyemez.
    """
    full = f'{lib_nick}:{sym_name}'
    if f'(symbol "{full}"' in sheet:
        return sheet
    lib = open(lib_path, encoding='utf-8').read()
    a, b = block_at(lib, lib.index(f'(symbol "{sym_name}"'))
    body = lib[a:b]
    if '(extends' in body:
        raise ValueError(f'{sym_name} baska sembolden turuyor, once bagimsizlastirin')
    body = body.replace(f'(symbol "{sym_name}"', f'(symbol "{full}"', 1)
    body = '\n'.join(('\t' + l if l.strip() else l) for l in body.split('\n'))
    i = sheet.index('(lib_symbols')
    _, lb = block_at(sheet, i)
    return sheet[:lb - 1] + body + '\n\t' + sheet[lb - 1:]


def next_power_ref(sheet_glob='*.kicad_sch'):
    """Kullanilmayan ilk #PWR/#FLG numarasi (ikisi ayni sayaci paylasir).
    Tekrarli referans annotation hatasi verir."""
    import glob
    used = set()
    for path in glob.glob(sheet_glob):
        used.update(int(x) for x in re.findall(r'"#(?:PWR|FLG)(\d+)"',
                                               open(path, encoding='utf-8').read()))
    return max(used, default=0) + 1


def sheet_path(sheet, root_uuid):
    """Sembol ornekleri icin hiyerarsik yol: /<kok-uuid>/<sayfa-uuid>."""
    m = re.search(r'\(path "/%s/([0-9a-f-]+)"' % re.escape(root_uuid), sheet)
    if not m:
        raise ValueError('sayfa yolu bulunamadi')
    return f'/{root_uuid}/{m.group(1)}'
