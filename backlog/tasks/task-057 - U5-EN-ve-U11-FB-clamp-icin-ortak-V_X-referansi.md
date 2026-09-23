---
id: TASK-057
title: U5 EN ve U11 FB clamp için ortak V_X referansı
status: Done
assignee: []
created_date: '2026-09-23 12:53'
updated_date: '2026-09-23 12:53'
labels:
  - schematic
  - procurement
milestone: m-0
dependencies: []
references:
  - design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md
  - design_decisions/reports/fb-clamp-20260923/fb_clamp.cir
  - design_decisions/reports/fb-clamp-20260923/fb_clamp_tlv431.cir
documentation:
  - hardware/datasheets/TLV431x_Rev10-2025.pdf
  - hardware/datasheets/BAS16HT1G.pdf
  - hardware/datasheets/TPS55340.pdf
  - hardware/datasheets/AOZ1284.pdf
modified_files:
  - hardware/usb_pd_controller.kicad_sch
  - hardware/libraries/Power_Path_Custom.kicad_sym
  - design_decisions/USB_PD_REV_C_tasarim_kararlari_handoff.md
  - CHANGES.TXT
ordinal: 108000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
EN_CTRL (U5 EN) ve U11 FB clamp referansı tek bir TLV431 düğümünde birleştirildi (V_X = 1.605 V). Böylece FB clamp'in +3.3V'a bağımlılığı kalktı. Worst-case analizi 0…60 °C ve V_PRE 4.3…34 V için yapıldı.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 U6 = TLV431BQDBZT, sembol Power_Path_Custom:TLV431xDBZ (1=REF, 2=K, 3=A)
- [x] #2 D5 = BAS16HT1G: anot BOOST_FB, katot EN_CTRL
- [x] #3 R43 4k7 2512, R50 2k87 (EN_CTRL→REF), R51 9k76 (REF→GND), R42 kaldırıldı
- [x] #4 Worst-case FB ≤2.40 V @34 V (abs 3 V), EN 1.566…1.652 V (1.2…5 V aralığında)
- [x] #5 ERC 0/0; netlist farkı yalnız EN_CTRL, U6-REF, V_CL, +3.3V/GND'den R50/R42
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanıt (verify.py --against, değişiklik öncesi netlist): ERC 0 ihlal (0 hata, 0 uyarı), 111 net.
Netlist farkı yalnızca beklenen netlerde:
- EN_CTRL = D5.1 (K), R43.2, R50.1, U5.8 (EN), U6.2 (K)
- yeni Net-(U6-REF) = R50.2, R51.1, U6.1 (REF)
- V_CL kalktı; +3.3V'tan R50.1, GND'den R42.2 çıktı

readability: 5 bulgu, değişiklik öncesiyle aynı (R21/R38/TH1/PD_VOUT, bu blokta değil). Bölgede lint boş. Render kontrol edildi; U6'nın metni R51 GND'sinden uzağa, U6'nın altına alındı.

Worst-case analizinin tamamı design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md dosyasında.

Commit henüz yapılmadı.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
verify.py --against (değişiklik öncesi netlist): ERC 0 ihlal (0 hata, 0 uyarı), 111 net. Fark yalnızca beklenen netlerde: EN_CTRL = D5.1, R43.2, R50.1, U5.8, U6.2; yeni Net-(U6-REF) = R50.2, R51.1, U6.1; V_CL kalktı; +3.3V'tan R50.1, GND'den R42.2 çıktı. readability bulgusu değişmedi (5, hepsi önceden vardı), bölgede lint boş, render kontrol edildi. Parçalar Özdisan'da (23.09.2026): TLV431BQDBZT 1587549 (stok 1134), BAS16HT1G 344295 (stok 6290), CQ121WF4701T4E 605074, 0402WGF2871TCE 506262, 0402WGF9761TCE 506310. Değişiklik henüz commit edilmedi.
<!-- SECTION:FINAL_SUMMARY:END -->
