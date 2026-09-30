---
id: TASK-120
title: Freerouting ile yerleşim adaylarını deneme routing'inde karşılaştır
status: Done
assignee: []
created_date: '2026-09-29 13:21'
updated_date: '2026-09-29 13:21'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/docs/reports/freerouting-20260929/
  - .claude/skills/kicad-placement/scripts/pcb_freeroute.py
documentation:
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
modified_files:
  - .claude/skills/kicad-placement/scripts/pcb_freeroute.py
priority: medium
ordinal: 206000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Yerleşim adaylarının routability'sini Freerouting 2.4.1 deneme routing'i ile ölç (A: FPC sonrası, B: routability seed 41, C: kartta). Koşul: In1.Cu=GND, In2.Cu=+3.3V düzlem (varsayım), sinyal F/B.Cu, 12 geçiş, GUI modu (Xvfb). Sonuç routing önerisi değil.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Üç aday aynı koşulda (düzlem, geçiş, mod) route edilmiş; açık bağlantı, via, iz uzunluğu KiCad DRC ile ölçülmüş
- [x] #2 Açık bağlantılar net bazında sınıflandırılmış (düzlem / sinyal)
- [x] #3 Rapor hardware/docs/reports/freerouting-20260929/ altında; hardware/gopo.kicad_pcb değişmemiş
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Ölçüm (29.09.2026, Freerouting 2.4.1, Java 25, GUI modu Xvfb :99, -mp 12 -mt 1; KiCad SES içe aktarma + kicad-cli DRC):
| | A FPC sonrası | B seed41 | C kartta |
| açık bağlantı | 43 | 47 | 47 |
| - düzlem (GND/+3.3V) | 30 | 31 | 26 |
| - sinyal | 13 | 16 | 21 |
| via | 79 | 89 | 63 |
| iz toplam (mm) | 2116,5 | 2108,2 | 2010,7 |
| DRC clearance / track_width | 4 / 0 | 0 / 3 | 0 / 6 |
| süre (s) | 861 | 834 | 786 |
- Freerouting log: C'de auto-routing 39 unrouted ile bitti, optimizer 47 ile başladı (B'nin son skoru 846,07 ile aynı): optimizer aşaması güvenilir değil.
- Headless ve GUI modu karşılaştırılamaz: GUI fanout aşaması çalıştırıyor (C: 390/469 pin kaçış).
- Duman testi (headless, 2 geçiş, C): 64 açık, 50 via.
- track_width ihlalleri MAIN_5A (3 mm) netleri.
- hardware/gopo.kicad_pcb değişmedi; CHANGES.TXT/karar değişmedi (ölçüm görevi).
- Rapor: hardware/docs/reports/freerouting-20260929/ (routed top/bot, Freerouting ekranı, result.json, log).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Tek koşuda C en az via (63 vs A 79, B 89) ve en kısa iz (2011 mm), açık bağlantı A 43 / B 47 / C 47. Açıkların ~%60'ı düzlem netleri (GND, +3.3V) -> deneme kurulumu sorunu; sinyal açıkları A 13, B 16, C 21. Tek koşu, fark gürültü içinde; karar için tekrar gerekli (TASK takip).
<!-- SECTION:FINAL_SUMMARY:END -->
