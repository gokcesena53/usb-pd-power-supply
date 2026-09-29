---
id: TASK-121
title: Freerouting denemesinde düzlem bağlantısını düzelt ve tekrarlı karşılaştır
status: To Do
assignee: []
created_date: '2026-09-29 13:21'
updated_date: '2026-09-29 13:27'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-120
references:
  - hardware/docs/reports/freerouting-20260929/
  - .claude/skills/kicad-placement/scripts/pcb_freeroute.py
priority: medium
ordinal: 207000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-120'de açık bağlantıların ~%60'ı GND/+3.3V düzlem netleri; deneme kurulumu (zone/via) sorunlu. Ayrıca tek koşu farkı gürültü içinde ve Freerouting optimizer aşaması sonucu kötüleştiriyor. In2 net ataması da varsayım (+3.3V).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Düzlem netlerinde (In1 GND, In2 güç polygonları) açık bağlantı <= 2 veya nedeni belgelenmiş
- [ ] #2 In2 POWER_PLANE: tüm güç hatları (MAIN_5A, POWER_3V3 sınıfları ve V_PRE vb.) bölünmüş polygon olarak tanımlanmış; polygon sınırları blok bölgelerine göre çizilmiş
- [ ] #3 Her aday >= 3 tekrar, açık sinyal ve via için ortalama ve aralık raporlanmış
- [ ] #4 Açık kalan sinyal bağlantıları küme/bölge bazında çıkarılmış ve yerleşim kısıtına (REGION/CRIT) geri beslenmiş veya gerekçelendirilmiş
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
29.09.2026 kullanıcı kararı: POWER_PLANE (In2) tüm güç hatlarının polygon olacağı şekilde kullanılır (tek net değil, bölünmüş düzlem). Canlı yayın (0.0.0.0) şimdilik kullanılmıyor.
<!-- SECTION:NOTES:END -->
