---
id: TASK-062
title: Board shape'i LCD görünür alanına göre belirle
status: Done
assignee: []
created_date: '2026-09-23 20:33'
updated_date: '2026-09-23 21:23'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/PCB_LAYOUT_YOL_HARITASI_20260912.md
  - design_decisions/output/KART_DIS_HATTI_LCD_20260924.md
  - hardware/datasheets/TFT032B018.pdf
priority: high
ordinal: 102000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kart dış hattı (Edge.Cuts) TFT032B018 ekranına göre şekillenecek. Referans LCD'nin görünür alanı (active/viewing area): ön paneldeki pencere bu alana oturur, kart ve modül dış ölçüleri (77,7 x 55,04 mm) bunun etrafında konumlanır. Eski 93 x 60 mm varsayımı (PCB_LAYOUT_YOL_HARITASI_20260912.md) geçersiz.

TFT032B018 mekanik çizimi depoda yok; önce datasheet hardware/datasheets/ altına alınıp görünür alanın modül dış hattına göre ofseti (genelde merkezde değil, FPC tarafına kaymış) okunmalı. Kart koordinat orijini görünür alan merkezine bağlanır ki kutu (3d_design/) aynı referansı kullansın.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 TFT032B018 mekanik çizimi hardware/datasheets/ altında; modül dış ölçüsü, görünür alan ölçüsü ve görünür alanın modül kenarlarına ofseti design_decisions/ altına yazılmış
- [x] #2 Edge.Cuts kapalı tek kontur; kart görünür alanı her kenarda kapsıyor, kart ölçüsü ve köşe yarıçapı karar dosyasında gerekçeli
- [x] #3 PCB'de görünür alan ve LCD modül dış hattı User.Drawings (veya User.1) katmanında referans çizim olarak var; grid/aux orijin görünür alan merkezinde
- [x] #4 Montaj delikleri (adet, çap, konum) LCD modül ve kutu ile çakışmayacak şekilde yerleşmiş
- [x] #5 DRC'de Edge.Cuts kaynaklı hata yok
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
- [x] #3 PCB_LAYOUT_YOL_HARITASI_20260912.md'deki 93 x 60 mm ve kenar atamaları yeni karara göre güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 - ilk commit b936b74 (107 x 61 mm). Kullanıcı itirazıyla revize edildi (ESP32 konumu sabit değildi); son hâlin commit'i aşağıda.

Kullanıcı kararları:
- LCD üst yüzde yatay; FPC sağ kenardan arkaya bükülüyor.
- Enkoder panele monte edilip kabloyla bağlanacak (TASK-066).
- Sağ ve sol kenarın AA'ya uzaklığı eşit; üst/alt pay LCD modülünden 3 mm.

LCD çizimi (hardware/datasheets/TFT032B018.pdf):
- Modül 77,70 x 55,04 x 2,40 mm, AA 64,80 x 48,60 mm.
- AA'nın modül kenarlarına ofseti: FPC kenarı 9,02, karşı kenar 3,88, uzun kenarlar 3,22/3,22 mm.
- Ön panel penceresi AA + 0,4 mm = 65,60 x 49,40 mm.

Kart:
- Edge.Cuts 99,40 x 61,04 mm, r 3. Tek kapalı kontur (4 çizgi + 4 yay).
- AA merkezine göre koordinatlar: x ±49,70, y ±30,52. Aux/grid orijini AA merkezinde, sayfa (100,100).
- AA → kart kenarı: sağ/sol 17,30 mm. LCD modülü → kart kenarı: sağ 8,28, sol 13,42, üst/alt 3,00 mm.
- 17,30 mm, sağ deliklerin LCD izdüşümü dışında kalması için gereken en küçük değer.
- Dwgs.User katmanında: AA, modül dış hattı, panel penceresi, merkez artısı ve FPC işareti.

Delikler:
- H1-H4 M3 NPTH Ø3,2, board-only, kilitli; konumlar (±45,70, ±26,52), delik dikdörtgeni 91,40 x 53,04 mm.
- H2/H4'te M3 başı ile LCD kenarı arasında 1,08 mm boşluk var. FPC bandı çizimden yaklaşık y -21,4..+17,05 aralığında, deliklerin dışında (numunede doğrulanacak).

ESP32 anteni kart ölçüsünü belirlemiyor; konumu TASK-063/054'te. Sağ şerit 8,28 mm; 15 mm anten boşluğu için modülü dışarı taşırma ya da MINI-1U değerlendirilmeli.

Başlangıç yerleşimi (+55,-9) mm kaydırıldı. Tüm parçalar tamamen içeride ya da tamamen dışarıda; itilen parça yok. SW3 geçici olarak sol üstte.

DRC (kicad-cli pcb drc --schematic-parity), önce -> sonra:
- invalid_outline 1 -> 0
- copper_edge_clearance 3 -> 0
- silk_edge_clearance 0 -> 0
- H1-H4 içeren ihlal 0
- parity 0 -> 0

Kalan 4 hole_clearance J7 footprint'inin kendi içinde, kenarla ilgili değil.

Son hâl: commit 112fcc5.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Kart dış hattı TFT032B018 görünür alanına göre 99,40 x 61,04 mm (r 3) oldu. Sağ/sol kenar AA'dan eşit 17,30 mm, üst/alt kenar LCD modülünden 3 mm. Orijin AA merkezinde. LCD/AA referansı Dwgs.User'da; 4 x M3 NPTH delik LCD izdüşümü dışında. Edge.Cuts kaynaklı DRC hatası 0. ESP32 anten konumu TASK-063/054'te. Enkoderin panele taşınması TASK-066'da. Karar dosyası: KART_DIS_HATTI_LCD_20260924.md.
<!-- SECTION:FINAL_SUMMARY:END -->
