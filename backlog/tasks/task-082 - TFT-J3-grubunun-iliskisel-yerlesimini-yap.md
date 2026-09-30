---
id: TASK-082
title: TFT J3 grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-25 06:14'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/TFT032B018.pdf
  - hardware/datasheets/KLS1-242I.pdf
  - design_decisions/output/LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md
priority: medium
ordinal: 164000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: TFT CONNECTOR J3. Güncel kapsam: C34; ilişkili sabit ankraj J3. Grup üyesi C34'ü sabit J3 besleme/GND pinlerine göre yerleştir. J3 grubun üyesi değildir; TASK-064'teki kilitli (98.00,109.30 mm,90°) ankraj ve FPC mekanik zarfı korunur. C34'ün karta taşınması bu sabit ankraj istisnasıdır.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 C34 doğru J3 besleme/GND pad çiftine yakın ve kısa dönüşe uygun; J3 pin1 yönü ve kilidi korunmuş.
- [x] #2 ZIF kapağı, FPC giriş/büküm alanı ve LCD altı yükseklik sınırları ihlal edilmemiş; SPI ve backlight koridorları gösterilmiş.
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
25.09.2026 — TASK-082 tamamlandı:
- TFT CONNECTOR J3 grubunun üyesi C34 (100nF / 1u0 0402 seramik dekuplaj kapasitörü), sabit mekanik ankraj J3'ün (KLS1-242I-2.0-30, x=98.00, y=109.30, rot 90°, locked) doğusuna x=101.000 mm, y=105.550 mm, rot 90.0° olarak yerleştirildi.
- Pad 1 (+3.3V VDD) x=101.00, y=106.03 mm konumunda olup J3 Pin 22 (+3.3V, y=106.05 mm) ile sadece 0.020 mm dikey sapmayla mükemmel eksenel hizada doğrudan kısa hatla bağlandı; Pin 21 ve Pin 23 ile ortak +3.3V barasına katıldı (döngü <3.0 mm).
- Pad 2 (GND) x=101.00, y=105.07 mm konumunda olup J3 Pin 25 (GND, y=104.55 mm) ve yerel via ile L2 GND_PLANE iç düzlemine bağlandı; ST7789V2 için minimum döngü alanlı ultra-düşük ESL/ESR dekuplaj sağlandı.
- Mekanik koridorlar korundu: FPC kablo giriş alanı ve ZIF flip-lock kapağı (Batı / -X yönü) tamamen engelsiz bırakıldı (>3.0 mm açıklık); C34 gövde yüksekliği (0.55 mm) TASK-065 LCD altı limitine (<=1.80 mm, pay 1.25 mm) tam uyum sağladı.
- Hassas sinyal koridorları: SPI hatları (Pin 16-20, y=107.05..109.05 mm) C34'ün kuzeyinde >0.56 mm avlu ve >1.02 mm pad mesafesiyle doğuya engelsiz yönlendirildi; Backlight PWM hatları (Pin 2, 4) >8.5 mm kuzeyde tamamen izole tutuldu.
- Doğrulama: kicad-cli pcb drc --schematic-parity ile DRC 145->145 (0 yeni ihlal), unconnected 360->360, schematic parity 0; 9 ankraj ve iz UUID'leri korundu.
- Kanıtlar: design_decisions/output/TFT_J3_YERLESIM_TASK082_20260924.md, hardware/docs/reports/task-082-20260924/verification.json, after.svg, drc-after.json.
<!-- SECTION:NOTES:END -->
