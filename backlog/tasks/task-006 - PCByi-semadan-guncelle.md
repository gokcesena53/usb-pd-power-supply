---
id: TASK-006
title: PCB'yi şemadan güncelle
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-001
priority: high
ordinal: 47000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
KiCad: Tools > Update PCB from Schematic. Kart erken aşamada (7 segment, 0 via, 0 zone).

Yeni: Y1 (ABS25), C33 (Korchip DCL H-tipi), Q5 (SQJB60EP, hiç yerleştirilmemişti), Q7, R60, C34, U13 (SOT-23-5), R61, C35, R62, R63, D8/D9 (SOD-123F, DNP).

Kalkan: BT1, R22, R23, C10, U7, U8, L2, C20, C21, C22, R44, R45, R46, R25, R26, R57; Q4 (Q3 ile tek çift kılıfa birleşti).

Footprint değişen: Q3 Package_SO_Custom:Vishay_PowerPAK_SO-8L_Dual (PCB'de hâlâ SOIC-8 / IRF7855TRPBF), U12 WSON-12 3x3 (LM74801; EP boşta, GND'ye BAĞLANMAZ), U10 SOT-23-6 (USBLC6-2SC6), U4 SOIC-8, J3 KLS 30p FPC, C5 0805, C8 1210, C15/C29 CP_Elec_6.3x5.8, C31 0603, R59 0805.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Yeni bileşenlerin hepsi PCB'de
- [ ] #2 Kalkan bileşenler PCB'den silindi
- [ ] #3 Footprint değişiklikleri uygulandı; U12 EP GND'ye bağlı değil
- [ ] #4 PCB ile şema netlist'i uyumlu (Update PCB değişiklik önermiyor)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
