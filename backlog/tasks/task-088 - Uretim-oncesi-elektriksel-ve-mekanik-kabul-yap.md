---
id: TASK-088
title: Uretim oncesi elektriksel ve mekanik kabul yap
status: To Do
assignee: []
created_date: '2026-09-24 13:06'
updated_date: '2026-09-24 13:06'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-087
  - TASK-054
  - TASK-053
  - TASK-009
  - TASK-011
  - TASK-012
  - TASK-013
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 170000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Gerber üretimine zorunlu giriş kontrolü. Elektriksel routing kabulünü, fiziksel numune/kutu doğrulamasını ve üretilebilirliği aynı son kart sürümünde birleştir. Bu görev prototip RF/termal performansının ölçüldüğünü iddia etmez; bu testlerin sayısal planını ve ölçüm erişimini hazırlar.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 İncelenen şema/PCB/kurallar/footprint ve üretici stackup revizyonları sabit bir hash/commit manifestinde kayıtlı; routing tamam, zone dolu, bağlantısız öğe 0 ve schematic parity 0.
- [ ] #2 Açıklanmamış DRC hatası 0; izin verilen her istisna ref/öğe/konum, gerekçe ve kanıtla listelenmiş. 3D kanıtlı mezanin courtyard istisnaları elektriksel clearance/short/bağlantısızlık kontrollerini kapatmıyor.
- [ ] #3 TASK-053 J8 numune mekanik ölçüleri, TASK-054 son kutu/fiş/anten/LCD/J9 boşlukları ve LCD/süperkap numune kontrolleri tamam; tahmini pin/çıkıntı ölçüsüyle üretime onay verilmemiş.
- [ ] #4 J7 top; J8 bottom ve USB-C altında; J9 Ethernet yanı ve slot kararı; U2 top/anten dışarı/RF koşullu USB-C yakınlığı; buck/boost–U2 ayrımı ve kritik güzergâhlar tek ister–kanıt tablosunda geçiyor.
- [ ] #5 Üretici DFM, çift yüz dizgi/THT sırası, ağır eleman tutunması, J8/LCD pin kesimi, lehim/temizlik/test erişimi ve mekanik destek son yerleşim için kontrol edilmiş.
- [ ] #6 RF ve besleme/termal prototip görevlerine test noktaları, düzenek, yük/ortam matrisi ve testten önce belirlenmiş sayısal geçme/kalma sınırları devredilmiş; prototip testleri yapılmış gibi gösterilmemiş.
- [ ] #7 Üretim için açık engel kalmamış; inceleme raporu Gerber görevine bağlı. Sonradan kart/kurallar değişirse bu kabul geçersiz sayılıp ilgili kontroller tekrarlanıyor.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Prototip test sahipleri: TASK-089 (RF), TASK-090 (besleme/termal). Sayısal test planları bu üretim öncesi kabulde kontrol edilir; fiziksel sonuçlar TASK-015 sonrasındadır.
<!-- SECTION:NOTES:END -->
