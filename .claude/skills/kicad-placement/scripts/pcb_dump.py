"""Karti yerlesim modeline doker (parca, pad, courtyard dilimleri, THT, izler).

Kullanim:
    sh $SK/kpy $PL/pcb_dump.py hardware/gopo.kicad_pcb parts.json

Neden ayri: pcbnew yalniz KiCad python'unda var (Windows); arama/skor betikleri
saf python calisir ve bu JSON'u okur. Courtyard dikdortgensel poligonsa yatay
dilimlere ayrilir: U2 (ESP32) courtyard'i T bicimli (kart disi anten keepout +
modul) ve bbox'i modulun iki yanindaki 30 mm'yi bosuna kapatiyordu.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'kicad-schematic', 'scripts'))
from kicadtools import ensure_pcbnew  # noqa: E402

pcbnew = ensure_pcbnew()
mm = pcbnew.ToMM


def slabs(pts):
    """Kapali poligonu yatay x-araligi dilimlerine boler (dikdortgensel icin kesin)."""
    ys = sorted(set(round(y, 4) for _, y in pts))
    out, n = [], len(pts)
    for y0, y1 in zip(ys, ys[1:]):
        ym = (y0 + y1) / 2
        xs = sorted(xa + (ym - ya) * (xb - xa) / (yb - ya)
                    for (xa, ya), (xb, yb) in ((pts[i], pts[(i + 1) % n]) for i in range(n))
                    if (ya <= ym) != (yb <= ym))
        out += [[a, y0, b, y1] for a, b in zip(xs[0::2], xs[1::2])]
    return out


def dump(board_path):
    B = pcbnew.LoadBoard(board_path)
    parts = []
    for f in B.GetFootprints():
        side = "B" if f.IsFlipped() else "F"
        cy = f.GetCourtyard(pcbnew.B_CrtYd if side == "B" else pcbnew.F_CrtYd)
        rects = []
        for i in range(cy.OutlineCount()):
            o = cy.Outline(i)
            pts = [(mm(o.CPoint(j).x), mm(o.CPoint(j).y)) for j in range(o.PointCount())]
            rectilinear = all(abs(pts[j][0] - pts[j - 1][0]) < 1e-3 or abs(pts[j][1] - pts[j - 1][1]) < 1e-3
                              for j in range(len(pts)))
            rects += slabs(pts) if rectilinear else [[min(p[0] for p in pts), min(p[1] for p in pts),
                                                       max(p[0] for p in pts), max(p[1] for p in pts)]]
        pads = []
        for pd in f.Pads():
            q, bb = pd.GetPosition(), pd.GetBoundingBox()
            pads.append({"n": pd.GetNumber(), "net": pd.GetNetname(), "x": mm(q.x), "y": mm(q.y),
                         "th": pd.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH),
                         "bb": [mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom())]})
        p = f.GetPosition()
        parts.append({"ref": f.GetReference(), "val": f.GetValue(), "fp": str(f.GetFPID().GetLibItemName()),
                      "side": side, "x": mm(p.x), "y": mm(p.y), "rot": f.GetOrientationDegrees(),
                      "locked": f.IsLocked(), "rects": rects, "pads": pads})
    eb = B.GetBoardEdgesBoundingBox()
    tracks = [{"net": t.GetNetname(), "layer": t.GetLayerName(), "cls": t.GetClass()} for t in B.GetTracks()]
    return {"board": [mm(eb.GetLeft()), mm(eb.GetTop()), mm(eb.GetRight()), mm(eb.GetBottom())],
            "parts": sorted(parts, key=lambda p: p["ref"]), "tracks": tracks}


if __name__ == "__main__":
    d = dump(sys.argv[1])
    json.dump(d, open(sys.argv[2], "w", encoding="utf-8"))
    locked = [p["ref"] for p in d["parts"] if p["locked"]]
    nets = sorted({t["net"] for t in d["tracks"]})
    print(f"{len(d['parts'])} parca, kilitli {locked}; iz/via {len(d['tracks'])} (netler {nets}); kart bbox {d['board']}")
