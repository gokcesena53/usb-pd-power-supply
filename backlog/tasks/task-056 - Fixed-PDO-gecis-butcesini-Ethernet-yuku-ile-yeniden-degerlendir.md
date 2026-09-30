---
id: TASK-056
title: Fixed PDO gecis butcesini Ethernet yuku ile yeniden degerlendir
status: To Do
assignee: []
created_date: '2026-09-23 12:10'
updated_date: '2026-09-23 13:08'
labels:
  - firmware
  - bring-up
milestone: m-2
dependencies:
  - TASK-060
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
  - software/FIRMWARE_GEREKSINIMLERI.md
priority: high
ordinal: 109000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Firmware gereksinimi, Fixed PDO gecislerinde Accept-PS_RDY arasi tuketimi 2,5 W ile siniriyor. 3,3 V rayi tepe 0,70 A cekiyor (2,31 W cikis) ve bu sinir ancak Wi-Fi TX ertelenip arka isik kisilarak tutturulabiliyordu.

TASK-060 ile Ethernet modulunun beslemesi Q8 uzerinden kesilebilir hale geldi, yani modulun ~0,66 W'i artik atilabiliyor ve butcenin kagit uzerinde kapanmasi bekleniyor. Bu gorev bunun gercekten boyle oldugunu hedef adaptorlerle olcup firmware davranisini karara baglar.

Bedeli: modul kesilip geri acildiginda link ve TCP oturumu 2-4 s icinde kurulur. Bu yuzden gerilim degisimi PPS/APDO ile yapilabiliyorsa modul hic kesilmemeli; standby kurali yalnizca Fixed PDO gecislerini baglar. TASK-020 (PD voltaj gecislerinde 3,3 V rail ve UVP davranisi) ile birlikte yurutulmeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Ethernet modulu bagliyken ve Q8 ile kesilmisken Fixed PDO gecisinde VBUS'tan cekilen guc hedef adaptorlerle olculmus ve 2,5 W sinirina gore raporlanmis
- [ ] #2 Kesme sirasi dogrulanmis: UART_TX ve CFG0 low -> GPIO0 high -> >=50 ms bekle -> PDO istegi; kesme sirasinda 3,3 V rayinda kalan Ethernet yuku olculmus
- [ ] #3 Modul geri acildiginda link ve TCP oturumunun kurulma suresi olculmus
- [ ] #4 PPS/APDO gecisinin ayni kosulda modulu kesmeden calistigi olcumle gosterilmis
- [ ] #5 Firmware davranisi karara baglanmis: ETH aktifken gerilim degisiminin hangi kosulda PPS ile yapilacagi ve Fixed'e dusuldugunde kullaniciya ne gosterilecegi
- [ ] #6 Sonuc ve varsa spesifikasyon sapmasi design_decisions/ altina ve software/FIRMWARE_GEREKSINIMLERI.md'ye yazilmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
