---
id: TASK-090
title: Eszamanli yukte MCU beslemesini ve kart sicakliklarini dogrula
status: Blocked
assignee: []
created_date: '2026-09-24 13:06'
updated_date: '2026-09-24 13:08'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
  - TASK-019
  - TASK-020
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 172000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Buck'ın MCU'dan uzak yerleştirilmesinin besleme bütünlüğüne etkisini ve son kutudaki termal marjı doğrula. Mevcut regülatör/PD testlerini tekrar etmek yerine tüm tüketicilerin eşzamanlı yükünü ve uzak besleme yolunu değerlendir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 TASK-008 bütçesiyle buck çıkışı–U2 pad DC düşüm sınırı, U2 izin verilen min/max gerilim, ripple/geçici çökme sınırı, akım/yük matrisi, ortam sıcaklığı ve bileşen sıcaklık sınırları ölçümden önce sayısal kayıtlı; üretici limitleri ile proje marjları ayrılmış.
- [ ] #2 Wi-Fi TX, Ethernet trafik/açılış ve ekran/backlight eşzamanlı yüklerinde buck çıkışı ile U2 besleme pedinde uygun kısa GND prob bağlantısıyla ölçüm alınmış; DC düşüm ve transient sınırları sağlanmış, brownout/reset yok.
- [ ] #3 Kapalı son kutuda ilgili giriş gerilimleri ve çıkış yüklerinde termal dengeye ulaşılmış; buck/boost, bobinler, MOSFET, şönt ve güç dirençleri ölçülmüş. Ortam/yük/denge ölçütü kayıtlı; datasheet ve proje sıcaklık sınırları aşılmamış.
- [ ] #4 TASK-019/020 yük basamağı ve PD geçiş sonuçlarıyla ilişki kurulmuş; dalga şekilleri, ölçüm noktaları, firmware/kart revizyonu ve geçme/kalma tablosu kayıtlı. Başarısızlıklar düzeltme/tekrar test olmadan kapatılmamış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
TASK-015 prototip PCB/dizgisi ve görev bağımlılıklarındaki test girdileri bekleniyor; ölçüm yapılmadı.
<!-- SECTION:NOTES:END -->
