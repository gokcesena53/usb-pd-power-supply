---
id: TASK-043
title: R8/R9 bölücüsünü 10k + 2×10k ile değiştir
status: Done
assignee: []
created_date: '2026-09-23 05:34'
updated_date: '2026-09-23 05:56'
labels:
  - schematic
  - procurement
milestone: m-1
dependencies: []
references:
  - hardware/usb_pd_controller.kicad_sch
  - design_decisions/output/PD_INT_BOLUCU_20260923.md
  - CHANGES.TXT
priority: medium
ordinal: 102000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PD_INT_5V (U1 pin 9) → PD_INT_3V3 (U2 GPIO pin 26) bölücüsü şu an R8=12k / R9=20k. Öneri: R8=10k, R9 yerine seri iki 10k (20k). Oran 5×20/30 = 3.33 V (mevcut 3.125 V); amaç BOM'da 12k ve 20k kalemlerini 10k'ya indirmek.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 En kötü durumda (VOH 4.37–5.33 V, direnç toleransları) PD_INT_3V3 ≤ VDD_min+0.3 = 3.52 V ve ≥ 0.75×VDD_max = 2.565 V hesabı yazıldı
- [x] #2 U1 INT çıkış tipi (open-drain/push-pull) ve yük akımı datasheet'ten doğrulandı; 30 kΩ toplam yük uygun
- [x] #3 Şemada R8=10k + R64 2k0 seri, R9=10k + R65 10k seri uygulandı, ERC temiz (kullanıcı kararı: 10k/2×10k VIH maks'ı aştığı için)
- [x] #4 BOM'da 12k ve 20k kalemleri kalmadı
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
AP33772S INT push-pull, VOH 4.37–5.33 V, ≥2 mA (DS46176). ESP32-C6: VIH ≥ 0.75×VDD, maks VDD+0.3. +3.3V rayı 3.22–3.42 V (AOZ1284 VFB 0.788–0.812, R39/R40 ±1 %) → pencere 2.565–3.52 V.
- Eski 12k/20k: 2.720–3.345 V (uygun).
- İlk öneri 10k / 2×10k (±0.1 %): 2.911–3.556 V → VIH maks'ı 36 mV aşıyor. Kullanıcıya soruldu; 10k+2k0 / 2×10k seçildi.
- Uygulanan: R8 10k + R64 2k0 (ERJ2RKF2001X) / R9 10k + R65 10k (TC0250B1002TCC ±0.1 %): 2.728–3.336 V.
Kanıt (verify.py --against 776ce38 netlist): ERC 0 hata / 0 uyarı; fark yalnız PD_INT_3V3 = R64.2, R9.1, TP8.1, U2.26; yeni Net-(R64-Pad1) = R8.2, R64.1; Net-(R65-Pad1) = R9.2, R65.1; GND'de R9.2 → R65.2. Netlistte 12k ve 20k değerli direnç yok.
<!-- SECTION:NOTES:END -->
