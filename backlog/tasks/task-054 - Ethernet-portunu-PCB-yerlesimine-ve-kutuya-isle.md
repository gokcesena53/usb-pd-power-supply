---
id: TASK-054
title: Ethernet portunu PCB yerlesimine ve kutuya isle
status: To Do
assignee: []
created_date: '2026-09-23 12:09'
updated_date: '2026-09-23 20:34'
labels:
  - layout
  - fabrication
milestone: m-1
dependencies:
  - TASK-053
  - TASK-060
  - TASK-063
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: medium
ordinal: 108000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modul 53 x 22 mm ve RJ45 govdesi modul kenarindan 4,3 mm disa tasiyor; ana kart 65,9 x 40,6 mm. Modul standoff kullanilmadan, 2x8 header ve RJ45 tarafindaki iki mekanik pinle dogrudan ana karta lehimlenecek (footprint: Module_Custom:Waveshare_2-CH_UART_TO_ETH); RJ45 arka panelden cikacak. 3d_design/ bos oldugu icin kutu henuz kisitli degil, karar kutu tasarimindan once verilmeli.

RF sorunu: ESP32-C6-MINI-1'in PCB anteni keep-out istiyor, metal govdeli RJ45 ve Ethernet kablosu antenin yakininda Wi-Fi menzilini dusurur. Kullanici hem Wi-Fi hem ETH istiyor, yani ya RJ45 karsi kenara alinip yeterli ayrim birakilmali ya da U2 harici antenli ESP32-C6-MINI-1U-H4'e gecirilmeli.

Toprak sorunu: uretici semasindan (2-CH_UART_TO_ETH_SCH.pdf) RJ45'in kabuk pedleri (J1 pin 13/14) dogrudan modul GND'sine bagli. Sinyal ciftleri trafo ile izole ama ekranli (STP) kablo gopo toprapini bina toprapina baglar. Cikisi 28 V'a kadar yuzen bir tezgah kaynagi icin bu istenmeyen bir yol; kullanim notuna ve gerekirse montaja yansimali.

Yerlesim henuz baslamadi (PCB'de 7 segment var), bu is TASK-006 ve TASK-008 ile birlikte yurutulmeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 RJ45 ve Ethernet kablosunun MINI-1 anten keep-out bolgesine olan mesafesi belirlenmis; yetersizse ESP32-C6-MINI-1U-H4 gecisi karara baglanip design_decisions/ altina yazilmis
- [ ] #2 Q8 ve ETH_3V3 yolu 0,20 A icin boyutlanmis; AOZ1284 bakir alani artan ~0,16 W kayip icin gozden gecirilmis
- [ ] #3 RJ45 kabuk pedlerinin dogrudan GND'de oldugu gercegi karara baglanmis: UTP zorunlulugu kullanim notuna yazilmis veya kabuk montajda ayrilmis
- [ ] #4 Kutu arka panelinde RJ45 kesiti ve modulun yuksekligi 3d_design/ tasarimina islenmis
- [x] #5 J8'e Module_Custom:Waveshare_2-CH_UART_TO_ETH atanmis ve PCB'ye alinmis; DRC schematic parity 0
- [ ] #6 Modul ana kart kenarina RJ45 4.3 mm disari tasacak sekilde yerlestirilmis; header pinlerinin kart altindan ~4.4 mm cikintisi (6.0 - 1.6) montaj/kutu icin degerlendirilmis
- [ ] #7 Modul footprint'i PCB'ye yerlesmis; modulun altinda (2,5 mm ara) kalan parcalar <=2 mm ve RJ45 pim alani keepout'unda F.Cu iz/via/parca yok; RJ45 icin mekanik cakisma yok
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026 (TASK-006): J8'in şemada footprint'i yok (Value TBD), bu yüzden PCB'ye gelmedi; DRC schematic parity'deki tek kalan sorun bu. Footprint numuneyle (TASK-052) atanınca `python .claude/skills/kicad-schematic/scripts/update_pcb.py hardware/gopo.kicad_pcb` ile PCB'ye alınır.

23.09.2026: Proje footprint'i cizildi: `Module_Custom:Waveshare_2-CH_UART_TO_ETH` (hardware/libraries/Module_Custom.pretty, fp-lib-table'a eklendi). Standoff yok, modul dogrudan lehimli: 2x8 header (1.7/1.0 mm ped, KiCad PinHeader ile ayni) + RJ45 tarafinda iki mekanik pin (P2/P3, modul semasinda baglantisiz; ped 'MP', 2.2/1.4 mm, net yok). Orijin pin 1 (dis sutun, RJ45'ten uzak alt kose). RJ45 modul kenarindan 4.3 mm tasar; courtyard bunu kapsiyor. RJ45 pim alaninda F.Cu keepout (iz/via/dokum/parca yok): header ara parcasi 2.5 mm, RJ45 lehim cikintisi ~2.2 mm. Olculer Waveshare olcu cizimi + modul semasindan; mekanik pin y konumu goruntuden (+-0.3 mm). J8'e atama KiCad kapaliyken yapilacak.

23.09.2026: J8 Footprint = Module_Custom:Waveshare_2-CH_UART_TO_ETH, Value = 2-CH UART TO ETH (verify.py: ERC 0, netlist farki YOK; alan geometrisi degismedi). PCB update_pcb.py --keep-tracks ile guncellendi (yalniz 'EKLE J8'); kicad-cli pcb drc --schematic-parity: parity 0. J8 henuz yerlesmemis parcalarin arasinda duruyor (courtyard cakismalari yerlesimle cozulecek). update_pcb.py Windows'ta KiCad python'uyla calisacak sekilde duzeltildi (kicad-cli ve footprint dizini otomatik bulunuyor).

23.09.2026: Footprint'e basitlestirilmis 3D model eklendi: libraries/Module_Custom.3dshapes/Waveshare_2-CH_UART_TO_ETH.step (Waveshare model yayinlamiyor). Olcu cizimi boyutlarinda renkli kutular: modul PCB z 2.5-4.1, RJ45 modul altindan 15.0 yuksek ve kenardan 4.3 tasar, CH9121/AMS1117, 2x8 header (ara parca 2.5, pin 6.0 asagi), iki mekanik pin. Model footprint koordinatinda, offset/rotate 0. kicad-cli pcb render (ust/izometrik/on) ve pcb export step ile dogrulandi; PCB'deki J8'e de eklendi. Kutu tasarimi (3d_design/) icin STEP dogrudan kullanilabilir; RJ45 ic geometrisi yok, yalniz dis zarf.
<!-- SECTION:NOTES:END -->
