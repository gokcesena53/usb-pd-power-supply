---
id: TASK-053
title: Ethernet modulunu numune ile dogrula
status: Blocked
assignee: []
created_date: '2026-09-23 12:09'
updated_date: '2026-09-23 13:08'
labels:
  - sample-eval
milestone: m-0
dependencies:
  - TASK-052
  - TASK-060
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: high
ordinal: 103000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Uretici semasi (hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf) okundugu icin pin sirasi, besleme zinciri (5V -> AMS1117 -> 3V3 -> RT9193-18 -> 1V8), CFG0'in CH9121 pin 60'a dogrudan gittigi ve RJ45'in entegre trafolu oldugu artik biliniyor. Geriye semadan okunamayan seyler kaldi: cipin dahili pull yonleri, gercek akim, header adimi ve besleme anahtarinin davranisi.

En kritik ikisi: (1) CFG0 GPIO8'e (strapping) bagli ve modulde hicbir pull yok, yani hatti yalnizca R37 10k belirliyor; CH9121'in pin 60'inda dahili pull-down varsa bolucu boot gerilimini VIH altina dusurup ESP32'yi acilmaz hale getirir. (2) Modul kapaliyken GPIO16/GPIO8 yuksek surulurse akim ESD klemplerinden modulun 3V3 rayina akar; bu dogrulanmazsa Q8 ile guc kesme ise yaramaz.

Olculen akim analizdeki 0,20 A / 0,66 W varsayiminin yerini alacak (design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md bolum 3).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Modul yalniz 3V3 pinlerinden (13/14) beslenerek calistirilmis, 5V pinleri bosken link kurdugu dogrulanmis
- [ ] #2 3,3 V'ta cekilen akim link yokken, link varken ve TX sirasinda olculmus; en buyuk deger 0,20 A varsayimiyla karsilastirilmis
- [ ] #3 CFG0 (pin 3) ve RST1 (pin 9) hatlarinin dahili pull yonu olculmus; CFG0 R37 10k ile surulurken gerilim ESP32 VIH'inin (>=0,75 x 3,3 V) uzerinde
- [ ] #4 Modul kapaliyken (ETH_3V3 = 0 V) GPIO16 ve GPIO8 low iken ETH_3V3 rayinda kalan gerilim ve kacak akim olculmus; kesme gercekten calisiyor
- [ ] #5 Q8 acilis/kapanis sureleri ve giris akimi osiloskopla olculmus; 3,3 V rayinda 100 mV'tan buyuk cokme yok
- [ ] #6 Guc kesilip verildikten sonra modulun EEPROM'daki ayarlarla geri geldigi ve link + TCP oturumunun kurulma suresi olculmus
- [ ] #7 2x8 header adimi ve mekanik olculeri (pin 1 konumu, kart kenarina uzaklik, RJ45 govde yuksekligi) olculup footprint icin kaydedilmis
- [ ] #8 Ucdan uca SCPI sorgu-yanit gecikmesi ve jitter'i 921600 baud'da olculmus
- [ ] #9 Tum olcum sonuclari Implementation Notes'a yazilmis ve analiz belgesindeki varsayimlardan sapma varsa belge guncellenmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
