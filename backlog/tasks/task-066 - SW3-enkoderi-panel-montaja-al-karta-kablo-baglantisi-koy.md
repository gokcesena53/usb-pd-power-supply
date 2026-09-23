---
id: TASK-066
title: 'SW3 enkoderi panel montaja al, karta kablo bağlantısı koy'
status: To Do
assignee: []
created_date: '2026-09-23 21:07'
updated_date: '2026-09-23 21:07'
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
ordinal: 148000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kullanıcı kararı (24.09.2026, TASK-062): enkoder (SW3, L-KLS4-EC1121S-E5A-F12.5) karta lehimlenmeyecek. Kutunun ön paneline sabitlenecek ve kablolarla karta bağlanacak. Şemada SW3 panel parçası olur (J5/J6 banana gibi, PCB'de footprint yok). Karta A, B, C(GND), S1, S2 (SW, GND) için kablo pedi ya da konnektör gelir. Enkoderin RC filtre/pull-up'ları kartta kalır. Şu an SW3 footprint'i PCB'de geçici olarak sol üst köşede duruyor.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 SW3 şemada panel parçası: Footprint alanı boş, PCB'ye gelmiyor. Karta 5 kablolu bağlantı eklenmiş (pad/konnektör; ref ve footprint seçili)
- [ ] #2 Kablo tipi ve uzunluğu (≤ 150 mm varsayım) ile enkoder hatlarının ESD/gürültü önlemi karar dosyasına yazılmış
- [ ] #3 ERC 0/0, update_pcb sonrası DRC schematic parity 0; SW3 PCB'den kalkmış
- [ ] #4 Konnektör/pedler LCD izdüşümü dışında veya yüksekliği ≤ J3 yüksekliği
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
