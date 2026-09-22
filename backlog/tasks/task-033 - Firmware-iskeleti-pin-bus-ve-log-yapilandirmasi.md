---
id: TASK-033
title: 'Firmware iskeleti: pin, bus ve log yapılandırması'
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
labels:
  - firmware
milestone: m-3
dependencies: []
documentation:
  - software/FIRMWARE_GEREKSINIMLERI.md
priority: high
ordinal: 74000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 OUT_EN (GPIO6) açılışta low
- [ ] #2 I2C GPIO18/19'da; AP33772S, INA226, BQ32000 adreslerinde yanıt veriyor
- [ ] #3 Loglar USB-Serial/JTAG üzerinden
- [ ] #4 Gereksinimler §1 karşılandı
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
