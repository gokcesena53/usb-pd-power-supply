"""Yerlesim adayini Freerouting ile deneme routing'inden gecirir (routability olcumu).

Kullanim:
    sh $SK/kpy $PL/pcb_freeroute.py cand.kicad_pcb $T/fr_cand --plane In1.Cu=GND --plane In2.Cu=+3.3V \
        [--passes 60] [--threads 1] [--timeout 1800]

Adimlar (hepsi KOPYADA; girdi karta dokunulmaz):
    1. --plane katmanlarini "power" tipine al (Freerouting orada sinyal cekmez) ve kart
       dis hatti boyunca o netin zone'unu ekle + doldur.
    2. ExportSpecctraDSN -> java -jar freerouting -de .dsn -do .ses (GUI kapali).
    3. Hazirlanan karta ImportSpecctraSES, zone'lari yeniden doldur, routed.kicad_pcb kaydet.
    4. result.json: iz/via sayisi, katman basina iz uzunlugu, kicad-cli DRC (baglantisiz,
       ihlal turleri), sure, Freerouting cikis kodu.

Java/Freerouting: FREEROUTING_JAVA ve FREEROUTING_JAR ortam degiskenleri; yoksa
~/.local/opt/freerouting/jdk*/bin/java(.exe) ve freerouting-*.jar aranir.
Freerouting 2.4.x Java 25 ister (class file 69); Java 21 "UnsupportedClassVersionError" verir.
Sonuc bir routing ONERISI degildir: yalniz yerlesimleri ayni kosulda karsilastirmak icindir.
"""
import argparse
import collections
import glob
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'kicad-schematic', 'scripts'))
sys.path.insert(0, HERE)
from kicadtools import ensure_pcbnew  # noqa: E402

pcbnew = ensure_pcbnew()
from pcb_check import drc  # noqa: E402
mm = pcbnew.ToMM


def find_tools():
    base = os.path.expanduser("~/.local/opt/freerouting")
    java = os.environ.get("FREEROUTING_JAVA") or next(iter(sorted(
        glob.glob(os.path.join(base, "jdk*", "bin", "java.exe")) + glob.glob(os.path.join(base, "jdk*", "bin", "java")),
        reverse=True)), None) or shutil.which("java")
    jar = os.environ.get("FREEROUTING_JAR") or next(iter(sorted(glob.glob(os.path.join(base, "freerouting-*.jar")), reverse=True)), None)
    if not java or not jar:
        raise SystemExit(f"java/freerouting bulunamadi (java={java}, jar={jar}); FREEROUTING_JAVA/JAR ver")
    return java, jar


def prepare(board, planes, out):
    B = pcbnew.LoadBoard(board)
    outline = pcbnew.SHAPE_POLY_SET()
    B.GetBoardPolygonOutlines(outline, True)
    for spec in planes:
        lname, net = spec.split("=", 1)
        lid = B.GetLayerID(lname)
        if lid < 0:
            raise SystemExit(f"katman yok: {lname}")
        ni = B.FindNet(net)
        if ni is None:
            raise SystemExit(f"net yok: {net}")
        B.SetLayerType(lid, pcbnew.LT_POWER)
        z = pcbnew.ZONE(B)
        z.SetLayer(lid); z.SetNet(ni); z.SetIsRuleArea(False); z.SetAssignedPriority(0)
        # SetOutline(SHAPE_POLY_SET*) sahipligi alir -> python kopyasi serbest kalinca segfault;
        # noktalari zone'un kendi poligonuna ekle
        zo = z.Outline()
        for i in range(outline.OutlineCount()):
            ol = outline.Outline(i); zo.NewOutline()
            for j in range(ol.PointCount()):
                q = ol.CPoint(j); zo.Append(q.x, q.y)
        B.Add(z)
    B.BuildConnectivity()
    pcbnew.ZONE_FILLER(B).Fill(B.Zones())
    B.Save(out)


def stats(path):
    B = pcbnew.LoadBoard(path)
    L = collections.Counter(); n_tr = n_via = 0
    for t in B.GetTracks():
        if t.GetClass() == "PCB_VIA":
            n_via += 1
        else:
            n_tr += 1; L[B.GetLayerName(t.GetLayer())] += mm(t.GetLength())
    return {"tracks": n_tr, "vias": n_via, "length_mm": {k: round(v, 1) for k, v in L.items()},
            "length_total_mm": round(sum(L.values()), 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board"); ap.add_argument("outdir")
    ap.add_argument("--plane", action="append", default=[], help="KATMAN=NET (or. In1.Cu=GND)")
    ap.add_argument("--passes", type=int, default=60); ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--display", default="", help="GUI'yi bu X ekraninda ac (or. :99 Xvfb); bos = headless")
    ap.add_argument("--project", default="", help="DRC icin proje dizini (vars.: girdi kartindan yukari aranir)")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    O = lambda n: os.path.join(a.outdir, n)
    res = {"board": a.board, "planes": a.plane, "passes": a.passes}
    json.dump(dict(res, status="hazirlaniyor"), open(O("result.json"), "w"))
    prepare(a.board, a.plane, O("prep.kicad_pcb"))
    B = pcbnew.LoadBoard(O("prep.kicad_pcb"))
    if not pcbnew.ExportSpecctraDSN(B, O("board.dsn")):
        raise SystemExit("DSN disa aktarilamadi")
    java, jar = find_tools()
    cmd = [java, "-jar", jar, "-de", O("board.dsn"), "-do", O("board.ses"), "-mp", str(a.passes), "-mt", str(a.threads)]
    env = dict(os.environ)
    if a.display:       # GUI sanal ekranda (Xvfb) -> ekran goruntusu alinabilir; GUI modu fanout asamasi da calistirir
        env["DISPLAY"] = a.display
    else:
        cmd.append("--gui.enabled=false")
    res["mode"] = "gui " + a.display if a.display else "headless"
    json.dump(dict(res, status="routing", started=time.time()), open(O("result.json"), "w"))
    t0 = time.time(); rc = None
    with open(O("freerouting.log"), "w", encoding="utf-8") as log:
        pr = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)
        last = None
        while rc is None:
            time.sleep(3)
            rc = pr.poll()
            if time.time() - t0 > a.timeout:
                pr.kill(); rc = "timeout"
            elif rc is None and os.path.exists(O("board.ses")):
                # GUI modu SES'i yazdiktan sonra acik kalabilir: dosya boyutu sabitlenince kapat
                sz = os.path.getsize(O("board.ses"))
                if sz and sz == last:
                    pr.terminate(); pr.wait(10); rc = "ses-yazildi"
                last = sz
    res.update(route_s=round(time.time() - t0), freerouting_rc=rc)
    if not os.path.exists(O("board.ses")):
        json.dump(dict(res, status="ses yok (log'a bak)"), open(O("result.json"), "w"), indent=1)
        raise SystemExit(f"SES uretilmedi (rc={rc}); {O('freerouting.log')}")
    B = pcbnew.LoadBoard(O("prep.kicad_pcb"))
    if not pcbnew.ImportSpecctraSES(B, O("board.ses")):
        raise SystemExit("SES ice aktarilamadi")
    pcbnew.ZONE_FILLER(B).Fill(B.Zones())
    B.Save(O("routed.kicad_pcb"))
    res.update(stats(O("routed.kicad_pcb")))
    c, un, par, _ = drc(O("routed.kicad_pcb"), a.project or os.path.dirname(os.path.abspath(a.board)), "fr", a.outdir)
    res.update(unconnected=un, parity=par, violations=dict(c.most_common()), status="bitti")
    json.dump(res, open(O("result.json"), "w"), indent=1)
    print(json.dumps(res, ensure_ascii=False))


if __name__ == "__main__":
    main()
