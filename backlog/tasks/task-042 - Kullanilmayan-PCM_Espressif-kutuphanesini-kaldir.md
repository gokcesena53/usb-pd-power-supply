---
id: TASK-042
title: Kullanılmayan PCM_Espressif kütüphanesini kaldır
status: Done
assignee: []
created_date: '2026-09-23 05:12'
updated_date: '2026-09-24 06:11'
labels:
  - schematic
milestone: m-1
dependencies:
  - TASK-006
priority: low
ordinal: 113000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
U2 RF_Module:ESP32-C6-MINI-1'e geçti (TASK-041). PCM_Espressif sembol/footprint kütüphanesi yalnız gopo.kicad_pcb'deki eski WROOM footprint'i tarafından kullanılıyor; PCB şemadan güncellendikten sonra kütüphane dosyaları ve sym-lib-table / fp-lib-table kayıtları kaldırılabilir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 PCB güncellemesi sonrası PCM_Espressif'e referans kalmadığı doğrulandı
- [x] #2 Kütüphane dosyaları ve lib-table kayıtları kaldırıldı, ERC/DRC temiz
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Aktif sema/PCB ve kutuphane bagimliliklarini tara; kullanilmayan PCM_Espressif sembol/footprint dosyalarini ve iki lib-table kaydini kaldir. Once/sonra ERC, DRC schematic parity, netlist ve tasarim dosyasi hashlerini karsilastir; kanit ve CHANGES.TXT kaydini ekle.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026: U2 sema ve PCB'de RF_Module:ESP32-C6-MINI-1 kullaniyor. PCM_Espressif.kicad_sym ve PCM_Espressif.pretty/ESP32-C6-WROOM-1.kicad_mod ile sym-lib-table/fp-lib-table kayitlari kaldirildi. Aktif 25 tasarim/kutuphane dosyasinda PCM_Espressif referansi 0. Tarihsel rapor/yedekler arsiv olarak korundu.
<!-- SECTION:NOTES:END -->
