---
id: TASK-052
title: Waveshare 2-CH UART TO ETH numunesi siparis et
status: To Do
assignee: []
created_date: '2026-09-23 12:09'
labels:
  - procurement
milestone: m-0
dependencies: []
references:
  - 'https://www.waveshare.com/2-CH-UART-TO-ETH.htm'
priority: high
ordinal: 102000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modulun veri sayfasi birkac kritik bilgiyi vermiyor: 3,3 V'tan gercekten calisip calismadigi (uzerinde 5 V isteyen bir LDO olabilir), 3,3 V'ta cektigi akim, RJ45'in entegre trafolu olup olmadigi (izolasyon buna bagli) ve CFG0/RST1/RUN pinlerinin lojik seviyeleri. Bu bilgiler olmadan ne guc butcesi ne de yerlesim kesinlestirilebilir. Ozdisan indeksinde hicbir Ethernet parcasi yok, tedarik ikinci kaynaktan olacak.

Birim fiyat 12,99 USD, 3 adet ve uzerinde 11,79 USD.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 En az 2 adet modul siparis edilmis ve teslim alinmis
- [ ] #2 Siparis kaydi (tedarikci, tarih, birim fiyat) Implementation Notes'a yazilmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
