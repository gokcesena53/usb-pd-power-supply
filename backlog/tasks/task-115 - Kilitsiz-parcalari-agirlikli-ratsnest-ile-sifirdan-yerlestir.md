---
id: TASK-115
title: Kilitsiz parçaları ağırlıklı ratsnest ile sıfırdan yerleştir
status: Done
assignee: []
created_date: '2026-09-29 09:07'
updated_date: '2026-09-29 09:07'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/placement-scratch-20260929/
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
documentation:
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - CHANGES.TXT
modified_files:
  - hardware/gopo.kicad_pcb
  - CHANGES.TXT
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
priority: high
ordinal: 201000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
kicad-placement skill'i ile H1-H4 ve J3 (kilitli) dışındaki parçaları sıfırdan yerleştir. IC'den dışa, blok içi sonra bloklar arası; kritik pad çiftleri 10/5/1 ağırlıklı. Onaylı TASK-101 mimarisi bölge kısıtı olarak korunur.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 H1-H4 ve J3 konumu 0,0000 mm sapma; parça yüzü, footprint, pad-net ve dış hat değişmemiş
- [x] #2 Courtyard çakışması 0 ve şematik parite 0 (KiCad DRC)
- [x] #3 Ağırlıklı skor S başlangıca göre düşük; blok içi ve bloklar arası ayrı raporlanmış
- [x] #4 Başlangıca göre uzayan her ağırlık-10 çift gerekçelendirilmiş
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanıt (29.09.2026):
- Yeniden açılan kart: 144/144 footprint, 137 taşındı; kilitli taşınan yok; pad-net, yüz, footprint değişikliği yok; dış hat aynı.
- Skor S 7171,1 -> 4025,2 (-%44); blok içi 5746,3 -> 3196,1; bloklar arası 1424,8 -> 829,1; L 2927,7 -> 1960,2.
- Döngüler: boost 33,1->17,0; buck giriş 79,0->43,8; bootstrap 9,6->4,1; USB TVS/ESD 49,2->32,6; D7 39,3->10,2; Kelvin 41,2->20,7; dekuplaj 162,1->78,0 mm.
- Uzayan w10: SW-D4 4,55->7,34 (döngü toplamı -%48), D3.1-J7 7,52->9,15 (sol şerit dar), C20-J8 3,48->4,20 (J8 altı boş). Gerekçe karar dosyasında.
- DRC: önce 25 / sonra 54 (+15 silk_overlap, +14 silk_over_copper), unconnected 360->361 (BOOST_FB deneme yolu silindi), parite 0, courtyard çakışması 0.
- Dosyalar: hardware/docs/reports/placement-scratch-20260929/ (before/after render, drc_before/after.json, score_after.json, before.kicad_pcb).
<!-- SECTION:NOTES:END -->
