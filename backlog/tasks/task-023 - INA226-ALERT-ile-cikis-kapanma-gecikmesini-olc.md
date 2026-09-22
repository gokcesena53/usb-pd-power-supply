---
id: TASK-023
title: INA226 ALERT ile çıkış kapanma gecikmesini ölç
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
priority: high
ordinal: 64000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
INA226 ALERT'i şönt dönüşümü sonunda değerlendirir: ~140 us (şönt-sürekli, AVG=1) – ~280 us; LM74801 HGATE kapanma deglitch'i 3-6 us. Q5 bu süreyi SOA içinde taşımalı; yedek katman AP33772S OCP.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Kısa devre testinde ALERT -> U13 -> U12 EN gecikmesi ölçüldü
- [ ] #2 Q5 bu sürede SOA içinde kaldı
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
