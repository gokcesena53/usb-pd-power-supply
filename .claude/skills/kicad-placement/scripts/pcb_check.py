"""Aday karti orijinale karsi denetler: kimlik/net/kilit karsilastirmasi + DRC ve sematik parite.

Kullanim:
    sh $SK/kpy $PL/pcb_check.py hardware/gopo.kicad_pcb $T/cand.kicad_pcb [--drc] [--out $T]

Kimlik: ayni referanslar, pad-net ciftleri, footprint adi, yuz; kilitli parca
0.0000 mm; dis hat bbox; iz/zon sayisi. --drc: iki kart icin kicad-cli DRC
(--schematic-parity --severity-all) ihlal turu sayilari ve baglantisiz ogeler.

Parite semayi karti yanindaki ayni adli .kicad_sch'den bulur; bu yuzden aday
gecici adla PROJE DIZININE kopyalanir (_placecheck_*), .kicad_pro/.kicad_dru/
.kicad_sch ile birlikte, sonra silinir. Asil proje dosyalarina dokunulmaz.
"""
import argparse
import collections
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kicad-schematic', 'scripts'))
from kicadtools import ensure_pcbnew, run_cli  # noqa: E402

pcbnew = ensure_pcbnew()
mm = pcbnew.ToMM


def info(path):
    B = pcbnew.LoadBoard(path)
    d = {}
    for f in B.GetFootprints():
        p = f.GetPosition()
        d[f.GetReference()] = dict(locked=f.IsLocked(), side=f.IsFlipped(), pos=(round(mm(p.x), 4), round(mm(p.y), 4), f.GetOrientationDegrees()),
                                   fp=str(f.GetFPID().GetLibItemName()), nets=sorted((q.GetNumber(), q.GetNetname()) for q in f.Pads()))
    eb = B.GetBoardEdgesBoundingBox()
    return d, len(B.GetTracks()), B.GetAreaCount(), (eb.GetLeft(), eb.GetTop(), eb.GetRight(), eb.GetBottom())


def find_project(start):
    """start'tan yukari .kicad_pro iceren ilk dizin (rapor klasorundeki before.kicad_pcb icin hardware/)."""
    d = os.path.abspath(start)
    while True:
        pros = [f for f in os.listdir(d) if f.endswith(".kicad_pro") and not f.startswith("_placecheck_")]
        if pros:
            return d, pros[0][:-len(".kicad_pro")]
        if os.path.dirname(d) == d:
            raise SystemExit(f".kicad_pro bulunamadi ({start} ve ustu); --project ver")
        d = os.path.dirname(d)


def drc(board, proj_dir, tag, out_dir):
    proj_dir, src_stem = find_project(proj_dir)
    tmp = os.path.join(proj_dir, f"_placecheck_{tag}")
    made = []
    try:
        for ext in (".kicad_pro", ".kicad_dru", ".kicad_sch"):
            s = os.path.join(proj_dir, src_stem + ext)
            if os.path.exists(s):
                shutil.copy(s, tmp + ext); made.append(tmp + ext)
        shutil.copy(board, tmp + ".kicad_pcb"); made.append(tmp + ".kicad_pcb")
        out = os.path.join(out_dir, f"drc_{tag}.json")
        run_cli(["pcb", "drc", "--format", "json", "--schematic-parity", "--severity-all", "-o", out, tmp + ".kicad_pcb"], check=False)
    finally:
        for f in made + [tmp + ".kicad_prl"]:
            if os.path.exists(f):
                os.remove(f)
    d = json.load(open(out, encoding="utf-8"))
    c = collections.Counter(v["type"] for v in d.get("violations", []))
    return c, len(d.get("unconnected_items", [])), len(d.get("schematic_parity", [])), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orig"); ap.add_argument("cand")
    ap.add_argument("--drc", action="store_true"); ap.add_argument("--out", default=".")
    ap.add_argument("--project", default="", help="proje dizini (vars.: orijinal kartin dizininden yukari aranir)")
    ap.add_argument("--allow-flip", nargs="*", default=[], help="yuz degistirmesine izin verilen referanslar (FLIP_DECAPS)")
    a = ap.parse_args()
    A, ta, za, ea = info(a.orig)
    C, tc, zc, ec = info(a.cand)
    if set(A) != set(C):
        raise SystemExit(f"referans farki: {sorted(set(A) ^ set(C))}")
    bad = {k: [r for r in A if A[r][k] != C[r][k]] for k in ("nets", "side", "fp")}
    flips = [r for r in bad["side"] if r in a.allow_flip and not A[r]["locked"]]
    bad["side"] = [r for r in bad["side"] if r not in flips]
    locked = [r for r in A if A[r]["locked"] and A[r]["pos"] != C[r]["pos"]]
    moved = [r for r in A if A[r]["pos"] != C[r]["pos"]]
    print(f"footprint {len(A)}; tasinan {len(moved)}; kilitli tasinan {locked}; pad-net farki {bad['nets']}; "
          f"yuz farki {bad['side']} (izinli flip {flips}); footprint farki {bad['fp']}; dis hat ayni {ea == ec}; iz {ta}->{tc}; zon {za}->{zc}")
    ok = not (locked or bad["nets"] or bad["side"] or bad["fp"]) and ea == ec
    if a.drc:
        proj = a.project or os.path.dirname(os.path.abspath(a.orig))
        for tag, b in (("orig", a.orig), ("cand", a.cand)):
            c, un, par, out = drc(b, proj, tag, a.out)
            print(f"DRC {tag}: ihlal {sum(c.values())} {dict(c.most_common())}; baglantisiz {un}; parite {par} ({out})")
            if tag == "cand" and (c.get("courtyards_overlap", 0) or par):
                ok = False
    print("SONUC:", "GECTI" if ok else "KALDI")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
