---
id: TASK-001
title: L3 boost bobinini seç
status: To Do
assignee: []
created_date: '2026-09-22 18:45'
updated_date: '2026-09-22 19:15'
labels:
  - schematic
  - procurement
milestone: m-0
dependencies: []
references:
  - hardware/docs/output/BOM_OZDISAN_REV_C_20260921.xlsx
priority: high
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Şemadaki B82422H1682K000 (1210 çip) Isat ≥3 A şartını karşılamıyor. Özdisan stoğunda 1210 ayağa uyan uygun parça yok; footprint değişikliği gerekebilir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 6.8–10 uH, Isat ≥3 A, düşük DCR bir parça seçildi
- [ ] #2 Sembol alanları (MPN, Manufacturer, SelectionNote) ve footprint güncellendi
- [ ] #3 ERC 0 hata
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
