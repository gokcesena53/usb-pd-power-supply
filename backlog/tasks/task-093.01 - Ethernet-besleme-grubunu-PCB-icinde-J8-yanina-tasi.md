---
id: TASK-093.01
title: Ethernet besleme grubunu PCB icinde J8 yanina tasi
status: Done
assignee: []
created_date: '2026-09-25 08:17'
updated_date: '2026-09-25 11:37'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/gopo.kicad_dru
  - design_decisions/output/PORT_HIZASI_ENKODER_DUZELTME_20260925.md
  - design_decisions/output/ETHERNET_BESLEME_YERLESIMI_TASK093_01_20260925.md
  - hardware/docs/reports/task-093-01-20260925/verification.json
parent_task_id: TASK-093
priority: high
ordinal: 176000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kullanicinin istegi: PCB disinda duran Ethernet besleme grubunu (Q8, R17, C21, C20, C10, TP14) kart icinde J8 Ethernet modulunun yanina tasi. Son USB-C/Ethernet tam ust uste hizasi ve duz J9 enkoder sirasi korunacak. J8 ankraji (102.5,79.61 mm; 0 derece; B.Cu). TASK-093 altinda besleme grubuna ait somut yerlesim isi olarak takip edilir; uygunlugu dogrulanmis modul alti hacim kullanilabilir, sigmayan/yukseklik nedeniyle uygun olmayan elemanlar modulun hemen yaninda kart icine alinmalidir. Genel routing ve sema/BOM degisikligi kapsam disidir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Q8, R17, C21, C20, C10 ve TP14 kart disindan kart icine, J8 besleme/test pinlerine yakin tasinmis; son ref/x/y/aci/yuz tablosu kaydedilmis.
- [x] #2 C20/C10 ETH_3V3-GND dongusu kisa tutulmus; R17/C21 Q8 gate-source cevresinde yakin yerlestirilmis; pad/net eslemeleri korunmus.
- [x] #3 USB-C/Ethernet ayni Y ekseni, J9 duz pin sirasi, montaj delikleri ve LCD/FPC alani korunmus; RJ45 pin keepout, header ve modul alti yukseklik cakismalari kontrol edilmis; TP14 erisilebilir kalmis.
- [x] #4 Once/sonra ust-alt gorunum ve 3D kontrol kaydedilmis; schematic parity 0, yeni aciklanmamis DRC hatasi 0; mevcut hata ve baglantisiz oge farklari raporlanmis.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 — Ethernet besleme grubu (Q8, R17, C21, C20, C10, TP14) kart içi son konumlarına taşındı:
- C20 (100nF, 0402): (96.500, 93.580 mm; 90°; B.Cu) — J8 altı (underlay), Pin 14 (ETH_3V3) & Pin 12 (GND) iç kolonuna 3.6 mm mesafede yüksek frekans dekuplajı. Montaj yüksekliği 0.50 mm, mezanin alt yüzeyine dikey açıklık +2.00 mm nominal (+1.40 mm konservatif marj). gopo.kicad_dru dosyasındaki mezzanine courtyard kuralına C20 istisnası eklendi.
- C10 (22uF, 0805): (107.000, 94.000 mm; -90°; B.Cu) — J8 modül dışı doğu kenarı, Pin 13 (ETH_3V3) & Pin 11 (GND) dış kolonuna 4.6 mm mesafede bulk filtre. Modül altı yükseklik riski yok, lehim muayenesine açık.
- Q8 (TSM3443CX6, SOT-23-6): (107.000, 88.500 mm; 90°; B.Cu) — J8 modül dışı doğu kenarı, C10'un kuzeyinde; Drain pinleri ETH_3V3'e, Gate/Source doğuya bakar. İletim kaybı ~2 mW, açık kenarda doğal soğutmalı.
- R17 (100k, 0402): (111.500, 87.200 mm; 0°; B.Cu) — Q8 Pin 3 (Gate) ve Pin 4 (Source) hemen doğusunda pull-up.
- C21 (100nF, 0402): (111.500, 89.800 mm; 0°; B.Cu) — R17 altında, Q8 kapı-kaynak yumuşak kalkış.
- TP14 (D1.0mm TestPoint): (107.000, 82.150 mm; 0°; B.Cu) — J8 Pin 4 (`/MCU/ETH_RUN`) karşısında modül dışı açık alanda; modül takılıyken test probu erişimi %100 açık.

Doğrulama ve Kanıtlar:
- FreeCAD 3D Katı Kesişim: `hardware/docs/reports/task-093-01-20260925/solid-check.json`. C20-J8 1.940 mm, C10-J8 2.395 mm, Q8-J8 1.623 mm, R17-J8 6.998 mm, C21-J8 6.944 mm mesafe; tüm kesişim hacimleri 0.000 mm³ (çakışma 0).
- KiCad DRC & Parite: Yeni DRC hatası 0; başlangıçtaki 15 U2 kart-kenarı hatası aynen korundu, 0 şema parite farkı, 360 değişmeyen bağlantısız öğe.
- 15/15 pad-net eşleşmesi ve kalan 137 footprint konumu %100 korundu (`after-inventory.json`).
- Karar: `design_decisions/output/ETHERNET_BESLEME_YERLESIMI_TASK093_01_20260925.md`
- Raporlar ve SVGs: `hardware/docs/reports/task-093-01-20260925/` (`final-top.svg`, `final-bottom.svg`, `verification.json`).
<!-- SECTION:NOTES:END -->
