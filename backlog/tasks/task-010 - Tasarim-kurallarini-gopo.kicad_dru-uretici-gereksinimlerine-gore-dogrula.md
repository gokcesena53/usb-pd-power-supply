---
id: TASK-010
title: Tasarım kurallarını (gopo.kicad_dru) üretici gereksinimlerine göre doğrula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-23 15:18'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_dru
priority: medium
ordinal: 116000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Üretici seçildi ve yetenekleri not edildi
- [ ] #2 gopo.kicad_dru buna göre güncellendi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026 (TASK-006): U11 footprint'i Package_SO:Texas_HTSSOP-14-1EP_..._ThermalVias 0.2 mm termal via delikleri içeriyor; gopo.kicad_dru/board setup min delik 0.3 mm -> 15x drill_out_of_range. Üreticinin min deliği netleşince ya kural ya da footprint (ThermalVias'sız varyant + elle via) seçilmeli.
<!-- SECTION:NOTES:END -->
