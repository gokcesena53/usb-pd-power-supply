"""Renkli eksen hizali kutulardan STEP (AP214) modeli - bagimliliksiz.

Uretici 3D model yayinlamiyorsa (Waveshare 2-CH UART TO ETH) olcu cizimindeki
zarfi kutularla modelle: kart, konnektor, entegre, header, pinler. cadquery/
FreeCAD gerekmez (Windows'ta kurulu degil, cadquery yuzlerce MB). KiCad render
ve `pcb export step` ile dogrulandi: renkler (STYLED_ITEM) korunur.

    import sys; sys.path.insert(0, '.claude/skills/kicad-footprint/scripts')
    from step_boxes import StepBoxes, BLUE, SILVER, BLACK, GOLD
    s = StepBoxes('Modul_X')
    s.box('PCB', BLUE, -51.15, 1.85, -19.89, 2.11, 2.5, 4.1)   # x0 x1 y0 y1 z0 z1
    s.pin_grid(...)  # ya da dongude s.box(...)
    s.write('hardware/libraries/Module_Custom.3dshapes/Modul_X.step')

Koordinat sozlesmesi (KiCad modeli, render ile dogrulandi):
  - x, y FOOTPRINT koordinatinda verilir (mm, y ASAGI); yazarken STEP Y = -y.
  - z yukari, z = 0 ANA KARTIN UST YUZEYI; kart altina inen pinler negatif z.
  - Boylece footprint'teki (model ...) offset/rotate 0 kalir; KiCad hazir
    modelinin offset/rotate isaretini tahmin etme derdi olmaz.
Kutular ust uste binebilir (pin kart icinden gecer); render/STEP disa aktarimi
sorun cikarmaz, ama boolean birlesim yapilmaz.
"""

BLUE, GREEN = (0.05, 0.25, 0.65), (0.05, 0.35, 0.15)
SILVER, BLACK, GOLD, WHITE = (0.78, 0.78, 0.80), (0.08, 0.08, 0.08), (0.85, 0.68, 0.20), (0.95, 0.95, 0.95)

# Kutu yuzleri: kose indeksi bit0=x, bit1=y, bit2=z. Kenar dongusu disaridan
# bakinca saat yonu tersine (normal disari, sag el kurali ile dogrulandi).
_FACES = [((0, 2, 3, 1), (0., 0., -1.)), ((4, 5, 7, 6), (0., 0., 1.)),
          ((0, 1, 5, 4), (0., -1., 0.)), ((2, 6, 7, 3), (0., 1., 0.)),
          ((0, 4, 6, 2), (-1., 0., 0.)), ((1, 3, 7, 5), (1., 0., 0.))]


def _r(v):
    s = f'{v:.4f}'.rstrip('0')          # STEP gercek sayisi: '1.' ve '-0.5' gecerli
    return s


class StepBoxes:
    def __init__(self, product):
        self.product, self.boxes = product, []

    def box(self, name, color, x0, x1, y0, y1, z0, z1):
        """Footprint koordinatinda (y asagi) kutu; x0<x1, y0<y1, z0<z1."""
        assert x0 < x1 and y0 < y1 and z0 < z1, (name, x0, x1, y0, y1, z0, z1)
        self.boxes.append((name, color, x0, x1, y0, y1, z0, z1))

    def pin(self, name, color, cx, cy, z0, z1, w=0.64):
        """Kare kesitli pin (2.54 mm header pini 0.64 mm)."""
        self.box(name, color, cx - w / 2, cx + w / 2, cy - w / 2, cy + w / 2, z0, z1)

    def cyl(self, name, color, cx, cy, r, z0, z1, n=6):
        """Dik silindiri n seritle ORTER (kapsayan) sekilde yaklastir: her serit
        genisligi merkeze yakin kenarindaki kiris. Cakisma/yukseklik kontrolu
        icin guvenli taraf; gorunus basamakli olur."""
        h = 2 * r / n
        for i in range(n):
            ya, yb = cy - r + i * h, cy - r + (i + 1) * h
            d = min(abs(ya - cy), abs(yb - cy)) if (ya - cy) * (yb - cy) > 0 else 0.0
            w = (r * r - d * d) ** 0.5
            self.box(f'{name}_{i}', color, cx - w, cx + w, ya, yb, z0, z1)

    def text(self, stamp='2026-01-01T00:00:00'):
        lines = []

        def add(s):
            lines.append(f'#{len(lines) + 1}={s};')
            return f'#{len(lines)}'
        app = add("APPLICATION_CONTEXT('core data for automotive mechanical design processes')")
        add(f"APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,{app})")
        pctx = add(f"PRODUCT_CONTEXT('',{app},'mechanical')")
        prod = add(f"PRODUCT('{self.product}','{self.product}','',({pctx}))")
        pdf = add(f"PRODUCT_DEFINITION_FORMATION('','',{prod})")
        pdc = add(f"PRODUCT_DEFINITION_CONTEXT('part definition',{app},'design')")
        pd = add(f"PRODUCT_DEFINITION('design','',{pdf},{pdc})")
        pds = add(f"PRODUCT_DEFINITION_SHAPE('','',{pd})")
        ul = add("( LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.) )")
        ua = add("( NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.) )")
        us = add("( NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT() )")
        unc = add(f"UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE(1.E-07),{ul},'distance_accuracy_value',"
                  f"'confusion accuracy')")
        ctx = add(f"( GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT(({unc})) "
                  f"GLOBAL_UNIT_ASSIGNED_CONTEXT(({ul},{ua},{us})) "
                  f"REPRESENTATION_CONTEXT('Context #1','3D Context with UNIT and UNCERTAINTY') )")
        dirs = {}

        def direction(d):
            if d not in dirs:
                dirs[d] = add(f"DIRECTION('',({_r(d[0])},{_r(d[1])},{_r(d[2])}))")
            return dirs[d]

        def point(p):
            return add(f"CARTESIAN_POINT('',({_r(p[0])},{_r(p[1])},{_r(p[2])}))")
        origin = add(f"AXIS2_PLACEMENT_3D('',{point((0, 0, 0))},{direction((0., 0., 1.))},"
                     f"{direction((1., 0., 0.))})")

        def solid(name, x0, x1, y0, y1, z0, z1):
            P = [(x1 if i & 1 else x0, y1 if i & 2 else y0, z1 if i & 4 else z0) for i in range(8)]
            V = [add(f"VERTEX_POINT('',{point(p)})") for p in P]
            edges = {}

            def edge(a, b):
                key = (min(a, b), max(a, b))
                if key not in edges:
                    i, j = key
                    d = tuple(float(P[j][k] - P[i][k]) for k in range(3))
                    L = max(abs(c) for c in d)
                    vec = add(f"VECTOR('',{direction(tuple(c / L for c in d))},{_r(L)})")
                    ln = add(f"LINE('',{point(P[i])},{vec})")
                    edges[key] = add(f"EDGE_CURVE('',{V[i]},{V[j]},{ln},.T.)")
                return edges[key], (a, b) == key
            fids = []
            for loop, nrm in _FACES:
                oes = []
                for k in range(4):
                    e, fwd = edge(loop[k], loop[(k + 1) % 4])
                    oes.append(add(f"ORIENTED_EDGE('',*,*,{e},{'.T.' if fwd else '.F.'})"))
                el = add(f"EDGE_LOOP('',({','.join(oes)}))")
                fb = add(f"FACE_OUTER_BOUND('',{el},.T.)")
                ref = (1., 0., 0.) if abs(nrm[0]) < 0.5 else (0., 1., 0.)
                ax = add(f"AXIS2_PLACEMENT_3D('',{point(P[loop[0]])},{direction(nrm)},{direction(ref)})")
                pl = add(f"PLANE('',{ax})")
                fids.append(add(f"ADVANCED_FACE('',({fb}),{pl},.T.)"))
            sh = add(f"CLOSED_SHELL('',({','.join(fids)}))")
            return add(f"MANIFOLD_SOLID_BREP('{name}',{sh})")
        styles, solids, styled = {}, [], []

        def style(col):
            if col not in styles:
                c = add(f"COLOUR_RGB('',{_r(col[0])},{_r(col[1])},{_r(col[2])})")
                fasc = add(f"FILL_AREA_STYLE_COLOUR('',{c})")
                fas = add(f"FILL_AREA_STYLE('',({fasc}))")
                ssfa = add(f"SURFACE_STYLE_FILL_AREA({fas})")
                sss = add(f"SURFACE_SIDE_STYLE('',({ssfa}))")
                ssu = add(f"SURFACE_STYLE_USAGE(.BOTH.,{sss})")
                styles[col] = add(f"PRESENTATION_STYLE_ASSIGNMENT(({ssu}))")
            return styles[col]
        for name, col, x0, x1, y0, y1, z0, z1 in self.boxes:
            s = solid(name, x0, x1, -y1, -y0, z0, z1)          # STEP Y = -footprint y
            solids.append(s)
            styled.append(add(f"STYLED_ITEM('color',({style(col)}),{s})"))
        shape = add(f"ADVANCED_BREP_SHAPE_REPRESENTATION('',({origin},{','.join(solids)}),{ctx})")
        add(f"SHAPE_DEFINITION_REPRESENTATION({pds},{shape})")
        add(f"MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION('',({','.join(styled)}),{ctx})")
        hdr = (f"ISO-10303-21;\nHEADER;\nFILE_DESCRIPTION(('{self.product} simplified model'),'2;1');\n"
               f"FILE_NAME('{self.product}.step','{stamp}',('gopo'),(''),'step_boxes.py','','');\n"
               "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));\nENDSEC;\nDATA;\n")
        return hdr + '\n'.join(lines) + '\nENDSEC;\nEND-ISO-10303-21;\n'

    def write(self, path, stamp='2026-01-01T00:00:00'):
        """Sabit zaman damgasi: ayni girdi ayni dosyayi uretir (git diff temiz)."""
        with open(path, 'w', encoding='ascii', newline='\n') as fh:
            fh.write(self.text(stamp))
        return path
