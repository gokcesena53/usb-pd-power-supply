---
id: TASK-036
title: BQ32000 RTC sürücüsü
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - firmware
milestone: m-3
dependencies:
  - TASK-033
documentation:
  - software/FIRMWARE_GEREKSINIMLERI.md
ordinal: 143000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Trickle charge TCHE=0x5, TCH2=1, TCFE=1
- [ ] #2 Güç kaybı sonrası VCC ≥1 ms koşulu sağlanıyor
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
