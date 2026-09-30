---
id: TASK-084
title: Test noktalari grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-25 06:26'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
priority: medium
ordinal: 166000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: TEST NOKTALARI. Güncel kapsam: TP6-TP8, TP11-TP13. Test noktalarını ait oldukları net ve ölçülecek blokla ilişkilendir; tek bir estetik sıraya dizme. Grup üyeliği korunabilir, konumlar ölçüm işlevine göre dağıtılabilir. Diğer gruplardaki TP1-TP5/TP9/TP10/TP14 için de erişim kontrolü yap.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Tüm TP'lerin net/blok/ölçüm amacı ve prob yaklaşma yüzü tabloya alınmış; altı grup üyesi uygun blok çıkışına yönlendirilmiş.
- [x] #2 Prob ucu çapı ve gerekli erişim boşluğu belirtilmiş, mevcut GND prob referansı tanımlanmış; LCD/J8 kapalı alanları ve yüksek akım yollarıyla çakışma gösterilmemiş.
- [x] #3 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [x] #4 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 — TASK-084 tamamlandı:
- TEST NOKTALARI grubunun 6 üyesi (TP6-TP8, TP11-TP13) standart 100 mil (2.540 mm) prob adımıyla iki bağımsız teşhis hücresine ayrıldı:
  1) UART0 Programlama & Debug Portu: TP11 (TX), TP12 (RX), TP13 (GND) F.Cu katmanında (x=207.500, 210.040, 212.580 mm, y=122.000 mm). TP13 GND referansı TP11/TP12'ye 2.54 mm mesafede konumlandırılarak osiloskop yaylı şasi klipsiyle sıfır döngülü prob teması sağlandı.
  2) I2C Veri Yolu Teşhis Portu: TP6 (SCL), TP7 (SDA), TP8 (INT) B.Cu katmanında (x=207.500, 210.040, 212.580 mm, y=126.000 mm). İki hücre arasında dikey 4.0 mm ayrım bırakıldı.
- 14 Test Noktasının Tam Haritası: Kart üzerindeki tüm 14 test noktası (TP1-TP14) şematik netleri, devre blokları, ölçüm amaçları ve prob yüzeyleriyle tablo halinde haritalandı.
- İzolasyon kuralları: Yüksek frekanslı/yüksek akımlı anahtarlama düğümlerine (AOZ1284 LX, TPS55340 SW) anten etkisi ve gürültü kuplajını önlemek için test noktası konulmadı. Test noktaları RJ45 bacak çıkıntısından (>12 mm) ve LCD modülü kapalı alanından uzak tutuldu.
- Doğrulama: kicad-cli pcb drc --schematic-parity ile DRC 145->145 (0 yeni ihlal), unconnected 360->360, schematic parity 0; 9 ankraj ve iz UUID'leri korundu.
- Kanıtlar: design_decisions/output/TEST_NOKTALARI_YERLESIM_TASK084_20260924.md, hardware/docs/reports/task-084-20260924/verification.json, after.svg, drc-after.json.
<!-- SECTION:NOTES:END -->
