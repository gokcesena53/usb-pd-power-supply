---
id: TASK-044
title: J4 klemensi yerine 4 mm banana jak + lehim pedi
status: Done
assignee: []
created_date: '2026-09-23 05:34'
updated_date: '2026-09-23 05:56'
labels:
  - schematic
  - layout
  - procurement
milestone: m-1
dependencies: []
references:
  - hardware/usb_pd_controller.kicad_sch
  - design_decisions/USB_PD_REV_C_tasarim_kararlari_handoff.md
  - 'https://www.motorobit.com/4mm-metal-disi-banana-konnektor-siyah'
  - 'https://www.motorobit.com/4mm-metal-disi-banana-konnektor-kirmizi'
  - design_decisions/output/CIKIS_KONNEKTORU_20260923.md
  - CHANGES.TXT
priority: medium
ordinal: 85000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
J4 (DEGSON DG142R-5.08-02P, OUT_POS/GND) kaldırılacak. Yerine çıkış akım/gerilimine uygun kablo lehim pedleri konacak; kablolar panele mekanik olarak sabitlenen 4 mm banana jaklara gider:
- GND: siyah 4 mm metal dişi banana konnektör — https://www.motorobit.com/4mm-metal-disi-banana-konnektor-siyah
- OUT_POS: kırmızı 4 mm metal dişi banana konnektör — https://www.motorobit.com/4mm-metal-disi-banana-konnektor-kirmizi
Maks. çıkış akımı handoff'ta 5 A varsayıldı.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 J4 DG142R şemadan kaldırıldı; yerine OUT_POS (pin 1) ve GND (pin 2) için 2 pozisyonlu kablo lehim pedi (Conn_01x02) kondu, ERC temiz, netlist değişmedi
- [x] #2 Ped deliği 1.5 mm² (AWG16) kablo için boyutlandırıldı (SolderWire-1.5sqmm, delik 1.7 mm, halka Ø3.9 mm); 3 A maks. çıkışta kablo/ped marjlı
- [x] #3 J5/J6 Motorobit kırmızı/siyah 4 mm banana jaklarına çevrildi (Value, MPN, Datasheet, Description); anma değeri/panel deliği ölçümü TASK-046'ya, PCB güncellemesi TASK-006'ya, OUT_POS/GND bakır boyutu TASK-008'e aktarıldı
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
J4: swap_lib DG142R-5.08-02P-14-00AH → Connector_Generic:Conn_01x02 (ref/uuid korundu), footprint Connector_Wire:SolderWire-1.5sqmm_1x02_P7.8mm_D1.7mm_OD3.9mm. Pin 1 eski konumda; pin 2 2.54 mm telle eski GND ucuna bağlandı.
J5 = Motorobit KOM.KNN.06.000021 (kırmızı, OUT_POS), J6 = KOM.KNN.06.000022 (siyah, GND). Satıcı sayfası anma değeri/ölçü vermiyor (23.09 kontrol) → TASK-046/047. Footprint Cinch panel kesimi olarak kaldı.
Maks. çıkış 3 A (CIKIS_AKIMI_3A_KARARI_20260922); görev açılırken yazılan 5 A handoff varsayımıydı.
Kanıt: verify.py --against 776ce38 netlist → J4.1 OUT_POS, J4.2 GND aynı; ERC 0 hata / 0 uyarı. PCB'de J4 footprint'i henüz eski: F8 ile TASK-006'da gelecek.
<!-- SECTION:NOTES:END -->
