---
id: TASK-079
title: I2C seviye donusturucu grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 12:26'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
priority: medium
ordinal: 161000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: I2C SEVIYE DONUSTURUCU 5V <-> 3.3V. Güncel kapsam: Q1, Q2, R4-R7. SDA/SCL için Q1/Q2 ve pull-up dirençlerini paralel iki kanal halinde düzenle. 5 V ve 3.3 V uçlarını güncel netlerden belirle; ilgili BSS138P üretici belgesini kullan.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Her MOSFET source/drain/gate ve pull-up besleme tarafı netlerden doğrulanmış; 5 V ve 3.3 V bağlantı yüzleri açıkça gösterilmiş.
- [x] #2 SDA/SCL koridorları karşılıklı dolaşma gerektirmiyor; MCU ve PD gruplarıyla giriş/çıkış yönleri uzlaştırılmış.
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
## I2C Seviye Dönüştürücü Grubu İliskisel Yerlesim Raporu

### 1. Kapsam ve Kurallar
`I2C SEVIYE DONUSTURUCU 5V <-> 3.3V` grubundaki 6 footprint (Q1, Q2, R4, R5, R6, R7), NXP AN10441 çift yönlü I2C seviye dönüştürücü uygulama notu ve TASK-065 B.Cu yüz atamasına göre B.Cu katmanında ilişkisel olarak yerleştirildi.

### 2. Yerleşim Detayları ve Simetri
- **Çift Kanal Paralel Kolon Yapısı:**
  - **SCL Kolonu (x=209.0 mm):** R4 (3.3V pull-up, y=107.5) → Q1 (BSS138P, y=111.0, rot 270°) → R5 (5V pull-up, y=114.5, rot 90°).
  - **SDA Kolonu (x=213.5 mm):** R7 (3.3V pull-up, y=107.5) → Q2 (BSS138P, y=111.0, rot 270°) → R6 (5V pull-up, y=114.5, rot 90°).
- **Gerilim Alanları ve Bağlantı Yüzleri:**
  - **3.3 V Alanı (Kuzey):** MOSFET kaynak (Source) pinleri ve 3.3 V pull-up'ları kuzeye bakar. BQ32000 RTC (U4) ve batıdaki ESP32-C6 / INA226 hatlarına kesişimsiz açılır.
  - **5.0 V Alanı (Güney):** MOSFET savak (Drain) pinleri ve 5 V pull-up'ları güneye bakar. Güneydeki AP33772S (U1) PD kontrolcüsüne doğrudan yönelir.
- **Kanal Simetrisi ve Ölçümler:**
  - Q1.2 → R4.1 (SCL_3V3): **2.600 mm**
  - Q2.2 → R7.2 (SDA_3V3): **2.600 mm**
  - Q1.3 → R5.2 (SCL_5V): **2.052 mm**
  - Q2.3 → R6.2 (SDA_5V): **2.052 mm**
  - Kanallar arası simetri farkı: **0.000 mm** (tam eşlenik!). Kesişen iz (crossover) yoktur.
- **Ortak Baralar:**
  - Gate Barası (+3.3V): Q1.1 ↔ Q2.1 yatay izi (**4.500 mm**).
  - 3.3V Pull-Up Barası: R4.2 ↔ R7.1 yatay izi (**4.500 mm**).
  - 5V Pull-Up Barası: R5.1 ↔ R6.1 yatay izi (**4.500 mm**).

### 3. Doğrulama ve DRC Sonuçları
- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni ihlal: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel envanter korundu).
  - **Schematic parity:** **0 → 0**.
- **Courtyard kontrolü:** 6 eleman arasında minimum 2D aralık **0.590 mm** (Q1–R5 ve Q2–R6); çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 ve mevcut izler korundu.

### 4. Bağlantılı Dokümanlar ve Kanıtlar
- [Tasarım Karar Raporu](../../design_decisions/output/I2C_SEVIYE_DONUSTURUCU_YERLESIM_TASK079_20260924.md)
- [Önce Görünüm SVG](../../hardware/docs/reports/task-079-20260924/before.svg)
- [Sonra Görünüm SVG](../../hardware/docs/reports/task-079-20260924/after.svg)
- [KiCad Top Katman SVG](../../hardware/docs/reports/task-079-20260924/board-top.svg)
- [KiCad Bottom Katman SVG](../../hardware/docs/reports/task-079-20260924/board-bottom.svg)
- [DRC Önce](../../hardware/docs/reports/task-079-20260924/drc-before.json)
- [DRC Sonra](../../hardware/docs/reports/task-079-20260924/drc-after.json)
- [Ölçüm ve Doğrulama Verileri](../../hardware/docs/reports/task-079-20260924/verification.json)
- [Yerleşim Betiği](../../hardware/docs/reports/task-079-20260924/place.py)
- [Doğrulama Betiği](../../hardware/docs/reports/task-079-20260924/verify.py)
- [CHANGES.TXT Değişiklik Kaydı](../../CHANGES.TXT)
<!-- SECTION:NOTES:END -->
