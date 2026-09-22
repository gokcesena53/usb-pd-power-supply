---
id: TASK-034
title: INA226 sürücüsünü yaz
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - firmware
milestone: m-3
dependencies:
  - TASK-033
references:
  - design_decisions/output/CIKIS_AKIMI_3A_KARARI_20260922.md
documentation:
  - software/FIRMWARE_GEREKSINIMLERI.md
priority: high
ordinal: 75000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Register haritası INA226'ya göre (§4)
- [ ] #2 CAL 0x2000, Alert limit 0x1B58, Mask/Enable 0x8001 yazılıyor
- [ ] #3 Mandallı ALERT'ten sonra yeniden açma sırası uygulandı
- [ ] #4 İşaretli akımda ters akım -> OUT_EN low
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
