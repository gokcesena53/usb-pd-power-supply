---
id: TASK-059
title: V_X ve U11 FB clamp'ini prototipte ölç
status: Blocked
assignee: []
created_date: '2026-09-23 12:54'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-058
references:
  - design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md
ordinal: 109000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-057 worst-case analizinin prototip üzerinde doğrulanması. Analizde doğrulanamayan iki varsayım var: AOZ1284'ün EN giriş akımı (≤10 µA varsayıldı) ve boost başlamadan önceki V_PRE (4.3 V varsayıldı). Hesaplanan değerler design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md dosyasında.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 V_X (EN_CTRL, U6 pin 2) 5 V ve 28 V PD profillerinde 1.566–1.652 V aralığında
- [ ] #2 28 V pass-through'da U11 FB (pin 9) ≤2.45 V
- [ ] #3 5 V profilde V_PRE 4.82–5.23 V; D5 akımı nedeniyle sapma <20 mV (D5 sökülü/takılı karşılaştırması)
- [ ] #4 Açılışta (vSafe5V attach) V_PRE aşımı osiloskopla kaydedildi, <5.5 V
- [ ] #5 U5 EN giriş akımı R43/R50 düşümünden hesaplandı, ≤100 µA
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
