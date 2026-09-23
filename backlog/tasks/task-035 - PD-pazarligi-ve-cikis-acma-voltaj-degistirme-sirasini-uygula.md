---
id: TASK-035
title: PD pazarlığı ve çıkış açma/voltaj değiştirme sırasını uygula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - firmware
milestone: m-3
dependencies:
  - TASK-033
  - TASK-034
documentation:
  - software/FIRMWARE_GEREKSINIMLERI.md
priority: high
ordinal: 141000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 VSELMIN boot sonrası ≤3.2 V
- [ ] #2 5 V altı yalnız PPS; APDO minimumu altına istek gönderilmiyor
- [ ] #3 Çıkış açma ve voltaj değiştirme sırası §3'e uygun
- [ ] #4 Hard Reset/detach -> OUT_EN hemen low
- [ ] #5 Çalışma akımı ≤3 A, OCP eşiği ayarlı
- [ ] #6 FAULT/UVP izleme ve PPS kablo düşümü kompanzasyonu
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
