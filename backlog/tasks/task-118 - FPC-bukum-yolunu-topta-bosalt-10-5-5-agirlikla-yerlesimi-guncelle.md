---
id: TASK-118
title: 'FPC büküm yolunu top''ta boşalt, 10/5/5 ağırlıkla yerleşimi güncelle'
status: Done
assignee: []
created_date: '2026-09-29 11:09'
updated_date: '2026-09-29 11:09'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/placement-fpc-20260929/
  - design_decisions/output/LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md
documentation:
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - CHANGES.TXT
modified_files:
  - hardware/gopo.kicad_pcb
  - CHANGES.TXT
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - .claude/skills/kicad-placement/scripts/placelib.py
  - .claude/skills/kicad-placement/examples/gopo_rev_c.py
  - .claude/skills/kicad-placement/SKILL.md
priority: high
ordinal: 204000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
LCD FPC büküm yolunda top layerda komponent bulunmamalı. kicad-placement ağırlıkları kullanıcı tarafından 10/5/1 → 10/5/5 yapıldı. Kilitli parçalar (H1-H4, J3) yerinde kalacak şekilde yerleşimi güncelle.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 FPC yolu (X 102.55-142.92, Y 101.05-117.55 mm) içinde F yüzde footprint 0; B THT pini 0 (termal via hariç)
- [x] #2 H1-H4 ve J3 0,0000 mm sapma; pad-net, yüz, footprint, dış hat farkı yok; parite 0
- [x] #3 Courtyard çakışması 0; >0,5 mm uzayan ağırlık-10/5 kritik kenar yok
- [x] #4 Skor 10/5/5 ağırlıkla önce/sonra, blok içi/arası ayrı raporlanmış
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanıt (29.09.2026):
- pcbnew taraması cand.kicad_pcb: FPC dikdörtgeniyle kesişen footprint'lerin hepsi B yüzde (U11, U5, L1, C12…); F yüzde 0.
- place.py pen: toplam ceza 0,000 (courtyard, keepout, bölge).
- pcb_check: footprint 144, taşınan 44, kilitli taşınan [], pad-net/yüz/footprint farkı [], dış hat aynı; DRC parite 0, bağlantısız 361→361; ihlal 54→62 (silk_overlap 15→20, silk_over_copper 14→17; copper_edge_clearance 15 ve lib_footprint_mismatch 10 değişmedi). SONUC: GECTI.
- Skor (10/5/5): S 10771,1 → 10973,1; blok içi 6625,5→6814,5, blok arası 4145,5→4158,5; uzayan kritik kenar (>0,5 mm) yok.
- Reddedilen adaylar: 4 tohumlu sıfırdan pipeline legalize edilemedi. Artımlı legal+refine C31–U12'yi 18 mm'ye çıkardı.
- Render: hardware/docs/reports/placement-fpc-20260929/cand-top.png, cand-bot.png; durum ga.json.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Ağırlık config'e taşındı (W_ORDINARY=5); FPC yolu @F keepout. OUTSW top kümesi rijit (+7.0, -15.5) mm taşındı, R60 ve UI küçük kaydırma; 44 parça taşındı. S 10771 -> 10973 (+%2), kritik kenar uzaması yok.
<!-- SECTION:FINAL_SUMMARY:END -->
