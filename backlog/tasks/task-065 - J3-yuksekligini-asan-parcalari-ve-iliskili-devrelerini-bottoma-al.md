---
id: TASK-065
title: J3 yüksekliğini aşan parçaları ve ilişkili devrelerini bottom'a al
status: Done
assignee: []
created_date: '2026-09-23 20:34'
updated_date: '2026-09-24 12:25'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-061
  - TASK-064
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/KLS1-242I.pdf
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 108000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
LCD modülü kartın top yüzüne J3 yüksekliği kadar yakın oturur. Bu yüzden gövde yüksekliği J3'ü (KLS1-242I-2.0, ~2,0 mm; kesin değer TASK-061 modelinden/datasheet'ten) aşan her parça LCD izdüşümü içinde top'ta kalamaz ve bottom'a alınır.

Bir parça bottom'a giderse onunla aynı akım döngüsünü veya kısa bağlantı gerektiren devreyi paylaşan parçalar da aynı tarafa gider. Örnek: DC-DC bobini (L1 FPI0705 5,0 mm, L3) J3'ten yüksekse bottom'a iner, dolayısıyla ilgili regülatör (U5 AOZ1284 / U11 TPS55340), giriş/çıkış kapasiteleri, diyot ve FB/COMP ağı da bottom'a iner; döngü katman değiştirmemeli.

Aday uzun parçalar (TASK-061 sonrası kesinleşir): L1, L3, C33 süperkapasitör, SW3 enkoder (panel parçası, ayrı değerlendirilir), J1 USB-C, CR2032 tutucu, elektrolitik/polimer kapasiteler.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 J3 gövde yüksekliği (h_J3) datasheet'ten mm cinsinden yazılmış; LCD alt yüzü ile kart arasındaki boşluk ve kullanılan pay (ör. h_J3 − 0,2 mm) karar dosyasında
- [x] #2 3D modellerden tüm parçaların yükseklik listesi çıkarılmış; h > h_J3 olan her parça ve yanına gelen ilişkili parçalar (ref listesi) design_decisions/ altında tablo
- [x] #3 LCD izdüşümü içinde top tarafta h > h_J3 olan parça 0 (3D görünüm veya betikle doğrulanmış); SW3 gibi panel parçaları izdüşüm dışında
- [x] #4 Her DC-DC bloğunun (U5, U11, backlight) güç döngüsü parçaları (IC, bobin, Cin, Cout, diyot/FET, FB/COMP) tek tarafta; döngü katman değiştirmiyor
- [x] #5 Bottom'a alınan parçalar için dizgi etkisi (çift taraflı SMT, ağır parçaların reflow yönü) TASK-015'e not düşülmüş
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — Uygulandı ve doğrulandı.
- 58 footprint B.Cu'ya alındı; ilişkili 8 blok alt yüzde tutarlı. Buck/boost
  güç/FB/COMP üyeleri B.Cu, backlight Q7/R28/R29/R60 ve J3 F.Cu.
- 143 footprint tarandı; 125 model / 36 farklı STEP dosyası FreeCAD ile
  ölçüldü. 14 test pedi +4 montaj deliği modelsiz PCB öğesi; eksik model 0.
  J9 kırık model yolu proje içi basit tel zarfıyla düzeltildi.
- LCD toleranslı izdüşümünde top h>2,00 mm parça 0; J3 harici 1,80 mm
  bütçeyi aşan çıkıntı 0. SW3 PCB'de yok; J9 tel zarfı LCD'nin dışında.
- D5.2–U11.9 BOOST_FB dört segmentiyle B.Cu'ya taşındı: 2,584607 mm,
  graf sürekliliği doğrulandı. Routing'in kalanı tamamlanmış değildir.
- J3/J9/H1–H4 ankrajları, tüm footprint/pad netleri/UUID'ler, grup üyelikleri
  ve Edge.Cuts korundu. C33 flip sonrası Y1 ile çakışmayacak şekilde
  aynı geçici gövde yuvasına geri ötelenip referans yazıları düzeltildi.
- kicad-cli pcb drc --schematic-parity: parity 0; DRC 148→146,
  unconnected 360→360; yeni ihlal 0; courtyard/clearance/shorting 0.
  Mevcut 146 bulgu nihai yerleşim ve üretim görevlerinde devam ediyor.
- Kanıt: `hardware/docs/reports/task-065-20260924/verification.json`,
  `drc-before.json`, `drc-after.json`, `inventory-before/after.json`,
  `heights-before/after.csv/json`; top/bottom SVG ve 3D görüntüler incelendi.
  `audit.py`, `apply_sides.py`, `verify.py` çalışma betikleridir.
- Karar ve tüm 143 ref için yükseklik tablosu:
  `design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.
  J3=2,00±0,15 mm; top bütçe 1,80 mm; LCD montaj hedefi 2,35±0,15 mm.
- Çift taraflı SMT/ağır parçalar ve C33/J8 pin kesme şartı TASK-015'e,
  fiziksel Z/FPC doğrulaması TASK-012'ye, yerleşim devri TASK-069/085'e yazıldı.
  Blokların kart dışı geçici yerleşimi korundu; son konumlarda tarama tekrarlanır.

24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir. Tamamlanan grup/yükseklik çalışmasının tarihsel kanıtı korunur; J7/U2 top'a taşıma ve yeniden doğrulama TASK-063/008 kapsamındadır.
<!-- SECTION:NOTES:END -->
