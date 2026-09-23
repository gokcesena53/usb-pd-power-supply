"""Mevcut bir sayfadaki blogu yeniden yerlestirme yardimcilari (kisch.py uzerine).

Is akisi "envanter -> temizle -> tasi -> yeniden tel ciz -> denetle":
  0. inventory / power_symbol_nets / label_shapes : pin->net tablosu, PWR_FLAG
                     netleri, global etiket sekilleri. Temizlemeden ONCE al.
  1. strip_region  : bolgedeki tel/etiket/junction/no_connect/metin/cerceve ve
                     GUC sembollerini siler; #PWR/#FLG referanslarini geri verir.
                     Normal semboller (R, C, U...) SILINMEZ. Notlari korumak icin
                     kinds'tan 'text' cikar; kendi basliklarini remove_texts ile sil.
  2. place         : mevcut sembolu tasir. uuid, footprint, MPN, instance korunur;
                     sembolu silip yeniden olusturmaktan her zaman iyidir.
  3. pin_at        : tasinmis sembolun pinini planla karsilastirir (ayna destekli).
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

STRIP_DEFAULT = ('symbol', 'wire', 'label', 'global_label', 'junction',
                 'no_connect', 'text', 'rectangle')


def strip_region(t, box, kinds=STRIP_DEFAULT):
    """Bolgedeki cizimi ve guc sembollerini siler.
    kinds: silinecek turler. Tasarim notlarini korumak icin 'text' cikar ve
    notlari move_text ile tasi.
    Donus: (yeni metin, serbest kalan #PWR/#FLG referanslari)."""
    freed, cut = [], []
    for a, b, kind, blk in items(t):
        if kind not in kinds:
            continue
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


def translate_region(t, box, dx, dy=0, stretch=False):
    """Bolgedeki TUM ogeleri (semboller ve alanlari dahil) oteler.
    Blok cercevesine tasan komsu gruplari kenara cekmek icin.

    stretch=False (varsayilan): bir ucu kutuda olan tel BUTUNUYLE tasinir;
    kutunun disindaki ucu da kayar ve baglantisi kopar (D3'u VBUS hattinda
    saga tasirken 118 mm'lik ray boyle kopacakti).
    stretch=True: telin yalniz kutu icindeki ucu tasinir (lastik bant);
    dy=0 iken yatay teller yatay kalir. dy != 0 ise capraz tel olusabilir,
    lint 'capraz tel' raporlar."""
    edits = []

    def sh(m):
        return f'{m.group(1)}{f(float(m.group(2)) + dx)} {f(float(m.group(3)) + dy)}'

    def sh_in(m):
        p = (float(m.group(2)), float(m.group(3)))
        return sh(m) if inside(p, box) else m.group(0)
    for a, b, kind, blk in items(t):
        if not any(inside(p, box) for p in pos(kind, blk)):
            continue
        fn = sh_in if (stretch and kind == 'wire') else sh
        edits.append((a, b, re.sub(r'(\((?:at|xy|start|end) )([-\d.]+) ([-\d.]+)', fn, blk)))
    for a, b, nb in sorted(edits, reverse=True):
        t = t[:a] + nb + t[b:]
    return t


def label_shapes(t):
    """Global etiket adi -> shape (input/output/bidirectional/passive...).
    Etiketleri silip yeniden uretmeden once al; sekil yon bilgisi tasir."""
    return {m.group(1): m.group(2) for m in
            re.finditer(r'\(global_label "([^"]+)"\s*\(shape (\w+)\)', t)}


def remove_items(t, pred):
    """pred(kind, blok) -> True olan ust seviye ogeleri siler.

    Artik oge temizligi icin (tasinan blogun eski cercevesi, kopmus tel parcasi,
    yanlis yere dusmus etiket). Etiketi yalniz ADA gore secmek yetmez - ayni ad
    baska blokta da olabilir; konumu da kontrol et:
        t = E.remove_items(t, lambda k, b: k == 'global_label'
                           and b.startswith('(global_label "SW_OUT"')
                           and E.pos(k, b)[0] == (355.6, 40.64))
    """
    cut = [(a, b) for a, b, kind, blk in items(t) if pred(kind, blk)]
    for a, b in sorted(cut, reverse=True):
        t = t[:t.rindex('\n', 0, a)] + t[b:]
    return t


def remove_texts(t, contents=(), prefixes=()):
    """Serbest metinleri siler: icerigi `contents`'ten biriyle TAM eslesen veya
    `prefixes`'ten biriyle baslayanlar.

    strip_region'dan 'text' cikarildiginda (notlar korunurken) betigin urettigi
    baslik/notlari her calistirmada temizlemek icin; yoksa tekrar calistirma
    ust uste baslik birakir. Icerik DOSYADAKI haliyle karsilastirilir: satir
    sonu iki karakterlik '\\\\n' (Python'da '\\\\n' yaz, '\\n' degil).
    Notun metnini betikte degistirdiysen eski surum tam eslesmez ve sayfada
    kalir (RTC ve J3 notlari boyle ikilendi) - degisebilecek notlari
    prefixes ile sil.
    """
    def hit(kind, blk):
        if kind != 'text':
            return False
        s = re.match(r'\(text "((?:[^"\\]|\\.)*)"', blk).group(1)
        return s in contents or any(s.startswith(p) for p in prefixes)
    return remove_items(t, hit)


def move_text(t, startswith, x, y):
    """Serbest metni (tasarim notu) icerigin basina gore bulup tasir."""
    for a, b, kind, blk in items(t):
        if kind == 'text' and re.match(r'\(text "' + re.escape(startswith), blk):
            nb = re.sub(r'\(at [-\d.]+ [-\d.]+ ([-\d.]+)\)',
                        lambda m: f'(at {f(x)} {f(y)} {m.group(1)})', blk, count=1)
            return t[:a] + nb + t[b:]
    raise KeyError(startswith)


def _sym_span(t, ref):
    for a, b, kind, blk in items(t):
        if kind == 'symbol' and ref_of(blk) == ref:
            return a, b, blk
    raise KeyError(ref)


def _set_prop(blk, name, x, y, rot=0, just='left', hide=None):
    """hide: True gizle, False goster, None MEVCUT gizliligi koru.

    None varsayilandir: place() guc sembolunun gizli #PWR### referansini ya da
    TestPoint'in gizli "TestPoint" degerini sessizce gorunur yapmasin.
    """
    a, b = K.block_at(blk, blk.index(f'(property "{name}"'))
    p = blk[a:b]
    p = re.sub(r'\(at [-\d.]+ [-\d.]+ [-\d.]+\)', f'(at {f(x)} {f(y)} {rot})', p, count=1)
    if hide is not None:
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
          just='left', prop_rot=None, hide_val=None):
    """Mevcut sembolu (x, y, ang, mirror) konumuna tasir.

    ref_at / val_at : sembol merkezine gore (dx, dy) veya (dx, dy, justify).
                      justify None -> ortali (sembolun ustune ortali yazi).
    just            : GORUNTUDEKI hizalama. ang 180 ve mirror y'nin KiCad'de
                      yaptigi left/right tersine cevirmesi burada telafi edilir.
    prop_rot        : verilmezse ang 90 -> 270, 270 -> 90, 0/180 -> 0 (metin yatay
                      ve okunur). Elle verirsen telafi hesabi senin sorumlulugunda.
    hide_val        : True gizle / False goster / None (varsayilan) mevcut
                      gizliligi koru. Reference'in gizliligi HER ZAMAN korunur:
                      guc sembolunde ref_at verince #PWR### gorunur hale gelip
                      sayfayi kalabaliklastiriyordu.
    Gizli alanlar (Footprint, Datasheet...) sembolle birlikte tasinir.
    ref_at / val_at VERILMEZSE Reference/Value sembolle ayni farkla (dx, dy)
    otelenir, goreli konumu korunur. (Eskiden yerinde kaliyordu: D3 35 mm
    saga tasininca "D3 SMBJ30A" yazisi eski konumda kaldi.) Aci degisiyorsa
    ref_at/val_at ver; fark otelemesi yazi yonunu duzeltmez.
    """
    a, b, blk = _sym_span(t, ref)
    m0 = re.search(r'\(at ([-\d.]+) ([-\d.]+) [-\d.]+\)', blk)
    ddx, ddy = x - float(m0.group(1)), y - float(m0.group(2))
    blk = re.sub(r'\(at [-\d.]+ [-\d.]+ [-\d.]+\)', f'(at {f(x)} {f(y)} {ang})', blk, count=1)
    blk = re.sub(r'\n\t\t\(mirror \w\)', '', blk)
    if mirror:
        blk = blk.replace('\n\t\t(unit ', f'\n\t\t(mirror {mirror})\n\t\t(unit ', 1)
    # Ampirik (KiCad 10, render ile dogrulandi, REV_C usb_pd_controller):
    #  - alan acisi: ang 90 -> 270, ang 270 -> 90, ang 0/180 -> 0 metni yatay
    #    ve okunur basar (ang 180'de 180 verirsen metin TERS basilir).
    #  - ang 180 veya (mirror y) left/right hizalamasini tersine cevirir;
    #    burada telafi edilir, cagiran her zaman goruntudeki hizalamayi yazar.
    pr = prop_rot if prop_rot is not None else {90: 270, 270: 90}.get(ang, 0)
    flip = (ang == 180) != (mirror == 'y')
    swap = {'left': 'right', 'right': 'left'}
    for name, o in (('Reference', ref_at), ('Value', val_at)):
        if o is None:
            if (ddx or ddy) and f'(property "{name}"' in blk:
                pa, pb = K.block_at(blk, blk.index(f'(property "{name}"'))
                p = re.sub(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)',
                           lambda mm: f'(at {f(float(mm.group(1)) + ddx)} '
                                      f'{f(float(mm.group(2)) + ddy)} {mm.group(3)})',
                           blk[pa:pb], count=1)
                blk = blk[:pa] + p + blk[pb:]
            continue
        j = o[2] if len(o) > 2 else just
        if flip and j in swap:
            j = swap[j]
        blk = _set_prop(blk, name, x + o[0], y + o[1], pr, j,
                        hide=hide_val if name == 'Value' else None)
    for m in list(re.finditer(r'\(property "([^"]+)"', blk))[::-1]:
        if m.group(1) in ('Reference', 'Value'):
            continue
        pa, pb = K.block_at(blk, m.start())
        p = re.sub(r'\(at [-\d.]+ [-\d.]+ ([-\d.]+)\)',
                   lambda mm: f'(at {f(x)} {f(y)} {mm.group(1)})', blk[pa:pb], count=1)
        blk = blk[:pa] + p + blk[pb:]
    return t[:a] + blk + t[b:]


# --------------------------------------------------------- sembol alanlari

def prop_escape(v):
    """KiCad string'i: ters bolu ve tirnak kacisi."""
    return str(v).replace('\\', '\\\\').replace('"', '\\"')


def prop_unescape(v):
    """Dosyadaki string'i duz metne cevirir (prop_escape'in tersi)."""
    return re.sub(r'\\(.)', r'\1', v)


def _prop_spans(blk):
    """[(ad, ham_deger, bas, son)] - property bloklarinin sembol icindeki yeri."""
    out, i = [], 0
    pat = re.compile(r'\n\t\t\(property "([^"]*)" "((?:[^"\\]|\\.)*)"')
    while True:
        m = pat.search(blk, i)
        if not m:
            break
        a, b = K.block_at(blk, m.start() + 3)
        out.append((m.group(1), m.group(2), a, b))
        i = b
    return out


def sym_props(blk):
    """Sembolun alanlari: [(ad, deger, gizli_mi, blok_metni)]. Deger kacissizdir."""
    return [(n, prop_unescape(v), '(hide yes)' in blk[a:b], blk[a:b])
            for n, v, a, b in _prop_spans(blk)]


def _retitle(p, name, val):
    return re.sub(r'\(property "[^"]*" "(?:[^"\\]|\\.)*"',
                  '(property "%s" "%s"' % (name, prop_escape(val)), p, count=1)


def _set_hide(p, hide):
    p = re.sub(r'\n\t\t\t\(hide yes\)', '', p, count=1)
    if hide:
        p = re.sub(r'(\n\t\t\t\(at [^\n]*\))', r'\1\n\t\t\t(hide yes)', p, count=1)
    return p


def set_sym_props(blk, fields, visible=('Reference', 'Value')):
    r"""Sembolun property bolumunu `fields` sirasina gore yeniden kurar.

    fields  : [(ad, deger)] - istenen tam alan listesi, istenen sirada.
    visible : gorunur kalacak alan adlari; kalan her alan gizlenir.
              None -> MEVCUT gorunurluk korunur, yeni alanlar gizli uretilir.
              Veri aktarimi (MPN, SelectionNote...) gibi gorunurluge dokunmamasi
              gereken islerde None kullan: varsayilan ('Reference', 'Value')
              TestPoint'lerin ve J7'nin bilincli gizlenmis Value'sunu gorunur
              yapti (Ozdisan aktariminda 14 sembol; field_visibility() ile
              yakalandi).

    Mevcut bir alanin blogu KORUNUR (konum, hizalama, font, aci); yalniz adi,
    degeri ve gizliligi degisir. Yeni alan sembol konumunda gizli uretilir.
    Boylece elle ayarlanmis Reference/Value yerlesimi bozulmaz - islem sonrasi
    field_geometry() farki bos cikmalidir.

    Bir alan standarda tasinirken adi degisiyorsa (Voltage -> VoltageRating)
    degerini fields'a yeni adla koy; listede olmayan alan dusar.

    TUZAK: property bloklari dosyada '\n\t\t' girintisiyle durur, block_at ise
    yalniz '(' ile baslayan govdeyi verir. Bloklari '\n' ile birlestirirsen
    ikinci property SUTUN 0'da baslar. KiCad dosyayi yine okur (ERC ve netlist
    etkilenmez) ama '\n\t\t\(property' arayan her arac - items(), sym_props() -
    artik yalniz ilk alani gorur; betik idempotent olmaktan cikar ve ikinci
    calistirma sembolu bozar. Ayirici bu yuzden '\n\t\t'.
    """
    spans = _prop_spans(blk)
    if not spans:
        raise ValueError('sembolde property yok')
    old = {n: blk[a:b] for n, _, a, b in spans}
    m = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', blk)
    x, y = float(m.group(1)), float(m.group(2))
    parts = []
    for name, val in fields:
        if visible is None:
            hide = name not in old or '(hide yes)' in old[name]
        else:
            hide = name not in visible
        if name in old:
            parts.append(_set_hide(_retitle(old[name], name, val), hide))
        else:
            parts.append(K._prop(name, prop_escape(val), x, y,
                                 hide=hide).rstrip('\n').lstrip('\t'))
    return blk[:spans[0][2]] + '\n\t\t'.join(parts) + blk[spans[-1][3]:]


def sym_blocks(t, ref):
    """Referansin TUM sembol bloklari (cok birimli semboller: Q3/Q5 SQJB60EP
    iki birim, iki blok): [(bas, son)]. Bulunamazsa KeyError."""
    out = [(a, b) for a, b, kind, blk in items(t) if kind == 'symbol' and ref_of(blk) == ref]
    if not out:
        raise KeyError(ref)
    return out


def update_fields(t, ref, upd, visible=None):
    """Referansin alanlarini gunceller: upd {ad: deger}; listede olmayan alan
    aynen kalir, olmayan alan sona GIZLI eklenir. Cok birimli sembolde tum
    birimlere uygulanir. visible set_sym_props'taki gibi (None = mevcut
    gorunurluk). Oturumda dort kez elle yazilan "blok bul + alan listesi kur +
    set_sym_props" dongusunun yerine:
        t = E.update_fields(t, 'R55', {'Value': '237k', 'MPN': '0402WGF2373TCE'})
    """
    for a, b in sorted(sym_blocks(t, ref), reverse=True):
        blk = t[a:b]
        flds = [(n, upd.get(n, v)) for n, v, _, _ in sym_props(blk)]
        have = {n for n, _ in flds}
        flds += [(n, v) for n, v in upd.items() if n not in have]
        t = t[:a] + set_sym_props(blk, flds, visible=visible) + t[b:]
    return t


def set_dnp(t, ref, dnp=True):
    """(dnp yes|no): montajsiz opsiyon (D8/D9 SMF30A). Render'da kirmizi carpi."""
    for a, b in sorted(sym_blocks(t, ref), reverse=True):
        blk = re.sub(r'\(dnp (?:yes|no)\)', f'(dnp {"yes" if dnp else "no"})', t[a:b], count=1)
        t = t[:a] + blk + t[b:]
    return t


def field_geometry(t):
    """{ref: {alan: (at_metni, justify)}} ve {ref: {'sym': at_metni}}.

    Yerlesimi degistirmemesi gereken bir islemin (alan ekleme, gorunurluk,
    deger normalizasyonu) once/sonra farkini almak icin. Fark bossa hicbir
    sembol veya metin oynamamistir; netlist farkiyla birlikte bu iki denetim
    "cizim bozulmadi" demeye yeter.
    """
    out = {}
    for _, _, kind, blk in items(t):
        if kind != 'symbol':
            continue
        g = {'sym': re.search(r'\(at ([-\d.]+ [-\d.]+ \d+)\)', blk).group(1)}
        for n, _, a, b in _prop_spans(blk):
            p = blk[a:b]
            at = re.search(r'\(at ([-\d.]+ [-\d.]+ \d+)\)', p)
            ju = re.search(r'\(justify ([^)]*)\)', p)
            g[n] = (at.group(1) if at else '', ju.group(1) if ju else '')
        out[ref_of(blk)] = g
    return out


def field_visibility(t):
    """{(ref, alan): gizli_mi} - alan gorunurlugu.

    field_geometry konum/hizalamayi, bu gorunurlugu kilitler. Veri aktarimi
    (MPN, parametrik alanlar) yapan betikten ONCE ve SONRA al, esit olmali:
        before = E.field_visibility(t); ...; assert E.field_visibility(t2) == before
    Yalniz sonradan eklenen alanlar farkli olabilir; onlar gizli olmali.
    """
    out = {}
    for _, _, kind, blk in items(t):
        if kind == 'symbol':
            r = ref_of(blk)
            for n, _, a, b in _prop_spans(blk):
                out[(r, n)] = '(hide yes)' in blk[a:b]
    return out


def sym_body(t, ref):
    """Sembolun sema koordinatindaki govde kutusu (aci + ayna uygulanmis).

    Metnin baska bir sembolun (veya kendi govdesinin) uzerine basip basmadigini
    anlamak icin; yalniz tel carpismasina bakan bir denetim bunu kacirir ve
    otomatik metin kaydirma degeri sembolun ICINE tasiyabilir.
    """
    _, _, blk = _sym_span(t, ref)
    lib = re.search(r'lib_id "([^"]+)"', blk).group(1)
    lb = K.lib_body(t, lib)
    if not lb:
        return None
    m = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', blk)
    x, y, ang = float(m.group(1)), float(m.group(2)), int(m.group(3))
    mm = re.search(r'\(mirror (\w)\)', blk)
    mir = mm.group(1) if mm else None
    pts = [K.xf((x, y), ang, (lb[i], lb[j]), mir) for i in (0, 2) for j in (1, 3)]
    return (min(p[0] for p in pts), min(p[1] for p in pts),
            max(p[0] for p in pts), max(p[1] for p in pts))


def field_boxes(t):
    """Gorunur sembol alanlarinin ekran kutulari: [('REF.Alan', metin, kutu)].

    Property acisi sembole GORELI saklanir: ekrandaki aci (sembol_ang +
    prop_rot) % 360'tir (R13 ang=90 + rot=270 -> yatay basilir). Ayrica ang 180
    ve (mirror y) left/right hizalamasini ters cevirir; place() yazarken telafi
    eder, burada okurken geri alinir. Bu iki telafiyi atlarsan kutular 90 derece
    doner ve carpisma raporu sahte bulgularla dolar.
    """
    out = []
    for _, _, kind, blk in items(t):
        if kind != 'symbol':
            continue
        ref = ref_of(blk)
        m = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', blk)
        sang = int(m.group(3))
        flip = (sang == 180) != ('(mirror y)' in blk)
        for n, v, a, b in _prop_spans(blk):
            p = blk[a:b]
            if '(hide yes)' in p or n not in ('Reference', 'Value'):
                continue
            at = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', p)
            ju = re.search(r'\(justify ([^)]*)\)', p)
            jt = ju.group(1).split()[0] if ju else 'center'
            if flip:
                jt = {'left': 'right', 'right': 'left'}.get(jt, jt)
            sz = re.search(r'\(size ([\d.]+)', p)
            txt = prop_unescape(v)
            out.append(('%s.%s' % (ref, n), txt,
                        K.text_box(txt, float(at.group(1)), float(at.group(2)),
                                   (sang + int(at.group(3))) % 360, jt,
                                   float(sz.group(1)) if sz else 1.27)))
    return out


def sym_pin(t, ref, num):
    """Yerlestirilmis sembolun pininin mutlak konumu (aci + ayna)."""
    _, _, blk = _sym_span(t, ref)
    lib = re.search(r'lib_id "([^"]+)"', blk).group(1)
    x, y, ang = map(float, re.search(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)', blk).groups())
    m = re.search(r'\(mirror (\w)\)', blk)
    return K.xf((x, y), int(ang), K.lib_pins(t, lib)[num], m.group(1) if m else None)


def pin_at(t, ref, num, expected):
    """sym_pin'i plandaki konumla karsilastirir; uyusmazsa AssertionError.

    Duz `sym_pin(...) == (x, y - 7.62)` yazma: 53.34 - 7.62 = 45.720000000000006
    olur ve dogru yerlesim yanlis diye reddedilir. Donus: expected (tel ucunda
    dogrudan kullanmak icin)."""
    p = sym_pin(t, ref, num)
    e = (round(expected[0], 4), round(expected[1], 4))
    assert (round(p[0], 4), round(p[1], 4)) == e, f'{ref}.{num}: {p} != {e}'
    return e


def _lib_pin_meta(t, lib):
    a, b = K.block_at(t, t.index(f'(symbol "{lib}"'))
    meta = {}
    for m in re.finditer(r'\(pin (\w+) \w+\s*\(at [^)]*\)[\s\S]*?\(name "([^"]*)"'
                         r'[\s\S]*?\(number "([^"]+)"', t[a:b]):
        meta[m.group(3)] = (m.group(2), m.group(1))
    return meta


def inventory(t, net):
    """Sayfanin tam envanteri: her sembol icin pin no, ad, tip, mutlak konum ve
    BAGLI OLDUGU NET; ayrica etiketler, metinler, no_connect'ler, etiket sekilleri.

    net: verify.parse(netlist) sozlugu. Yerlesim planini bununla yap: hangi pin
    nereye gidiyor, hangi pin 'unconnected-(...)' (eski ERC hatalari cogu zaman
    gercek baglanti hatasidir; SDA seviye donusturucusu boyle bulundu)."""
    p2n = {p: n for n, ps in net.items() for p in ps}
    out = [f'shapes {label_shapes(t)}']
    for _, _, kind, blk in items(t):
        if kind == 'symbol':
            ref = ref_of(blk)
            lib = re.search(r'lib_id "([^"]+)"', blk).group(1)
            val = re.search(r'property "Value" "([^"]*)"', blk).group(1)
            at = re.search(r'\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)', blk).groups()
            mir = re.search(r'\(mirror (\w)\)', blk)
            if ref.startswith('#'):
                out.append(f'  PWR {ref} {val} {at[:2]}')
                continue
            out.append(f'SYM {ref} {lib} "{val}" at={at}'
                       + (f' mirror={mir.group(1)}' if mir else ''))
            meta = _lib_pin_meta(t, lib)
            for num in sorted(K.lib_pins(t, lib), key=lambda n: (len(n), n)):
                nm, ty = meta.get(num, ('?', '?'))
                out.append(f'    {num:>3} {nm:<22} {ty:<14} {sym_pin(t, ref, num)} '
                           f'-> {p2n.get(f"{ref}.{num}", "-")}')
        elif kind in ('label', 'global_label', 'text'):
            s = re.match(r'\(\w+ "([^"]*)"', blk).group(1)
            out.append(f'{kind.upper()} {s[:70]} {pos(kind, blk)[0]}')
        elif kind == 'no_connect':
            out.append(f'NC {pos(kind, blk)[0]}')
    return '\n'.join(out)


def power_symbol_nets(t, net):
    """#PWR/#FLG sembollerinin bagli oldugu net (tel baglantisindan cozulur).

    PWR_FLAG netlist'te gorunmez; silip yeniden koyarken hangi nette oldugunu
    bilmek icin bunu kullan (usb_pd_controller'da bir PWR_FLAG'in GND'de oldugu
    boyle anlasildi). Donus: {ref: (deger, konum, {net adlari})}."""
    par = {}

    def fnd(a):
        par.setdefault(a, a)
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    R = lambda p: (round(p[0], 2), round(p[1], 2))  # noqa: E731
    segs = []
    for _, _, kind, blk in items(t):
        if kind == 'wire':
            p = [R(q) for q in pos(kind, blk)]
            segs.append(p)
            par[fnd(p[0])] = fnd(p[1])
    ends = {q for s in segs for q in s}
    for (x0, y0), (x1, y1) in segs:
        for q in ends:
            if (x0 == x1 == q[0] and min(y0, y1) < q[1] < max(y0, y1)) or \
               (y0 == y1 == q[1] and min(x0, x1) < q[0] < max(x0, x1)):
                par[fnd(q)] = fnd((x0, y0))
    p2n = {p: n for n, ps in net.items() for p in ps}
    node, pw = {}, []
    for _, _, kind, blk in items(t):
        if kind != 'symbol':
            continue
        ref = ref_of(blk)
        if ref.startswith('#'):
            pw.append((ref, re.search(r'property "Value" "([^"]*)"', blk).group(1),
                       R(pos(kind, blk)[0])))
            continue
        lib = re.search(r'lib_id "([^"]+)"', blk).group(1)
        for num in K.lib_pins(t, lib):
            node.setdefault(fnd(R(sym_pin(t, ref, num))), set()).add(p2n.get(f'{ref}.{num}'))
    return {ref: (val, q, node.get(fnd(q), set())) for ref, val, q in pw}


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


def prune_lib_symbols(t):
    """lib_symbols onbelleginden hicbir sembolun lib_id'si ile kullanilmayan
    tanimlari siler. Donus: (yeni metin, silinen adlar).

    Sembol kaldirildiginda (BT1 Battery_Cell, U7 TPS61023...) veya swap_lib ile
    degistirildiginde eski tanim onbellekte kalir; zararsizdir ama diff'i ve
    dosyayi sisirir, eski parcayi 'hala tasarimda' gibi gosterir.
    """
    i = t.index('(lib_symbols')
    la, lb = K.block_at(t, i)
    used = set(re.findall(r'\(lib_id "([^"]+)"\)', t))
    cut, names = [], []
    j = t.index('\n', la)
    while True:
        m = re.compile(r'\n\t\t\(symbol "([^"]+)"').search(t, j, lb)
        if not m:
            break
        a, b = K.block_at(t, m.start() + 3)
        if m.group(1) not in used:
            cut.append((a, b))
            names.append(m.group(1))
        j = b
    for a, b in sorted(cut, reverse=True):
        t = t[:t.rindex('\n', 0, a)] + t[b:]
    return t, names


def missing_lib_symbols(t):
    """Orneklerin kullandigi ama lib_symbols onbelleginde OLMAYAN lib_id'ler.

    K.sym()/K.power() onbellege eklemez. Eksik tanim ERC'de hata VERMEZ:
    power:+3.3V eksikken U10 VBUS pini netlist'te 'Net-(U10-VBUS)' adli ayri
    bir nete dustu, ERC yalniz pin_to_pin "Pin 1 [???]" uyarisi verdi.
    K.lib_pins de ValueError('substring not found') ile patlar."""
    i = t.index('(lib_symbols')
    la, lb = K.block_at(t, i)
    cached = set(re.findall(r'\n\t\t\(symbol "([^"]+)"', t[la:lb]))
    used = set(re.findall(r'\(lib_id "([^"]+)"\)', t[lb:]))
    return sorted(used - cached)


def ensure_used_lib_symbols(t, table='sym-lib-table'):
    """missing_lib_symbols'taki her tanimi kutuphanesinden onbellege kopyalar
    (proje kutuphanesi sym-lib-table'dan, yoksa KiCad sistem kutuphanesi).
    Yeni sembol/guc sembolu ekleyen her betigin sonunda cagir."""
    from kicadtools import project_symbol_lib
    for lid in missing_lib_symbols(t):
        nick, name = lid.split(':', 1)
        t = K.ensure_lib_symbol(t, project_symbol_lib(nick, table), name, nick)
    return t


def refresh_lib_symbol(t, lib_id, lib_path=None, allow_pin_move=False):
    """Onbellekteki tanimi kutuphanedeki guncel haliyle degistirir (ERC
    lib_symbol_mismatch). KiCad surum yukseltmesinde kutuphane sembolu yalniz
    cizimde degisebilir: KiCad 10 TL431DBZ'de pin uzunlugu 2.54 -> 1.27 mm,
    pin uclari (at) ayni. Pin uc konumu degisirse baglanti kopar; bu yuzden
    allow_pin_move=False iken pinler karsilastirilir, fark varsa ValueError."""
    from kicadtools import project_symbol_lib
    nick, name = lib_id.split(':', 1)
    old = K.lib_pins(t, lib_id)
    a, b = K.block_at(t, t.index(f'(symbol "{lib_id}"'))
    t2 = K.ensure_lib_symbol(t[:t.rindex('\n', 0, a)] + t[b:],
                             lib_path or project_symbol_lib(nick), name, nick)
    new = K.lib_pins(t2, lib_id)
    if not allow_pin_move and old != new:
        raise ValueError(f'{lib_id} pin konumlari degisti: {old} -> {new}')
    return t2


def swap_lib(t, ref, lib_id, lib_path=None):
    """Yerlestirilmis sembolun kutuphane sembolunu degistirir (ayni referans,
    ayni uuid/instance/alanlar): RV-3028-C7 -> BQ32000, Conn_01x40 -> Conn_01x30.

    Sembolu silip yeniden olusturma - alanlar, uuid ve PCB baglantisi kaybolur.
    Yapilanlar:
      * lib_id degisir, yeni tanim onbellege kopyalanir (lib_path verilmezse
        sym-lib-table'daki proje kutuphanesi, yoksa KiCad sistem kutuphanesi;
        `extends` ile turetilmis semboller bagimsizlastirilir);
      * sembol ornegindeki (pin "N") uuid kayitlari yeni sembolun pin
        numaralarina esitlenir: fazlalar silinir (40 -> 30 pinde 31..40),
        eksikler yeni uuid ile eklenir;
      * kullanilmayan eski tanim prune_lib_symbols ile silinir.
    Pin KONUMLARI degisir: ardindan place() + pin_at() ile yeniden yerlestir ve
    telleri yeniden ciz. Alanlari (Value, Footprint, MPN...) set_sym_props ile yaz.
    """
    from kicadtools import project_symbol_lib
    nick, name = lib_id.split(':', 1)
    t = K.ensure_lib_symbol(t, lib_path or project_symbol_lib(nick), name, nick)
    a, b, blk = _sym_span(t, ref)
    blk = re.sub(r'\(lib_id "[^"]+"\)', f'(lib_id "{lib_id}")', blk, count=1)
    want = set(K.lib_pins(t, lib_id))
    have = re.findall(r'\n\t\t\(pin "([^"]+)"\n\t\t\t\(uuid "[^"]+"\)\n\t\t\)', blk)
    for n in have:
        if n not in want:
            blk = re.sub(r'\n\t\t\(pin "%s"\n\t\t\t\(uuid "[^"]+"\)\n\t\t\)' % re.escape(n),
                         '', blk, count=1)
    add = ''.join(f'\n\t\t(pin "{n}"\n\t\t\t(uuid "{K.uid()}")\n\t\t)'
                  for n in sorted(want - set(have), key=lambda s: (len(s), s)))
    if add:
        k = blk.index('\n\t\t(instances')
        blk = blk[:k] + add + blk[k:]
    t = t[:a] + blk + t[b:]
    return prune_lib_symbols(t)[0]


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
