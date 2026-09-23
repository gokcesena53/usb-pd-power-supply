---
id: TASK-009
title: SMBJ30A katot bandı yönünü PCB'de doğrula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-006
priority: medium
ordinal: 115000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Şema/footprint tarafı 22.09'da kontrol edildi: pin 1 (D_SMB katot pedi) D3'te USB_VBUS, D7'de OUT_POS'ta.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 D3 katot bandı VBUS tarafında
- [ ] #2 D7 katot bandı OUT_POS tarafında
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
