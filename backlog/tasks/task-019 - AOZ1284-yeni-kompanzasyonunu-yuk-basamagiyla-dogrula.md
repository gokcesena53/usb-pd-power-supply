---
id: TASK-019
title: AOZ1284 yeni kompanzasyonunu yük basamağıyla doğrula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
ordinal: 126000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
R41 51k, C19 15n, fC ~20 kHz. C15 hibrit + C16 seramiğin gerçek kapasitesiyle.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 0.3 A yük basamağında 3.3 V çökmesi ~25 mV
- [ ] #2 Faz payı yeterli
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
