---
id: TASK-124
title: BOOST ve PD bloklarını blok bazlı yeniden yerleştir (LNS)
status: Done
assignee: []
created_date: '2026-09-29 14:56'
updated_date: '2026-09-29 14:57'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/placement-lns-20260929/
  - .claude/skills/kicad-placement/scripts/place.py
documentation:
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - CHANGES.TXT
modified_files:
  - hardware/gopo.kicad_pcb
  - CHANGES.TXT
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - .claude/skills/kicad-placement/scripts/place.py
priority: medium
ordinal: 210000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Seçili bloğu söküp diğer her şey sabitken yeniden kur (anneal --inp --blocks, legal/refine/untangle --blocks). Hedef: BOOST'ta C23 (SS) U11'e yakın, PD'de dekuplaj/kesişme iyileşmesi; sıcak döngüler ve kilitli parçalar korunur.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 C23-U11 SS mesafesi < 4 mm
- [x] #2 Boost sıcak döngü toplamı (17,0 mm) ve dekuplaj toplamı uzamamış; uzayan w>=5 kenar gerekçelendirilmiş
- [x] #3 Dekuplaj kondansatörü yer varken karşı yüze geçmemiş
- [x] #4 Kilitli H1-H4/J3 yerinde; pad-net/yüz/footprint farkı yok; parite 0; courtyard çakışması 0
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanıt (29.09.2026):
- BOOST tam blok: seed 71 sıcak döngü 17,0 → 20,8 mm (red), seed 72 legal L3 slot yok (red).
- BOOST sıcak döngü sabit (FIXED_EXTRA U11 L3 D4 C25-C28): seed 73 D5 FB 2,89 → 6,92 (red); seed 74 kabul: C23 SS 7,01 → 2,68, R53 EN 6,72 → 5,25, R49 GND 1,77 → 1,11, R52 2,99 → 2,65, C24 GND 1,58 → 2,64 (In1 via), D5 2,89 → 3,14; sıcak döngü 17,0 aynı; kesişme 38 → 38; S 7841,2 → 7840,1; kopuk 6 → 5.
- PD (U1 R11 Q3 sabit): seed 81 PD blok 422 → 454; seed 82 C1/C3/C4 flip (kural ihlali, red; flip refine/untangle'dan kaldırıldı); seed 83 dekuplaj +%8; seed 84 +%2 → PD değişmedi.
- pcb_apply taşınan 20 (BOOST 10; diğerleri align ızgara ≤ 0,017 mm), pad sapması 0; pcb_check kilitli taşınan [], pad-net/yüz/footprint farkı yok; DRC 60 → 61 (silk_overlap +1), bağlantısız 361, parite 0, GECTI.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
BOOST (sıcak döngü sabit) kabul: C23 7,0 -> 2,7 mm, R53 6,7 -> 5,3 mm, sıcak döngü aynı; C24 GND +1,1 mm. PD değişmedi (4 tohum da kötü). Flip yalnız legal'de (yer yoksa) kısıtı eklendi.
<!-- SECTION:FINAL_SUMMARY:END -->
