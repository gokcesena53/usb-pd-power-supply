"""Yerlesim modeli: parca geometrisi, agirlikli skor grafigi ve kisit motoru (saf python).

pcbnew GEREKMEZ: `pcb_dump.py` karti JSON'a doker, bu modul yalniz JSON ve
proje config'i (examples/gopo_rev_c.py gibi) okur. numpy/matplotlib yok; KiCad'in
Linux python'unda da Windows python'unda da ayni calisir.

Durum (state): {ref: [x_mm, y_mm, k]}; k & 3 = mevcut yonelime gore ek 90 derece adim
sayisi (kart cercevesinde, +90 = ekranda saat yonu tersi), k & 4 = karsi yuze cevrilmis
(flip). `pcb_apply.py` once footprint.Flip(pos, LEFT_RIGHT) (ofset x aynalanir), sonra
footprint.Rotate(pos, 90*(k&3)) uygular; 137 parcada (F/B) ve 7 parcada flip+90 ile
pad sapmasi 0.0000 mm olarak dogrulandi. k'yi degistirirken turn()/flip bitini koru.

Skor (SKILL.md "Define and compare the metric"):
    S = sum(w * pad merkezleri arasi Oklid mesafe)
kritik ciftler sabit kenar; kalan baglanti her nette kritik bilesenler daraltilip
MST ile tamamlanir. EXCLUDE_ORDINARY (vars. GND) aramada disarida, raporda icerde.

Config anahtarlari (hepsi BUYUK harf; eksik olan varsayilani alir):
    BLOCKS {blok: "ref ref ..."}   tum parcalar bir bloga ait olmali
    CRIT [(a, b, w, neden) | ("DECAP", kond, ic, w, neden)]
        a/b: "R.n" = R'nin n numarali padi; "R@NET" = R'nin NET (kisa ad) uzerindeki
        en yakin padi. DECAP her kondansator padini IC'nin ayni netteki padina baglar.
    FIXED_EXTRA, OUTLINE_BOUND  kilitli olmayan ama tasinmayacak parcalar
    CUTOUTS [rect]               kart bbox'indan cikarilan dikdortgen girintiler
    KEEPOUTS [(rect, "ref ... @F", neden)]  bu parcalar rect'e giremez (LCD golgesi vb.);
        "@F"/"@B" o yuzdeki tum sabit olmayan parcalar (+ karsi yuzden gelen THT pinleri)
    SLIDE {ref: ("x"|"y", lo, hi)}   kenara bagli tek eksen serbest parca
    TIED {ref: (baz_ref, "x"|"y")}   baz parcayla ayni ofsette kayar
    NO_EDGE_CHECK {ref}          kart disina tasmasi tasarim geregi (konnektor, anten)
    ALLOW_OVERLAP [(a, b)]       bilincli ust uste istif (USB-C THT - RJ45 modulu)
    REGION {(blok, "F"|"B"): rect}  parca merkezi icin bolge (mimari/zonlama)
    ANCHOR {blok: (x, y)}        sifirdan baslangic noktasi
    PULL [(a, b, w, neden)]      elektriksel olmayan gruplama cekimi (raporda yok)
    LOOP_GROUPS {ad: [onek...]}  rapor icin kritik kenar gruplari
    W_ORDINARY                   siradan (MST tamamlama) kenar agirligi
    W_CROSS                      ayni yuzde kesisen iki kenar basina ceza (GND haric)
    W_DECAP_SIDE                 DECAP kondansatoru SMD IC'den farkli yuzdeyse ceza
    FLIP_DECAPS                  True: DECAP kondansatorleri karsi yuze gecebilir (yer yoksa)
    W_GND_LOCAL                  GND padinin ayni bloktaki en yakin GND padina uzakligi (mm basina)
    PLANE_NETS, W_PLANE          ic katman duzlem/polygon netleri (GND dahil edilir): siradan MST kenarlari
                                 W_PLANE ile (polygon kompaktligi) sayilir ve kesismeye girmez; bu
                                 netlerdeki KRITIK kenarlar (dekuplaj, Kelvin) gercek iz, aynen kalir
    AUTO_LOCAL                   IC pini-tek pasif 2 padli netleri kritik listeye W_ORDINARY ile ekle
    NO_WORSE_W                   --no-worse bu agirlik ve ustundeki kritik kenarlari korur
    FAR_MM                       raporda "kopuk" esigi: en yakin bagli pad bu mesafeden uzak
    EDGE_MARGIN, GAP, EXCLUDE_ORDINARY
rect = (x0, y0, x1, y1) mm, kart koordinatinda.
"""
import json
import math
import runpy

DEFAULTS = dict(BLOCKS={}, CRIT=[], FIXED_EXTRA=set(), OUTLINE_BOUND=set(), CUTOUTS=[], KEEPOUTS=[],
                SLIDE={}, TIED={}, NO_EDGE_CHECK=set(), ALLOW_OVERLAP=[], REGION={}, ANCHOR={}, PULL=[],
                LOOP_GROUPS={}, W_ORDINARY=1.0, W_CROSS=0.0, W_DECAP_SIDE=0.0, FLIP_DECAPS=False,
                W_GND_LOCAL=0.0, FAR_MM=6.0, AUTO_LOCAL=False, NO_WORSE_W=10,
                PLANE_NETS=set(), W_PLANE=None, EDGE_MARGIN=0.3, GAP=0.1, EXCLUDE_ORDINARY={"GND"})


def load_cfg(path):
    ns = runpy.run_path(path)
    cfg = dict(DEFAULTS)
    cfg.update({k: v for k, v in ns.items() if k.isupper()})
    cfg["BLOCKS"] = {b: (v.split() if isinstance(v, str) else list(v)) for b, v in cfg["BLOCKS"].items()}
    cfg["PLANE_NETS"] = set(cfg["PLANE_NETS"])
    cfg["KEEPOUTS"] = [(tuple(r), set(refs.split() if isinstance(refs, str) else refs), why)
                       for r, refs, why in cfg["KEEPOUTS"]]
    return cfg


def short(net):
    return net.split("/")[-1]


def rot(dx, dy, k):
    """k & 4: once x aynalama (Flip LEFT_RIGHT); sonra k*90 derece, footprint.Rotate(+90) yonu."""
    if k & 4:
        dx = -dx
    k %= 4
    if k == 0: return dx, dy
    if k == 1: return dy, -dx
    if k == 2: return -dx, -dy
    return -dy, dx


def turn(k, dk):
    """Flip bitini koruyarak dk*90 derece dondur."""
    return (k & 4) | ((k + dk) % 4)


def seg_cross(a, b):
    """Iki dogru parcasi uclar haric kesisiyor mu (a, b = (x0, y0, x1, y1))."""
    if max(a[0], a[2]) < min(b[0], b[2]) or max(b[0], b[2]) < min(a[0], a[2]) or \
       max(a[1], a[3]) < min(b[1], b[3]) or max(b[1], b[3]) < min(a[1], a[3]):
        return False

    def o(px, py, qx, qy, rx, ry):
        return (qx - px) * (ry - py) - (qy - py) * (rx - px)
    d1 = o(a[0], a[1], a[2], a[3], b[0], b[1]); d2 = o(a[0], a[1], a[2], a[3], b[2], b[3])
    d3 = o(b[0], b[1], b[2], b[3], a[0], a[1]); d4 = o(b[0], b[1], b[2], b[3], a[2], a[3])
    return d1 * d2 < 0 and d3 * d4 < 0


def ov(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0]); h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def infl(a, g):
    return (a[0] - g, a[1] - g, a[2] + g, a[3] + g)


def load_state(path):
    return {k: list(v) for k, v in json.load(open(path, encoding="utf-8"))["state"].items()}


def save_state(path, st, **extra):
    json.dump(dict(state=st, **extra), open(path, "w", encoding="utf-8"))


class Model:
    """Parcalar, bloklar, kritik kenarlar ve skor fonksiyonlari."""

    def __init__(self, parts_json, cfg):
        d = json.load(open(parts_json, encoding="utf-8"))
        self.cfg = cfg
        self.board = tuple(d["board"])
        self.P = {}
        for p in d["parts"]:
            r = p["ref"]
            pads = [{"n": q["n"], "net": q["net"], "s": short(q["net"]), "dx": q["x"] - p["x"], "dy": q["y"] - p["y"],
                     "th": q["th"], "bb": [q["bb"][0] - p["x"], q["bb"][1] - p["y"], q["bb"][2] - p["x"], q["bb"][3] - p["y"]]}
                    for q in p["pads"] if q["n"] != ""]      # "" = EP termal alt padi
            rects = []
            for a in p["rects"]:
                if r in cfg["NO_EDGE_CHECK"]:              # kart disindaki kismi (anten keepout) at
                    a = [max(a[0], self.board[0]), max(a[1], self.board[1]), min(a[2], self.board[2]), min(a[3], self.board[3])]
                    if a[2] <= a[0] + 0.01 or a[3] <= a[1] + 0.01:
                        continue
                rects.append([a[0] - p["x"], a[1] - p["y"], a[2] - p["x"], a[3] - p["y"]])
            self.P[r] = {"ref": r, "side": p["side"], "x0": p["x"], "y0": p["y"], "fp": p["fp"],
                         "pads": pads, "rects": rects, "locked": p["locked"]}
        self.block_of = {r: b for b, rs in cfg["BLOCKS"].items() for r in rs}
        missing = sorted(set(self.P) - set(self.block_of))
        if missing:
            raise SystemExit(f"BLOCKS'ta olmayan parcalar: {missing}")
        self.refs = sorted(self.P)
        self.fixed = {r for r in self.refs if self.P[r]["locked"]} | set(cfg["FIXED_EXTRA"])
        self.static = self.fixed | set(cfg["OUTLINE_BOUND"])
        self.free = [r for r in self.refs if r not in self.static and r not in cfg["TIED"] and r not in cfg["SLIDE"]]
        self.net_pads = {}
        for r in self.refs:
            for i, q in enumerate(self.P[r]["pads"]):
                if q["net"]:
                    self.net_pads.setdefault(q["s"], []).append((r, i))
        self.nets_of = {r: sorted({q["s"] for q in self.P[r]["pads"] if q["net"]}) for r in self.refs}
        self._resolve_crit()
        # DECAP kondansatoru -> IC; IC bu kondansatorun netlerinde yalniz THT pinle bagliysa yuz serbest
        self.decap_ic = {}
        for e in cfg["CRIT"]:
            if e[0] == "DECAP":
                c, ic = e[1], e[2]
                nets = {q["s"] for q in self.P[c]["pads"] if q["net"]} - {"GND"}
                smd = any(not q["th"] and q["s"] in nets for q in self.P[ic]["pads"])
                if smd:
                    self.decap_ic[c] = ic
        self.ics_of_decap = {}
        for c, ic in self.decap_ic.items():
            self.ics_of_decap.setdefault(ic, []).append(c)
        self.flippable = {c for c in self.decap_ic if c in self.free} if cfg["FLIP_DECAPS"] else set()
        self.gnd_pads = {r: [i for i, q in enumerate(self.P[r]["pads"]) if q["s"] == "GND"] for r in self.refs}

    # ---------------------------------------------------------------- kritik kenarlar
    def _sel(self, spec, net_hint=None):
        if "@" not in spec:
            r, n = spec.split(".", 1)
            idx = [i for i, q in enumerate(self.P[r]["pads"]) if q["n"] == n]
        else:
            r, net = spec.split("@")
            net = net_hint if net == "*" else net
            idx = [i for i, q in enumerate(self.P[r]["pads"]) if q["s"] == net]
        if not idx:
            raise SystemExit(f"kritik kenar ucu cozulemedi: {spec} ({net_hint})")
        return r, idx

    def _resolve_crit(self):
        raw = []
        for e in self.cfg["CRIT"]:
            if e[0] == "DECAP":
                _, c, ic, w, why = e
                for q in self.P[c]["pads"]:
                    if q["net"]:
                        raw.append((f"{c}.{q['n']}", f"{ic}@*", w, why))
            else:
                raw.append(tuple(e))
        if self.cfg["AUTO_LOCAL"]:
            # IC pini (>3 padli parca) ile tek pasif arasindaki 2 padli net: IC-yerel destek parcasi
            # (SS/seri/pull kondansator-direnc). Kritik listeye W_ORDINARY ile girer -> skor ayni,
            # ama refine cekme hamlesi ve --no-worse korumasi alir.
            have = {tuple(sorted((a.split(".")[0].split("@")[0], b.split(".")[0].split("@")[0]))) for a, b, _, _ in raw}
            for net, pads in sorted(self.net_pads.items()):
                if len(pads) != 2 or net in self.cfg["EXCLUDE_ORDINARY"]:
                    continue
                (ra, ia), (rb, ib) = pads
                big, small = (ra, rb) if len(self.P[ra]["pads"]) > len(self.P[rb]["pads"]) else (rb, ra)
                if len(self.P[big]["pads"]) <= 3 or len(self.P[small]["pads"]) > 3 or tuple(sorted((ra, rb))) in have:
                    continue
                raw.append((f"{small}@{net}", f"{big}@{net}", self.cfg["W_ORDINARY"], f"auto: {big} pinine yerel destek parcasi"))
        self.crit = []
        for a, b, w, why in raw:
            ra, ia = self._sel(a)
            neta = self.P[ra]["pads"][ia[0]]["s"]
            rb, ib = self._sel(b, neta)
            if {self.P[rb]["pads"][i]["s"] for i in ib} != {neta}:
                raise SystemExit(f"kritik kenar ayni nette degil: {a} - {b}")
            self.crit.append({"a": (ra, ia), "b": (rb, ib), "w": w, "why": why, "net": neta, "sa": a, "sb": b})
        self.crit_of, self.crit_by_net = {}, {}
        for k, c in enumerate(self.crit):
            for r in {c["a"][0], c["b"][0]}:
                self.crit_of.setdefault(r, []).append(k)
            self.crit_by_net.setdefault(c["net"], []).append(k)

    # ---------------------------------------------------------------- geometri
    def initial_state(self):
        return {r: [self.P[r]["x0"], self.P[r]["y0"], 0] for r in self.refs}

    def w_ord(self, net):
        """Siradan (MST) kenar agirligi: duzlem netleri W_PLANE (verilmisse), digerleri W_ORDINARY."""
        c = self.cfg
        if c["W_PLANE"] is not None and (net in c["PLANE_NETS"] or net == "GND"):
            return c["W_PLANE"]
        return c["W_ORDINARY"]

    def side_of(self, st, r):
        s = self.P[r]["side"]
        return ("B" if s == "F" else "F") if st[r][2] & 4 else s

    def decap_side_bad(self, st, caps):
        return sum(1 for c in caps if c in self.decap_ic and self.side_of(st, c) != self.side_of(st, self.decap_ic[c]))

    def gnd_local(self, st, r):
        """r'nin GND padindan ayni bloktaki baska parcanin en yakin GND padina mesafe (yoksa 0)."""
        if not self.gnd_pads[r]:
            return 0.0
        mine = [self.pad_xy(st, r, i) for i in self.gnd_pads[r]]
        best = None
        for o in self.cfg["BLOCKS"][self.block_of[r]]:
            if o == r:
                continue
            for j in self.gnd_pads[o]:
                xo, yo = self.pad_xy(st, o, j)
                for x, y in mine:
                    d = math.hypot(x - xo, y - yo)
                    if best is None or d < best:
                        best = d
        return best or 0.0

    def net_segs(self, st, net):
        """Netin skor grafigi kenarlari: [(x0, y0, x1, y1, yuz|None)]; yuz degistiren kenar None (via)."""
        out = []
        for k in self.crit_by_net.get(net, []):
            _, i, j = self.crit_len(st, k); c = self.crit[k]
            out.append(((c["a"][0], i), (c["b"][0], j)))
        if net not in self.cfg["PLANE_NETS"]:          # duzlem netinin siradan baglantisi via ile
            out += [(a, b) for a, b, _ in self.net_mst(st, net, True)[1]]
        segs = []
        for (ra, i), (rb, j) in out:
            if ra == rb:
                continue
            xa, ya = self.pad_xy(st, ra, i); xb, yb = self.pad_xy(st, rb, j)
            sa, sb = self.side_of(st, ra), self.side_of(st, rb)
            segs.append((xa, ya, xb, yb, sa if sa == sb else None))
        return segs

    def crossings(self, st, nets=None):
        """Ayni yuzde farkli netlere ait kesisen kenar ciftleri ve via (yuz degistiren) kenar sayisi."""
        nets = sorted(n for n in self.net_pads if n not in self.cfg["EXCLUDE_ORDINARY"]) if nets is None else nets
        S = {n: self.net_segs(st, n) for n in nets}
        flat = [(n, s) for n in nets for s in S[n]]
        x = 0; per = {}
        for i in range(len(flat)):
            na, a = flat[i]
            if a[4] is None:
                continue
            for nb, b in flat[i + 1:]:
                if nb != na and b[4] == a[4] and seg_cross(a, b):
                    x += 1; per[na] = per.get(na, 0) + 1; per[nb] = per.get(nb, 0) + 1
        vias = sum(1 for _, s in flat if s[4] is None)
        return x, vias, per

    def pad_xy(self, st, r, i):
        x, y, k = st[r]
        q = self.P[r]["pads"][i]
        dx, dy = rot(q["dx"], q["dy"], k)
        return x + dx, y + dy

    def _xf(self, st, r, a):
        x, y, k = st[r]
        c0, c1 = rot(a[0], a[1], k), rot(a[2], a[3], k)
        return (x + min(c0[0], c1[0]), y + min(c0[1], c1[1]), x + max(c0[0], c1[0]), y + max(c0[1], c1[1]))

    def rects(self, st, r):
        return [self._xf(st, r, a) for a in self.P[r]["rects"]]

    def tht_obstacles(self, st, r, clr=0.3, pins_only=False):
        """THT/NPTH padlar karsi yuzde de engeldir (J8 header pinleri ustte, U11 termal via'lari J3 altinda).
        pins_only: SMD padiyla ayni numarali termal via padlarini at (govde pini degiller)."""
        pads = self.P[r]["pads"]
        smd = {q["n"] for q in pads if not q["th"]} if pins_only else set()
        return [infl(self._xf(st, r, q["bb"]), clr) for q in pads if q["th"] and q["n"] not in smd]

    def sync_tied(self, st):
        for r, (base, ax) in self.cfg["TIED"].items():
            i = 1 if ax == "y" else 0
            k0 = "y0" if i else "x0"
            st[r][i] = self.P[r][k0] + (st[base][i] - self.P[base][k0])

    # ---------------------------------------------------------------- skor
    def crit_len(self, st, k):
        c = self.crit[k]
        (ra, ia), (rb, ib) = c["a"], c["b"]
        best = None
        for i in ia:
            xa, ya = self.pad_xy(st, ra, i)
            for j in ib:
                xb, yb = self.pad_xy(st, rb, j)
                d = math.hypot(xa - xb, ya - yb)
                if best is None or d < best[0]:
                    best = (d, i, j)
        return best

    def net_mst(self, st, net, want_edges=False):
        pads = self.net_pads.get(net, [])
        if len(pads) < 2:
            return (0.0, []) if want_edges else 0.0
        idx = {p: n for n, p in enumerate(pads)}
        parent = list(range(len(pads)))

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]; a = parent[a]
            return a
        for k in self.crit_by_net.get(net, []):
            _, i, j = self.crit_len(st, k)
            parent[find(idx[(self.crit[k]["a"][0], i)])] = find(idx[(self.crit[k]["b"][0], j)])
        xy = [self.pad_xy(st, r, i) for r, i in pads]
        e = sorted((math.hypot(xy[a][0] - xy[b][0], xy[a][1] - xy[b][1]), a, b)
                   for a in range(len(pads)) for b in range(a + 1, len(pads)))
        tot, used = 0.0, []
        for d, a, b in e:                                     # esitlikte pad sirasi belirleyici
            fa, fb = find(a), find(b)
            if fa != fb:
                parent[fa] = fb; tot += d
                if want_edges:
                    used.append((pads[a], pads[b], d))
        return (tot, used) if want_edges else tot

    def pull_cost(self, st, movers=None):
        return sum(w * math.hypot(st[a][0] - st[b][0], st[a][1] - st[b][1])
                   for a, b, w, _ in self.cfg["PULL"] if movers is None or a in movers or b in movers)

    def report(self, st):
        """Tam metrik (GND dahil); blok ici / bloklar arasi ayrimi ve blok basina ic skor."""
        bo = self.block_of
        rep = {"crit": [], "ord": [], "S_int": 0.0, "S_inter": 0.0, "L_int": 0.0, "L_inter": 0.0, "blocks": {}}

        def add(ra, rb, w, d):
            inter = bo[ra] != bo[rb]
            rep["S_inter" if inter else "S_int"] += w * d
            rep["L_inter" if inter else "L_int"] += d
            if not inter:
                rep["blocks"][bo[ra]] = rep["blocks"].get(bo[ra], 0.0) + w * d
        for k, c in enumerate(self.crit):
            d = self.crit_len(st, k)[0]
            rep["crit"].append([c["sa"], c["sb"], c["w"], round(d, 3), c["why"]])
            add(c["a"][0], c["b"][0], c["w"], d)
        for net in sorted(self.net_pads):
            for (ra, i), (rb, j), d in self.net_mst(st, net, True)[1]:
                rep["ord"].append([f"{ra}.{self.P[ra]['pads'][i]['n']}", f"{rb}.{self.P[rb]['pads'][j]['n']}", net, round(d, 3)])
                add(ra, rb, self.w_ord(net), d)
        rep["S"] = rep["S_int"] + rep["S_inter"]; rep["L"] = rep["L_int"] + rep["L_inter"]
        rep["X"], rep["V"], rep["X_net"] = self.crossings(st)
        rep["decap_side"] = sorted(c for c in self.decap_ic if self.side_of(st, c) != self.side_of(st, self.decap_ic[c]))
        rep["flipped"] = sorted(r for r in self.refs if st[r][2] & 4)
        far = []
        for r in self.refs:
            if r in self.static:
                continue
            ds = [d for a, b, d in sum((self.net_mst(st, n, True)[1] for n in self.nets_of[r] if n != "GND"), [])
                  if (a[0] == r) != (b[0] == r)]
            ds += [self.crit_len(st, k)[0] for k in self.crit_of.get(r, [])]
            dmin = min(ds) if ds else None
            if dmin is None or dmin > self.cfg["FAR_MM"]:
                far.append((r, None if dmin is None else round(dmin, 1)))
        rep["far"] = far
        return rep


class Engine:
    """Kisit cezasi (mm^2 alan + bolge disi mm) ve arama maliyeti; parca geometrisini onbellekte tutar."""

    def __init__(self, m, st, baseline=None, no_worse_w=10, no_worse_lam=0.0):
        self.m, self.st, self.cfg = m, st, m.cfg
        self.side = {r: m.side_of(st, r) for r in m.refs}
        self.R, self.T = {}, {}
        self.wx = self.cfg["W_CROSS"]
        self.xnets = sorted(n for n in m.net_pads if n not in self.cfg["EXCLUDE_ORDINARY"])
        self.segs = {n: m.net_segs(st, n) for n in self.xnets} if self.wx else {}
        self.update(m.refs)
        b = m.board; em = self.cfg["EDGE_MARGIN"]
        self.inner = (b[0] + em, b[1] + em, b[2] - em, b[3] - em)
        self.cuts = [infl(c, em) for c in self.cfg["CUTOUTS"]]
        self.allow = {frozenset(p) for p in self.cfg["ALLOW_OVERLAP"]}
        # montaj delikleri iki yuzde de engel (NPTH padi numarasiz oldugu icin pad listesinde yok)
        self.holes = {r for r in m.refs if m.P[r]["fp"].startswith("MountingHole")} | set(self.cfg.get("BOTH_SIDES", ()))
        # "kotulesme yok" kisiti: w >= no_worse_w kenarlar baseline uzunlugunu asarsa lam*mm ceza
        self.base = {}
        self.lam_nw = no_worse_lam
        if baseline is not None and no_worse_lam > 0:
            self.base = {k: m.crit_len(baseline, k)[0] for k, c in enumerate(m.crit) if c["w"] >= no_worse_w}

    def update(self, movers):
        nets = set()
        for r in movers:
            self.R[r] = self.m.rects(self.st, r); self.T[r] = self.m.tht_obstacles(self.st, r)
            self.side[r] = self.m.side_of(self.st, r)
            nets.update(self.m.nets_of[r])
        if self.wx:
            for n in nets:
                if n in self.segs:
                    self.segs[n] = self.m.net_segs(self.st, n)

    def cross_of(self, nets):
        """nets'e ait kenarlarin (onbellekten) tum diger kenarlarla ayni yuz kesisme sayisi."""
        nets = [n for n in nets if n in self.segs]
        x = 0; done = set()
        for n in nets:
            done.add(n)
            for a in self.segs[n]:
                if a[4] is None:
                    continue
                for o, bs in self.segs.items():
                    if o == n or o in done:
                        continue
                    for b in bs:
                        if b[4] == a[4] and seg_cross(a, b):
                            x += 1
        return x

    def pair_pen(self, r, o):
        if (r in self.m.static and o in self.m.static) or frozenset((r, o)) in self.allow:
            return 0.0
        R, T, S = self.R, self.T, self.side
        g = self.cfg["GAP"] / 2
        s = 0.0
        if S[r] == S[o] or r in self.holes or o in self.holes:
            for a in R[r]:
                aa = infl(a, g)
                for b in R[o]:
                    s += ov(aa, infl(b, g))
        if S[r] != S[o]:
            for a in R[r]:
                for b in T[o]:
                    s += ov(a, b)
            for a in T[r]:
                for b in R[o]:
                    s += ov(a, b)
        return s

    def indiv_pen(self, r):
        m, cfg = self.m, self.cfg
        s = 0.0
        if r not in cfg["NO_EDGE_CHECK"] and r not in m.static:
            for a in self.R[r]:
                s += (a[2] - a[0]) * (a[3] - a[1]) - ov(a, self.inner)
                for c in self.cuts:
                    s += ov(a, c)
        for rect, refs, _ in cfg["KEEPOUTS"]:
            side = self.side[r]
            if r in refs or ("@" + side in refs and r not in m.static):
                for a in self.R[r]:
                    s += ov(a, rect)
            if "@" + ("B" if side == "F" else "F") in refs and r not in m.static:
                for a in m.tht_obstacles(self.st, r, pins_only=True):   # karsi yuzden cikan THT pinleri
                    s += ov(a, rect)
        reg = cfg["REGION"].get((m.block_of[r], self.side[r]))
        if reg and r in m.free:
            x, y = self.st[r][0], self.st[r][1]
            s += max(0.0, reg[0] - x, x - reg[2]) + max(0.0, reg[1] - y, y - reg[3])
        return s

    def pen_of(self, movers):
        ms = set(movers); s = 0.0
        for r in movers:
            s += self.indiv_pen(r)
            for o in self.m.refs:
                if o != r and not (o in ms and o < r):
                    s += self.pair_pen(r, o)
        return s

    def offenders(self):
        out = {}
        refs = self.m.refs
        for r in refs:
            p = self.indiv_pen(r)
            if p > 1e-9:
                out[(r, "kenar/keepout/bolge")] = p
        for i, r in enumerate(refs):
            for o in refs[i + 1:]:
                p = self.pair_pen(r, o)
                if p > 1e-9:
                    out[(r, o)] = p
        return out

    def wire(self, movers, crit_only=False):
        """Arama maliyeti: etkilenen netlerin MST'si (GND haric) + kritik kenarlar + PULL + kotulesme cezasi."""
        m = self.m
        ks, ns = set(), set()
        for r in movers:
            ks.update(m.crit_of.get(r, [])); ns.update(m.nets_of[r])
        ns -= self.cfg["EXCLUDE_ORDINARY"]
        s = m.pull_cost(self.st, set(movers)) + sum(m.w_ord(n) * m.net_mst(self.st, n) for n in ns)
        s += self.extra(movers, ns)
        for k in ks:
            d = m.crit_len(self.st, k)[0]
            s += m.crit[k]["w"] * d
            if k in self.base:
                s += self.lam_nw * max(0.0, d - self.base[k])
        return s

    def total(self):
        m = self.m
        s = sum(m.w_ord(n) * m.net_mst(self.st, n) for n in m.net_pads if n not in self.cfg["EXCLUDE_ORDINARY"]) + m.pull_cost(self.st)
        s += self.extra(m.refs, set(self.xnets))
        for k, c in enumerate(m.crit):
            d = m.crit_len(self.st, k)[0]
            s += c["w"] * d + (self.lam_nw * max(0.0, d - self.base[k]) if k in self.base else 0.0)
        return s

    def extra(self, movers, nets):
        """Kesisme, dekuplaj yuzu ve yerel GND terimleri (config agirligi 0 ise hesaplanmaz)."""
        m, cfg = self.m, self.cfg
        s = 0.0
        if self.wx:
            s += self.wx * self.cross_of(sorted(nets))
        if cfg["W_DECAP_SIDE"]:
            caps = set()
            for r in movers:
                if r in m.decap_ic:
                    caps.add(r)
                caps.update(m.ics_of_decap.get(r, []))
            s += cfg["W_DECAP_SIDE"] * m.decap_side_bad(self.st, caps)
        if cfg["W_GND_LOCAL"]:
            s += cfg["W_GND_LOCAL"] * sum(m.gnd_local(self.st, r) for r in movers if r in m.free)
        return s
