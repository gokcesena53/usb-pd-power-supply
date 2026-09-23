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

__all__ = ['block_at', 'children', 'f', 'uid', 'lib_pins', 'lib_body', 'xf', 'sym',
           'power', 'wire', 'wires', 'no_connect', 'label', 'junction', 'rect', 'text',
           'insert', 'ensure_lib_symbol', 'lib_symbol_source', 'next_power_ref',
           'sheet_path', 'text_width', 'text_box']


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


def text_box(s, x, y, rot=0, just='left', size=1.27, extra=0.0):
    """Metnin kapladigi kutu: (x0, y0, x1, y1) mm. Cakisma denetimi icin.

    rot EKRANDAKI aci olmali (sembol alanlarinda bkz. kisch_edit.field_boxes;
    property acisi sembole GORELIDIR). KiCad 180'i okunur yone cevirir ama
    metin yine cipadan ters yone uzar, bu yuzden 180 ayri ele alinir.

    just: ekrandaki hizalama. 'left' cipadan saga, 'right' cipadan sola,
    digerleri (None/'center') ortali.
    extra: govdeli ogelerde (global etiket ok ucu) eklenecek pay, ~3 mm.
    """
    w = text_width(s, size) + extra
    h = size * 1.1
    lo, hi = (0.0, w) if just == 'left' else (-w, 0.0) if just == 'right' else (-w / 2, w / 2)
    if rot == 0:
        return (x + lo, y - h / 2, x + hi, y + h / 2)
    if rot == 180:
        return (x - hi, y - h / 2, x - lo, y + h / 2)
    if rot == 90:                      # yazi yukari dogru uzar
        return (x - h / 2, y - hi, x + h / 2, y - lo)
    if rot == 270:
        return (x - h / 2, y + lo, x + h / 2, y + hi)
    raise ValueError(f'gecersiz aci: {rot}')


def boxes_overlap(a, b, pad=0.2):
    """Iki kutu gorsel olarak bindiriyor mu. pad kadar temas sorun sayilmaz."""
    return (a[0] < b[2] - pad and b[0] < a[2] - pad and
            a[1] < b[3] - pad and b[1] < a[3] - pad)


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


def lib_body(sheet, lib_id):
    """Sembolun CIZIM ogelerinin kutuphane koordinatindaki kutusu (pinler haric).

    Metnin bir sembolun govdesine binip binmedigini anlamak icin. Donus
    (x0, y0, x1, y1) veya sembolde cizim yoksa None. Kutuphane Y ekseni ters
    oldugu icin sema koordinatina cevirirken xf kullanilir (bkz. kisch_edit.sym_body).
    """
    try:
        a, b = block_at(sheet, sheet.index(f'(symbol "{lib_id}"'))
    except ValueError:
        return None
    src = sheet[a:b]
    xs, ys = [], []
    for m in re.finditer(r'\((?:start|end|mid|xy) (-?[\d.]+) (-?[\d.]+)\)', src):
        xs.append(float(m.group(1)))
        ys.append(float(m.group(2)))
    for m in re.finditer(r'\(center (-?[\d.]+) (-?[\d.]+)\)\s*\n\s*\(radius ([\d.]+)\)', src):
        cx, cy, r = float(m.group(1)), float(m.group(2)), float(m.group(3))
        xs += [cx - r, cx + r]
        ys += [cy - r, cy + r]
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


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
        hide_ref=False, hide_val=False, prop_rot=0, extra=(), dnp=False):
    """Sembol ornegi yerlestirir.

    dnp               : True -> (dnp yes); KiCad sembolun ustune kirmizi carpi
                        cizer, BOM'da DNP isaretlenir (opsiyonel TVS D8/D9).

    ref_off / val_off : referans ve deger metninin sembol merkezine gore ofseti.
                        Buyuk IC'lerde govdenin disina cikacak sekilde verin.
    hide_ref          : guc sembollerinde True (#PWR### gorunmemeli).
    hide_val          : GND gibi grafigi kendini anlatan sembollerde True.
    prop_rot          : dondurulmus sembollerde metin de doner; 90/270 ile geri alin.
    """
    s = (f'\t(symbol\n\t\t(lib_id "{lib_id}")\n\t\t(at {f(x)} {f(y)} {ang})\n'
         '\t\t(unit 1)\n\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n'
         '\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n'
         f'\t\t(dnp {"yes" if dnp else "no"})\n\t\t(fields_autoplaced no)\n\t\t(uuid "{uid()}")\n')
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


def children(blk):
    """Blogun dogrudan alt s-expression'lari: [(bas, son)] (blok icindeki indis)."""
    out, depth, in_str, j = [], 0, False, 0
    start = None
    while j < len(blk):
        c = blk[j]
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
            if depth == 2:
                start = j
        elif c == ')':
            if depth == 2:
                out.append((start, j + 1))
            depth -= 1
        j += 1
    return out


def lib_symbol_source(lib, name):
    """Kutuphane metnindeki sembol tanimi; `extends` ile turuyorsa BAGIMSIZ hali.

    KiCad'in bazi sembolleri govdeyi baskasindan alir (USBLC6-2SC6 ->
    USBLC6-2P6, SMAJ30A -> SM6T6V8A). Sayfa onbellegine extends'li tanim
    kopyalanirsa KiCad kutuphaneyi yukleyemez. Burada ebeveynin govdesi ve
    pinleri alinir, alt alt semboller (`Ebeveyn_0_1`) yeniden adlandirilir,
    alanlar (property) cocugunkiyle degistirilir.
    """
    a, b = block_at(lib, lib.index(f'(symbol "{name}"'))
    body = lib[a:b]
    m = re.search(r'\(extends "([^"]+)"\)', body)
    if not m:
        return body
    parent = m.group(1)
    pa = lib_symbol_source(lib, parent)
    pa = pa.replace(f'(symbol "{parent}"', f'(symbol "{name}"', 1)
    pa = re.sub(r'\(symbol "%s_(\d+_\d+)"' % re.escape(parent),
                lambda mm: f'(symbol "{name}_{mm.group(1)}"', pa)
    cprops = [body[x:y] for x, y in children(body) if body.startswith('(property', x)]
    spans = [(x, y) for x, y in children(pa) if pa.startswith('(property', x)]
    ind = re.search(r'\n(\t*)\(property', pa).group(1)
    return pa[:spans[0][0]] + ('\n' + ind).join(cprops) + pa[spans[-1][1]:]


def ensure_lib_symbol(sheet, lib_path, sym_name, lib_nick):
    """Harici kutuphanedeki sembol tanimini sayfanin lib_symbols onbellegine kopyalar.

    `extends` ile turetilmis semboller lib_symbol_source ile bagimsizlastirilir.
    DIKKAT: sym()/power() onbellege EKLEMEZ. Onbellekte olmayan lib_id'li sembol
    ERC'de hata vermez; power:+3.3V boyle eklendiginde pin netlist'te sessizce
    ayri bir nete dustu ("Net-(U10-VBUS)"; ERC yalniz pin_to_pin "Pin 1 [???]").
    Yeni sembol urettikten sonra kisch_edit.ensure_used_lib_symbols cagir.
    """
    full = f'{lib_nick}:{sym_name}'
    if f'(symbol "{full}"' in sheet:
        return sheet
    lib = open(lib_path, encoding='utf-8').read()
    body = lib_symbol_source(lib, sym_name)
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
