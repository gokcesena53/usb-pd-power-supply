---
id: TASK-005
title: USER_İNTERFACE.kicad_sch sayfasını kaldır
status: Done
assignee: []
created_date: '2026-09-22 18:45'
updated_date: '2026-09-23 05:12'
labels:
  - schematic
milestone: m-0
dependencies: []
priority: low
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Sayfa yalnızca encoder seçim notlarını tutuyor; şematik içerik yok.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Encoder notları docs/ veya design_decisions/ altına taşındı
- [x] #2 Sayfa hiyerarşiden kaldırıldı, ERC 0 hata
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Sayfadaki tek oge olan arayuz sinyal listesi docs/arayuz-sinyalleri.md'ye tasindi ve guncel pin atamalariyla yazildi (TFT_CS GPIO14, TFT_DC GPIO7 - TASK-041). Sayfa kisch_sheet.remove_sheet ile kaldirildi: USER_İNTERFACE.kicad_sch dosyasi, userinterface.kicad_sch icindeki sayfa sembolu ve gopo.kicad_pro sheets kaydi (uuid 2a78504e-...) birlikte silindi.
Kanit: ERC 0 hata / 0 uyari, 'netlist farki: YOK', sayfa listesi 6 -> 5 (1 kok, USB_C_INPUT, USB_PD_CONTROLLER, MCU, USER INTERFACE).
<!-- SECTION:NOTES:END -->
