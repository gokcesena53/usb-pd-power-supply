---
id: TASK-002
title: Özdisan'da stokta olmayan parçalar için tedarik/muadil kararı ver
status: To Do
assignee: []
created_date: '2026-09-22 18:45'
updated_date: '2026-09-22 19:36'
labels:
  - procurement
  - schematic
milestone: m-1
dependencies: []
references:
  - hardware/docs/output/BOM_OZDISAN_REV_C_20260921.xlsx
priority: medium
ordinal: 36000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
U1 AP33772S, U2 ESP32-C6, L1 SRI0704-220M Özdisan'da stokta değil.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 U1 için tedarik kaynağı veya muadil belirlendi
- [ ] #2 U2 için tedarik kaynağı veya muadil belirlendi
- [ ] #3 L1 için tedarik kaynağı veya muadil belirlendi
- [ ] #4 Karar SelectionNote alanlarına işlendi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
