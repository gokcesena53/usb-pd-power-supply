---
id: TASK-117
title: AOZ1284 çıkış kondansatörü yerleşim kuralını datasheet ile teyit et
status: To Do
assignee: []
created_date: '2026-09-29 09:07'
labels:
  - layout
  - docs
milestone: m-1
dependencies:
  - TASK-115
references:
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
priority: low
ordinal: 203000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-115'te C16 (buck çıkış) için C16.1-L1.2 ve C16.2-D2.2 çiftleri ağırlık 10 olarak eklendi; AOZ1284 datasheet layout bölümüyle teyit edilmedi. Teyit edilip ağırlık sınıfı kesinleştirilecek.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 AOZ1284PI datasheet layout maddesi sayfa numarasıyla alıntılanmış
- [ ] #2 C16 çiftlerinin ağırlığı (10 veya 1) karar dosyasında kesinleştirilmiş
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
