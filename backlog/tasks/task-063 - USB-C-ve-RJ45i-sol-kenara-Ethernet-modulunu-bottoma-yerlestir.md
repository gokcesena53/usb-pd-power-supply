---
id: TASK-063
title: 'USB-C ve RJ45''i sol kenara, Ethernet modülünü bottom''a yerleştir'
status: To Do
assignee: []
created_date: '2026-09-23 20:33'
updated_date: '2026-09-23 20:34'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-062
references:
  - hardware/gopo.kicad_pcb
  - design_decisions/output/ETHERNET_MODULU_ANALIZI_20260923.md
priority: high
ordinal: 103000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
J1 (USB-C) ve J8'in RJ45'i kartın sol kenarında, kutunun sol paneline açılacak. J8 (Waveshare 2-CH UART TO ETH) kartın bottom tarafına lehimlenir; RJ45 kart kenarından 4,3 mm dışarı taşar (TASK-054).

Dikkat: J8 bottom'da olunca 2x8 header pinleri kartın top tarafına ~4,4 mm çıkar (pin 6,0 mm - 1,6 mm kart). Bu çıkıntı LCD modülünün altına denk gelirse LCD'ye çarpar; header ya LCD izdüşümü dışına alınmalı ya da pinler montajda kesilmeli (kesme payı Implementation Notes'a).

ESP32-C6 anteni karşı (sağ) kenarda kalmalı; RJ45/kablo ile anten mesafesi TASK-054 AC#1'e girdi olur.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J1 ve J8 RJ45 ağzı sol Edge.Cuts kenarında; J1 ağzı kenarla hizalı (üretici önerisi ±0,1 mm), RJ45 kenardan 4,3 mm taşıyor
- [ ] #2 J8 B.Cu tarafında (footprint flip), 3D görünümde modül kartın altında
- [ ] #3 J8 header pinlerinin top tarafındaki çıkıntısı LCD modül izdüşümüyle çakışmıyor veya pin kesme yüksekliği (≤ J3 yüksekliği) karara bağlanmış
- [ ] #4 J1 ve J8 arası mesafe iki kabloyu aynı anda takmaya izin veriyor (fiş gövdeleri arası ≥ 2 mm)
- [ ] #5 Sol panel kesit ölçüleri (USB-C ve RJ45 merkezleri, kart üst yüzeyine göre z) design_decisions/ altına yazılmış
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
