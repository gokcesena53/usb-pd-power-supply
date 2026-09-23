---
id: TASK-001
title: L3 boost bobinini seç
status: Done
assignee: []
created_date: '2026-09-22 18:45'
updated_date: '2026-09-23 04:48'
labels:
  - schematic
  - procurement
milestone: m-0
dependencies: []
references:
  - hardware/docs/output/BOM_OZDISAN_REV_C_20260921.xlsx
priority: high
ordinal: 18000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Şemadaki B82422H1682K000 (1210 çip) Isat ≥3 A şartını karşılamıyor. Özdisan stoğunda 1210 ayağa uyan uygun parça yok; footprint değişikliği gerekebilir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 6.8–10 uH, Isat ≥3 A, düşük DCR bir parça seçildi
- [x] #2 Sembol alanları (MPN, Manufacturer, SelectionNote) ve footprint güncellendi
- [ ] #3 ERC 0 hata
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Gereksinim TPS55340 datasheet'i (SLVSBD4E, denk. 11-16) ile hesaplandi: Vin(min) 3,3 V PPS, Vout 5,02 V, VD 0,45 V, fsw 600 kHz (R47 78k7), V_PRE yuku 0,6 A -> D 0,397, IL(ort) 1,07 A, dalga 0,32 A, tepe 1,24 A. KIND 0,3 icin Lmin 6,78 uH: semadaki 6,8 uH dogru deger, degistirilmedi.
Eski parca B82422H1682K000 (1210): 6,8 uH ama 0,35 A / 570 mOhm - tepe akimin altinda; Özdisan stogu 10 adet.
Secilen: SRI0704-6R8M (Özdisan 587796, 15,05 TL, stok 657): 6,8 uH +-20%, RDC 0,04 ohm max, IDC 3,5 A (tepe akimin 2,8 kati). Footprint 1210 -> Inductor_SMD:L_7.3x7.3_H4.5 (KiCad'de hazir).
Elenenler: FPI0705-100M (10 uH, 0,058 ohm / 3,4 A, 8,28 TL, L1 ile ortak footprint) L degisimi RHP sifirini %32 asagi tasiyip kompanzasyonun yeniden dogrulanmasini gerektirecekti; FPI0504-6R8M (2,7 A, stok 108); SRI0605B-6R8M (0,08 ohm); 74437356068 (5,1 A ama stok 34).
TPS55340 akim limiti 5,25-7,75 A; TI'nin Isat > limit onerisi 12x12 mm bobin isterdi, gorevdeki >=3 A sarti benimsendi.
Kanit: ERC 0 hata / 0 uyari, 'netlist farki: YOK', field_geometry farki bos. Ayrinti design_decisions/output/PARCA_TEDARIK_KARARLARI_20260922.md, kayit CHANGES.TXT REV_C.
<!-- SECTION:NOTES:END -->
