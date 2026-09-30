---
id: TASK-022
title: HGATE yumuşak açılışını ve Q5 SOA'yı doğrula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
references:
  - hardware/datasheets/sqjb60ep.pdf
priority: high
ordinal: 129000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
HGATE 55 uA + R54/C30, SQJB60EP ile hesap: ~2.7 V/ms yumuşak açılış -> 2.7 A, 10.4 ms, t=0'da 75 W (die başına ~37 W). Datasheet SOA'sı 10 ms / 14 V'ta ~4-5 A gösteriyor (TC=25 C); marj var gibi ama ölçülmeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 1000 uF kapasitif yükte inrush ölçüldü, SOA içinde
- [ ] #2 3 A rezistif yükte açılış SOA içinde
- [ ] #3 3.3 V çıkışta gate voltajı ve D6 zener clamp uygun
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
