---
id: TASK-046
title: Motorobit 4 mm banana jak numunesini ölç
status: Blocked
assignee: []
created_date: '2026-09-23 05:55'
updated_date: '2026-09-23 05:55'
labels:
  - procurement
  - sample-eval
milestone: m-2
dependencies:
  - TASK-047
references:
  - design_decisions/output/CIKIS_KONNEKTORU_20260923.md
  - 'https://www.motorobit.com/4mm-metal-disi-banana-konnektor-kirmizi'
  - 'https://www.motorobit.com/4mm-metal-disi-banana-konnektor-siyah'
priority: medium
ordinal: 87000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
J5 (KOM.KNN.06.000021, kırmızı) ve J6 (KOM.KNN.06.000022, siyah) için satıcı sayfası akım/gerilim anma değeri, panel deliği ve ölçü vermiyor. Numune alınıp ölçülecek; J5/J6 footprint'i şu an Cinch 108-090x double-D panel kesimi.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Numune temin edildi (2 kırmızı, 2 siyah)
- [ ] #2 3 A sürekli akımda jak + 1.5 mm² lehimli kablo sıcaklık artışı ≤ 30 °C ölçüldü; temas direnci ≤ 5 mΩ
- [ ] #3 Panel delik çapı, düz/yuvarlak kesim, gövde boyu ve lehim ucu ölçüldü; J5/J6 panel footprint'i buna göre güncellendi
- [ ] #4 Gerilim anma değeri (≥ 30 V) ve metal gövdenin panele yalıtımı teyit edildi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
