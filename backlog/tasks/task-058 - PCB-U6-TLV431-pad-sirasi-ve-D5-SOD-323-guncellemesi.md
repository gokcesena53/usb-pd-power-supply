---
id: TASK-058
title: 'PCB: U6 TLV431 pad sırası ve D5 SOD-323 güncellemesi'
status: To Do
assignee: []
created_date: '2026-09-23 12:54'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-057
references:
  - design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md
ordinal: 108000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-057 şema değişikliğinin PCB'ye aktarılması. U6'nın SOT-23 kılıfı aynı kalıyor ama pin eşlemesi değişti: pad 1 = REF, pad 2 = K. D5'in footprint'i Diode_SMD:D_SOD-123 yerine D_SOD-323 oldu. R42 kaldırıldı, R43'ün değeri değişti (2512 kalıyor).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 PCB 'Update from schematic' sonrası U6 pad1 = Net-(U6-REF), pad2 = EN_CTRL, pad3 = GND
- [ ] #2 D5 SOD-323; pad1 (katot) EN_CTRL, pad2 (anot) BOOST_FB
- [ ] #3 R42 PCB'den silindi; DRC 0 hata, bağlanmamış öğe yok
- [ ] #4 D5, U11 FB pinine yakın: BOOST_FB yolu ≤10 mm
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
