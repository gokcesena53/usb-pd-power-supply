---
id: TASK-033
title: 'Firmware iskeleti: pin, bus ve log yapılandırması'
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-29 14:20'
labels:
  - firmware
milestone: m-3
dependencies: []
documentation:
  - software/FIRMWARE_GEREKSINIMLERI.md
priority: high
ordinal: 140000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 OUT_EN (GPIO6) açılışta low
- [ ] #2 I2C GPIO22 SCL / GPIO23 SDA'da (TASK-123 pin tablosu); AP33772S, INA226, BQ32000 adreslerinde yanıt veriyor
- [ ] #3 Loglar USB-Serial/JTAG üzerinden
- [ ] #4 Gereksinimler §1 karşılandı (pin tablosu 29.09.2026)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
29.09.2026: TASK-123 ile ESP32 pin ataması değişti (I2C 18/19 -> 22/23, TFT/encoder/kesme pinleri); güncel tablo software/FIRMWARE_GEREKSINIMLERI.md §1.
<!-- SECTION:NOTES:END -->
