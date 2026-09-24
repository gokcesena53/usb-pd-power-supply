---
id: TASK-089
title: Son kutuda eszamanli yuk altinda RF performansini dogrula
status: Blocked
assignee: []
created_date: '2026-09-24 13:06'
updated_date: '2026-09-24 13:08'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
  - TASK-054
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 171000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Antenin geometrik keepout kontrolünü son ürün RF testiyle tamamla. Sayısal hedefler test sonucuna bakılarak gevşetilmez; düzenek ve hedefler üretim öncesi incelemede hazırlanır. Gerekli trafik üreten test firmware'i hazır olmadan ölçüme başlanmaz.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Ölçümden önce kullanım senaryosuna göre mesafe/yönler, AP/kanal, trafik türü/süre, gerekli minimum throughput, maksimum paket kaybı ve izin verilen kopma sayısı sayısal olarak kaydedilmiş; üretim öncesi kabuldeki test planıyla eşleşiyor.
- [ ] #2 Son kutuda USB/Ethernet kabloları takılı; Ethernet trafiği, LCD/backlight ve buck/boost'un ilgili yük durumları matrise göre denenmiş. Referans olarak aynı test koşullarındaki açık-kutu ölçümü kaydedilmiş.
- [ ] #3 Her koşulda throughput/paket kaybı/kopma ve varsa RSSI ölçülmüş; bütün hedef kullanım koşulları önceden belirlenen sınırları sağlıyor. Sağlamayan durum düzeltme ve tekrar test olmadan Done yapılmamış.
- [ ] #4 Firmware sürümü, cihaz/kablo/yön/mesafe/kanal ve kart revizyonu sonuçlarla kayıtlı; gerektiğinde anten/yerleşim düzeltmesi ilgili donanım görevine devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
TASK-015 prototip PCB/dizgisi ve TASK-054 test planı bekleniyor; ölçüm yapılmadı.
<!-- SECTION:NOTES:END -->
