---
id: TASK-004
title: Şema tasarım notlarını seçilmiş parçalara göre güncelle
status: To Do
assignee: []
created_date: '2026-09-22 18:45'
updated_date: '2026-09-22 19:15'
labels:
  - schematic
milestone: m-0
dependencies: []
priority: medium
ordinal: 45000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
usb_pd_controller AOZ1284 bölgesindeki eski not ("Cout: 10V X7R ... >=44uF", "L/D exact MPN and footprints require selection", "L: Isat >=2A") güncel değil: L1 SRI0704-220M, D2 SS2060FL, C15 hibrit + C16 seçildi.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 AOZ1284 notu seçilmiş parçalara göre yeniden yazıldı
- [ ] #2 Diğer sayfalardaki notlar tarandı, eskiyenler düzeltildi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
