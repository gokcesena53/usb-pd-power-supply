---
id: TASK-027
title: OUT_EN'in reset/boot boyunca çıkışı kapalı tuttuğunu doğrula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
ordinal: 68000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 ESP32 reset ve boot boyunca U12 kapalı (GPIO6 zayıf pull-up'a karşı R61 4k7)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
