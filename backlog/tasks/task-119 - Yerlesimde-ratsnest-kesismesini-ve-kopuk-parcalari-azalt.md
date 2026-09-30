---
id: TASK-119
title: Yerleşimde ratsnest kesişmesini ve kopuk parçaları azalt
status: Done
assignee: []
created_date: '2026-09-29 12:06'
updated_date: '2026-09-29 12:06'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/placement-routability-20260929/
  - .claude/skills/kicad-placement/scripts/placelib.py
  - .claude/skills/kicad-placement/scripts/place.py
documentation:
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - CHANGES.TXT
modified_files:
  - hardware/gopo.kicad_pcb
  - CHANGES.TXT
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - .claude/skills/kicad-placement/SKILL.md
  - .claude/skills/kicad-placement/scripts/placelib.py
  - .claude/skills/kicad-placement/scripts/place.py
  - .claude/skills/kicad-placement/scripts/pcb_apply.py
  - .claude/skills/kicad-placement/scripts/pcb_check.py
  - .claude/skills/kicad-placement/examples/gopo_rev_c.py
priority: high
ordinal: 205000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ağırlıklı uzunluk kesişme/via ve IC-yerel parçaları görmüyor. Kesişme cezası, dekuplaj-IC aynı yüz kuralı (yer yoksa karşı yüz, flip desteği), IC-yerel otomatik kenar ve w>=5 kötüleşme koruması ekle; mevcut yerleşime uygula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Aynı yüz kesişme sayısı başlangıca (113) göre en az %25 düşük
- [x] #2 Dekuplaj kondansatörü SMD IC'den farklı yüzde 0 (flip varsa gerekçeli)
- [x] #3 >0,5 mm uzayan ağırlık>=5 kritik kenar yok; S artışı <= %1
- [x] #4 Kilitli H1-H4/J3 yerinde; pad-net/yüz/footprint farkı yok; parite 0; courtyard çakışması 0
- [x] #5 Flip modeli pcb_apply ile 0,0000 mm pad sapmasıyla doğrulanmış
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanıt (29.09.2026):
- place.py score (m4.json): S 10973,1 → 10982,7; aynı yüz kesişme 113 → 75; via kenarı 28 → 27; kopuk 10 → 7; dekuplaj yüz ihlali [] → []; flip yok; uzayan kritik kenar (>0,5 mm) [].
- pen: toplam ceza 0,000.
- pcb_check: footprint 144, taşınan 105, kilitli taşınan [], pad-net/yüz/footprint farkı [], dış hat aynı; DRC 62 → 59 (silk_overlap 20→19, silk_over_copper 17→15), bağlantısız 361→361, parite 0. SONUC: GECTI.
- Flip testi: C14 (k=5), C3 (k=4), C5 (k=7) pcb_apply → pad sapması 0,0000 mm; pcb_check izinsiz C5 flip'ini yakaladı (KALDI). Ayrıca 7 parçada Flip+Rotate(90) modeli 58 padde 0 sapma.
- İlk deneme (NO_WORSE_W=10) reddedildi: R11 Kelvin 6,7 → 10,6 mm, RShunt1/R39 FB uzadı. NO_WORSE_W=5 ile tekrarlandı.
- R2/R3 elle U2 pinlerine (1,5 mm) alındı: kesişme 69 → 75 (bilinçli ödünleşim).
- Kalan: C23 için U11 çevresinde daha yakın yasal slot yok (en yakın 7,17 mm).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Kesişme 113 -> 75, via kenarı 28 -> 27, kopuk 10 -> 7, S +%0,1; kritik kenar uzaması yok. W_CROSS/W_DECAP_SIDE/W_GND_LOCAL öneri değerleri kullanıcı onayı bekliyor.
<!-- SECTION:FINAL_SUMMARY:END -->
