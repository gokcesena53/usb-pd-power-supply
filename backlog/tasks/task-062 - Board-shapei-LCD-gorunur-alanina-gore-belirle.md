---
id: TASK-062
title: Board shape'i LCD görünür alanına göre belirle
status: Done
assignee: []
created_date: '2026-09-23 20:33'
updated_date: '2026-09-23 21:07'
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
24.09.2026 - commit b936b74.

Kullanıcı kararları: LCD üst yüzde yatay, FPC sağ kenardan arkaya bükülüyor. Enkoder panele monte edilip kabloyla bağlanacak (TASK-066).

Çizim (hardware/datasheets/TFT032B018.pdf): modül 77,70 x 55,04 x 2,40 mm, AA 64,80 x 48,60 mm. AA'nın modül kenarlarına ofseti: FPC kenarı 9,02, karşı kenar 3,88, uzun kenarlar 3,22/3,22 mm. Ön panel penceresi AA + 0,4 mm = 65,60 x 49,40 mm.

Kart: Edge.Cuts 107,0 x 61,0 mm, r 3; tek kapalı kontur (4 çizgi + 4 yay). AA merkezine göre koordinatlar: x -44,5..+62,5, y ±30,5. Aux/grid orijini AA merkezinde, sayfa (100,100). LCD modülü x -36,28..+41,42, y ±27,52. Kenar payları: üst/alt 2,98, sol 8,22 (M3), sağ 21,08 (anten). Dwgs.User katmanında AA, modül, panel penceresi, merkez artısı, FPC işareti ve LCD+15 mm çizgisi var.

Delikler: H1-H4 M3 NPTH Ø3,2, board-only, kilitli; konumlar (±) (-40,5/+58,5, ±26,5). H1/H3'ün M3 baş dairesi ile LCD kenarı arasında 1,02 mm var. H2/H4 anten alanından 16,7 mm uzakta.

U2 alt yüzde, y=0'da; modül ucu x=+62,0. Anten alanı LCD kenarından 15,18 mm uzakta.

Başlangıç yerleşimi (+61,-3) mm kaydırıldı. C23/C33/D10/J8/R55 kart dışına itildi; SW3 geçici olarak sol üstte.

DRC (kicad-cli pcb drc --schematic-parity), önce -> sonra: invalid_outline 1->0, copper_edge_clearance 3->0, silk_edge_clearance 0->0. H1-H4'ü içeren ihlal 0, parity 0->0. Kalan 4 hole_clearance J7 footprint'inin kendi içinde, kenarla ilgili değil.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Kart dış hattı TFT032B018 görünür alanına göre 107 x 61 mm (r 3) oldu. Orijin AA merkezinde. LCD/AA referansı Dwgs.User'da, 4 x M3 NPTH delik var. U2 anteni sağ kenarda, LCD kenarından 15,2 mm uzakta. Edge.Cuts kaynaklı DRC hatası 0. Karar dosyası: KART_DIS_HATTI_LCD_20260924.md. Enkoderin panele taşınması TASK-066'da.
<!-- SECTION:FINAL_SUMMARY:END -->
