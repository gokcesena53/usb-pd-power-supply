---
id: TASK-122
title: Yerleşim metriğine In2 güç polygonlarını yansıt
status: Done
assignee: []
created_date: '2026-09-29 13:49'
updated_date: '2026-09-29 13:49'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/placement-plane-20260929/
  - .claude/skills/kicad-placement/examples/gopo_rev_c.py
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
ordinal: 208000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
In2 POWER_PLANE tüm güç hatları için bölünmüş polygon (kullanıcı kararı). Güç netleri ve GND'nin sıradan bağlantılarını kesişmeden çıkar, W_PLANE ile say; kritik kenarlar iz olarak kalır. Yeni metrikle yerleşimi iyileştir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 PLANE_NETS ve W_PLANE config'te; düzlem netlerinin kritik kenarları skor ve kesişmede kalıyor
- [x] #2 Yeni tabanla sinyal kesişmesi azalmış; uzayan ağırlık>=5 kritik kenar yok
- [x] #3 Kilitli H1-H4/J3 yerinde; pad-net/yüz/footprint farkı yok; parite 0; courtyard çakışması 0
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanıt (29.09.2026):
- Metrik değişikliği (hiç taşıma yok), m4 durumu: kesişme 75 → 57, via kenarı 27 → 19; S tabanı 10982,7 → 8237,1 (anlam değişti).
- untangle 57 → 55; refine 2 tohum × 200k (--no-worse, NO_WORSE_W=5, taban = şu anki kart) + untangle + align: seed 51 kesişme 51, S 8170,0; seed 52 kesişme 52, S 8163,1. Seed 51 seçildi (kopuk parça sayısı 7'de kaldı; seed 52'de R28 eklendi, 8 oldu).
- place.py pen: 0,000. Uzayan kritik kenar []. Döngüler: Kelvin 20,7 → 20,1 mm, diğerleri ±%0.
- pcb_check: footprint 144, taşınan 100, kilitli taşınan [], pad-net/yüz/footprint farkı []; DRC 59 → 56, bağlantısız 361, parite 0. SONUC: GECTI.
- Kalan en çok kesişen netler: TFT_MOSI 8, TFT_SCLK 7, ENCODER_A/B/SW 6, TFT_DC 6 → pin ataması görevi.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Metrik değişikliği tek başına kesişmeyi 75 -> 57 yaptı; optimizasyonla 57 -> 51, S 8237 -> 8170. Kalan kesişmeler TFT/encoder netlerinde (pin ataması).
<!-- SECTION:FINAL_SUMMARY:END -->
