---
id: TASK-066
title: 'SW3 enkoderi panel montaja al, karta kablo bağlantısı koy'
status: Done
assignee: []
created_date: '2026-09-23 21:07'
updated_date: '2026-09-24 06:06'
labels:
  - schematic
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/userinterface.kicad_sch
  - design_decisions/output/KART_DIS_HATTI_LCD_20260924.md
  - hardware/datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf
priority: medium
ordinal: 53500
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kullanıcı kararı (24.09.2026, TASK-062): enkoder (SW3, L-KLS4-EC1121S-E5A-F12.5) karta lehimlenmeyecek. Kutunun ön paneline sabitlenecek ve kablolarla karta bağlanacak. Şemada SW3 panel parçası olur (J5/J6 banana gibi, PCB'de footprint yok). Karta A, B, C(GND), S1, S2 (SW, GND) için kablo pedi ya da konnektör gelir. Enkoderin RC filtre/pull-up'ları kartta kalır. Şu an SW3 footprint'i PCB'de geçici olarak sol üst köşede duruyor.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 SW3 şemada panel parçası: Footprint alanı boş, PCB'ye gelmiyor. Karta 5 kablolu bağlantı eklenmiş (pad/konnektör; ref ve footprint seçili)
- [x] #2 Kablo tipi ve uzunluğu (≤ 150 mm varsayım) ile enkoder hatlarının ESD/gürültü önlemi karar dosyasına yazılmış
- [x] #3 ERC 0/0, update_pcb sonrası DRC schematic parity 0; SW3 PCB'den kalkmış
- [x] #4 Konnektör/pedler LCD izdüşümü dışında veya yüksekliği ≤ J3 yüksekliği
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
SW3 panel parcasina donusturulecek; kartta bes ayri kablo icin J9 lehim pedi baglantisi eklenecek. Mevcut enkoder devresi ve pinler netlist ile karsilastirilacak, kablo/ESD/gurultu karari belgelenip sema render, ERC, PCB senkronizasyonu ve schematic parity ile dogrulanacak.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026: SW3 panel parcasi yapildi (Footprint bos, on_board no, in_pos_files no, in_bom yes). PCB'den SW3 kalkti. J9 = Connector_Wire:SolderWire-0.25sqmm_1x05_P4.2mm_D0.65mm_OD1.7mm; 1=A, 2=C/GND, 3=B, 4=S1, 5=S2/GND. Pad 1 (58.00,91.60) mm, -90 derece; LCD sol sinirina footprint boslugu 4.275 mm (0.2 mm toleransla 4.075 mm).
<!-- SECTION:NOTES:END -->
