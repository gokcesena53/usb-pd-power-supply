---
id: TASK-002
title: Özdisan'da stokta olmayan parçalar için tedarik/muadil kararı ver
status: Done
assignee: []
created_date: '2026-09-22 18:45'
updated_date: '2026-09-22 20:26'
labels:
  - procurement
  - schematic
milestone: m-1
dependencies: []
references:
  - hardware/docs/output/BOM_OZDISAN_REV_C_20260921.xlsx
priority: medium
ordinal: 36000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
U1 AP33772S, U2 ESP32-C6, L1 SRI0704-220M Özdisan'da stokta değil.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 U1 için tedarik kaynağı veya muadil belirlendi
- [x] #2 U2 için tedarik kaynağı veya muadil belirlendi
- [x] #3 L1 için tedarik kaynağı veya muadil belirlendi
- [x] #4 Karar SelectionNote alanlarına işlendi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
L1: SRI0704-220M stokta yok. Özdisan 'Sabit İndüktörler' (468) 22 uH taramasi (35 sonuc) datasheet'lerle karsilastirildi; secilen FPI0705-220K (Özdisan 507505, 8,28 TL, stok 3467): 22 uH +-10%, RDC 0,11 ohm max (tasarimdakiyle ayni), IDC 2,3 A (1,95 A idi), govde 7,8x7,0x5,0 mm. 3,3 V rayinda tepe akim ~0,83 A -> 2,8x marj. Reddedilenler: TPY0705-220M (mevcut footprint'e uyuyor ama 0,35 ohm), SRI0704-330M (ayni ayak, 0,25 ohm / 1,2 A), FPI1005-220M (0,07 ohm / 3,4 A ama 10x9 mm), IHLP2525CZER220M11 (62 TL). Yeni footprint cizildi: Inductor_Custom:L_CoreMaster_FPI0705_7.8x7.0mm_H5.0 (land 7,5x3,25 mm iki ped, 2,0 mm bosluk; spec DWG MY0212071), fp-lib-table'a eklendi, render ile kontrol edildi.
U1 AP33772S ve U2 ESP32-C6-WROOM-1: Özdisan'da yok, karsilayan muadil de yok (ESP32-C3-MINI-1-N4 GPIO sayisi yetmiyor; ESP32-WROOM-32E-N4 native USB yok). Karar: Mouser/DigiKey katalogundan alinacak.
Kanit: alan guncellemesi sonrasi ERC 0 hata / 0 uyari, 'netlist farki: YOK', field_geometry farki bos. Kararlar L1/U1/U2 SelectionNote alanlarina islendi; ayrinti design_decisions/output/PARCA_TEDARIK_KARARLARI_20260922.md, kayit CHANGES.TXT REV_C.
<!-- SECTION:NOTES:END -->
