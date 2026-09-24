---
id: TASK-054
title: Ethernet portunu PCB yerlesimine ve kutuya isle
status: To Do
assignee: []
created_date: '2026-09-23 12:09'
updated_date: '2026-09-24 13:06'
labels:
  - layout
  - fabrication
milestone: m-1
dependencies:
  - TASK-053
  - TASK-060
  - TASK-063
  - TASK-008
  - TASK-080
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
documentation:
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: medium
ordinal: 122000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Güncel kart 99,40 × 61,04 mm. TASK-063'te belirlenen J7 top, J8 bottom/USB-C altı ve U2 top/anten dışarı mekanik yerleşimini son kutuya uygula. J8 53 × 22 mm modül, RJ45 nominal 4,3 mm taşma; 2x8 header ve iki mekanik pinle doğrudan montaj. Sol panel açıklıkları, fişler/mandal, kablolar, LCD/FPC ve header'ın top çıkıntıları birlikte doğrulanır. Numune ölçüleri TASK-053'ten alınır; modül altı bölgeler TASK-080 raporuna göre değerlendirilir.

ESP32 için karşı sağ kenar veya MINI-1U'ya otomatik geçiş şartı yoktur; mevcut MINI-1 anteninin dışarı taşması ve boşluğu esas alınır. Çözüm bu parça/kart zarfına sığmazsa ölçülü alternatif karar sunulur. RJ45 kabuk pedleri üretici şemasında modül GND'sine doğrudan bağlıdır; UTP kullanım veya kabuk izolasyonu kararı korunarak son montaja yansıtılır.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 RJ45/USB-C, takılı kablolar, LCD ve son kutunun U2 antenine mesafeleri numune/kutu geometrisiyle ölçülmüş; TASK-063/üretici RF boşlukları sağlanmış. Son kutu RF testi için mesafe/yön/trafik matrisi ve sayısal throughput/paket kaybı/kopma hedefleri testten önce belirlenip ayrı RF prototip görevine devredilmiş.
- [ ] #2 Q8 ve ETH_3V3 yolu 0,20 A için boyutlanmış; AOZ1284 bakır alanı artan yaklaşık 0,16 W kayıp için gözden geçirilmiş.
- [ ] #3 RJ45 kabuk pedlerinin doğrudan GND'de olduğu gerçeği karara bağlanmış: UTP zorunluluğu kullanım notuna yazılmış veya kabuk montajda ayrılmış.
- [ ] #4 Kutu sol panelinde üst USB-C/alt RJ45 açıklıkları, merkezleri, mandal/fiş boşlukları ve modül yüksekliği 3d_design tasarımına işlenmiş.
- [x] #5 J8'e Module_Custom:Waveshare_2-CH_UART_TO_ETH atanmış ve PCB'ye alınmış; DRC schematic parity 0.
- [ ] #6 J8 bottom ve nominal RJ45 4,3 mm taşma numuneyle doğrulanmış; top header pinleri LCD dışında veya metal+lehim≤1,50 mm olarak kesim/montaj şartına bağlanmış.
- [ ] #7 Modül altındaki ref/yükseklik/toleranslar TASK-080 haritasıyla uyumlu; RJ45 pim keepout'u bottom montaj yüzüne doğru dönüşmüş, yasak bölgede parça/iz/via/dolgu yok. Genel ≤2 mm varsayımı kullanılmamış; 3D çakışma yok.
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

24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir.

24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.
<!-- SECTION:NOTES:END -->
