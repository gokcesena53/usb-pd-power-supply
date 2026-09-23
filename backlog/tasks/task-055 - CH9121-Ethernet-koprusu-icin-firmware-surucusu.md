---
id: TASK-055
title: CH9121 Ethernet koprusu icin firmware surucusu
status: To Do
assignee: []
created_date: '2026-09-23 12:10'
updated_date: '2026-09-23 18:58'
labels:
  - firmware
milestone: m-3
dependencies:
  - TASK-053
  - TASK-060
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
  - software/FIRMWARE_GEREKSINIMLERI.md
  - 'https://www.waveshare.com/wiki/2-CH_UART_TO_ETH'
  - hardware/datasheets/CH9121DS1.PDF
priority: medium
ordinal: 105000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ethernet, ESP32'ye IP arayuzu vermiyor; CH9121 seffaf bir UART-TCP tuneli. Firmware'in modulu bir ag arayuzu gibi degil, yapilandirilabilir bir seri koprusu ve kesilebilir bir guc tuketicisi gibi surmesi gerekiyor: en fazla 2 eszamanli soket, her biri onceden sabitlenmis (IP, port, rol) cifti.

Pin haritasi: TXD1/RXD1 GPIO16/17 (UART0, artik log tasimiyor), CFG0 GPIO8, ETH_PWR_EN GPIO0 (aktif-low, Q8 besleme anahtari). RST1 ve RUN bagli degil; RSTI/RESET/CFG girislerinde cip ici 30-55 kOhm pull-up oldugu icin bos pinler kendiliginden inaktif (hardware/datasheets/CH9121DS1.PDF).

Uretici belgelerinden kesinlesenler (design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md, Revizyon ve Revizyon 2): yapilandirma CFG0 low ile ve sabit 9600 bps'te yapilir; 0x0d parametreleri EEPROM'a yazar, 0x0e uygular ve cipi reset'ler, 0x02 cipi reset'ler. 0x0d gonderilirse ayarlar guc kesilse de kalicidir, yani guc anahtari ayar kaybina yol acmaz. EEPROM omurludur, her acilista yazilmamali.

Zamanlama: modulde RSTI cip ici pull-up ile C25 1 uF uzerinden yukselir (28-51 ms) + 11-19 ms hazirlik; ETH_3V3 geldikten sonra ilk komut icin >=100 ms beklenmeli. Yazilim reset'inden sonra >=20 ms (tRSTTEMP2 maks 18 ms).

GPIO8 strapping pinidir (yalniz GPIO9=0 download boot'ta okunur): boot tamamlanmadan surulmemeli, varsayilani high (normal mod). Modulu kapatmadan once GPIO16 ve GPIO8 low yapilmali, yoksa modul RXD1/CFG pull-up'lari ve ESD klempleri uzerinden beslenir ve kesme ise yaramaz.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Surucu modulun parametrelerini (IP, maske, gateway, hedef IP/port, baud, calisma modu) CFG0 low + 9600 bps dizisiyle yazip 0x0d ile kaydedip 0x0e ile uygulayabiliyor; sonra UART0 calisma hizina donuyor
- [ ] #2 0x0d yalnizca ayar gercekten degistiginde gonderiliyor (EEPROM omru)
- [ ] #3 Guc kesilip verildikten sonra surucu yeniden yapilandirma yapmadan calismaya devam ediyor
- [ ] #4 Acma sirasi: GPIO8 high -> GPIO0 low -> >=100 ms bekle -> (gerekirse yapilandirma) -> link bekle. 0x02/0x0e sonrasi >=20 ms bekleniyor. Kapatma sirasi: UART0 TX ve GPIO8 low -> GPIO0 high -> >=50 ms bekle
- [ ] #5 CFG0 boot sirasinda surulmuyor; GPIO8 yalniz uygulama basladiktan sonra cikis yapiliyor ve varsayilani high
- [ ] #6 Baglanti durumu (link ve TCP oturumu) keepalive/zaman asimi ile takip ediliyor ve TFT'de gosteriliyor; RUN pini yok
- [ ] #7 SCPI sorgu-yanit dongusu en az bir gercek lab cihaziyla ucdan uca calisiyor ve olculen gecikme Implementation Notes'a yazilmis
- [ ] #8 software/FIRMWARE_GEREKSINIMLERI.md pin haritasi ve Ethernet bolumu guncellenmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
