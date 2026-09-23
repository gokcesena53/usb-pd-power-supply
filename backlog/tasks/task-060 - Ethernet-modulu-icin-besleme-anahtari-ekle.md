---
id: TASK-060
title: Ethernet modulu icin besleme anahtari ekle
status: Done
assignee: []
created_date: '2026-09-23 13:06'
updated_date: '2026-09-23 13:07'
labels:
  - schematic
milestone: m-0
dependencies:
  - TASK-051
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
  - hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf
  - 'https://files.waveshare.com/upload/e/ef/CH9121_SPCC.pdf'
modified_files:
  - hardware/mcu.kicad_sch
  - hardware/libraries/Power_Supply_Custom.kicad_sym
  - hardware/datasheets/TSM3443CX6.pdf
  - hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf
  - software/FIRMWARE_GEREKSINIMLERI.md
  - docs/arayuz-sinyalleri.md
  - CHANGES.TXT
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: high
ordinal: 110000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Firmware gereksinimi Fixed PDO gecislerinde Accept-PS_RDY arasi tuketimi 2,5 W ile siniriyor. 3,3 V rayi zaten 0,70 A (2,31 W cikis) cekiyor ve bu sinir ancak Wi-Fi TX ertelenip arka isik kisilarak tutturuluyordu; Ethernet modulunun surekli ~0,66 W'i bunu tasiriyordu ve firmware bu yuku kisamiyordu.

Uretici semasi (hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf) ve CH9121 komut seti okunduktan sonra cozum netlesti: CH9121 ayarlarini 0x0d komutuyla EEPROM'a kaydediyor, yani gucu kesip vermek yeniden yapilandirma gerektirmiyor; ayrica 0x02/0x0e ile yazilimdan reset'lenebildigi icin RST1 hatti gereksiz ve GPIO0 serbest kaliyor. Boylece modulun 3,3 V beslemesi bir P-kanal yuksek-yan anahtariyla kesilebiliyor ve GPIO0 bu anahtari surebiliyor.

Analiz ve hesaplar: design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md (Revizyon bolumu).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Semada P-kanal yuksek-yan anahtari ETH_3V3'u besliyor; source +3.3V, drain ETH_3V3, gate GPIO0'dan suruluyor
- [x] #2 Anahtar ariza-emniyetli: GPIO0 reset/boot boyunca yuksek empedans iken modul KAPALI (gate pull-up)
- [x] #3 Acikken Vgs ve RDS(on) 0,2 A icin yeterli; gerilim dusumu 50 mV altinda
- [x] #4 Yumusak kalkis elemani var ve giris akimi 100 mA altinda; acilma/kapanma sureleri hesaplanip firmware dokumanina yazilmis
- [x] #5 J8 pinout'u ureticinin semasindaki P1 Header 8X2 duzenine gore; kullanilmayan pinlerde no_connect var
- [x] #6 RST1 baglantisi kaldirilmis ve gerekcesi (0x02/0x0e yazilim reset) belgelenmis
- [x] #7 ERC 0 hata / 0 uyari; netlist farki yalnizca Ethernet blogunun netleri
- [x] #8 software/FIRMWARE_GEREKSINIMLERI.md, docs/arayuz-sinyalleri.md ve CHANGES.TXT guncellenmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Q8 = TSM3443CX6 (Taiwan Semiconductor, P-kanal, -20 V, -4,3 A, RDS(on) 100 mOhm max @ Vgs -2,5 V, SOT-26). Ozdisan 1211076, stok 2950, 9,71 TL (23.09.2026) - indekste bulunan tek uygun P-kanal SOT-23 FET. 0,2 A'de dusum 20 mV.

Devre:
  +3.3V -> Q8 S(4);  Q8 D(1,2,5,6) -> ETH_3V3 -> J8.13/14 + C10 22u + C20 100n
  Q8 G(3) <- R16 10k <- GPIO0;  R17 100k ve C21 100n gate-source arasi
Aktif-low: GPIO0 low = acik. Acikken gate 3,3 x 10/110 = 0,30 V -> Vgs -3,0 V.
Acilma tau ~0,9 ms (~35 uF yuke giris akimi ~60 mA), kapanma R17 x C21 = 10 ms,
pratikte ~30 ms -> firmware kapattiktan sonra PDO gecisine baslamadan >=50 ms bekler.
GPIO0 boot'ta yuksek empedans -> R17 Q8'i kapali tutar (modul acilista KAPALI).

Deger degisiklikleri: R16 22R -> 10k (gate seri), R17 10k (eski RST1 pull-up) -> 100k
(gate pull-up), C21 100n yeni. J8 Conn_01x07 -> Conn_02x08_Odd_Even, uretici semasindaki
P1 Header 8X2 pinout'u: 3 CFG0, 4 RUN, 5 RXD1, 7 TXD1, 11/12 GND, 13/14 3V3;
1,2,6,8,9,10,15,16 no_connect. 5V pinleri bos - 3V3 dogrudan beslendigi icin modulun
AMS1117 LDO'su atlanir.

Yeni sembol Power_Supply_Custom:TSM3443CX6 (Q_PMOS_GSD govdesinden turetildi;
G=3, S=4, D pedleri 1/2/5/6 ayni dugumde istiflenmis, 2/5/6 gizli passive).

Kanit - verify.py gopo.kicad_sch --against (v1 durumundan alinan taze referans):
  ERC: 0 ihlal (0 hata, 0 uyari);  netlist 111 -> 120 net
  /MCU/ETH_3V3   : C10.1, C20.1, J8.13, J8.14, Q8.1, Q8.2, Q8.5, Q8.6
  /MCU/ETH_PWR_EN: C21.2, Q8.3, R16.1, R17.2, TP10.1
  +3.3V          : += C21.1, Q8.4, R17.1
  /MCU/ETH_CFG0  : J8.3, R15.2, TP9.1
  /MCU/UART_TX   : J8.5, TP11.1, U2.31   (J8.5 = modulun RXD1'i)
  /MCU/UART_RX   : J8.7, TP12.1, U2.30   (J8.7 = modulun TXD1'i)
  /MCU/ETH_RUN   : J8.4, TP14.1
  KAYIP /MCU/ETH_RST1 (RST1 artik baglanmiyor)
  8 adet unconnected-(J8-Pin_N): bilincli no_connect
readability.py mcu.kicad_sch: 5 bulgu (R4, SW2, TP9) - degisiklik oncesiyle birebir ayni.

Semadan cikan diger bulgular (analiz belgesinin Revizyon bolumune islendi):
- CFG0 CH9121 pin 60'a dogrudan, modulde pull yok -> hattı belirleyen tek direnc R37 10k.
- RST1'de modulde C25 1 uF POR kapasitesi var; pull-up cip ici.
- RJ45 entegre trafolu (CTTD/CTRD), ama kabuk pedleri 13/14 dogrudan GND'de -> STP kablo
  gopo toprapini bina toprapina baglar, UTP kullanilmali.

Not: bu oturum sirasinda usb_pd_controller.kicad_sch baska bir calisma tarafindan
degistirildi (FB clamp / TLV431, 15:51). Referans netlist yenilenerek fark ayristirildi;
o sayfaya dokunulmadi.
<!-- SECTION:NOTES:END -->
