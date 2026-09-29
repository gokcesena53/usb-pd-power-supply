"""Yerlesim state'ini kartin KOPYASINA uygular ve pad konumlarini modele karsi dogrular.

Kullanim:
    sh $SK/kpy $PL/pcb_apply.py hardware/gopo.kicad_pcb best.json $T/cand.kicad_pcb \
        --parts $T/parts.json [--drop-net BOOST_FB ...]

--drop-net: iki ucu da tasinan deneme izlerini (kisa net adi) siler; silinen izler
raporlanir, sessizce atilmaz. Kilitli parca state'te farkli konumdaysa durur.

Tuzaklar (KiCad 10 SWIG):
- B.Remove(track) SONRASI footprint.Pads() 'SwigPyObject' dondurur -> izleri en son
  B.Delete ile sil, footprint'lere once eris.
- FindFootprintByReference yerine bir kez {ref: fp} sozlugu kur.
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kicad-schematic', 'scripts'))
sys.path.insert(0, HERE)
from kicadtools import ensure_pcbnew  # noqa: E402

pcbnew = ensure_pcbnew()
from placelib import rot, load_state  # noqa: E402
import json  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board"); ap.add_argument("state"); ap.add_argument("out")
    ap.add_argument("--parts", required=True, help="pcb_dump.py ciktisi (ayni karttan)")
    ap.add_argument("--drop-net", nargs="*", default=[])
    a = ap.parse_args()
    if os.path.abspath(a.board) == os.path.abspath(a.out):
        raise SystemExit("cikti kopya olmali; asil karta pcb_check sonrasi elle kopyala")
    st = load_state(a.state)
    parts = {p["ref"]: p for p in json.load(open(a.parts, encoding="utf-8"))["parts"]}
    B = pcbnew.LoadBoard(a.board)
    V = lambda x, y: pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))
    FP = {f.GetReference(): f for f in B.GetFootprints()}
    moved = 0; flipped = []
    for r, (x, y, k) in st.items():
        f, p = FP[r], parts[r]
        same = abs(x - p["x"]) < 1e-6 and abs(y - p["y"]) < 1e-6 and k == 0
        if f.IsLocked():
            if not same:
                raise SystemExit(f"kilitli parca tasinmak isteniyor: {r}")
            continue
        if same:
            continue
        f.SetPosition(V(x, y))
        if k & 4:                                   # karsi yuz: ofset x aynalanir (placelib.rot ile ayni)
            f.Flip(V(x, y), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
            flipped.append(r)
        if k % 4:
            f.Rotate(V(x, y), pcbnew.EDA_ANGLE(90.0 * (k % 4), pcbnew.DEGREES_T))
        moved += 1
    worst = 0.0
    for r, (x, y, k) in st.items():
        p = parts[r]
        ref_pads = [q for q in p["pads"] if q["n"] != ""]
        pads = [q for q in list(FP[r].Pads()) if q.GetNumber() != ""]
        for q, mp in zip(pads, ref_pads):
            assert q.GetNumber() == mp["n"], (r, q.GetNumber(), mp["n"])
            dx, dy = rot(mp["x"] - p["x"], mp["y"] - p["y"], k)
            pos = q.GetPosition()
            worst = max(worst, math.hypot(pcbnew.ToMM(pos.x) - (x + dx), pcbnew.ToMM(pos.y) - (y + dy)))
    if worst > 1e-3:
        raise SystemExit(f"pad sapmasi {worst:.4f} mm: donme yonu/modeli uyusmuyor, kaydedilmedi")
    dropped = [t for t in B.GetTracks() if t.GetNetname().split("/")[-1] in a.drop_net]
    for t in dropped:
        B.Delete(t)
    B.Save(a.out)
    print(f"tasinan {moved}; yuz degistiren {flipped}; silinen iz/via {len(dropped)} ({a.drop_net}); en buyuk pad sapmasi {worst:.4f} mm -> {a.out}")


if __name__ == "__main__":
    main()
