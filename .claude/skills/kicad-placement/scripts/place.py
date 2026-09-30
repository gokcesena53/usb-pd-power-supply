"""Yerlesim arama/skor CLI'i (saf python). Her adim state JSON okur/yazar.

    PL=.claude/skills/kicad-placement/scripts; K="sh .claude/skills/kicad-schematic/scripts/kpy"
    $K $PL/pcb_dump.py hardware/gopo.kicad_pcb $T/parts.json
    C="--parts $T/parts.json --cfg .claude/skills/kicad-placement/examples/gopo_rev_c.py"
    $K $PL/place.py score $C                         # baslangic skoru
    $K $PL/place.py pipeline $C --seeds 21,22,23,24 --out $T   # 4 tohum paralel
    $K $PL/place.py score $C $T/best.json            # once/sonra, dongu toplamlari
    $K $PL/place.py pen $C $T/best.json              # kalan kisit ihlalleri

Adimlar (pipeline sirasi):
    anneal  sifirdan (ANCHOR + rastgele) benzetilmis tavlama; ceza agirligi artar.
            --inp S --blocks B: blok bazli yeniden kurma (LNS), digerleri sabit
    legal   kalan ihlalleri: parcanin cevresinde tum yasal slotlari tara, en iyisini sec
            (kucuk rastgele adimlar 20 mm^2 cakismayi cozemiyordu)
    refine  yalniz cezasiz hamle; kritik kenar boyunca cekme + IC'yi kondansatorleriyle
            birlikte kaydirma (legal IC'leri dekuplajindan koparir; bu geri toplar);
            --no-worse: w>=10 kenar baslangic uzunlugunu asamaz (lam*mm)
    sweep   deterministik yerel tarama (parca basina 4 mm, 4 yon; IC gruplari)
    untangle deterministik kesisme cozme: 90/180/270 donme (flip korunur), ayni blok/paket/yuz
            esleriyle yer degistirme; yalniz cezasiz ve maliyeti dusuren. Yuz degisimi (FLIP_DECAPS)
            yalniz legal'de ve ayni yuzde yasal slot yokken: ceza agirligi kurali garanti etmiyordu
            (PD LNS'te C1/C3/C4 yer varken karsi yuze gecti)
    align   0.05 mm izgara + bagli pad merkezi / ayni paket govde kenari hizalama
            (skor artisi <= --tol ise), sonunda hizalama denetimi
"""
import argparse
import json
import math
import os
import random
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from placelib import Model, Engine, load_cfg, load_state, save_state, rot, turn  # noqa: E402


def setup(a, state=None, no_worse=False):
    cfg = load_cfg(a.cfg)
    m = Model(a.parts, cfg)
    st = load_state(state) if state else m.initial_state()
    E = Engine(m, st, baseline=m.initial_state() if no_worse else None, no_worse_w=cfg["NO_WORSE_W"],
               no_worse_lam=50.0 if no_worse else 0.0)
    return m, st, E


def attempt(E, movers, mut, temp, lam=None, strict=False):
    """Hamleyi dene. lam=None: cezasiz olmak zorunda (hard); aksi halde ceza lam ile maliyete eklenir."""
    st = E.st
    old = {r: st[r][:] for r in movers}
    c0 = E.wire(movers); p0 = E.pen_of(movers)
    mut(); E.m.sync_tied(st); E.update(movers)
    p1 = E.pen_of(movers)
    if lam is None:
        ok = p1 <= 1e-9
        if ok:
            d = E.wire(movers) - c0
            ok = d <= 0 or (not strict and random.random() < math.exp(-d / temp))
    else:
        c1 = E.wire(movers)
        if strict:
            ok = p1 < p0 - 1e-9 or (p1 <= p0 + 1e-12 and c1 <= c0)
        else:
            dE = (c1 - c0) + lam * (p1 - p0)
            ok = dE <= 0 or random.random() < math.exp(-dE / temp)
    if not ok:
        for r in movers:
            st[r] = old[r]
        E.m.sync_tied(st); E.update(movers)
    return ok


def tied_with(m, r):
    return [r] + [t for t, (b, _) in m.cfg["TIED"].items() if b == r]


# ------------------------------------------------------------------ anneal
def cmd_anneal(a):
    random.seed(a.seed)
    cfg = load_cfg(a.cfg); m = Model(a.parts, cfg)
    st = load_state(a.inp) if a.inp else m.initial_state()
    sel = set(a.blocks.split(",")) if a.blocks else None
    free = [r for r in m.free if sel is None or m.block_of[r] in sel]
    # --blocks (LNS): yalniz secili bloklar sokulup yeniden kurulur, digerleri sabit engel;
    # merkez bloğun mevcut agirlik merkezi (--inp) -> onayli yerlesim plani korunur
    cen = {}
    for r in free:
        cen.setdefault(m.block_of[r], []).append(st[r][:2])
    cen = {b: (sum(p[0] for p in v) / len(v), sum(p[1] for p in v) / len(v)) for b, v in cen.items()}
    for r in free:
        ax, ay = cen[m.block_of[r]] if a.inp else cfg["ANCHOR"].get(m.block_of[r], (st[r][0], st[r][1]))
        st[r] = [ax + random.uniform(-a.spread, a.spread), ay + random.uniform(-a.spread, a.spread),
                 (st[r][2] & 4) | random.randrange(4)]
    slide = [r for r in cfg["SLIDE"] if sel is None or m.block_of[r] in sel]
    if not a.inp:
        for r in slide:
            ax, lo, hi = cfg["SLIDE"][r]; st[r][0 if ax == "x" else 1] = (lo + hi) / 2
    m.sync_tied(st)
    E = Engine(m, st)
    blk = {}
    for r in free:
        blk.setdefault(m.block_of[r], []).append(r)
    sg = {}
    for r in free:
        sg.setdefault((m.block_of[r], m.P[r]["fp"], m.P[r]["side"]), []).append(r)
    swaps = [g for g in sg.values() if len(g) > 1]
    T0, T1, L0, L1 = 40.0, 0.03, 0.3, 300.0
    t0 = time.time()
    for it in range(a.iters):
        f = it / a.iters
        temp = T0 * (T1 / T0) ** f
        lam = L0 * (L1 / L0) ** min(1.0, f * 1.15)
        sig = 0.08 + 7.0 * (temp / T0) ** 0.6
        u = random.random()
        if u < 0.04:
            movers = blk[random.choice(list(blk))]; dx, dy = random.gauss(0, sig), random.gauss(0, sig)

            def mut():
                for r in movers:
                    st[r][0] += dx; st[r][1] += dy
        elif u < 0.10 and swaps:
            p, q = random.sample(random.choice(swaps), 2); movers = [p, q]

            def mut():
                st[p][0], st[p][1], st[q][0], st[q][1] = st[q][0], st[q][1], st[p][0], st[p][1]
        elif u < 0.16 and slide:
            r = random.choice(slide); ax, lo, hi = cfg["SLIDE"][r]; i = 0 if ax == "x" else 1
            movers = tied_with(m, r); step = random.gauss(0, sig)

            def mut():
                st[r][i] = min(hi, max(lo, st[r][i] + step))
        else:
            r = random.choice(free); movers = [r]
            if random.random() < 0.15:
                dk = random.choice((1, 2, 3)); s2 = sig * 0.3 if random.random() < 0.5 else 0
                dx, dy = random.gauss(0, s2) if s2 else 0, random.gauss(0, s2) if s2 else 0
            else:
                dk = 0; dx, dy = random.gauss(0, sig), random.gauss(0, sig)

            def mut():
                st[r][2] = turn(st[r][2], dk); st[r][0] += dx; st[r][1] += dy
        attempt(E, movers, mut, temp, lam=lam)
        if it % max(1, a.iters // 10) == 0:
            print(f"it {it} T={temp:.3f} lam={lam:.1f} maliyet={E.total():.1f} ceza={E.pen_of(m.refs):.2f} t={time.time()-t0:.0f}s", flush=True)
    p = E.pen_of(m.refs)
    print(f"anneal bitti maliyet={E.total():.1f} ceza={p:.3f}")
    save_state(a.out, st, pen=p)


# ------------------------------------------------------------------ legal
def cmd_legal(a):
    m, st, E = setup(a, a.inp)
    pin = set(a.pin.split(",")) if a.pin else set()
    if a.blocks:                                     # LNS: secili bloklar disindaki her sey sabit
        pin |= {r for r in list(m.free) + list(m.cfg["SLIDE"]) if m.block_of[r] not in a.blocks.split(",")}
    free = [r for r in m.free if r not in pin]

    def relocate(r):
        """Once mevcut yuzde slot ara; yoksa ve parca FLIP_DECAPS ile cevrilebiliyorsa karsi yuzde."""
        x0, y0, k0 = st[r]; best = None
        for fb in [k0 & 4] + ([(k0 & 4) ^ 4] if r in m.flippable else []):
            for rad, step in ((3, 0.25), (8, 0.5), (16, 1.0)):
                n = int(rad / step)
                for ix in range(-n, n + 1):
                    for iy in range(-n, n + 1):
                        for k in range(4):
                            st[r] = [x0 + ix * step, y0 + iy * step, fb | k]; E.update([r])
                            if E.pen_of([r]) > 1e-9:
                                continue
                            c = E.wire([r])
                            if best is None or c < best[0]:
                                best = (c, st[r][:])
                if best:
                    break
            if best:
                break
        st[r] = best[1] if best else [x0, y0, k0]; E.update([r])
        return best is not None

    def relocate_slide(r):
        ax, lo, hi = m.cfg["SLIDE"][r]; i = 0 if ax == "x" else 1
        movers = tied_with(m, r); orig = st[r][i]; best = None
        for s in range(int(round((hi - lo) / 0.05)) + 1):
            st[r][i] = lo + s * 0.05; m.sync_tied(st); E.update(movers)
            if E.pen_of(movers) <= 1e-9:
                c = E.wire(movers)
                if best is None or c < best[0]:
                    best = (c, st[r][i])
        if best is None:
            # slot yok: karttaki (daha once yasal) konuma don; onu kapatan serbest parcalar
            # sonraki turda tasinir (TASK-115'te J7 icin elle yapilan duzeltme)
            orig = m.P[r]["y0" if i else "x0"]
        st[r][i] = best[1] if best else orig; m.sync_tied(st); E.update(movers)
        return best is not None

    for rnd in range(10):
        off = E.offenders()
        if not off:
            break
        bad = []
        for key in sorted(off, key=lambda k: -off[k]):
            for r in key:
                r = m.cfg["TIED"].get(r, (r,))[0]
                if (r in free or r in m.cfg["SLIDE"]) and r not in bad and r not in pin:
                    bad.append(r)
        print(f"tur {rnd}: ceza={sum(off.values()):.3f} yeniden yerlesen {bad}", flush=True)
        for r in bad:
            if E.pen_of(tied_with(m, r)) < 1e-9:
                continue
            if not (relocate_slide(r) if r in m.cfg["SLIDE"] else relocate(r)):
                print("  yasal slot yok:", r)
    p = E.pen_of(m.refs)
    print(f"legal ceza={p:.4f}")
    save_state(a.out, st, pen=p)
    return p


# ------------------------------------------------------------------ refine
def cmd_refine(a):
    random.seed(a.seed)
    m, st, E = setup(a, a.inp, no_worse=a.no_worse)
    if E.pen_of(m.refs) > 1e-9:
        raise SystemExit("refine cezasiz baslangic ister; once legal calistir")
    P = m.P
    free = [r for r in m.free if not a.blocks or m.block_of[r] in a.blocks.split(",")]
    fset = set(free)
    sat = {}
    for c in m.crit:
        ra, rb = c["a"][0], c["b"][0]
        big, small = (ra, rb) if len(P[ra]["pads"]) >= len(P[rb]["pads"]) else (rb, ra)
        if big in fset and small in fset:
            sat.setdefault(big, set()).add(small)
    ks = [k for k, c in enumerate(m.crit) if c["a"][0] in fset or c["b"][0] in fset]
    T0, T1 = 3.0, 0.01
    t0 = time.time()
    print(f"refine basla maliyet={E.total():.1f}")
    for it in range(a.iters):
        temp = T0 * (T1 / T0) ** (it / a.iters)
        sig = 0.1 + 2.5 * (temp / T0) ** 0.5
        u = random.random()
        if u < 0.35 and ks:                             # agir kritik kenar boyunca cekme
            k = max(random.sample(ks, min(6, len(ks))), key=lambda k: m.crit[k]["w"] * m.crit_len(st, k)[0])
            c = m.crit[k]; _, i, j = m.crit_len(st, k)
            ra, rb = c["a"][0], c["b"][0]
            if ra in fset and (len(P[ra]["pads"]) <= len(P[rb]["pads"]) or rb not in fset):
                mv, pi, tr, tj = ra, i, rb, j
            elif rb in fset:
                mv, pi, tr, tj = rb, j, ra, i
            else:
                continue
            kk = (st[mv][2] & 4) | random.randrange(4)  # yuz degisimi yalniz legal'de (yer yoksa)
            tx, ty = m.pad_xy(st, tr, tj)
            dx, dy = rot(P[mv]["pads"][pi]["dx"], P[mv]["pads"][pi]["dy"], kk)
            ang, rr = random.uniform(0, 2 * math.pi), random.uniform(0.4, 2.5)
            nx, ny = tx - dx + rr * math.cos(ang), ty - dy + rr * math.sin(ang)

            def mut():
                st[mv][:] = [nx, ny, kk]
            attempt(E, [mv], mut, temp)
        elif u < 0.5 and sat:                           # IC + uydulari birlikte
            big = random.choice(list(sat)); movers = [big] + sorted(sat[big])
            dx, dy = random.gauss(0, sig), random.gauss(0, sig)

            def mut():
                for r in movers:
                    st[r][0] += dx; st[r][1] += dy
            attempt(E, movers, mut, temp)
        else:
            r = random.choice(free)
            dk = random.choice((1, 2, 3)) if random.random() < 0.2 else 0
            dx, dy = (0, 0) if dk else (random.gauss(0, sig), random.gauss(0, sig))

            def mut():
                st[r][2] = turn(st[r][2], dk); st[r][0] += dx; st[r][1] += dy
            attempt(E, [r], mut, temp)
        if it % max(1, a.iters // 8) == 0:
            print(f"it {it} T={temp:.3f} maliyet={E.total():.1f} t={time.time()-t0:.0f}s", flush=True)
    p = E.pen_of(m.refs)
    print(f"refine bitti maliyet={E.total():.1f} ceza={p:.4f}")
    save_state(a.out, st, pen=p)


# ------------------------------------------------------------------ sweep
def cmd_sweep(a):
    m, st, E = setup(a, a.inp, no_worse=a.no_worse)
    P = m.P; fset = set(m.free)
    maxw = {r: max([m.crit[k]["w"] for k in m.crit_of.get(r, [])] or [1]) for r in m.free}
    order = sorted(m.free, key=lambda r: (-maxw[r], r))
    sat = {}
    for c in m.crit:
        ra, rb = c["a"][0], c["b"][0]
        big, small = (ra, rb) if len(P[ra]["pads"]) >= len(P[rb]["pads"]) else (rb, ra)
        if big in fset and small in fset and len(P[big]["pads"]) > 3:
            sat.setdefault(big, set()).add(small)
    t0 = time.time()
    for rnd in range(a.rounds):
        gain = 0.0
        for big, sm in sat.items():
            movers = [big] + sorted(sm); base = {r: st[r][:] for r in movers}
            c0 = E.wire(movers); best = (c0, 0, 0)
            for ix in range(-6, 7):
                for iy in range(-6, 7):
                    for r in movers:
                        st[r] = [base[r][0] + ix * 0.5, base[r][1] + iy * 0.5, base[r][2]]
                    E.update(movers)
                    if E.pen_of(movers) <= 1e-9:
                        c = E.wire(movers)
                        if c < best[0] - 1e-6:
                            best = (c, ix, iy)
            for r in movers:
                st[r] = [base[r][0] + best[1] * 0.5, base[r][1] + best[2] * 0.5, base[r][2]]
            E.update(movers); gain += c0 - best[0]
        for r in order:
            x0, y0, k0 = st[r]; c0 = E.wire([r]); best = (c0, st[r][:])
            for ix in range(-16, 17):
                for iy in range(-16, 17):
                    for k in range(4):
                        st[r] = [x0 + ix * 0.25, y0 + iy * 0.25, (k0 & 4) | k]; E.update([r])
                        if E.pen_of([r]) <= 1e-9:
                            c = E.wire([r])
                            if c < best[0] - 1e-6:
                                best = (c, st[r][:])
            st[r] = best[1]; E.update([r]); gain += c0 - best[0]
        print(f"sweep tur {rnd}: kazanc {gain:.1f} toplam {E.total():.1f} t={time.time()-t0:.0f}s", flush=True)
        if gain < 1.0:
            break
    save_state(a.out, st, pen=E.pen_of(m.refs))


# ------------------------------------------------------------------ untangle
def cmd_untangle(a):
    m, st, E = setup(a, a.inp, no_worse=a.no_worse)
    if E.pen_of(m.refs) > 1e-9:
        raise SystemExit("untangle cezasiz baslangic ister; once legal calistir")
    P = m.P
    free = [r for r in m.free if not a.blocks or m.block_of[r] in a.blocks.split(",")]
    t0 = time.time()

    def try_states(movers, cands):
        """cands: [{ref: state}] ; cezasiz ve en dusuk wire olani uygula, kazanci dondur."""
        old = {r: st[r][:] for r in movers}; c0 = E.wire(movers); best = (c0, None)
        for cd in cands:
            for r, v in cd.items():
                st[r] = v[:]
            E.update(movers)
            if E.pen_of(movers) <= 1e-9:
                c = E.wire(movers)
                if c < best[0] - 1e-6:
                    best = (c, {r: st[r][:] for r in movers})
            for r in movers:
                st[r] = old[r][:]
            E.update(movers)
        if best[1]:
            for r, v in best[1].items():
                st[r] = v
            E.update(movers)
        return c0 - best[0]

    for rnd in range(a.rounds):
        gain, n = 0.0, 0
        for r in free:
            x, y, k = st[r]
            ks = [turn(k, d) for d in (1, 2, 3)]      # flip yok: kullanici kurali "yalniz yer yoksa"
            g = try_states([r], [{r: [x, y, kk]} for kk in ks])
            gain += g; n += g > 0
        for i, r in enumerate(free):
            for o in free[i + 1:]:
                if P[o]["fp"] != P[r]["fp"] or m.block_of[o] != m.block_of[r] or m.side_of(st, o) != m.side_of(st, r):
                    continue
                if math.hypot(st[r][0] - st[o][0], st[r][1] - st[o][1]) > a.swap_mm:
                    continue
                (xr, yr, kr), (xo, yo, ko) = st[r], st[o]
                cands = [{r: [xo, yo, kr], o: [xr, yr, ko]}, {r: [xo, yo, ko], o: [xr, yr, kr]},
                         {r: [xo, yo, turn(ko, 2)], o: [xr, yr, turn(kr, 2)]}]
                g = try_states([r, o], cands)
                gain += g; n += g > 0
        X = m.crossings(st)[0]
        print(f"untangle tur {rnd}: hamle {n}, kazanc {gain:.1f}, kesisme {X}, t={time.time()-t0:.0f}s", flush=True)
        if gain < 1.0:
            break
    p = E.pen_of(m.refs)
    save_state(a.out, st, pen=p)


# ------------------------------------------------------------------ align
def cmd_align(a):
    m, st, E = setup(a, a.inp)
    P = m.P

    def try_set(r, x, y, tol):
        old = st[r][:]; p0 = E.pen_of([r]); c0 = E.wire([r])
        st[r][0], st[r][1] = x, y; E.update([r])
        if E.pen_of([r]) <= p0 + 1e-9 and E.wire([r]) - c0 <= tol:
            return True
        st[r] = old; E.update([r])
        return False

    snapped = sum(try_set(r, round(st[r][0] / a.grid) * a.grid, round(st[r][1] / a.grid) * a.grid, 0.05) for r in m.free)
    two = [r for r in m.free if len(P[r]["pads"]) == 2]

    def partners(r):
        """(r pad, diger ref, pad): kritik + MST kenarlari; yalniz AYNI YUZDEKI esler hizalanir."""
        out = []
        for k in m.crit_of.get(r, []):
            _, i, j = m.crit_len(st, k); c = m.crit[k]
            out.append((i, c["b"][0], j) if c["a"][0] == r else (j, c["a"][0], i))
        for n in m.nets_of[r]:
            for (ra, i), (rb, j), _ in m.net_mst(st, n, True)[1]:
                if ra == r and rb != r: out.append((i, rb, j))
                elif rb == r and ra != r: out.append((j, ra, i))
        return [t for t in out if m.side_of(st, t[1]) == m.side_of(st, r)]

    def bb(r):
        rs = E.R[r]
        return (min(q[0] for q in rs), min(q[1] for q in rs), max(q[2] for q in rs), max(q[3] for q in rs))

    def neighbours(r, o):
        if o == r or P[o]["fp"] != P[r]["fp"] or m.side_of(st, o) != m.side_of(st, r) or m.block_of[o] != m.block_of[r] \
                or st[o][2] % 2 != st[r][2] % 2:
            return None
        p, q = bb(r), bb(o)
        cx, cy = ((p[0] + p[2]) - (q[0] + q[2])) / 2, ((p[1] + p[3]) - (q[1] + q[3])) / 2
        if math.hypot(cx, cy) > 4:
            return None
        return (p[1] - q[1], "y") if abs(cx) > abs(cy) else (p[0] - q[0], "x")   # yan yana: ust kenar; ust uste: sol kenar

    moves = 0
    for _ in range(6):
        changed = 0
        for r in two:
            for i, o, j in partners(r):
                (xa, ya), (xb, yb) = m.pad_xy(st, r, i), m.pad_xy(st, o, j)
                dx, dy = xb - xa, yb - ya
                if abs(dx) < 1e-3 or abs(dy) < 1e-3:
                    continue
                if abs(dx) < 1.2 and abs(dy) > abs(dx):
                    changed += try_set(r, st[r][0] + dx, st[r][1], a.tol)
                elif abs(dy) < 1.2 and abs(dx) > abs(dy):
                    changed += try_set(r, st[r][0], st[r][1] + dy, a.tol)
        for r in two:
            for o in two:
                nb = neighbours(r, o)
                if nb and 1e-3 < abs(nb[0]) < 0.8:
                    changed += try_set(r, st[r][0] - (nb[0] if nb[1] == "x" else 0), st[r][1] - (nb[0] if nb[1] == "y" else 0), a.tol)
        moves += changed
        if not changed:
            break
    # denetim: kalan kaymalar raporlanir (goruntuden "tam hizali" denmez)
    edge_ok, edge_res = 0, []
    for x, r in enumerate(two):
        for o in two[x + 1:]:
            nb = neighbours(r, o)
            if nb:
                if abs(nb[0]) < 0.01: edge_ok += 1
                elif abs(nb[0]) < 0.8: edge_res.append((r, o, round(abs(nb[0]), 3)))
    pad_ok, pad_res = 0, []
    for r in two:
        for i, o, j in partners(r):
            (xa, ya), (xb, yb) = m.pad_xy(st, r, i), m.pad_xy(st, o, j)
            if math.hypot(xa - xb, ya - yb) <= 3:
                off = min(abs(xa - xb), abs(ya - yb))
                if off < 0.01: pad_ok += 1
                else: pad_res.append((f"{r}.{P[r]['pads'][i]['n']}", f"{o}.{P[o]['pads'][j]['n']}", round(off, 3)))
    p = E.pen_of(m.refs)
    print(f"izgara {snapped}/{len(m.free)}; hizalama hamlesi {moves}; ceza={p:.4f}")
    print(f"govde kenari: hizali {edge_ok}, kalan {len(edge_res)} {edge_res[:10]}")
    print(f"<=3 mm ayni yuz pad baglantisi: hizali {pad_ok}, kalan {len(pad_res)}")
    save_state(a.out, st, pen=p, align={"edge_ok": edge_ok, "edge_res": edge_res, "pad_ok": pad_ok, "pad_res": pad_res})


# ------------------------------------------------------------------ score / pen
def cmd_score(a):
    cfg = load_cfg(a.cfg); m = Model(a.parts, cfg)
    b = m.report(m.initial_state())
    if not a.state:
        print(f"S={b['S']:.1f} (ic {b['S_int']:.1f} / arasi {b['S_inter']:.1f}); L={b['L']:.1f}; kritik kenar {len(m.crit)}")
        print(f"kesisme {b['X']}, via kenari {b['V']}, dekuplaj yuz ihlali {b['decap_side']}, kopuk {b['far']}")
        for c in sorted(b["crit"], key=lambda c: -c[2] * c[3])[:12]:
            print(f"  w{c[2]} {c[0]}-{c[1]}: {c[3]:.2f}  ({c[4]})")
        return
    st = load_state(a.state); r = m.report(st)
    print(f"{'':8s} {'once':>9s} {'sonra':>9s}")
    for k in ("S", "S_int", "S_inter", "L", "L_int", "L_inter"):
        print(f"{k:8s} {b[k]:9.1f} {r[k]:9.1f}  ({100 * (r[k] - b[k]) / b[k]:+.0f}%)")
    for k in sorted(set(b["blocks"]) | set(r["blocks"])):
        print(f"  blok {k:9s} {b['blocks'].get(k, 0):8.1f} {r['blocks'].get(k, 0):8.1f}")
    for name, keys in cfg["LOOP_GROUPS"].items():
        tb = sum(x[3] for x in b["crit"] if any(x[0].startswith(p) for p in keys))
        ta = sum(x[3] for x in r["crit"] if any(x[0].startswith(p) for p in keys))
        print(f"  dongu {name:44s} {tb:7.1f} -> {ta:7.1f} mm ({100 * (ta - tb) / max(tb, 1e-9):+.0f}%)")
    worse = [(x[0], x[1], x[2], y[3], x[3]) for x, y in zip(r["crit"], b["crit"]) if x[3] > y[3] + 0.5]
    print("uzayan kritik kenarlar (>0.5 mm):", worse)
    print(f"ayni yuz kesisme {b['X']} -> {r['X']}; via gerektiren kenar {b['V']} -> {r['V']}")
    print("en cok kesisen netler:", sorted(r["X_net"].items(), key=lambda t: -t[1])[:10])
    print(f"dekuplaj IC'den farkli yuzde: {b['decap_side']} -> {r['decap_side']}; flip: {r['flipped']}")
    print(f"kopuk (en yakin bagli pad > FAR_MM): {len(b['far'])} -> {len(r['far'])} {r['far'][:15]}")
    if a.json:
        json.dump(r, open(a.json, "w", encoding="utf-8"), indent=0)


def cmd_pen(a):
    m, st, E = setup(a, a.state)
    off = E.offenders()
    print(f"toplam ceza {sum(off.values()):.3f}, cift {len(off)}")
    for k, v in sorted(off.items(), key=lambda kv: -kv[1])[:40]:
        print(" ", k, round(v, 3))


# ------------------------------------------------------------------ pipeline
def cmd_pipeline(a):
    """Her tohum icin anneal -> legal -> refine(--no-worse) -> untangle -> align; paralel. En dusuk S'li yasal sonuc best.json."""
    me = os.path.abspath(__file__); py = sys.executable
    base = ["--parts", a.parts, "--cfg", a.cfg]
    os.makedirs(a.out, exist_ok=True)
    procs = []
    for s in a.seeds.split(","):
        o = lambda n: os.path.join(a.out, f"{n}{s}.json")
        chain = [["anneal", "--seed", s, "--iters", str(a.iters), "--out", o("p")],
                 ["legal", o("p"), o("l")],
                 ["refine", o("l"), o("r"), "--iters", str(a.refine_iters), "--seed", s, "--no-worse"],
                 ["untangle", o("r"), o("u"), "--no-worse"],
                 ["align", o("u"), o("a")]]
        script = " && ".join(" ".join([f'"{py}"', f'"{me}"', c[0]] + [f'"{x}"' for x in base + c[1:]]) for c in chain)
        log = open(os.path.join(a.out, f"log{s}.txt"), "w", encoding="utf-8")
        procs.append((s, subprocess.Popen(script, shell=True, stdout=log, stderr=subprocess.STDOUT)))
    best = None
    cfg = load_cfg(a.cfg); m = Model(a.parts, cfg)
    for s, p in procs:
        p.wait()
        f = os.path.join(a.out, f"a{s}.json")
        if p.returncode or not os.path.exists(f):
            print(f"tohum {s}: basarisiz (log{s}.txt)"); continue
        d = json.load(open(f, encoding="utf-8"))
        S = m.report(d["state"])["S"]
        print(f"tohum {s}: ceza={d['pen']:.4f} S={S:.1f}")
        if d["pen"] <= 1e-9 and (best is None or S < best[0]):
            best = (S, f)
    if best:
        import shutil
        shutil.copy(best[1], os.path.join(a.out, "best.json"))
        print("best.json <-", best[1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def sp(name, fn, *pos):
        p = sub.add_parser(name)
        p.add_argument("--parts", required=True); p.add_argument("--cfg", required=True)
        for x in pos:
            p.add_argument(x)
        p.set_defaults(fn=fn)
        return p
    p = sp("anneal", cmd_anneal); p.add_argument("--seed", type=int, default=1); p.add_argument("--iters", type=int, default=180000); p.add_argument("--out", required=True)
    p.add_argument("--inp", default="", help="baslangic state (LNS); yoksa kart + ANCHOR")
    p.add_argument("--blocks", default="", help="yalniz bu bloklari sok/yeniden kur (virgul)"); p.add_argument("--spread", type=float, default=5.0)
    p = sp("legal", cmd_legal, "inp", "out"); p.add_argument("--pin", default=""); p.add_argument("--blocks", default="")
    p = sp("refine", cmd_refine, "inp", "out"); p.add_argument("--iters", type=int, default=300000); p.add_argument("--seed", type=int, default=1)
    p.add_argument("--blocks", default=""); p.add_argument("--no-worse", action="store_true")
    p = sp("sweep", cmd_sweep, "inp", "out"); p.add_argument("--rounds", type=int, default=3); p.add_argument("--no-worse", action="store_true")
    p = sp("untangle", cmd_untangle, "inp", "out"); p.add_argument("--rounds", type=int, default=4)
    p.add_argument("--blocks", default=""); p.add_argument("--no-worse", action="store_true"); p.add_argument("--swap-mm", type=float, default=6.0)
    p = sp("align", cmd_align, "inp", "out"); p.add_argument("--grid", type=float, default=0.05); p.add_argument("--tol", type=float, default=0.3)
    p = sp("score", cmd_score); p.add_argument("state", nargs="?"); p.add_argument("--json", default="")
    sp("pen", cmd_pen, "state")
    p = sp("pipeline", cmd_pipeline); p.add_argument("--seeds", default="21,22,23,24"); p.add_argument("--out", required=True)
    p.add_argument("--iters", type=int, default=180000); p.add_argument("--refine-iters", type=int, default=300000)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
