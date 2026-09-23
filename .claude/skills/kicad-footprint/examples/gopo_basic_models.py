"""gopo: 3D modeli olmayan proje footprint'lerine basitlestirilmis STEP (TASK-061).

Uretici STEP'i olmayan alti parca icin olcu cizimindeki dis zarf kutularla
modellenir (step_boxes.py; koordinat footprint'te, y asagi, z=0 kart ustu,
offset/rotate 0). Yukseklikler nominal; maks. degerler not olarak asagida.
Betik mevcut footprint'e yalniz (model ...) blogu ekler (varsa dokunmaz),
satir sonunu dosyadan alir (hepsi CRLF). Deterministik.

    sh .claude/skills/kicad-schematic/scripts/kpy \\
       .claude/skills/kicad-footprint/examples/gopo_basic_models.py hardware/libraries

Kaynaklar ve olcu cozumu:
- J3 KLS L-KLS1-242I-2.0-30 (KLS1-242I.pdf): govde 0.5N+0.52 = 15.52 (kulaklarla
  0.5N+3.54 = 18.54), derinlik 5.30 (bacak ucu dahil, bacak govdeden 0.65
  tasar), yukseklik 2.00 +-0.15 (flip kapak ACIKKEN 3.1). Footprint Fab'i
  y -4.55..0.10 = 4.65 govde; bacaklar y 0.75'e kadar -> 4.65 + 0.65 = 5.30.
  Kablo girisi -y (on), flip kapak arkada (bacak tarafi).
- L1 Core Master FPI0705 (FPI0705-220K.pdf): A 7.8 x B 7.0 x C 5.0 +-0.3;
  terminal D 2.1 (REF), Fab ile ayni eksen (x 7.8, y 7.0, pedler +-y).
- Q3/Q5 Vishay PowerPAK SO-8L Dual (sqjb60ep.pdf): A 1.00/1.07/1.14;
  govde footprint Fab'i 4.90 x 6.15. Leadless, pin 1-4 +y kenari.
- C33 Korchip DCL H-type (korchip_dcl.pdf): coin D 19.0 +-0.3 yatik, H 6.5
  +-0.5 (maks 7.0), P 20 +-0.5, bacak 1.0 x 0.2, kart altina 3.5. Coin
  merkezi bacaklarin ortasi (footprint varsayimi, numune ile dogrulanacak).
- SW3 KLS L-KLS4-EC1121S-E5A-F12.5 (cizim): bushing E -> D = 5, mil F tipi
  L 12.5 (F 4.5); govde 12.0 x 11.7 (tespit kulaklariyla 12.5), govde 4.5,
  bushing D7 x 5, mil D6 -> mil ucu kart ustunden 4.5 + 12.5 = 17.0; pinler
  kart altina 3.5. Mil duzlugu (F) modellenmedi.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from step_boxes import StepBoxes, BLACK, GOLD, GREEN, SILVER, WHITE  # noqa: E402

STAMP = '2026-09-23T00:00:00'
BROWN = (0.55, 0.35, 0.15)
YELLOW = (0.85, 0.72, 0.30)


def j3():
    s = StepBoxes('KLS_L-KLS1-242I-2.0-30')
    s.box('Housing', WHITE, -7.76, 7.76, -4.55, 0.10, 0.0, 1.30)
    s.box('Ear_L', WHITE, -9.27, -7.76, -4.55, -1.60, 0.0, 1.30)
    s.box('Ear_R', WHITE, 7.76, 9.27, -4.55, -1.60, 0.0, 1.30)
    s.box('Actuator', BROWN, -7.76, 7.76, -2.60, 0.10, 1.30, 2.00)
    for i in range(30):
        x = -7.25 + 0.5 * i
        s.box(f'Lead_{i + 1}', GOLD, x - 0.1, x + 0.1, -0.60, 0.75, 0.0, 0.15)
    for sx in (-1, 1):
        s.box(f'MP_{sx}', SILVER, sx * 8.52 - 0.5, sx * 8.52 + 0.5, -3.90, -2.30, 0.0, 0.20)
    return s


def l1():
    s = StepBoxes('L_CoreMaster_FPI0705')
    s.box('Body', BLACK, -3.9, 3.9, -3.5, 3.5, 0.3, 5.0)
    for sy in (-1, 1):
        y0, y1 = sorted((sy * 1.4, sy * 3.55))
        s.box(f'Term_{sy}', SILVER, -3.0, 3.0, y0, y1, 0.0, 0.3)
    s.box('Base', BLACK, -3.9, 3.9, -1.4, 1.4, 0.0, 0.3)
    return s


def q_powerpak():
    s = StepBoxes('Vishay_PowerPAK_SO-8L_Dual')
    s.box('Body', BLACK, -2.45, 2.45, -3.075, 3.075, 0.10, 1.07)
    s.box('Frame', SILVER, -2.45, 2.45, -3.075, 1.50, 0.0, 0.10)
    for i, x in enumerate((-1.905, -0.635, 0.635, 1.905)):
        s.box(f'Pin_{i + 1}', SILVER, x - 0.2, x + 0.2, 2.40, 3.075, 0.0, 0.25)
    s.box('Pin1_mark', WHITE, -2.05, -1.65, 2.10, 2.50, 1.07, 1.08)
    return s


def c33():
    s = StepBoxes('Korchip_DCL_H-Type_D19.0mm')
    s.cyl('Coin', YELLOW, -10.0, 0.0, 9.5, 0.0, 6.5, n=10)
    s.box('Lead_pos_h', SILVER, -1.5, 0.1, -0.5, 0.5, 0.5, 0.7)
    s.box('Lead_pos_v', SILVER, -0.1, 0.1, -0.5, 0.5, -3.5, 0.7)
    s.box('Lead_neg_h', SILVER, -20.1, -18.5, -0.5, 0.5, 0.5, 0.7)
    s.box('Lead_neg_v', SILVER, -20.1, -19.9, -0.5, 0.5, -3.5, 0.7)
    return s


def sw3():
    s = StepBoxes('L-KLS4-EC1121S-E5A-F12.5')
    s.box('Body', BLACK, 1.5, 13.5, -3.35, 8.35, 0.0, 4.5)
    s.box('Frame_top', SILVER, 1.5, 13.5, -3.35, 8.35, 4.3, 4.5)
    for i, y0 in enumerate((-3.75, 8.35)):
        s.box(f'Tab_{i}', SILVER, 6.5, 8.5, y0, y0 + 0.4, -2.5, 4.5)
    s.cyl('Bushing', SILVER, 7.5, 2.5, 3.5, 4.5, 9.5)
    s.cyl('Shaft', SILVER, 7.5, 2.5, 3.0, 9.5, 17.0)
    for n, (x, y) in enumerate(((0, 0), (0, 2.5), (0, 5), (14.5, 0), (14.5, 5)), 1):
        s.box(f'Pin_{n}_v', GOLD, x - 0.4, x + 0.4, y - 0.15, y + 0.15, -3.5, 1.0)
        a, b = sorted((x, 1.5 if x < 7.5 else 13.5))
        s.box(f'Pin_{n}_h', GOLD, a - 0.4, b, y - 0.15, y + 0.15, 0.6, 1.0)
    return s


def l3():
    # SRI0704-6R8M (SRI0704_series.pdf): A 7.3 x B 7.3 x C 4.5 MAX; pedler +-x
    s = StepBoxes('L_7.3x7.3_H4.5')
    s.box('Body', BLACK, -3.65, 3.65, -3.65, 3.65, 0.3, 4.5)
    for sx in (-1, 1):
        x0, x1 = sorted((sx * 2.4, sx * 3.7))
        s.box(f'Term_{sx}', SILVER, x0, x1, -1.0, 1.0, 0.0, 0.3)
    s.box('Base', BLACK, -2.4, 2.4, -3.65, 3.65, 0.0, 0.3)
    return s


def u12():
    # LM74801QDRRRQ1 DRR0012E (LM7480-Q1.pdf): 3 x 3, 0.8 MAX (0.7..0.8)
    s = StepBoxes('WSON-12-1EP_3x3mm')
    s.box('Body', BLACK, -1.5, 1.5, -1.5, 1.5, 0.0, 0.75)
    for i in range(6):
        y = -1.25 + 0.5 * i
        for sx in (-1, 1):
            x0, x1 = sorted((sx * 1.1, sx * 1.5))
            s.box(f'Pin_{sx}_{i}', SILVER, x0, x1, y - 0.12, y + 0.12, 0.0, 0.2)
    s.box('Pin1_mark', WHITE, -1.2, -0.9, -1.35, -1.05, 0.75, 0.76)
    return s


def u2():
    # ESP32-C6-MINI-1 (datasheet): 13.2 x 16.6 x 2.4; anten bolgesi Fab'daki
    # y -11.0..-5.6 (kalkansiz modul PCB'si), geri kalani kalkan.
    s = StepBoxes('ESP32-C6-MINI-1')
    s.box('Module_PCB', GREEN, -6.6, 6.6, -11.0, 5.6, 0.0, 0.8)
    s.box('Shield', SILVER, -6.4, 6.4, -5.5, 5.4, 0.8, 2.4)
    s.box('Antenna', GOLD, -6.0, 6.0, -10.6, -9.6, 0.8, 0.85)
    return s


def y1():
    # Abracon ABS25 (ABS25.pdf): 8.0 x 3.8 x 2.5; footprint'te uzun kenar y
    s = StepBoxes('Crystal_SMD_Abracon_ABS25')
    s.box('Body', WHITE, -1.9, 1.9, -4.0, 4.0, 0.0, 2.2)
    s.box('Lid', SILVER, -1.7, 1.7, -3.8, 3.8, 2.2, 2.5)
    return s


def j4():
    # SolderWire 1.5 mm2: iletken D1.7, izolasyon OD3.9 (footprint descr);
    # kablo yonu kutuya gore belirlenecek -> dik 10 mm kablo cikisi (zarf).
    s = StepBoxes('SolderWire-1.5sqmm_1x02')
    for i, x in enumerate((0.0, 7.8)):
        s.cyl(f'Core_{i}', GOLD, x, 0.0, 0.85, -1.8, 1.0, n=4)
        s.cyl(f'Insul_{i}', BLACK if i else (0.75, 0.1, 0.1), x, 0.0, 1.95, 1.0, 10.0, n=6)
    return s


# (kutuphane, footprint adi, model uretici)
PARTS = [
    ('Connector_FPC_Custom', 'KLS_L-KLS1-242I-2.0-30_1x30-2MP_P0.50mm_Horizontal', j3),
    ('Inductor_Custom', 'L_CoreMaster_FPI0705_7.8x7.0mm_H5.0', l1),
    ('Package_SO_Custom', 'Vishay_PowerPAK_SO-8L_Dual', q_powerpak),
    ('Power_Output_Custom', 'Korchip_DCL_H-Type_D19.0mm_P20.00mm_Horizontal', c33),
    ('L-KLS4-EC1121S-E5A-F12.5', 'L-KLS4-EC1121S-E5A-F12.5', sw3),
]


# KiCad 10 standart footprint'leri; atadiklari model dosyasi KiCad 10 3dmodels
# kurulumunda YOK (KiCad sessizce modelsiz cizer). Ikame model proje
# dizininde; PCB'deki kopyanin model yolu degistirilir (--pcb).
STD_DIR = 'Generic_Custom.3dshapes'
STD = [
    ('L3', 'Inductor_SMD.3dshapes/L_7.3x7.3_H4.5.step', l3),
    ('U12', 'Package_SON.3dshapes/WSON-12-1EP_3x3mm_P0.5mm_EP1.5x2.5mm.step', u12),
    ('U2', 'RF_Module.3dshapes/ESP32-C6-MINI-1.step', u2),
    ('Y1', 'Crystal.3dshapes/Crystal_SMD_Abracon_ABS25-4Pin_8.0x3.8mm.step', y1),
    ('J4', 'Connector_Wire.3dshapes/SolderWire-1.5sqmm_1x02_P7.8mm_D1.7mm_OD3.9mm.step', j4),
]
# Govdesi ayni olan KiCad modeline yonlendirilenler (EP yalniz alt yuzde)
STD_REDIRECT = {
    'Package_SO.3dshapes/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.71x3.7mm.step':
        '${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/SOIC-8-1EP_3.9x4.9mm_P1.27mm_EP2.41x3.81mm.step',
}


def std_models(root):
    d = os.path.join(root, STD_DIR)
    os.makedirs(d, exist_ok=True)
    table = dict(STD_REDIRECT)
    for ref, old, gen in STD:
        name = os.path.basename(old)
        print(gen().write(os.path.join(d, name), stamp=STAMP))
        table[old] = f'${{KIPRJMOD}}/libraries/{STD_DIR}/{name}'
    return table


def fix_pcb(pcb, table):
    """PCB'deki kirik KiCad model yollarini ikame yolla degistir (metin)."""
    lck = os.path.join(os.path.dirname(pcb), '~' + os.path.basename(pcb) + '.lck')
    if os.path.exists(lck):
        sys.exit(f'PCB editoru acik ({lck}); kapatip tekrar calistir')
    raw = open(pcb, 'rb').read().decode('utf-8')
    for old, new in table.items():
        key = f'(model "${{KICAD10_3DMODEL_DIR}}/{old}"'
        n = raw.count(key)
        raw = raw.replace(key, f'(model "{new}"')
        print(f'  {n} x {os.path.basename(old)} -> {new}')
    with open(pcb, 'w', encoding='utf-8', newline='') as fh:
        fh.write(raw)


def add_model(mod_path, model_ref):
    raw = open(mod_path, 'rb').read().decode('utf-8')
    if '(model ' in raw:
        return 'var'
    nl = '\r\n' if '\r\n' in raw else '\n'
    body = raw.rstrip()
    assert body.endswith(')'), mod_path
    block = (f'\t(model "{model_ref}"\n\t\t(offset\n\t\t\t(xyz 0 0 0)\n\t\t)\n'
             f'\t\t(scale\n\t\t\t(xyz 1 1 1)\n\t\t)\n\t\t(rotate\n\t\t\t(xyz 0 0 0)\n\t\t)\n\t)\n')
    out = body[:-1].rstrip() + nl + block.replace('\n', nl) + ')' + nl
    with open(mod_path, 'w', encoding='utf-8', newline='') as fh:
        fh.write(out)
    return 'eklendi'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('root', help='hardware/libraries')
    ap.add_argument('--pcb', help='kirik model yollarini bu PCB dosyasinda duzelt')
    a = ap.parse_args()
    table = std_models(a.root)
    if a.pcb:
        fix_pcb(a.pcb, table)
    for lib, name, gen in PARTS:
        d = os.path.join(a.root, f'{lib}.3dshapes')
        os.makedirs(d, exist_ok=True)
        print(gen().write(os.path.join(d, f'{name}.step'), stamp=STAMP))
        ref = f'${{KIPRJMOD}}/libraries/{lib}.3dshapes/{name}.step'
        print(' ', add_model(os.path.join(a.root, f'{lib}.pretty', f'{name}.kicad_mod'), ref))


if __name__ == '__main__':
    main()
