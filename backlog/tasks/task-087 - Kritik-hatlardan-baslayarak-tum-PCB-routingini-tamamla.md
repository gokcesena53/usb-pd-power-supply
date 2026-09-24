---
id: TASK-087
title: Kritik hatlardan baslayarak tum PCB routingini tamamla
status: To Do
assignee: []
created_date: '2026-09-24 13:06'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-008
  - TASK-010
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 169000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-008 kritik güzergâh denemelerini gerçek bakır tasarımına tamamla. Önce kritik devreleri route edip kontrol et, ardından kalan bağlantıları ve dolguları bitir. Yerleşim değişikliği gerektiren geçişlerde ilgili kabulleri tekrar doğrula; Gerber üretimi bu görevin kapsamı değildir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Önce Cin/anahtarlama/GND güç döngüleri, D5–U11 FB, V_X/FB/COMP, Kelvin sense, USB/CC ve U2 beslemesi tamamlanmış; kritik güzergâh incelemesinden sonra kalan sinyaller route edilmiş.
- [ ] #2 Güç iz/polygon/via boyutları TASK-008 akım/gerilim düşümü bütçesi ve TASK-010 üretici stackup'ına uyuyor; her sinyal katmanı ve geçişi için referans/dönüş yolu gösterilmiş. SW/LX alanları ve anten keepout'u korunmuş.
- [ ] #3 USB çiftinin hedef empedansı ve stackup'a dayanan genişlik/aralığı kaynaklı; katman geçişleri, kesintisiz referans ve dönüş via'ları incelenmiş. Kelvin hatları yük akımı taşımıyor.
- [ ] #4 Zone'lar yeniden doldurulmuş; bağlantısız öğe 0, schematic parity 0, açıklanmamış DRC hatası 0. Kısa devre, eksik bağlantı ve üretilemeyen delikler istisnayla gizlenmemiş.
- [ ] #5 Tüm routing sonrası top/bottom/iç katmanlar, 3D ve termal alanlar incelenmiş; zorunlu yerleşim değişikliği olursa TASK-063/008 mekanik/elektriksel kabulleri yeniden doğrulanmış.
- [ ] #6 Son kart revizyonu/hash, DRC/parity raporları ve kritik net/ölçü tablosu üretim öncesi incelemeye devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
