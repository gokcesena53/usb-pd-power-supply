"""Ornek + yeniden uretim: Waveshare 2-CH UART TO ETH (J8) footprint'i ve STEP'i.

    SK=.claude/skills/kicad-schematic/scripts
    sh $SK/kpy .claude/skills/kicad-footprint/examples/waveshare_2ch_uart_to_eth.py [--root hardware/libraries]

Kaynaklar (23.09.2026): Waveshare olcu cizimi (ust + yan gorunus), alt gorunus
fotografindaki pin etiketleri, modul semasi (2-CH_UART_TO_ETH_SCH.pdf: P1
Header 8X2 pin numaralari, P2/P3 "Header 1" baglantisiz).

Olcu cozumu:
  - Modul PCB 53.00 x 22.00, kalinlik 1.60 (cizim).
  - Header: dis sutun sag kenardan 1.85 (tek pinler), ic sutun +2.54 (cift);
    ilk/son sira kenardan 2.11 (2.11 + 7x2.54 + 2.11 = 22.00 tutuyor).
  - Pin 1 = DIR1: sema P1 (1 DIR1 / 2 DIR2 ... 15-16 5V) + alt gorunus
    etiket tablosu (sol sutun tek, alt sira DIR) + ust gorunusteki pin-1 silk
    kutusu (alt sira). Alt gorunus soldan-saga aynadir, satirlar ayni kalir.
  - RJ45 tasmasi: cizimde "4.00" yaziyor ama 57.30 - 53.00 = 4.30 ve mekanik
    pin (RJ45 onunden 8.30) goruntuden 3.85-3.91 mm -> 4.30 ile tutarli.
  - Mekanik pin y: goruntuden 1.31 / 1.44 mm (kenardan) -> 1.35 simetrik;
    +-0.3 mm belirsizlik icin delik 1.4 / ped 2.2.
  - Header plastik ara parcasi 10.10 - 1.60 - 6.00 = 2.50 mm; RJ45 lehim
    cikintisi yan gorunusten ~2.2 mm -> RJ45 pim alaninda F.Cu keepout.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
from kifp import Footprint, PINHEADER_PAD, PINHEADER_DRILL  # noqa: E402
from step_boxes import StepBoxes, BLUE, SILVER, BLACK, GOLD  # noqa: E402

NAME, LIB = 'Waveshare_2-CH_UART_TO_ETH', 'Module_Custom'
P = 2.54
X1, Y1 = 53.00 - 1.85, 22.00 - 2.11          # pin 1'in modul koordinati (sol-ust kose 0,0)


def m(x, y):
    """Modul koordinati (ust gorunus, sol-ust kose) -> footprint (orijin pin 1)."""
    return round(x - X1, 4), round(y - Y1, 4)


L, R = m(0, 0)[0], m(53.00, 0)[0]
T, B = m(0, 0)[1], m(0, 22.00)[1]
RJ_L, RJ_R = m(-4.30, 0)[0], m(17.60, 0)[0]
RJ_T, RJ_B = m(0, 3.00)[1], m(0, 19.00)[1]
MP = [m(4.00, 1.35), m(4.00, 22.00 - 1.35)]
KO = [m(0, 2.50), m(18.50, 2.50), m(18.50, 18.90), m(0, 18.90)]
NETS = {1: 'DIR1', 2: 'DIR2', 3: 'CFG0', 4: 'RUN', 5: 'RXD1', 6: 'RXD2', 7: 'TXD1', 8: 'TXD2',
        9: 'RST1', 10: 'RESET', 11: 'GND', 12: 'GND', 13: '3V3', 14: '3V3', 15: '5V', 16: '5V'}
Z0, ZT = 2.5, 4.1                              # modul alt / ust yuzeyi (ana kart ustu = 0)


def pin_xy(n):
    return (0.0 if n % 2 else -P), -((n - 1) // 2) * P


def footprint():
    f = Footprint(NAME, datasheet='https://www.waveshare.com/wiki/2-CH_UART_TO_ETH',
                  descr='Waveshare 2-CH UART TO ETH (CH9121) modulu, 2x8 2.54 mm header ile '
                        'dogrudan lehimli; P2/P3 mekanik pin (baglantisiz); RJ45 kart kenarindan 4.3 mm tasar')
    f.prop_ref((L + R) / 2, T - 1.3)
    f.prop_value((L + R) / 2, (T + B) / 2 + 3.0)
    s = 0.12
    f.rect(L - s, T - s, R + s, B + s, 'F.SilkS', 0.12)                       # modul siniri
    f.poly([(R + 0.45, 0), (R + 1.05, -0.45), (R + 1.05, 0.45)], 'F.SilkS', 0.12, fill=True)  # pin 1
    f.rect(L, T, R, B, 'F.Fab', 0.1)
    f.rect(RJ_L, RJ_T, RJ_R, RJ_B, 'F.Fab', 0.1)
    f.text('RJ45', (RJ_L + RJ_R) / 2, (RJ_T + RJ_B) / 2, 'F.Fab')
    f.poly([(-P - 1.27, 1.27), (1.27, 1.27), (1.27, -7 * P - 1.27), (-P - 1.27, -7 * P - 1.27),
            (-P - 1.27, 1.27)], 'F.Fab', 0.1)
    f.line((0.27, 1.27), (1.27, 0.27), 'F.Fab', 0.1)
    f.text('${REFERENCE}', (L + R) / 2, (T + B) / 2, 'F.Fab')
    for n, net in NETS.items():
        x, y = pin_xy(n)
        f.text(net, x + (3.4 if n % 2 else -3.4), y, 'F.Fab', 0.6, 0.09,
               justify='left' if n % 2 else 'right')
    f.text('Header spacer 2.5 mm; RJ45 pim cikintisi ~2.2 mm: tarali alanda F.Cu iz/via/parca yok',
           (L + R) / 2, B + 1.6, 'Cmts.User', 0.8, 0.12)
    c = 0.25
    f.poly([(R + c, T - c), (R + c, B + c), (L - c, B + c), (L - c, RJ_B + c), (RJ_L - c, RJ_B + c),
            (RJ_L - c, RJ_T - c), (L - c, RJ_T - c), (L - c, T - c)], 'F.CrtYd', 0.05)
    for n in range(1, 17):
        f.pad_tht(n, *pin_xy(n), PINHEADER_PAD, PINHEADER_DRILL, 'rect' if n == 1 else 'circle')
    for x, y in MP:
        f.pad_tht('MP', x, y, 2.2, 1.4)
    f.keepout(KO, name='RJ45 pim alani')
    f.model(f'${{KIPRJMOD}}/libraries/{LIB}.3dshapes/{NAME}.step')
    return f


def model():
    s = StepBoxes(NAME)
    s.box('PCB', BLUE, L, R, T, B, Z0, ZT)
    s.box('RJ45_overhang', SILVER, RJ_L, L, RJ_T, RJ_B, Z0, Z0 + 15.0)
    s.box('RJ45', SILVER, L, RJ_R, RJ_T, RJ_B, ZT, Z0 + 15.0)
    s.box('RJ45_port', BLACK, RJ_L - 0.1, RJ_L, -14.69, -3.09, Z0 + 2.5, Z0 + 11.5)
    s.box('CH9121', BLACK, -26.75, -16.75, -14.39, -4.39, ZT, ZT + 1.4)    # ust gorunusten
    s.box('AMS1117', BLACK, -11.65, -5.75, -17.29, -12.59, ZT, ZT + 1.6)
    s.box('Header_body', BLACK, -P - 1.27, 1.27, -7 * P - 1.27, 1.27, 0.0, Z0)
    for n in range(1, 17):
        s.pin(f'Pin_{n}', GOLD, *pin_xy(n), -6.0, ZT + 0.5)
    for i, (x, y) in enumerate(MP, 1):
        s.box(f'MP{i}_spacer', BLACK, x - 1.27, x + 1.27, y - 1.27, y + 1.27, 0.0, Z0)
        s.pin(f'MP{i}_pin', GOLD, x, y, -6.0, ZT + 0.5)
    return s


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='hardware/libraries', help='.pretty/.3dshapes ust dizini')
    a = ap.parse_args()
    for d in (f'{LIB}.pretty', f'{LIB}.3dshapes'):
        os.makedirs(os.path.join(a.root, d), exist_ok=True)
    print(footprint().write(os.path.join(a.root, f'{LIB}.pretty', f'{NAME}.kicad_mod')))
    print(model().write(os.path.join(a.root, f'{LIB}.3dshapes', f'{NAME}.step'), stamp='2026-09-23T00:00:00'))
