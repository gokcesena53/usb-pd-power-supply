---
id: TASK-009
title: SMBJ30A katot bandı yönünü PCB'de doğrula
status: Done
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-24 07:27'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-006
priority: medium
ordinal: 124000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Şema/footprint tarafı 22.09'da kontrol edildi: pin 1 (D_SMB katot pedi) D3'te USB_VBUS, D7'de OUT_POS'ta.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 D3 katot bandı VBUS tarafında
- [x] #2 D7 katot bandı OUT_POS tarafında
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
KiCad PCB (hardware/gopo.kicad_pcb), sema (hardware/*.kicad_sch) ve sembol tanimlari uzerinde yapilan inceleme ve dogrulama sonuclari:

1. D3 (SMBJ30A - USB_VBUS TVS Diyotu):
- Footprint: Diode_SMD:D_SMB, konum: (at 40.879999 74.25 180)
- Pad 1: (at -2.15 0 180), Net: USB_VBUS
- Pad 2: (at 2.15 0 180), Net: GND
- Silkscreen katot cizgisi: (fp_line (start -3.66 -2.15) (end -3.66 2.15) (layer "F.SilkS")) ile Pad 1 (USB_VBUS) tarafindadir. Katot bandi yonu dogrudur.

2. D7 (SMBJ30A - OUT_POS TVS Diyotu):
- Footprint: Diode_SMD:D_SMB, konum: (at 151.904288 57.67 0)
- Pad 1: (at -2.15 0), Net: OUT_POS
- Pad 2: (at 2.15 0), Net: GND
- Silkscreen katot cizgisi: (fp_line (start -3.66 -2.15) (end -3.66 2.15) (layer "F.SilkS")) ile Pad 1 (OUT_POS) tarafindadir. Katot bandi yonu dogrudur.

3. Sema ve Sembol Uyumu:
- Power_Path_Custom:SMBJ30A sembolunde Pin 1 (A1) katot barina, Pin 2 (A2) anot ucuna baglidir.
- kicad-cli pcb drc --schematic-parity kontrolunde 0 schematic parity hatasi dogrulanmistir.

4. Karar Degisikligi:
- Mevcut sema ve PCB yerlesimi gereksinimi tam karsilamaktadir; tasarim/karar degisikligi olmadigindan CHANGES.TXT veya design_decisions guncellemesi gerekmemistir.
<!-- SECTION:NOTES:END -->
