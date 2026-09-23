---
id: TASK-006
title: PCB'yi şemadan güncelle
status: Done
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-23 15:18'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-001
modified_files:
  - hardware/gopo.kicad_pcb
  - CHANGES.TXT
  - .claude/skills/kicad-schematic/scripts/update_pcb.py
  - .claude/skills/kicad-schematic/SKILL.md
priority: high
ordinal: 112000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
KiCad: Tools > Update PCB from Schematic. Kart erken aşamada (7 segment, 0 via, 0 zone).

Yeni: Y1 (ABS25), C33 (Korchip DCL H-tipi), Q5 (SQJB60EP, hiç yerleştirilmemişti), Q7, R60, C34, U13 (SOT-23-5), R61, C35, R62, R63, D8/D9 (SOD-123F, DNP).

Kalkan: BT1, R22, R23, C10, U7, U8, L2, C20, C21, C22, R44, R45, R46, R25, R26, R57, #PWR023; Q4 (Q3 ile tek çift kılıfa birleşti).

Footprint değişen: U2 RF_Module:ESP32-C6-MINI-1 (WROOM-1 18x25.5 -> MINI-1 13.2x16.6; anten keepout yeniden konumlanmalı, TFT_CS/TFT_DC pinleri değişti), Q3 Package_SO_Custom:Vishay_PowerPAK_SO-8L_Dual (PCB'de hâlâ SOIC-8 / IRF7855TRPBF), U12 WSON-12 3x3 (LM74801; EP boşta, GND'ye BAĞLANMAZ), U10 SOT-23-6 (USBLC6-2SC6), U4 SOIC-8, J3 KLS 30p FPC, L1 Inductor_Custom:L_CoreMaster_FPI0705_7.8x7.0mm_H5.0, L3 Inductor_SMD:L_7.3x7.3_H4.5 (1210'du), C5 0805, C8 1210, C15/C29 CP_Elec_6.3x5.8, C31 0603, R59 0805.

Yer değişen (şemada): R10, R15, R37, TP9, SW1 U2'nin soluna alındı (MINI-1'de IO8/IO9 sol kenarda).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Yeni bileşenlerin hepsi PCB'de
- [x] #2 Kalkan bileşenler PCB'den silindi
- [x] #3 Footprint değişiklikleri uygulandı; U12 EP GND'ye bağlı değil
- [x] #4 J4 SolderWire-1.5sqmm footprint'i ve yeni R64/R65 PCB'ye geldi; R8/R9 değerleri güncellendi (TASK-043/044)
- [x] #5 PCB ile şema netlist'i uyumlu (Update PCB değişiklik önermiyor); tek istisna footprint'i TBD olan J8 (TASK-052 numunesi, TASK-054)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026, commit 1792ccb. kicad-cli'da Update PCB yok; headless eşdeğeri .claude/skills/kicad-schematic/scripts/update_pcb.py yazıldı (footprint'ler referansla eşlenir, çünkü TASK-048 sayfa taşıması UUID yolunu değiştirdi).

Deponun son haline göre (TASK-041..060 dahil) uygulanan: 54 footprint eklendi (kart dışında, sağda ızgaraya dizili; yerleşim TASK-008), 15 kaldırıldı (BT1, C22, J2, L2, R22, R23, R25, R26, R42, R44, R45, R46, U7, U8, U9), 20 footprint değişti (U2 WROOM-1 -> ESP32-C6-MINI-1, Q3 PowerPAK SO-8L Dual, Q4 SOIC-8 -> SOT-23 BSS138P, U10 SOT-23-6, U4 SOIC-8, J3 KLS FPC, J4 SolderWire-1.5sqmm, L1 FPI0705, D3 SMB, C3/C5/C10 0805, C8/C12/C13/C16 1210, C15 CP_Elec_6.3x5.8, R11/R43/RShunt1 2512). Değişen footprint'ler eski konum/yön/katmanda. Tüm sembol alanları footprint'lere aktarıldı (gizli, Fab).

İzler: eski WROOM-1 USB D+/D- ve BT1 pad'lerine giden 7 segment silindi. İkisi MINI-1'de yanlış pad'e denk geliyordu (D- -> IO13).

Kanıt: kicad-cli pcb drc --schematic-parity: önce 416 parity sorunu (182 net_conflict, 84 field mismatch, 80 fp mismatch, 55 missing, 15 extra), sonra 1 (J8 missing_footprint, Value TBD). update_pcb.py --dry-run yalnız 'ATLA J8' raporluyor. Pad kontrolü: U12 pad13 (EP) = unconnected-(U12-RTN-Pad13), GND değil; U6 1=Net-(U6-REF) 2=EN_CTRL 3=GND; D5 SOD-323 1=EN_CTRL 2=BOOST_FB; J4 1=OUT_POS 2=GND; R64 2k0, R65 10k, R8/R9 10k (şemayla aynı).

Kalan DRC (350): yerleşim yapılmadığı için courtyard/silk/short/clearance, önceden var olan text_height/thickness ve açık Edge.Cuts (invalid_outline). Yeni: U11 HTSSOP-14 ThermalVias footprint'inin 0.2 mm delikleri kuraldaki 0.3 mm minimumun altında (15x drill_out_of_range), TASK-010'a not düşüldü.
<!-- SECTION:NOTES:END -->

## Comments

<!-- COMMENTS:BEGIN -->
author: claude
created: 2026-09-23 11:34
---
23.09.2026 (TASK-049): yeni parçalar Q4, Q6 (BSS138P SOT-23), D10 (SOD-123), R66 (0603), R67 (2512, 2 W: dış kaynak durumunda sürekli ~0.9 W, bakır alanıyla soğutulmalı). R59 footprint 0805 -> 0603. Q1/Q2/R4-R7 şemada mcu sayfasına taşındı (TASK-048); PCB'de sheet path değişir, footprint eşleşmesi referansla korunur.
---
<!-- COMMENTS:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
PCB şemanın son haline göre güncellendi (commit 1792ccb): 54 ekle / 15 sil / 20 footprint değişimi, alanlar ve netler eşit. DRC schematic parity 416 -> 1; kalan tek sorun footprint'i TBD olan J8 (TASK-054). Yeni footprint'ler kart dışında dizili; yerleşim TASK-008. Headless güncelleme aracı: .claude/skills/kicad-schematic/scripts/update_pcb.py.
<!-- SECTION:FINAL_SUMMARY:END -->
