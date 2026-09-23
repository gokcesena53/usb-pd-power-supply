---
id: TASK-051
title: Ethernet mezanin blogunu semaya ekle
status: Done
assignee: []
created_date: '2026-09-23 12:09'
updated_date: '2026-09-23 12:29'
labels:
  - schematic
milestone: m-0
dependencies: []
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
  - software/FIRMWARE_GEREKSINIMLERI.md
  - 'https://www.waveshare.com/wiki/2-CH_UART_TO_ETH'
modified_files:
  - hardware/mcu.kicad_sch
  - software/FIRMWARE_GEREKSINIMLERI.md
  - docs/arayuz-sinyalleri.md
  - CHANGES.TXT
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: high
ordinal: 107000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
gopo'ya deterministik, kablolu laboratuvar agi baglantisi isteniyor: lab cihazlariyla ETH uzerinden konusmak ve secilen parametreleri TFT'ye basmak. Secilen cozum, Waveshare 2-CH UART TO ETH (CH9121) modulunu ana karta mezanin olarak baglamak; modul kartin ustune yerlesemeyecek kadar buyuk (53 x 22 mm, kart 65,9 x 40,6 mm), bu yuzden header ile baglanip RJ45 arka panelden cikacak.

Pin atamasi kullanici tarafindan karara baglandi ve I2C genisletici kullanilmayacak: UART0 (GPIO16/17) bugun yalniz TP11/TP12 test noktalarina gidiyor ve loglar USB-Serial/JTAG'den aktigi icin serbest; IO0 ve IO8 de yalniz 22 ohm seri direnc uzerinden TP10/TP9'a gidiyor. IO8 bir strapping pini oldugu icin oraya modulun bir cikisi baglanamaz, yalnizca girisi baglanabilir; mevcut R37 10k pull-up boot'ta high tuttugu ve CH9121'de CFG0 high = normal mod oldugu icin IO8 CFG0'a gidiyor. IO0 ise RST1'e gidiyor ve low-active oldugu icin yeni bir pull-up gerektiriyor. Modulun RUN cikisi hicbir GPIO'ya baglanmiyor.

Analiz ve gerekce: design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Semada Ethernet mezanin konnektoru J8 yer aliyor; 3V3, GND, TXD1, RXD1, CFG0, RST1, RUN pinleri bagli, pin NUMARALARI gecici olarak isaretli
- [x] #2 Modulun TXD1'i GPIO17 (U2 pin 30, UART_RX), RXD1'i GPIO16 (U2 pin 31, UART_TX) ile baglantili; TP11/TP12 ayni netlerde tap olarak duruyor
- [x] #3 ETH_CFG0 net'i GPIO8'e (U2 pin 22) R15 22 ohm uzerinden bagli ve mevcut R37 10k pull-up bu net uzerinde kaliyor; TP9 ayni nette
- [x] #4 ETH_RST1 net'i GPIO0'a (U2 pin 12) R16 22 ohm uzerinden bagli ve net uzerinde 3V3'e yeni bir 10k pull-up (R17) var; TP10 ayni nette
- [x] #5 Modulun RUN cikisi TP14 pedine gidiyor, hicbir GPIO'ya baglanmiyor
- [x] #6 3V3 besleme pinine modul yaninda ayirma kondansatoru konmus (C10 22u + C20 100n, mevcut MPN'ler; yeni BOM satiri yok)
- [x] #7 ERC 0 hata / 0 uyari ve verify.py netlist karsilastirmasinda mevcut netlerin uyeleri degismemis; cikti Implementation Notes'a yazilmis
- [x] #8 software/FIRMWARE_GEREKSINIMLERI.md, docs/arayuz-sinyalleri.md ve CHANGES.TXT guncellenmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
mcu.kicad_sch sayfasina "ETHERNET MEZANIN (CH9121)" blogu eklendi (cerceve 27,94/163,83 - 114,30/222,25).

Kanit - verify.py gopo.kicad_sch --against (oturum basi referansi):
  ERC: 0 ihlal (0 hata, 0 uyari)     [referansla ayni]
  netlist: 110 -> 111 net
  baglanti farki, yalniz beklenenler:
    +3.3V      += C10.1, C20.1, J8.1, R17.1
    GND        += C10.2, C20.2, J8.7
    UART_RX    += J8.2   (TP12.1, U2.30 yerinde)
    UART_TX    += J8.3   (TP11.1, U2.31 yerinde)
    Net-(R15-Pad2) -> /MCU/ETH_CFG0 : R15.2, TP9.1, J8.4
    Net-(R16-Pad1) -> /MCU/ETH_RST1 : R16.1, TP10.1, J8.5, R17.2
    YENI /MCU/ETH_RUN : J8.6, TP14.1
  lib_symbols onbellek uyarisi yok.
readability.py mcu.kicad_sch: 5 bulgu (R4, SW2, TP9) - degisiklik oncesiyle ayni,
yeni bulgu yok. E.lint blok kutusunda ve stub bolgesinde bos.

Yeni parcalar: J8 Conn_01x07 (Value TBD, footprint bos - pin sirasi/adim numuneden,
TASK-053), R17 10k 0402 (R37 ile ayni MPN), C10 22u 0805 (C5 ile ayni MPN),
C20 100n 0402 (C6 ile ayni MPN), TP14. Yeni BOM satiri yalniz J8.

Etiketleme karari: UART0 netleri UART_TX/UART_RX adinda birakildi (sinyal gercekten
UART0; TP11/TP12 de ayni adla etiketli). Yalniz adsiz iki net yeni ad aldi.

Notlar dosyalara islendi: software/FIRMWARE_GEREKSINIMLERI.md (bolum 1 pin haritasi,
bolum 3 pSnkStdby uyarisi, yeni bolum 5 Ethernet), docs/arayuz-sinyalleri.md,
CHANGES.TXT (REV_C).
<!-- SECTION:NOTES:END -->
