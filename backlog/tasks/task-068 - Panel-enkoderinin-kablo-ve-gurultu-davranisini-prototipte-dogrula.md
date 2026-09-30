---
id: TASK-068
title: Panel enkoderinin kablo ve gurultu davranisini prototipte dogrula
status: Blocked
assignee: []
created_date: '2026-09-24 06:02'
labels:
  - bring-up
  - sample-eval
  - firmware
milestone: m-2
dependencies:
  - TASK-066
  - TASK-015
references:
  - design_decisions/output/ENCODER_PANEL_TASK066_20260924.md
priority: medium
ordinal: 150000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-066 ile SW3 panel parcasi ve J9 besli lehim pedi oldu. Mevcut devrede R34-R36 10k pull-up bulunuyor; RC/harici TVS yok. <=150 mm ic kablo, yalitkan dugme, kablo sabitleme ve yazilim debounce varsayimlarini bitmis kutu/prototipte dogrula. Prototip (TASK-015) bekleniyor; bu gorev ESD dayanim iddiasi degildir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J9 1-A, 2-C/GND, 3-B, 4-S1, 5-S2/GND surekliligi ve kablo uzunlugu <=150 mm olculdu; lehim ve gerilim alma sabitlemesi fotografla kaydedildi.
- [ ] #2 Her yonde 100 detent ve 100 basmada analizor AB kaydi ile firmware olaylari karsilastirildi; yon hatasi ve fazladan/kayip basma olayi yok.
- [ ] #3 Buck/boost ve cikis yuk gecisleri altinda 10 dakika beklemede sahte enkoder/buton olayi veya MCU reseti yok; ham GPIO ve besleme olcumleri raporlandi.
- [ ] #4 Son kutunun erisilebilir yuzeyleri icin ESD test seviyesi/yontemi tanimlandi ve test edildi; reset, kalici hasar ve sahte olay sonucu kaydedildi. Basarisizlikta J9 girisinde RC/TVS karari semaya geri beslendi.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
