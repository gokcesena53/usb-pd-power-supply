---
id: TASK-007
title: BOM'u şemadan yeniden üret
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - procurement
milestone: m-1
dependencies:
  - TASK-006
priority: medium
ordinal: 48000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
hardware/docs/output/BOM_REV_C_20260918.xlsx eski: INA228, AP74502Q, TPD4EUSB30 içeriyor; U13/R61/C35, R62/R63, D8/D9 (DNP) yok; R41/R55/C19 değerleri eski.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Yeni BOM şemadan üretildi, DNP'ler işaretli
- [ ] #2 Eski BOM dosyası kaldırıldı veya eski diye işaretlendi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
