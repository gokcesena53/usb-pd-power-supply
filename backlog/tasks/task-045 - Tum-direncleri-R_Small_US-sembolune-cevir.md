---
id: TASK-045
title: Tüm dirençleri R_Small_US sembolüne çevir
status: Done
assignee: []
created_date: '2026-09-23 05:34'
updated_date: '2026-09-23 05:56'
labels:
  - schematic
milestone: m-1
dependencies: []
references:
  - CHANGES.TXT
priority: low
ordinal: 104000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Şema kuralı: tüm dirençler Device:R_Small_US gösterimiyle çizilecek. Şu an Device:R kullananlar: mcu.kicad_sch (8), usb_pd_controller.kicad_sch (13). Değer, footprint ve BOM alanları korunmalı.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 grep ile şemada lib_id "Device:R" (R_Small_US dışı direnç sembolü) sayısı 0
- [x] #2 Değişimden önce/sonra netlist karşılaştırması aynı (bağlantı değişmedi), ERC yeni hata vermiyor
- [x] #3 Değer/footprint/MPN alanları korunmuş; yeni sembollerde üst üste binen metin yok
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
mcu (8: R1, R2, R3, R10, R15, R16, R24, R37) ve usb_pd_controller (13: R4, R5, R6, R7, R8, R9, R11, R12, R13, R14, R21, R27, RShunt1) swap_lib ile Device:R_Small_US'e çevrildi; ref/uuid/alanlar korundu. Device:R pinleri ±3.81, R_Small_US ±2.54 → her uca 1.27 mm tel eklendi. R8/R9 TASK-043 kapsamında yeniden yerleştirildi. Kullanılmayan Device:R önbellekten silindi.
Kanıt: grep -c 'lib_id "Device:R"' *.kicad_sch → tüm sayfalarda 0. verify.py --against 776ce38 netlist: ERC 0 hata / 0 uyarı; bağlantı farkı yalnız TASK-043 netleri. readability.py bulgu 12 → 10 (yeni bulgu yok; R8.Value ve R13.Value üst üste binmesi kalktı). Değer/footprint/MPN değişmedi (swap_lib alanlara dokunmaz). Render ile p3 R8/R9, RShunt1 ve p4 MCU dirençleri kontrol edildi.
<!-- SECTION:NOTES:END -->
