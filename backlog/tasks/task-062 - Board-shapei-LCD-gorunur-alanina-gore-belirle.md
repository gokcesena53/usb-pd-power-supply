---
id: TASK-062
title: Board shape'i LCD görünür alanına göre belirle
status: To Do
assignee: []
created_date: '2026-09-23 20:33'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/PCB_LAYOUT_YOL_HARITASI_20260912.md
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
- [ ] #1 TFT032B018 mekanik çizimi hardware/datasheets/ altında; modül dış ölçüsü, görünür alan ölçüsü ve görünür alanın modül kenarlarına ofseti design_decisions/ altına yazılmış
- [ ] #2 Edge.Cuts kapalı tek kontur; kart görünür alanı her kenarda kapsıyor, kart ölçüsü ve köşe yarıçapı karar dosyasında gerekçeli
- [ ] #3 PCB'de görünür alan ve LCD modül dış hattı User.Drawings (veya User.1) katmanında referans çizim olarak var; grid/aux orijin görünür alan merkezinde
- [ ] #4 Montaj delikleri (adet, çap, konum) LCD modül ve kutu ile çakışmayacak şekilde yerleşmiş
- [ ] #5 DRC'de Edge.Cuts kaynaklı hata yok
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
- [ ] #3 PCB_LAYOUT_YOL_HARITASI_20260912.md'deki 93 x 60 mm ve kenar atamaları yeni karara göre güncellendi
<!-- DOD:END -->
