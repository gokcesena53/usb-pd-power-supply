---
id: TASK-053
title: Ethernet modulunu numune ile dogrula
status: Blocked
assignee: []
created_date: '2026-09-23 12:09'
updated_date: '2026-09-25 08:09'
labels:
  - sample-eval
milestone: m-0
dependencies:
  - TASK-052
  - TASK-060
references:
  - design_decisions/output/ETHERNET_ALTI_ALAN_ANALIZI_20260925.md
  - design_decisions/output/PORT_HIZASI_ENKODER_DUZELTME_20260925.md
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
  - hardware/datasheets/CH9121DS1.PDF
priority: high
ordinal: 103000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Uretici semasi (hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf) ve CH9121 veri sayfasi (hardware/datasheets/CH9121DS1.PDF) okundugu icin pin sirasi, besleme zinciri (5V -> AMS1117 -> 3V3 -> RT9193-18 -> 1V8), RJ45'in entegre trafolu oldugu ve CFG/RSTI/RESET/RXD1/RXD2 girislerinde cip ici 30-55 kOhm pull-up oldugu artik biliniyor. Geriye olculmesi gerekenler kaldi: gercek akim, header adimi, besleme anahtarinin davranisi ve modul kapaliyken geri besleme.

Eski en kritik risk (CFG0'da dahili pull-down -> R37 ile bolucu) veri sayfasiyla kapandi: pin 60'ta pull-up var, modul acikken hat yuksek.

Yerine gecen iki risk, ikisi de modul KAPALIYKEN: (1) Boot sirasinda Q8 kapali; R37 10k, GPIO8 hattini CFG pull-up'i ve ESD diyotu uzerinden beslemesiz ETH_3V3 rayina baglar. Ray L1 guc LED'iyle ~1,8 V'ta kalirsa GPIO8 ~2,0-2,4 V olur (ESP32-C6 VIH 2,475 V). ESP32-C6 GPIO8'i yalniz GPIO9=0 (download boot) iken okudugu icin normal acilis etkilenmez; yalniz BOOT tusuyla download'a giris bozulabilir. (2) ROM boot mesajlarini varsayilan olarak UART0'a basar; GPIO16 her acilista RXD1 pull-up'i/ESD uzerinden kapali modulu kisa sure besler.

Olculen akim analizdeki 0,20 A / 0,66 W varsayiminin yerini alacak. Veri sayfasi tahmini ~0,09 A (CH9121A 76 mA + LED'ler); Waveshare 140 mA diyor ve moduldeki cip eski harfsiz CH9121 (design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md bolum 3 ve Revizyon 2).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Modul yalniz 3V3 pinlerinden (13/14) beslenerek calistirilmis, 5V pinleri bosken link kurdugu dogrulanmis
- [ ] #2 3,3 V'ta cekilen akim link yokken, link varken ve TX sirasinda olculmus; en buyuk deger 0,20 A varsayimi ve veri sayfasi tahmini (~0,09 A) ile karsilastirilmis
- [ ] #3 Modul kapaliyken (Q8 kapali) ESP32 reset/boot sirasinda GPIO8 gerilimi ve ETH_3V3 rayinin yukseldigi deger olculmus; GPIO9=0 ile download boot'a girisin calistigi dogrulanmis, calismiyorsa R37 degeri icin karar yazilmis
- [ ] #4 Modul kapaliyken (ETH_3V3 = 0 V) GPIO16 ve GPIO8 low iken ETH_3V3 rayinda kalan gerilim ve kacak akim olculmus; ROM boot mesajlari sirasinda (GPIO16 high) ETH_3V3'e geri beslenen gerilim/akim da kaydedilmis
- [ ] #5 Q8 acilis/kapanis sureleri ve giris akimi osiloskopla olculmus; 3,3 V rayinda 100 mV'tan buyuk cokme yok
- [ ] #6 Guc kesilip verildikten sonra modulun EEPROM'daki ayarlarla geri geldigi ve link + TCP oturumunun kurulma suresi olculmus; ETH_3V3 yukselmesinden ilk komut kabulune kadar gecen sure (hesap 40-70 ms) olculmus
- [ ] #7 Module_Custom:Waveshare_2-CH_UART_TO_ETH footprint'i numuneyle dogrulanmis: 1:1 cikti uzerine modul oturtulmus; mekanik pin (MP) konumu (tahmin kenardan x 4.00, y 1.35) ve RJ45 lehim cikintisinin modul altindan yuksekligi (tahmin ~2.2 mm, ara parca 2.5 mm) olculmus; pin 1 = DIR1 surekliligi CH9121 pin 51 ile dogrulanmis
- [ ] #8 Ucdan uca SCPI sorgu-yanit gecikmesi ve jitter'i 921600 baud'da olculmus
- [ ] #9 Tum olcum sonuclari Implementation Notes'a yazilmis ve analiz belgesindeki varsayimlardan sapma varsa belge guncellenmis
- [ ] #10 TASK-093 Ethernet altı yerleşimi için modül-anakart gerçek minimum ara mesafesi, yerel alt komponent/lehimin maksimum çıkıntısı, RJ45/header/mekanik pim boyları ve PCB eğrilik farkı en az iki numunede XY bölgeleriyle ölçülmüş; ölçüm belirsizliği ve montaj toleransı dahil kalan hacim haritası TASK-093/088 e devredilmiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-09-23: TASK-052 kapandi — tedarikci SAMM Market (MP02965, 634,89 TL + KDV). Bu gorev en az 2 adet numune SAMM'den teslim alinana kadar Blocked kalir.

25.09 port-stack-fix: USB ve RJ45 artik Y=88.500 mm ortak merkezde ust uste. J8=(102.5,79.61), J7=(53.975,88.5). Nominal STEP mesafesi 3.23 mm fakat RJ45 gercek lehim/pin cikintilari modelde yok: USB THT lehimleri ile aralik numunede olculmeli, ikisi ayni anda takili kablo govde acikligi >=2 mm ve mandal erisimi dogrulanmali. J8 ust header uclari LCD altinda <=1.50 mm kalmali. J7/J8 courtyard istisnasi yalniz nominal modele dayanir.
<!-- SECTION:NOTES:END -->
