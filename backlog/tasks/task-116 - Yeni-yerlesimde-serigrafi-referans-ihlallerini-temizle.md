---
id: TASK-116
title: Yeni yerleşimde serigrafi referans ihlallerini temizle
status: To Do
assignee: []
created_date: '2026-09-29 09:07'
labels:
  - layout
  - fabrication
milestone: m-1
dependencies:
  - TASK-115
references:
  - hardware/docs/reports/placement-scratch-20260929/drc_after.json
  - hardware/gopo.kicad_pcb
priority: medium
ordinal: 202000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-115 sonrası referans yazıları parçalarla taşındı; DRC'de 15 silk_overlap ve 14 silk_over_copper yeni ihlal var. TASK-103 kurallarıyla düzelt.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 KiCad DRC silk_overlap = 0 ve silk_over_copper = 0
- [ ] #2 Parça konumları değişmemiş (0,0000 mm), courtyard çakışması 0, parite 0
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
