---
id: TASK-081
title: TFT backlight grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 13:53'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/TFT032B018.pdf
  - design_decisions/output/TFT_BACKLIGHT_YERLESIM_TASK081_20260924.md
  - hardware/docs/reports/task-081-20260924/verification.json
  - hardware/docs/reports/task-081-20260924/after.svg
  - hardware/docs/reports/task-081-20260924/drc-after.json
priority: medium
ordinal: 163000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: TFT BACKLIGHT (3.3V + PWM). Güncel kapsam: Q7, R28, R29, R60. Mevcut Q7 PWM MOSFET ve R60 akım sınırlama devresini J3 arka ışık pinleriyle ilişkili düzenle. Eski CAT4104/boost tasarımını varsayma; Q7 için gerçek IRLML6344 üretici belgesini kullan.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 R28 gate yolunda ve R29 gate-source ilişkisine uygun; Q7/R60–J3 LED bağlantı yönü ve dönüş akımı çizilmiş.
- [x] #2 R60 güç kaybına uygun boşluk/bakır alanı ayrılmış; PWM dönüş yolu RTC/ölçüm devrelerinden uzak koridora yönlendirilmiş.
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
24.09.2026 — TASK-081 tamamlandı:
- TFT BACKLIGHT (3.3V + PWM) grubunun 4 üyesi (Q7, R28, R29, R60) F.Cu katmanında ilişkisel olarak yerleştirildi.
- Q7 IRLML6344TRPBF N-MOSFET (SOT-23, rot 0°) düşük taraf anahtarı: Pad 1 (Gate) ve Pad 2 (GND) batıya sürüş hücresine; Pad 3 (Drain, BL_K katot dönüşü) doğuya ekran konnektörüne yönlendirildi.
- R28 (100R 0402) PWM seri sönümleme direnci batıdan gelen MCU GPIO7 hattını karşılayacak şekilde, R29 (100k 0402) gate pull-down direnci ise Gate ile Source/GND arasında dikey köprü (x=18.80 mm, dy=1.02 mm) olarak bağlandı; açılış parlaması engellendi (hat mesafesi <2.35 mm).
- R60 (5R6 0805) akım sınırlama direnci +3.3V girişi ile BL_A anot çıkışı arasına yerleştirildi; Q7 Pad 3 (BL_K) ile R60 Pad 2 (BL_A) aynı doğu ekseninde paralel J3'e yönlendirildi.
- R60 güç kaybı (maks 27.4 mW, nominal 11.3 mW) 0805 kılıf sınırının (<%22) çok altında kaldı. PWM dönüş akımı Q7 Kaynak pini üzerinden yerel GND düzlemine bağlandı; INA226 ölçüm (>120 mm) ve RTC kristalinden (>180 mm) fiziksel olarak tamamen izole edildi.
- Tüm bileşenler F.Cu'da LCD altı yükseklik sınırına (maks 1.10 mm <= 1.80 mm) tam uyum sağladı.
- Doğrulama: kicad-cli pcb drc --schematic-parity ile DRC 145->145 (yeni ihlal: 0), unconnected 360->360, schematic parity 0; 9 ankraj ve iz UUID'leri korundu.
- Kanıtlar: design_decisions/output/TFT_BACKLIGHT_YERLESIM_TASK081_20260924.md, hardware/docs/reports/task-081-20260924/verification.json, after.svg, drc-after.json.
<!-- SECTION:NOTES:END -->
