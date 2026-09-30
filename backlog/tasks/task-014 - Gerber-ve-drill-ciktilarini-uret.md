---
id: TASK-014
title: Gerber ve drill çıktılarını üret
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-24 13:06'
labels:
  - fabrication
milestone: m-1
dependencies:
  - TASK-008
  - TASK-009
  - TASK-010
  - TASK-011
  - TASK-012
  - TASK-013
  - TASK-088
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: medium
ordinal: 121000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Üretim öncesi elektriksel/mekanik kabul aynı son PCB revizyonu için tamam; zone'lar dolu, bağlantısız öğe 0, schematic parity 0, açıklanmamış DRC hatası 0. İzinli istisnalar kanıtlı ve manifestte listeli.
- [ ] #2 Çıktılar hardware/gerber/ altında
- [ ] #3 Gerber/drill çıktıları son kabuldeki kart hash'i ve üretici stackup'ıyla eşleşiyor; katman/delik/slot görsel incelemesi ve çıktı manifesti kayıtlı. Sonradan değişiklik olursa kabul ve export tekrarlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.
<!-- SECTION:NOTES:END -->
