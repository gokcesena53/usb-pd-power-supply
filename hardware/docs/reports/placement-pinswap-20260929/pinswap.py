"""U2 pin atamasi aramasi: yerlesim sabit, izinli padlar arasinda net degisimi; Engine.total() en aza indirilir."""
import sys, random, time, itertools, json
sys.path.insert(0, ".claude/skills/kicad-placement/scripts")
from placelib import Model, Engine, load_cfg, load_state
cfg = load_cfg(".claude/skills/kicad-placement/examples/gopo_rev_c.py")
m = Model(sys.argv[1], cfg); st = load_state(sys.argv[2])
IC = "U2"
PADS = ["5", "6", "9", "10", "13", "16", "19", "20", "24", "25", "26", "27", "28", "29"]
STRAP = {"9", "10", "20"}                      # GPIO4, GPIO5, GPIO15
TFT_HIZ = {"TFT_SCLK", "TFT_MOSI", "TFT_DC", "TFT_CS", "TFT_RST"}
idx = {q["n"]: i for i, q in enumerate(m.P[IC]["pads"])}
full = {m.P[IC]["pads"][idx[p]]["s"]: m.P[IC]["pads"][idx[p]]["net"] for p in PADS}
orig = {p: m.P[IC]["pads"][idx[p]]["s"] for p in PADS}

def ok(a):
    return all(a[p] in TFT_HIZ for p in STRAP)

def rebuild(a):
    for p, n in a.items():
        q = m.P[IC]["pads"][idx[p]]; q["s"] = n; q["net"] = full[n]
    m.net_pads = {}
    for r in m.refs:
        for i, q in enumerate(m.P[r]["pads"]):
            if q["net"]:
                m.net_pads.setdefault(q["s"], []).append((r, i))
    m.nets_of = {r: sorted({q["s"] for q in m.P[r]["pads"] if q["net"]}) for r in m.refs}
    m._resolve_crit()

def cost(a):
    rebuild(a); E = Engine(m, st); return E.total(), m.crossings(st)[0]

t0 = time.time()
c0, x0 = cost(orig); print(f"mevcut: maliyet {c0:.1f} kesisme {x0}  ({time.time()-t0:.2f}s/deger)", flush=True)
best = (c0, x0, dict(orig))
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
starts = [dict(orig)]
for _ in range(int(sys.argv[3]) if len(sys.argv) > 3 else 3):
    while True:
        v = list(orig.values()); random.shuffle(v); a = dict(zip(PADS, v))
        if ok(a): starts.append(a); break
for si, a in enumerate(starts):
    c, x = cost(a)
    improved = True
    while improved:
        improved = False
        for p, q in itertools.combinations(PADS, 2):
            b = dict(a); b[p], b[q] = a[q], a[p]
            if not ok(b): continue
            cb, xb = cost(b)
            if cb < c - 1e-6:
                a, c, x, improved = b, cb, xb, True
    print(f"baslangic {si}: maliyet {c:.1f} kesisme {x} t={time.time()-t0:.0f}s", flush=True)
    if c < best[0]: best = (c, x, dict(a))
c, x, a = best
print(f"EN IYI: maliyet {c0:.1f} -> {c:.1f}, kesisme {x0} -> {x}")
for p in PADS:
    if a[p] != orig[p]: print(f"  pad {p}: {orig[p]} -> {a[p]}")
json.dump({"assign": a, "orig": orig, "cost": [c0, c], "cross": [x0, x]}, open(sys.argv[5] if len(sys.argv) > 5 else "pin.json", "w"), indent=1)
