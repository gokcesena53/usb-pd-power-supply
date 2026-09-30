---
id: TASK-098
title: Test noktalarinin yerlesimini ve erisilebilirligini dogrula
status: Done
assignee: []
created_date: '2026-09-28 06:29'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-096
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/task-098-20260928/test_points_map.md
priority: high
ordinal: 184000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TP1-TP14 test noktalarinin mekanik erisilebilirligini, katmanlarini ve sinyallerini dogrula. LCD altinda kalan TP9 ve TP10u erisilebilir bolgeye tasi, eksik guc rayi test noktalarini ekle.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 TP9 ve TP10 test noktalari LCD kapali alanindan cikarilip B.Cu katmanina veya acik alana tasinmis; montaj sonrasi prob erisimi saglanmis.
- [x] #2 TP11, TP12, TP13 (UART) hucresi LCD cerceve sinirindan en az 1.5 mm guvenli mesafeye cekilmis.
- [x] #3 TP6, TP7, TP8 (I2C) hucresi yanina osiloskop sasi klipsi icin GND olcum noktasi degerlendirilmis (TP13 ve J8 GND prob referansi olarak dokumante edildi).
- [x] #4 +3.3V, V_PRE, OUT_POS ve SW_EN hatlari icin test noktasi ihtiyaci degerlendirilmis; sematige dokunulmadan mevcut komponent bacaklari uzerinden alternatif prob kilavuzu cikarilmis; guncel TP haritasi yayinlanmis.
- [x] #5 DRC calistirilmis, 0 yeni ihlal ve schematic parity 0 dogrulanmis.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

### 1. Relocated Test Points (TP1-TP14)
- **TP9 (`/MCU/ETH_CFG0`)**: F.Cu $(120.40, 89.20)$ -> B.Cu $(107.50, 82.50)$. LCD altından çıkarıldı. Mezanin modül gövdesine $3.03\text{ mm} \ge 1.5\text{ mm}$ güvenli açıklık sağlandı.
- **TP10 (`/MCU/ETH_PWR_EN`)**: F.Cu $(120.40, 91.20)$ -> B.Cu $(107.50, 79.50)$. LCD altından çıkarıldı.
- **TP14 (`/MCU/ETH_RUN`)**: B.Cu $(107.50, 82.50)$'de bulunuyordu; TP9 yerleşimiyle çakışmayı önlemek için B.Cu $(110.50, 82.50)$'ye kaydırıldı.
- **TP11, TP12, TP13 (UART Cell)**: F.Cu $Y=72.70\text{ mm}$ -> $Y=70.70\text{ mm}$. LCD üst çerçeve sınırı $Y=72.48\text{ mm}$'ye olan mesafe $1.78\text{ mm} \ge 1.5\text{ mm}$'dir. Silkscreen çakışmalarını önlemek için metinler `(hide yes)` yapıldı.

### 2. Şematik ve BOM Bütünlüğü (Ek Bileşen Eklenmedi)
- Kullanıcı direktifi doğrultusunda şematik dosyalarına (`mcu.kicad_sch` ve `usb_pd_controller.kicad_sch`) hiçbir yeni komponent veya test noktası eklenmemiş, şematik %100 orijinal halinde korunmuştur.
- +3.3V, V_PRE, OUT_POS, SW_EN ve I2C GND hatları donanım dokümantasyonunda (`test_points_map.md`) mevcut devre elemanları (C16, C27/C28/D4, J4/C31, R27/U13, TP13/J8) üzerinden alternatif prob noktaları olarak tanımlanmıştır.

### 3. Verification & DRC Metrics
- **KiCad DRC:**
  - Komut: `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
  - Toplam İhlal: 164 (Taban: 168. UART serigrafi çakışmaları çözülerek 4 ihlal azaltıldı, 0 yeni ihlal).
  - Parite: **0 schematic parity issue** (%100 parite).
  - Bağlantısız: 360 (Taban korundu, 0 yeni bağlantısız).
- **Rapor ve Harita Dokümantasyonu:**
  - `hardware/docs/reports/task-098-20260928/test_points_map.md` oluşturuldu. Tüm 14 test noktasının koordinatları, katmanları, sinyalleri, pad boyutları ve mekanik erişilebilirlik durumları ile güç rayları prob kılavuzu belgelendi.
