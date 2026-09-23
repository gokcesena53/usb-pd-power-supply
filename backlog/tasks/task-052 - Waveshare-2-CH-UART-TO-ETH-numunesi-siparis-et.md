---
id: TASK-052
title: 'Waveshare 2-CH UART TO ETH semasini incele, tedarikciyi belirle'
status: Done
assignee: []
created_date: '2026-09-23 12:09'
updated_date: '2026-09-23 18:43'
labels:
  - procurement
milestone: m-0
dependencies: []
references:
  - 'https://www.waveshare.com/2-CH-UART-TO-ETH.htm'
  - >-
    https://market.samm.com/2-ch-uarttan-ethernete-donusturucu-seri-port-seffaf-iletim-modulu
  - hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: high
ordinal: 107000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modulun veri sayfasi birkac kritik bilgiyi vermiyordu: 3,3 V'tan calisip calismadigi (uzerinde 5 V isteyen bir LDO olabilir), RJ45'in entegre trafolu olup olmadigi (izolasyon buna bagli) ve CFG0/RST1/RUN pinlerinin baglantilari. Bunlar uretici semasindan (hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf) okunur; semadan okunamayanlar (akim, cip ici pull, header adimi) TASK-053'e kalir.

Ozdisan indeksinde hicbir Ethernet parcasi yok, tedarik ikinci kaynaktan olacak: SAMM Market (MP02965).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Uretici semasi (hardware/datasheets/2-CH_UART_TO_ETH_SCH.pdf) incelenmis; 3,3 V besleme yolu, RJ45 trafosu ve CFG0/RST1/RUN baglantilari belirlenmis
- [x] #2 Tedarikci, urun kodu ve birim fiyat Implementation Notes'a ve analiz belgesine yazilmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Sema incelemesi (2-CH_UART_TO_ETH_SCH.pdf, tek sayfa Altium ciktisi; netlist PyMuPDF ile metinden cikarildi):

- **3,3 V calisma:** 5V (P1.15/16) -> AMS1117 -> 3V3 -> RT9193-18 -> 1V8 (CH9121 VCC18). P1.13/14 dogrudan 3V3 rayi (CH9121 VCC33 + RJ45 orta uclari). 3V3'ten beslenince AMS1117 atlanir, 5V pinleri bos kalir. Veri sayfasindaki "5 V isteyen LDO olabilir" suphesi kapandi.
- **RJ45 (J1 net_port):** CTTD/CTRD (4/5) 3V3'e, TD+/-, RD+/- 49,9R ile sonlanmis -> entegre trafolu. Kabuk (13/14) **dogrudan GND** -> UTP kablo onerisi gecerli.
- **Header P1 (8x2):** 1 DIR1 / 2 DIR2 / 3 CFG0 / 4 RUN / 5 RXD1 / 6 RXD2 / 7 TXD1 / 8 TXD2 / 9 RST1 / 10 RESET / 11-12 GND / 13-14 3V3 / 15-16 5V. Analiz belgesi ve J8 semasindaki pinout ile birebir ayni.
- **Lojik hatlar:** CFG0 (U3.60), RUN (U3.31), RESET (U3.59) modulde hicbir elemana bagli degil; RST1 (U3.36) yalniz C25 1 uF ile GND'ye. Harici pull yok -> cip ici pull yonu TASK-053 KK#3'te olculecek.
- Semadan okunamayanlar (akim, cip ici pull, header adimi) TASK-053'te kaliyor.

Tedarik: **SAMM Market**, https://market.samm.com/2-ch-uarttan-ethernete-donusturucu-seri-port-seffaf-iletim-modulu
- Waveshare, SAMM urun kodu MP02965
- 634,89 TL + KDV (761,87 TL KDV dahil), 23.09.2026 itibariyla stok 19 adet
- Siparis kaydi bu gorevde tutulmuyor; numune teslimi TASK-053'un on kosulu.

Guncellenen belge: design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md (§4 izolasyon, §5 tedarik karari, §7 kapanan maddeler). CHANGES.TXT degismedi (donanim tasariminda degisiklik yok, yalniz tedarik karari).
<!-- SECTION:NOTES:END -->
