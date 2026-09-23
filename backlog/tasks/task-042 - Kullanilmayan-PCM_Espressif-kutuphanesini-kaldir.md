---
id: TASK-042
title: Kullanılmayan PCM_Espressif kütüphanesini kaldır
status: To Do
assignee: []
created_date: '2026-09-23 05:12'
labels:
  - schematic
milestone: m-1
dependencies:
  - TASK-006
priority: low
ordinal: 111000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
U2 RF_Module:ESP32-C6-MINI-1'e geçti (TASK-041). PCM_Espressif sembol/footprint kütüphanesi yalnız gopo.kicad_pcb'deki eski WROOM footprint'i tarafından kullanılıyor; PCB şemadan güncellendikten sonra kütüphane dosyaları ve sym-lib-table / fp-lib-table kayıtları kaldırılabilir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 PCB güncellemesi sonrası PCM_Espressif'e referans kalmadığı doğrulandı
- [ ] #2 Kütüphane dosyaları ve lib-table kayıtları kaldırıldı, ERC/DRC temiz
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
