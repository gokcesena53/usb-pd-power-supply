"""Sematik okunabilirlik denetimi: ust uste binen metinler, deterministik.

Render'a bakarak cakisma aramak yavas ve guvenilmez; 12 piksel yuksekligindeki
bir "5" ile "6" ayirt edilemez. Bu modul metin kutularini hesaplar ve uc hata
sinifini raporlar:

  1. metin <-> metin   : iki gorunur yazi ust uste (etiket / alan / blok basligi)
  2. metin <-> tel/govde: sembol alani bir telin veya bir sembol govdesinin uzerine
                          basiyor (etiketin tel uzerinde olmasi DOGRUDUR, o haric)
  3. govdesinden tel gecen global etiket: cipada tel olmasi dogru, govdenin
                          altindan gecip yaziyi cizmesi degil

Kullanim:
    python readability.py sayfa.kicad_sch [...]        # rapor, cikis kodu = bulgu sayisi
    import readability as R;  tt, tw = R.problems(t);  ls = R.labels_struck(t)

SINIRLARI - her bulgu render ile teyit edilmelidir:
  * govde kutusu sembolun gercek cizimi degil, kaba dikdortgen cevresidir:
    anahtar/buton gibi seyrek sembollerde yakin duran metni bile bulgu sayar.
  * sembol grafigi (TestPoint cubugu gibi) bir etiketin govdesine girerse
    yakalanmaz; bu sinif icin gozle bakmak gerekir.
Yani: bulgu YOKSA temizdir; bulgu VARSA once render et, sonra oynat.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kisch as K  # noqa: E402
import kisch_edit as E  # noqa: E402
from kicadtools import read_sheet  # noqa: E402

PAD = 0.2          # mm: bu kadar temas gorsel sorun sayilmaz
LABEL_ARROW = 3.0  # global etiket govdesinin ok ucu payi (SKILL.md: ~3 mm)


def wires(t):
    """Iki uclu tel parcalari: [(x1, y1, x2, y2)]."""
    out = []
    for _, _, kind, blk in E.items(t):
        if kind != 'wire':
            continue
        p = re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)', blk)
        if len(p) == 2:
            out.append((float(p[0][0]), float(p[0][1]),
                        float(p[1][0]), float(p[1][1])))
    return out


def seg_in_box(seg, bx):
    """Yatay/dikey tel parcasi kutunun ICINDEN geciyor mu."""
    x1, y1, x2, y2 = seg
    if abs(y1 - y2) < 1e-6:
        return (bx[1] + PAD < y1 < bx[3] - PAD and
                min(x1, x2) < bx[2] - PAD and bx[0] + PAD < max(x1, x2))
    if abs(x1 - x2) < 1e-6:
        return (bx[0] + PAD < x1 < bx[2] - PAD and
                min(y1, y2) < bx[3] - PAD and bx[1] + PAD < max(y1, y2))
    return False


def label_boxes(t):
    """Etiket ve serbest metinlerin ekran kutulari: [('tur:ad', metin, kutu)].

    Etikette govde yonunu ROT belirler; KiCad'in yazdigi (justify ...) zaten o
    yonun sonucudur. Ikisini birden uygularsan kutu ters doner ve bitisikteki
    her sembol alani sahte cakisma verir (PD_5V rot=180 + justify right boyle
    bulundu: raporda Q1/Q2 ile cakisiyordu, render'da 8 mm uzaktaydilar).
    """
    out = []
    for _, _, kind, blk in E.items(t):
        at = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', blk)
        if kind in ('label', 'global_label', 'hierarchical_label'):
            nm = re.search(r'\((?:global_|hierarchical_)?label "((?:[^"\\]|\\.)*)"',
                           blk).group(1)
            extra = LABEL_ARROW if kind != 'label' else 0.0
            out.append(('%s:%s' % (kind, nm), nm,
                        K.text_box(nm, float(at.group(1)), float(at.group(2)),
                                   int(at.group(3)), 'left', 1.27, extra)))
        elif kind == 'text':
            s = re.search(r'\(text "((?:[^"\\]|\\.)*)"', blk).group(1)
            sz = re.search(r'\(size ([\d.]+)', blk)
            size = float(sz.group(1)) if sz else 1.27
            for n, line in enumerate(s.split('\\n')):
                out.append(('text:%s' % line[:18], line,
                            K.text_box(line, float(at.group(1)),
                                       float(at.group(2)) + n * size * 1.4,
                                       int(at.group(3)), 'left', size)))
    return out


def bodies(t):
    """Sayfadaki sembol govdelerinin sema kutulari: [(ref, kutu)]."""
    out = []
    for _, _, kind, blk in E.items(t):
        if kind != 'symbol':
            continue
        ref = E.ref_of(blk)
        bx = E.sym_body(t, ref)
        if bx:
            out.append((ref, bx))
    return out


def problems(t):
    """(metin-metin cakismalari, tel/govde uzerine basan sembol alanlari).

    Ayni sembolun Reference/Value cifti haric tutulur: onlar tasarlanmis iki
    satirdir ve araliklari SKILL.md'deki yerlesim kurallarina tabidir.
    """
    items = E.field_boxes(t) + label_boxes(t)
    tt = set()
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            ai, aj = items[i][0], items[j][0]
            if '.' in ai and '.' in aj and ai.split('.')[0] == aj.split('.')[0]:
                continue
            if K.boxes_overlap(items[i][2], items[j][2], PAD):
                tt.add((ai, aj))
    ws, bd = wires(t), bodies(t)
    tw = set()
    for nm, _, bx in E.field_boxes(t):
        if any(seg_in_box(sg, bx) for sg in ws) or \
           any(K.boxes_overlap(bb, bx, PAD) for _, bb in bd):
            tw.add(nm)
    return tt, tw


def labels_struck(t):
    """Govdesinden tel gecen global/hiyerarsik etiketler: [(ad, x, y, rot)].

    Yerel etiketin metni KiCad'de telin USTUNE kaydirilarak cizilir, govdesi
    yoktur: tel uzerinde olmasi dogrudur, taranmaz. Global etiketin govdesi
    cipaya oturur; tel cipada durmayip govde yonunde devam ederse yaziyi cizer.
    Cipanin 1 mm'lik ucu disarida birakilir.
    """
    ws = wires(t)
    out = []
    for _, _, kind, blk in E.items(t):
        if kind not in ('global_label', 'hierarchical_label'):
            continue
        m = re.search(r'\(at ([-\d.]+) ([-\d.]+) (\d+)\)', blk)
        nm = re.search(r'\((?:global_|hierarchical_)?label "((?:[^"\\]|\\.)*)"',
                       blk).group(1)
        x, y, r = float(m.group(1)), float(m.group(2)), int(m.group(3))
        L = K.text_width(nm, 1.27) + LABEL_ARROW
        dx, dy = {0: (1, 0), 90: (0, -1), 180: (-1, 0), 270: (0, 1)}[r]
        x0, y0, x1, y1 = x + dx * 1.0, y + dy * 1.0, x + dx * L, y + dy * L
        bx = ((min(x0, x1), y - 1.0, max(x0, x1), y + 1.0) if dy == 0 else
              (x - 1.0, min(y0, y1), x + 1.0, max(y0, y1)))
        if any(seg_in_box(sg, bx) for sg in ws):
            out.append((nm, x, y, r))
    return out


def report(sheets):
    """Sayfalari denetler, insan-okur rapor basar, toplam bulgu sayisi doner."""
    total = 0
    for fn in sheets:
        t, _ = read_sheet(fn)
        tt, tw = problems(t)
        ls = labels_struck(t)
        print('== %-28s %d metin-metin, %d tel/govde uzeri, %d telden gecen etiket'
              % (os.path.basename(fn), len(tt), len(tw), len(ls)))
        for a, b in sorted(tt):
            print('   cakisma  %-26s <-> %s' % (a, b))
        for nm in sorted(tw):
            print('   uzerine  %s' % nm)
        for nm, x, y, r in ls:
            print('   etiket   %-20s @ (%.2f, %.2f) rot=%d' % (nm, x, y, r))
        total += len(tt) + len(tw) + len(ls)
    print('\nTOPLAM BULGU: %d' % total)
    return total


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(min(report(sys.argv[1:]), 100))
