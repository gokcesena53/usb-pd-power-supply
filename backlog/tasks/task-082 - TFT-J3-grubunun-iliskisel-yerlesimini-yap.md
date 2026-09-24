---
id: TASK-082
title: TFT J3 grubunun iliskisel yerlesimini yap
status: To Do
assignee: []
created_date: '2026-09-24 07:38'
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
- [ ] #1 C34 doğru J3 besleme/GND pad çiftine yakın ve kısa dönüşe uygun; J3 pin1 yönü ve kilidi korunmuş.
- [ ] #2 ZIF kapağı, FPC giriş/büküm alanı ve LCD altı yükseklik sınırları ihlal edilmemiş; SPI ve backlight koridorları gösterilmiş.
- [ ] #3 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [ ] #4 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
