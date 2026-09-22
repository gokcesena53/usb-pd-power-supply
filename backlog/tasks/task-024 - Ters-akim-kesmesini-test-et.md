---
id: TASK-024
title: Ters akım kesmesini test et
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
ordinal: 65000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
LM74801 DGATE kesmesi: V(A-C) -4.5 mV, 0.5 us; 12 mOhm'da ~0.1-0.5 A ters akımda. Hafif yükte DGATE ileri yönde 177 mV'ta (gövde diyotu) açılır.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Çıkışa ayar değerinden yüksek harici kaynak bağlanınca DGATE kesiyor
- [ ] #2 Kesme sonrası Q5B gövde diyotu ters akımı bloke ediyor
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
