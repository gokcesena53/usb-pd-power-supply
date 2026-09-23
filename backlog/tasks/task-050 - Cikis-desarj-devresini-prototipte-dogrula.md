---
id: TASK-050
title: Çıkış deşarj devresini prototipte doğrula
status: To Do
assignee: []
created_date: '2026-09-23 11:23'
updated_date: '2026-09-23 11:23'
labels:
  - bring-up
milestone: m-2
dependencies:
  - TASK-015
  - TASK-049
references:
  - hardware/usb_pd_controller.kicad_sch
priority: high
ordinal: 109000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-049 R59 bleed direncinin yerine SW_EN kontrollü aktif deşarj koydu: SW_EN low iken (OUT_EN low, INA_ALERT veya kartta güç yok) deşarj FET'i OUT_POS'u 1 kΩ/2 W R_dis üzerinden boşaltır, gate SW_OUT'tan beslenir ve 12 V zenerle sınırlanır. Hesaplar ölçümle doğrulanmalı: deşarj süresi, çıkış açıkken deşarjın kapalı kalması, açma/kapama geçişinde çakışma olmaması ve GPIO olmadığı için kapatılamayan "dış kaynak bağlı" durumunda R_dis'in ısıl dayanımı.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Yüksüz çıkışta 28 V açık → OUT_EN low: OUT_POS 1 V'un altına 50 ms içinde iner (osiloskop)
- [ ] #2 Çıkış açıkken (28 V, SW_EN high) DISCH_G < 0,3 V ve deşarj FET'i drain akımı < 10 µA (R_dis üzerinde < 10 mV)
- [ ] #3 OUT_EN yükselip düşerken SW_OUT/OUT_POS'ta deşarj ile LM74801 arasında çakışma akımı R_dis üzerinden ≤ 30 mA ve ≤ 1 ms
- [ ] #4 INA_ALERT tetiklenince (SOL eşiği aşılınca) deşarj kendiliğinden açılır
- [ ] #5 USB çekildiğinde (kart güçsüz) 1000 µF yük 28 V'tan 5 V altına ≤ 2,5 s içinde iner
- [ ] #6 Çıkış kapalıyken OUT_POS'a 30,4 V dış kaynak 30 dk: R_dis sıcaklığı ≤ 105 °C (25 °C ortam), kart ve komşu parçalar hasarsız; kaynaktan çekilen akım 30–31 mA
- [ ] #7 INA226 akim okuması çıkış açık ve yüksüzken 28 V'ta |I| ≤ 0,5 mA (R59 100k katkısı 0,28 mA)
- [ ] #8 1000 µF harici yükle 28 V → 5 V altı: ≤ 2,0 s (hesap 1,72 s); 28 V → 2 V: ≤ 3,5 s (hesap 2,64 s). 2 V altı FET eşiği nedeniyle R59 ile yavaş iner; kalan gerilim ve süre not edilir
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
