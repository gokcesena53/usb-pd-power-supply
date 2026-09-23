---
id: TASK-054
title: Ethernet portunu PCB yerlesimine ve kutuya isle
status: To Do
assignee: []
created_date: '2026-09-23 12:09'
updated_date: '2026-09-23 15:18'
labels:
  - layout
  - fabrication
milestone: m-1
dependencies:
  - TASK-053
  - TASK-060
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: medium
ordinal: 108000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modul 53 x 22 mm ve RJ45 govdesi disa tasiyor; ana kart 65,9 x 40,6 mm oldugu icin modul kart ustune yerlesemiyor, mezanin olarak 2x8 header ve standoff uzerinde duracak ve RJ45 arka panelden cikacak. 3d_design/ bos oldugu icin kutu henuz kisitli degil, karar kutu tasarimindan once verilmeli.

RF sorunu: ESP32-C6-MINI-1'in PCB anteni keep-out istiyor, metal govdeli RJ45 ve Ethernet kablosu antenin yakininda Wi-Fi menzilini dusurur. Kullanici hem Wi-Fi hem ETH istiyor, yani ya RJ45 karsi kenara alinip yeterli ayrim birakilmali ya da U2 harici antenli ESP32-C6-MINI-1U-H4'e gecirilmeli.

Toprak sorunu: uretici semasindan (2-CH_UART_TO_ETH_SCH.pdf) RJ45'in kabuk pedleri (J1 pin 13/14) dogrudan modul GND'sine bagli. Sinyal ciftleri trafo ile izole ama ekranli (STP) kablo gopo toprapini bina toprapina baglar. Cikisi 28 V'a kadar yuzen bir tezgah kaynagi icin bu istenmeyen bir yol; kullanim notuna ve gerekirse montaja yansimali.

Yerlesim henuz baslamadi (PCB'de 7 segment var), bu is TASK-006 ve TASK-008 ile birlikte yurutulmeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 2x8 mezanin konnektoru ve standoff delikleri PCB'ye yerlesmis, modul govdesi ve RJ45 icin mekanik cakisma yok
- [ ] #2 RJ45 ve Ethernet kablosunun MINI-1 anten keep-out bolgesine olan mesafesi belirlenmis; yetersizse ESP32-C6-MINI-1U-H4 gecisi karara baglanip design_decisions/ altina yazilmis
- [ ] #3 Q8 ve ETH_3V3 yolu 0,20 A icin boyutlanmis; AOZ1284 bakir alani artan ~0,16 W kayip icin gozden gecirilmis
- [ ] #4 RJ45 kabuk pedlerinin dogrudan GND'de oldugu gercegi karara baglanmis: UTP zorunlulugu kullanim notuna yazilmis veya kabuk montajda ayrilmis
- [ ] #5 Kutu arka panelinde RJ45 kesiti ve modulun yuksekligi 3d_design/ tasarimina islenmis
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026 (TASK-006): J8'in şemada footprint'i yok (Value TBD), bu yüzden PCB'ye gelmedi; DRC schematic parity'deki tek kalan sorun bu. Footprint numuneyle (TASK-052) atanınca `python .claude/skills/kicad-schematic/scripts/update_pcb.py hardware/gopo.kicad_pcb` ile PCB'ye alınır.
<!-- SECTION:NOTES:END -->
