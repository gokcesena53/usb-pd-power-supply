---
id: TASK-123
title: ESP32 TFT/encoder pin atamasını J3/J9 sırasına göre yeniden düzenle
status: Done
assignee: []
created_date: '2026-09-29 13:49'
updated_date: '2026-09-29 14:21'
labels:
  - schematic
  - layout
  - firmware
milestone: m-1
dependencies:
  - TASK-122
references:
  - hardware/gopo.kicad_pcb
  - software/FIRMWARE_GEREKSINIMLERI.md
  - hardware/docs/reports/placement-pinswap-20260929/
documentation:
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - software/FIRMWARE_GEREKSINIMLERI.md
modified_files:
  - hardware/mcu.kicad_sch
  - hardware/gopo.kicad_pcb
  - software/FIRMWARE_GEREKSINIMLERI.md
  - CHANGES.TXT
  - design_decisions/output/SIFIRDAN_YERLESIM_AGIRLIKLI_RATSNEST_20260929.md
  - .claude/skills/kicad-schematic/scripts/update_pcb.py
priority: high
ordinal: 209000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kalan sinyal kesişmelerinin çoğu TFT SPI (MOSI, SCLK, DC, CS) ve ENCODER_A/B/SW netlerinde; ESP32-C6 pin sırası J3/J9 sırasına uymuyor. GPIO matrisi ile pin değişimi öner, kazancı ölç, kullanıcı onayıyla şemaya uygula. Kullanıcı pin değişikliğine olumlu (29.09.2026).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Strapping pinleri, USB (IO12/IO13) ve ESP32-C6 datasheet kısıtları korunmuş; TFT SPI saat hızı için IOMUX/GPIO matrisi sınırı datasheet'ten doğrulanmış
- [x] #2 Önerilen atama ile sinyal kesişmesi ölçülmüş (taban 51) ve kullanıcı onayı alınmış
- [x] #3 Şema güncellenmiş; ERC temiz, PCB update sonrası parite 0
- [x] #4 software/FIRMWARE_GEREKSINIMLERI.md pin tablosu güncellenmiş
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Öneri (29.09.2026, onay bekliyor). Sabit: EN, GPIO0 ETH_PWR_EN, GPIO6 OUT_EN, GPIO12/13 USB, GPIO8/9 boot, GPIO16/17 UART0. Değişebilir 14 pad; GPIO4/5/15 (strapping) yalnız TFT SCLK/MOSI/DC/CS/RST (TFT tarafı yüksek empedans, kartta pull yok).
Arama: pinswap (yerleşim sabit, Engine.total, 40 rastgele başlangıç + açgözlü ikili değişim) → yeniden yerleşim (untangle + refine 150k + align) → ikinci pinswap turu değişiklik bulmadı (yakınsadı).
Önerilen atama:
- TFT_SCLK GPIO4 (aynı), TFT_BL_PWM GPIO1 (aynı)
- TFT_DC GPIO7 → GPIO5; TFT_CS GPIO14 → GPIO15; TFT_MOSI GPIO5 → GPIO18; TFT_RST GPIO15 → GPIO19
- ENCODER_A GPIO22 → GPIO3; ENCODER_B GPIO23 → GPIO7; ENCODER_SW GPIO21 → GPIO14
- PD_INT_3V3 GPIO20 → GPIO2; INA_ALERT GPIO3 → GPIO20; RTC_INT GPIO2 → GPIO21
- I2C SCL GPIO18 → GPIO22; SDA GPIO19 → GPIO23
Sonuç: sinyal kesişmesi 51 → 42 (sabit yerleşim) → 38 (yeniden yerleşim); S 8170 → 7841; uzayan kritik kenar yok; ceza 0; R34 12,3 mm'de kaldı.
Datasheet (esp32-c6-mini-1 v1.5): FSPICLK=GPIO6 (OUT_EN) → TFT SPI bugün de GPIO matrisi üzerinden; hız sınırı değişmez. GPIO15 strap yalnız EFUSE_JTAG_SEL_ENABLE=1 ise etkili (varsayılan 0); MTDI (GPIO5) strap SDIO örnekleme kenarı (SDIO kullanılmıyor).
Dikkat: RTC_INT ve INA_ALERT LP GPIO'dan (2/3) LP olmayan pine (21/20) geçiyor → deep-sleep uyanması gerekirse sorun; firmware dokümanında bu gereksinim yok. ENCODER_A (GPIO3) ve PD_INT (GPIO2) LP pine geçiyor.

Uygulama (29.09.2026, kullanıcı onayı: deep-sleep uyanması yok, pull'lar kalsın, pin tablosu güncellenebilir, kilitli parçalar yerinde):
- mcu.kicad_sch: U2 pinlerine doğrudan bağlı 12 etiket yeniden adlandırıldı (geometri aynı; IO21 RTC_INT yerel etiketi INA_ALERT etiketine bindiği için tel 142.24'te bitirilip etiket rot 180 yapıldı). verify: ERC 0 ihlal, 120 net, bağlantı farkı yalnız 12 beklenen net (her biri planlanan U2 pinine). readability: 5 bulgu (R4/SW2/TP9, HEAD'de de 5).
- update_pcb.py board-only/kilitli footprint'leri silmiyordu -> düzeltildi (KORU H1-H4, MECH_ENC). PCB güncellemesi: yalnız U2'nin 12 pad neti değişti, taşınan 0.
- Yerleşim (a.json, seed 61): pcb_apply taşınan 85, pad sapması 0; pcb_check kilitli taşınan [], pad-net/yüz/footprint farkı yok, DRC 56 -> 60 (silk_overlap 15->18, silk_over_copper 16->17), bağlantısız 361, parite 0, GECTI. score: kesişme 42 -> 38 (pin öncesi yerleşimde 51), S 7918,9 -> 7841,2, uzayan kritik kenar yok.
- FIRMWARE_GEREKSINIMLERI.md §1 pin tablosu; TASK-033 AC#2 I2C 22/23.

Düzeltme: update_pcb.py şemada olmayan board-only/kilitli footprint'leri SİLİYORDU (dry-run: SIL H1-H4, MECH_ENC); artık KORU.
<!-- SECTION:NOTES:END -->
