---
id: TASK-077
title: ESP32-C6 grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 12:25'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/esp32-c6-mini-1_datasheet_en.pdf
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 159000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: ESP32-C6-MINI-1-H4. Güncel kapsam: U2, C5-C7, R1-R3, R10, R15, R16, R37, SW1, SW2, TP9, TP10. U2 modülünü esas alarak besleme, reset/boot, USB seri dirençleri ve programlama erişimini düzenle. Espressif modül datasheet ve resmi Hardware Design Guidelines kaynağından anten şartlarını çıkar.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Antenin sağ kart kenarına bakacağı yön ve tüm katmanlar için gerekli keepout ölçüleri kaynakla belgelenmiş; komşu bloklara ayrılacak yasak alan gösterilmiş.
- [x] #2 Bypass elemanları ilgili pinlere, seri dirençler üretici önerisindeki uca yerleştirilmiş; USB yolu ve I2C/UART çıkış koridorları tanımlanmış.
- [x] #3 SW1/SW2 ve TP9/TP10 erişimi LCD/mekanik kısıtlarla kontrol edilmiş; boot/reset hatları güç anahtarlama alanından ayrılmış.
- [x] #4 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [x] #5 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## ESP32-C6-MINI-1-H4 Grubu İliskisel Yerlesim Raporu

### 1. Kapsam ve Kurallar
`ESP32-C6-MINI-1-H4` grubundaki 15 footprint (U2, C5, C6, C7, R1, R2, R3, R10, R15, R16, R37, SW1, SW2, TP9, TP10), Espressif ESP32-C6-MINI-1 Datasheet (§10/§11) ve Donanım Tasarım Kılavuzu RF/anten, bypass, reset ve strapping kurallarına göre B.Cu katmanında ilişkisel olarak yerleştirildi.

### 2. Anten Keepout ve Yerleşim Koordinatları
- **Anten Yönü:** Modül PCB anteni DOĞU yönünde (kart kenarına doğru) konumlandırıldı (U2 rot: 90°).
- **Anten Keepout Bölgesi:** x: 166.22–186.62 mm, y: 72.00–115.20 mm alanı tüm 4 bakır katmanda (F.Cu, B.Cu, GND_PLANE, POWER_PLANE) ve 14 çevre elemanından %100 arındırıldı (keepout ihlali: 0).
- **Güç Dekuplajı:** C6 (100n 0402 RF bypass) VDD Pin 3 dibine (3.041 mm), C5 (22u 0805 bulk) hemen arkasına (5.585 mm) yerleştirildi.
- **EN Donanım Reset:** C7 (1u 0402) Pin 8 dibine (3.035 mm), R1 (10k 0402) bitişiğine (3.453 mm) yerleştirildi (tau = 10 ms >= 50 us).
- **Buton Koridoru:** SW2 (Reset) ve SW1 (Boot) taktil butonlar modül altında (x=158.5 mm, antenden >8 mm uzakta) 1.25 mm aralıkla dikey istiflendi.
- **Batı Sinyal Kolonu (x=152.0 mm):** R2 (22R USB_DM, 3.43 mm), R3 (22R USB_DP, 3.48 mm), R16 (10k ETH_PWR_EN, 2.41 mm), R10 (10k Boot, 3.43 mm), R37 (10k IO8, 3.52 mm), R15 (22R ETH_CFG0, 4.49 mm), TP9 (3.04 mm), TP10 (6.62 mm) Edge.Cuts'tan >2.2 mm açıkta hizalandı.

### 3. Doğrulama ve DRC Sonuçları
- `kicad-cli pcb drc --schematic-parity`:
  - **DRC ihlalleri:** **145 → 145** (yeni ihlal: **0**).
  - **Bağlantısız öğeler:** **360 → 360** (temel envanter korundu).
  - **Schematic parity:** **0 → 0**.
- **Courtyard kontrolü:** 14 çevre elemanı arasında minimum 2D aralık **0.410 mm** (R2–R3); çakışma **0**.
- **Ankrajlar ve izler:** J7, J3, J9, H1–H4, D5, U11 ve mevcut izler korundu.

### 4. Bağlantılı Dokümanlar ve Kanıtlar
- [Tasarım Karar Raporu](../../design_decisions/output/ESP32_C6_YERLESIM_TASK077_20260924.md)
- [Önce Görünüm SVG](../../hardware/docs/reports/task-077-20260924/before.svg)
- [Sonra Görünüm SVG](../../hardware/docs/reports/task-077-20260924/after.svg)
- [KiCad Top Katman SVG](../../hardware/docs/reports/task-077-20260924/board-top.svg)
- [KiCad Bottom Katman SVG](../../hardware/docs/reports/task-077-20260924/board-bottom.svg)
- [DRC Önce](../../hardware/docs/reports/task-077-20260924/drc-before.json)
- [DRC Sonra](../../hardware/docs/reports/task-077-20260924/drc-after.json)
- [Ölçüm ve Doğrulama Verileri](../../hardware/docs/reports/task-077-20260924/verification.json)
- [Yerleşim Betiği](../../hardware/docs/reports/task-077-20260924/place.py)
- [Doğrulama Betiği](../../hardware/docs/reports/task-077-20260924/verify.py)
- [CHANGES.TXT Değişiklik Kaydı](../../CHANGES.TXT)

24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir. Tamamlanan grup/yükseklik çalışmasının tarihsel kanıtı korunur; J7/U2 top'a taşıma ve yeniden doğrulama TASK-063/008 kapsamındadır.
<!-- SECTION:NOTES:END -->
