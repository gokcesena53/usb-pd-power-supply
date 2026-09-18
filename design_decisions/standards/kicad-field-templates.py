#!/usr/bin/env python3
"""
KiCad Field Name Templates yukleyici
====================================

Komponent field standardinin "cekirdek" katmanini bir KiCad projesinin
Field Name Templates listesine yazar. Boylece her yeni sembolun ozellik
penceresinde bu alanlar hazir gelir.

Kullanim
--------
    python3 kicad-field-templates.py "masaustu guc kaynagi_REV_B.kicad_pro"
    python3 kicad-field-templates.py proje.kicad_pro --dry-run
    python3 kicad-field-templates.py --print          # elle girmek icin liste

Notlar
------
* KiCad KAPALI olmaliyken calistirilir; acik proje dosyayi kapanirken
  ustune yazar.
* Dosyanin .bak yedegi otomatik alinir.
* Mevcut template alanlari korunur, sadece eksik olanlar eklenir.
* Reference / Value / Footprint / Datasheet / Description alanlari KiCad'de
  yerlesiktir; template olarak eklenemezler, script bunlari reddeder.
* Field Name Templates proje genelindedir: gruba ozel alanlar (Tolerance,
  RdsOn, Pitch ...) buraya girmez, sembol kutuphanesinden gelir.
"""

import json
import re
import shutil
import sys

# --- Cekirdek alanlar (komponent-field-standardi.csv, Layer = Cekirdek/Ortak) ---
CORE_FIELDS = [
    "Category",
    "Subcategory",
    "Manufacturer",
    "MPN",
    "Package",
    "MountingType",
    "Lifecycle",
    "RoHS",
    "OperatingTemp",
    "DesignNote",
]

# KiCad'de yerlesik (mandatory) alanlar - template olarak eklenemez
RESERVED = {"Reference", "Value", "Footprint", "Datasheet", "Description"}

KEY_PATH = ("schematic", "drawing", "field_names")


def serialize(names):
    body = "".join('(field (name "%s"))' % n for n in names)
    return "(templatefields %s)" % body


def existing_names(blob):
    if isinstance(blob, list):
        text = " ".join(str(x) for x in blob)
    elif isinstance(blob, str):
        text = blob
    else:
        text = ""
    return re.findall(r'\(name\s+"([^"]+)"\)', text)


def main():
    args = [a for a in sys.argv[1:]]
    dry = "--dry-run" in args
    if "--dry-run" in args:
        args.remove("--dry-run")

    if "--print" in args:
        for n in CORE_FIELDS:
            print(n)
        return 0

    if not args:
        print(__doc__)
        return 1

    path = args[0]
    if not path.endswith(".kicad_pro"):
        print("HATA: .kicad_pro dosyasi bekleniyor, verilen: %s" % path)
        return 1

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    node = data
    for key in KEY_PATH[:-1]:
        node = node.setdefault(key, {})
    leaf = KEY_PATH[-1]
    current = node.get(leaf)

    have = existing_names(current)
    to_add = [n for n in CORE_FIELDS if n not in have and n not in RESERVED]
    merged = have + to_add

    if not to_add:
        print("Degisiklik yok: %d alan zaten tanimli." % len(have))
        return 0

    # Mevcut sekli koru: liste ise liste, degilse tek s-expression string
    if isinstance(current, list):
        node[leaf] = ['(field (name "%s"))' % n for n in merged]
    else:
        node[leaf] = serialize(merged)

    print("Mevcut  : %s" % (", ".join(have) if have else "(yok)"))
    print("Eklenen : %s" % ", ".join(to_add))
    print("Toplam  : %d alan" % len(merged))

    if dry:
        print("\n--dry-run: dosya yazilmadi.")
        print(json.dumps({leaf: node[leaf]}, ensure_ascii=False, indent=2))
        return 0

    shutil.copy2(path, path + ".bak")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print("\nYazildi: %s" % path)
    print("Yedek  : %s.bak" % path)
    print("KiCad'i acip Schematic Setup > Field Name Templates altindan dogrula.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
