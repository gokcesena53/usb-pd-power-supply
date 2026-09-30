---
id: TASK-078
title: RTC grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 12:21'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/bq32000.pdf
  - hardware/datasheets/ABS25.pdf
  - hardware/datasheets/korchip_dcl.pdf
priority: medium
ordinal: 160000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: RTC BQ32000 + 1F5 süper kapasitör. Güncel kapsam: U4, Y1, C9, C33, R24. U4–Y1 osilatör ilişkisini, C9 bypass ve C33 yedekleme yolunu temel al. Süperkapasitör yüksekliği TASK-065 ile birlikte ele alınır.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Y1 U4 osilatör pinlerine yakın ve kısa/simetrik bağlantıya uygun; kristal altında/çevresinde üreticinin bakır ve sinyal kısıtları işaretlenmiş.
- [x] #2 C9 besleme/GND pinlerine yöneltilmiş; C33 polaritesi, gövde/yükseklik alanı ve RTC çevresinin SW/ısı kaynaklarından uzaklığı kaydedilmiş.
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
## RTC BQ32000 + 1F5 Süperkapasitör Grubu İliskisel Yerlesim Raporu

### 1. Kapsam ve Kurallar
`RTC BQ32000 + 1F5 süper kapasitör` grubundaki 5 footprint (U4, Y1, C9, C33, R24), TI BQ32000 Datasheet (§8.3 Yerleşim Kılavuzu & Şekil 8-4), Abracon ABS25 kristal kılavuzu ve TASK-065 B.Cu yükseklik koordinasyonuna göre B.Cu katmanında ilişkisel olarak yerleştirildi.

### 2. Yerleşim Detayları ve Simetri
- **Osilatör (Y1 ↔ U4):** U4 (SOIC-8) rot 180° konumunda (214.0, 99.0) yerleştirildi; Y1 (ABS25 32.768kHz) rot 270° ile doğrudan U4 Pin 1/2 doğusuna (223.5, 97.725) konumlandırıldı.
  - U4.1 → Y1.1 (OSCI): **4.384 mm**
  - U4.2 → Y1.4 (OSCO): **4.381 mm**
  - Simetri farkı (skew): **0.003 mm** (3 mikron!). Kesişimsiz, paralel diferansiyel eşleşme.
  - Y1 toprak pedleri (Pad 2 & 3) doğuya bakarak sessiz koruyucu toprak halkasına (guard ring) açılmıştır.
- **Besleme Filtresi (C9):** 1uF 0402 seramik bypass kapasitörü U4 Pin 8 (+3.3V) dibine (2.115 mm) yerleştirildi; GND dönüşü Pin 4'e iç toprak düzlemiyle bağlanır.
- **IRQ Pull-Up (R24):** 4.7k 0402 direnç Pin 7 (RTC_INT) ile Pin 8 (+3.3V) arasına doğrudan U4 batısına (2.601 mm) yerleştirildi.
- **Süperkapasitör Yedekleme (C33):** Korchip DCL H-Tipi 1.5F 5.5V yatay madeni para tipi süperkapasitör (207.98, 82.50) rot 180° konumunda tutuldu; Pad 1 (VBACK) doğrudan U4 Pin 3'e yönelir.
- **Termal ve Gürültü İzolasyonu:** Kristal ve süperkapasitör, 2W çıkış deşarj direnci R67'den **>19.7 mm** ve anahtarlamalı güç dönüştürücülerinden **>100 mm** uzakta izole edilmiştir.
- **Mekanik / Yükseklik Uyumu:** C33 (6.5 mm) ve Y1 (2.5 mm) gövdeleri üst yüzdeki LCD ekran modülünün 1.80 mm sınırını aştığı için TASK-065 kararına uygun olarak B.Cu'da tutulmuştur.

### 3. Doğrulama ve DRC Sonuçları
- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni ihlal: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel envanter korundu).
  - **Schematic parity:** **0 → 0**.
- **Courtyard kontrolü:** 5 eleman arasında minimum 2D aralık **0.540 mm** (C33–C9); çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 ve mevcut izler korundu.

### 4. Bağlantılı Dokümanlar ve Kanıtlar
- [Tasarım Karar Raporu](../../design_decisions/output/RTC_BQ32000_YERLESIM_TASK078_20260924.md)
- [Önce Görünüm SVG](../../hardware/docs/reports/task-078-20260924/before.svg)
- [Sonra Görünüm SVG](../../hardware/docs/reports/task-078-20260924/after.svg)
- [KiCad Top Katman SVG](../../hardware/docs/reports/task-078-20260924/board-top.svg)
- [KiCad Bottom Katman SVG](../../hardware/docs/reports/task-078-20260924/board-bottom.svg)
- [DRC Önce](../../hardware/docs/reports/task-078-20260924/drc-before.json)
- [DRC Sonra](../../hardware/docs/reports/task-078-20260924/drc-after.json)
- [Ölçüm ve Doğrulama Verileri](../../hardware/docs/reports/task-078-20260924/verification.json)
- [Yerleşim Betiği](../../hardware/docs/reports/task-078-20260924/place.py)
- [Doğrulama Betiği](../../hardware/docs/reports/task-078-20260924/verify.py)
- [CHANGES.TXT Değişiklik Kaydı](../../CHANGES.TXT)
<!-- SECTION:NOTES:END -->
