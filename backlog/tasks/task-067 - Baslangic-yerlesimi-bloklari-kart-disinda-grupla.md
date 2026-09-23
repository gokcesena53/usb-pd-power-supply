---
id: TASK-067
title: 'Baslangic yerlesimi: bloklari kart disinda grupla'
status: Done
assignee: []
created_date: '2026-09-23 21:35'
updated_date: '2026-09-23 21:37'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-062
references:
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 149000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Layout başlangıcı. Footprint'ler şemadaki blok çerçevelerine göre board shape dışında gruplanır (her blok bir PCB grubu + Cmts.User başlık). Kart içinde yalnız J3 (LCD FPC konnektörü) ve H1-H4 kalır; J3 kilitlenir. J3'ün kesin konumu TASK-064'te belirlenecek.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Her footprint şemadaki bloğuyla aynı PCB grubunda; grup adı blok başlığı (15 grup)
- [x] #2 J3 ve H1-H4 dışında hiçbir courtyard Edge.Cuts dikdörtgeniyle kesişmiyor
- [x] #3 J3 board shape içinde ve locked
- [x] #4 DRC courtyards_overlap 0, schematic parity 0
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 - pcbnew betiğiyle uygulandı (yalnız konum/grup/kilit; side ve açı korunmuş, iz yoktu).

Blok ataması: şema sayfalarındaki üst düzey rectangle + içindeki en üst başlık metni; sembol hangi çerçevedeyse o blok. usb_c_input çerçevesiz → "USB-C GIRIS". J5/J6 panel jakı, PCB'de yok.

Kenar dağılımı (kart kenarından 5 mm, bloklar arası 4 mm):
- Sol: USB-C GIRIS, TFT BACKLIGHT, TFT CONNECTOR J3 (C34), ROTARY ENCODER
- Üst: TPS55340, AOZ1284, LM74801, INA226, CIKIS DESARJI
- Sağ: ESP32-C6 | 2. sütun: RTC, I2C seviye dönüştürücü, TEST NOKTALARI
- Alt: AP33772S, ETHERNET MEZANIN

J3: (113,29; 105,02) rot 90, kart içinde, locked. Kesin konum TASK-064.

DRC (kicad-cli pcb drc --schematic-parity), HEAD -> sonra:
- courtyards_overlap 64 -> 0; silk_over_copper 55 -> 4 (C33/SW3/D10 kendi içinde); shorting_items 29 -> 0; items_not_allowed 30 -> 0; clearance 11 -> 0
- parity 0 -> 0
- Değişmeyen: text_thickness/height 63, drill_out_of_range 15, J7 hole_clearance 4

Commit: a23a401. Tasarım kararı değişmedi (geçici yerleşim), design_decisions/ ve CHANGES.TXT güncellemesi gerekmedi.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Footprint'ler şemadaki 15 bloğa göre PCB grupları halinde kart dışına, dört kenara dağıtıldı; kart içinde yalnız J3 (kilitli) ve H1-H4 kaldı. DRC courtyards_overlap 64 -> 0, parity 0. Commit a23a401. J3'ün kesin konumu TASK-064'te.
<!-- SECTION:FINAL_SUMMARY:END -->
