"""KiCad 10 footprint (.kicad_mod) ureticisi.

Datasheet/olcu ciziminden proje footprint'i cizmek icin: koordinatlari bir
kez hesapla, bu sinifla yaz, `fp_check.py` ile dogrula. Cikti KiCad 10'un
kendi kayit bicimine yakindir (tab girinti, version 20260206); `kicad-cli fp
upgrade` ile dogrulanmis (keepout zone ve MP pedleri korunuyor).

    import sys; sys.path.insert(0, '.claude/skills/kicad-footprint/scripts')
    from kifp import Footprint
    f = Footprint('Modul_X', descr='...', datasheet='https://...')
    f.prop_ref(0, -12); f.prop_value(0, 12)
    f.pad_tht(1, 0, 0, 1.7, 1.0, shape='rect')          # pin 1 kare
    f.pad_tht('MP', -47.15, -18.54, 2.2, 1.4)           # mekanik, net yok
    f.pad_smd(2, 5, 0, 1.5, 0.6)                        # SMD (roundrect)
    f.rect(-1, -1, 1, 1, 'F.SilkS', 0.12)
    f.poly([(0, 0), (1, 1), (0, 1)], 'F.CrtYd', 0.05)
    f.keepout([(0, 0), (5, 0), (5, 5), (0, 5)], name='RJ45 pim alani')
    f.model('${KIPRJMOD}/libraries/Module_Custom.3dshapes/Modul_X.step')
    f.write('hardware/libraries/Module_Custom.pretty/Modul_X.kicad_mod')

Koordinat: mm, x saga, y ASAGI (KiCad), ust gorunus. Orijin sen secersin;
header tabanli modulde pin 1 (KiCad PinHeader gibi).
Satir sonu: yeni kutuphanede LF; mevcut kutuphaneye yazarken komsu
dosyanin satir sonuna uy (crlf=True).
"""
import uuid

# KiCad PinHeader_*_P2.54mm ile ayni THT ped/delik (kicad share footprints'ten okundu)
PINHEADER_PAD, PINHEADER_DRILL = 1.7, 1.0


def num(v):
    """KiCad gibi sayi yaz: 4 ondalik, sondaki sifirlar atilir."""
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


_NS = uuid.UUID('6f1c2a4e-9b1d-4c1e-8a57-3f0d2b7e5c11')   # kifp ad alani (sabit)


def _stroke(w):
    return f'\t\t(stroke\n\t\t\t(width {w})\n\t\t\t(type solid)\n\t\t)\n'


class Footprint:
    def __init__(self, name, descr='', datasheet='', attr='through_hole'):
        self.name, self.items, self._n = name, [], 0
        self.descr, self.datasheet, self.attr = descr, datasheet, attr
        self._ref = self._val = None

    def _u(self):
        """Deterministik uuid (ad + sira): ayni betik ayni dosyayi uretir, yeniden
        uretim git'te fark yaratmaz. uuid4 ile her calisma tum satirlari degistirirdi."""
        self._n += 1
        return str(uuid.uuid5(_NS, f'{self.name}/{self._n}'))

    # --- alanlar
    def _prop(self, name, val, x, y, layer, hide=False, size=1.0):
        h = '\t\t(hide yes)\n' if hide else ''
        return (f'\t(property "{name}" "{val}"\n\t\t(at {num(x)} {num(y)} 0)\n\t\t(layer "{layer}")\n{h}'
                f'\t\t(uuid "{uuid.uuid5(_NS, f"{self.name}/prop/{name}")}")\n\t\t(effects\n'
                f'\t\t\t(font\n\t\t\t\t(size {size} {size})\n'
                f'\t\t\t\t(thickness 0.15)\n\t\t\t)\n\t\t)\n\t)')

    def prop_ref(self, x, y, layer='F.SilkS'):
        self._ref = (x, y, layer)

    def prop_value(self, x, y, layer='F.Fab'):
        self._val = (x, y, layer)

    # --- cizim
    def line(self, a, b, layer, w):
        self.items.append(f'\t(fp_line\n\t\t(start {num(a[0])} {num(a[1])})\n\t\t(end {num(b[0])} {num(b[1])})\n'
                          f'{_stroke(w)}\t\t(layer "{layer}")\n\t\t(uuid "{self._u()}")\n\t)')

    def rect(self, x0, y0, x1, y1, layer, w):
        self.items.append(f'\t(fp_rect\n\t\t(start {num(x0)} {num(y0)})\n\t\t(end {num(x1)} {num(y1)})\n'
                          f'{_stroke(w)}\t\t(fill no)\n\t\t(layer "{layer}")\n\t\t(uuid "{self._u()}")\n\t)')

    def poly(self, pts, layer, w, fill=False):
        xy = ' '.join(f'(xy {num(x)} {num(y)})' for x, y in pts)
        self.items.append(f'\t(fp_poly\n\t\t(pts\n\t\t\t{xy}\n\t\t)\n{_stroke(w)}'
                          f'\t\t(fill {"yes" if fill else "no"})\n\t\t(layer "{layer}")\n\t\t(uuid "{self._u()}")\n\t)')

    def text(self, s, x, y, layer, size=1.0, th=0.15, rot=0, justify=None):
        j = f'\t\t\t(justify {justify})\n' if justify else ''
        self.items.append(f'\t(fp_text user "{s}"\n\t\t(at {num(x)} {num(y)} {rot})\n\t\t(layer "{layer}")\n'
                          f'\t\t(uuid "{self._u()}")\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size {size} {size})\n'
                          f'\t\t\t\t(thickness {th})\n\t\t\t)\n{j}\t\t)\n\t)')

    # --- pedler
    def pad_tht(self, number, x, y, size, drill, shape='circle'):
        """Delikli ped. Mekanik pin icin number='MP' (sembolde pini yok -> net yok;
        PCB guncellemesinde hata vermez). Konumu belirsiz pinde (goruntuden olculmus)
        deligi buyut: 23.09'da +-0.3 mm icin 1.4/2.2 kullanildi."""
        sz = size if isinstance(size, tuple) else (size, size)
        self.items.append(f'\t(pad "{number}" thru_hole {shape}\n\t\t(at {num(x)} {num(y)})\n'
                          f'\t\t(size {num(sz[0])} {num(sz[1])})\n\t\t(drill {num(drill)})\n'
                          f'\t\t(layers "*.Cu" "*.Mask")\n\t\t(remove_unused_layers no)\n'
                          f'\t\t(uuid "{self._u()}")\n\t)')

    def pad_smd(self, number, x, y, w, h, shape='roundrect', rratio=0.25, rot=0):
        rr = f'\t\t(roundrect_rratio {rratio})\n' if shape == 'roundrect' else ''
        at = f'{num(x)} {num(y)}' + (f' {rot}' if rot else '')
        self.items.append(f'\t(pad "{number}" smd {shape}\n\t\t(at {at})\n\t\t(size {num(w)} {num(h)})\n'
                          f'\t\t(layers "F.Cu" "F.Mask" "F.Paste")\n{rr}\t\t(uuid "{self._u()}")\n\t)')

    # --- kurallar
    def keepout(self, pts, name='keepout', layer='F.Cu', tracks=False, vias=False, pads=True,
                copperpour=False, footprints=False):
        """Footprint icine kural alani (izin verilmeyenler False). Ornek: modul
        alti lehim cikintisi (RJ45 ~2.2 mm) ile ara parca (2.5 mm) arasinda
        ~0.3 mm kalinca ust bakirda iz/via/dokum/parca yasak."""
        def ok(v):
            return 'allowed' if v else 'not_allowed'
        xy = ' '.join(f'(xy {num(x)} {num(y)})' for x, y in pts)
        self.items.append(
            f'\t(zone\n\t\t(net 0)\n\t\t(net_name "")\n\t\t(layer "{layer}")\n\t\t(uuid "{self._u()}")\n'
            f'\t\t(name "{name}")\n\t\t(hatch edge 0.5)\n\t\t(connect_pads\n\t\t\t(clearance 0)\n\t\t)\n'
            f'\t\t(min_thickness 0.25)\n\t\t(filled_areas_thickness no)\n'
            f'\t\t(keepout\n\t\t\t(tracks {ok(tracks)})\n\t\t\t(vias {ok(vias)})\n\t\t\t(pads {ok(pads)})\n'
            f'\t\t\t(copperpour {ok(copperpour)})\n\t\t\t(footprints {ok(footprints)})\n\t\t)\n'
            f'\t\t(fill\n\t\t\t(thermal_gap 0.5)\n\t\t\t(thermal_bridge_width 0.5)\n\t\t)\n'
            f'\t\t(polygon\n\t\t\t(pts\n\t\t\t\t{xy}\n\t\t\t)\n\t\t)\n\t)')

    def model(self, path, offset=(0, 0, 0), rotate=(0, 0, 0)):
        """3D model. Model footprint koordinatinda uretildiyse (step_boxes.py)
        offset/rotate 0 kalir; KiCad hazir modellerinde offset/rotate isaretini
        fp_check.py --3d render'i ile dogrula, tahmin etme."""
        o, r = ' '.join(num(v) for v in offset), ' '.join(num(v) for v in rotate)
        self.items.append(f'\t(model "{path}"\n\t\t(offset\n\t\t\t(xyz {o})\n\t\t)\n'
                          f'\t\t(scale\n\t\t\t(xyz 1 1 1)\n\t\t)\n\t\t(rotate\n\t\t\t(xyz {r})\n\t\t)\n\t)')

    # --- cikti
    def text_out(self):
        out = [f'(footprint "{self.name}"\n\t(version 20260206)\n\t(generator "pcbnew")\n'
               f'\t(generator_version "10.0")\n\t(layer "F.Cu")']
        rx, ry, rl = self._ref or (0, -2, 'F.SilkS')
        vx, vy, vl = self._val or (0, 2, 'F.Fab')
        out.append(self._prop('Reference', 'REF**', rx, ry, rl))
        out.append(self._prop('Value', self.name, vx, vy, vl))
        out.append(self._prop('Datasheet', self.datasheet, 0, 0, 'F.Fab', True, 1.27))
        out.append(self._prop('Description', self.descr, 0, 0, 'F.Fab', True, 1.27))
        out.append(f'\t(attr {self.attr})\n\t(duplicate_pad_numbers_are_jumpers no)')
        # KiCad sirasi: cizimler, pedler, zone, model
        order = {'(fp_': 0, '(pad': 1, '(zon': 2, '(mod': 3}
        out += sorted(self.items, key=lambda s: order.get(s.lstrip()[:4], 0))
        return '\n'.join(out) + '\n)\n'

    def write(self, path, crlf=False):
        data = self.text_out()
        if crlf:
            data = data.replace('\n', '\r\n')
        with open(path, 'w', encoding='utf-8', newline='') as fh:
            fh.write(data)
        return path
