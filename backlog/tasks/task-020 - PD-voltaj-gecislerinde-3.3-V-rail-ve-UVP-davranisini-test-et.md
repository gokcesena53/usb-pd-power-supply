---
id: TASK-020
title: PD voltaj geçişlerinde 3.3 V rail ve UVP davranışını test et
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
ordinal: 127000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 5→12, 5→28, 28→5, 5→3.3 V geçişlerinde ESP32 3.3 V rail'i ayakta
- [ ] #2 AP33772S UVP yanlış tetiklenmiyor
- [ ] #3 En az 3 farklı adaptörle denendi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
