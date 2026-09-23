---
id: TASK-008
title: Kritik yerleşim kurallarını uygula
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-23 05:56'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-006
references:
  - hardware/datasheets/LM7480-Q1.pdf
priority: high
ordinal: 49000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 D3 SMBJ30A ve C3 J7'nin dibinde; CC1/CC2 izleri kısa (AP33772S yerleşim notu)
- [ ] #2 U10 D+/D- flow-through (1-6, 3-4)
- [ ] #3 U12 A/DGATE/C pinleri Q5B'nin S/G/D'sine, HGATE/OUT Q5A'nın G/S'sine yakın; DGATE izi kısa (LM7480 §12.1)
- [ ] #4 C32 VS ve GND'ye yakın; C31 MOSFET'lerden uzak
- [ ] #5 OUT_POS ve GND bakırı J4 lehim pedlerine (SolderWire-1.5sqmm) polygonla bağlı; 3 A'de ΔT ≤ 10 °C (IPC-2152) (TASK-044)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
