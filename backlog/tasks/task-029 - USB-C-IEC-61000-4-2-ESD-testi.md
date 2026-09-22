---
id: TASK-029
title: USB-C IEC 61000-4-2 ESD testi
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
ordinal: 70000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
CC1/CC2'de yalnız AP33772S (HBM 2 kV) var. Test geçmezse D8/D9 SMF30A takılır; takmadan önce CC BMC dalga şekli ve toplam CC kapasitesi (cReceiver ≤600 pF; SMF30A ~400 pF @0 V) ölçülmeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J7 üzerinde 8 kV kontak / 15 kV hava testi yapıldı
- [ ] #2 Sonuca göre D8/D9 kararı verildi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
