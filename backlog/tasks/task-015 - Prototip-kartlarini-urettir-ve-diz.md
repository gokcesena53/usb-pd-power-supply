---
id: TASK-015
title: Prototip kartlarını ürettir ve diz
status: To Do
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-22 19:15'
labels:
  - fabrication
milestone: m-2
dependencies:
  - TASK-014
  - TASK-002
priority: medium
ordinal: 122000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Kartlar teslim alındı
- [ ] #2 Dizgi tamamlandı, ilk enerjide kısa devre yok
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — TASK-065 dizgi devri:
- Çift taraflı SMT: L1/L3, C15/C29 ve ilişkili buck/boost devreleri B.Cu'da.
  Dizgiciyle önce hafif top SMT, sonra bottom yüz yukarı bakarken ağır bottom
  SMT'nin son reflow'u planlanacak; profil/ikinci çevrimde parça tutunması
  doğrulanacak. Ağır parçaların aşağı bakarak yeniden erimesine güvenilmeyecek;
  farklı sırada fikstür/yapıştırıcı veya sonradan lehimleme değerlendirilecek.
- C33 süperkapasitör, J8 Ethernet modül/header ve J4/J9 teller SMT sonrasında
  uygun THT/elle lehimlenecek. C33/modül için reflow uygunluğu varsayılmayacak;
  mekanik destek ve kablo gerilim alma uygulanacak.
- C33'ün top bacak çıkıntısı modelde 1,9 mm, J8'inki 4,4 mm (kart 1,6 mm).
  LCD altında kalırlarsa üstte metal+lehim zarfı ≤1,5 mm olacak şekilde kesilip
  ölçülecek veya pinler LCD izdüşümünün dışında tutulacak. Kesim artıkları
  temizlenecek; elektriksel bağlantı/lehim kalitesi kontrol edilecek.
- LCD arka yüz–PCB üst yüz hedefi 2,35±0,15 mm (min.2,20); J3 kapalı maks.2,15.
  J3 dışındaki toplam top zarf sınırı 1,80 mm. Önce FPC tak/kilitle, sonra
  LCD'yi mesafe elemanlarına sabitle; J3 üzerine montaj yükü bindirme.
- Ayrıntı ve yükseklik listesi:
  `design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`.
  Bu not dizginin yapıldığını veya fiziksel doğrulamanın tamamlandığını göstermez.
<!-- SECTION:NOTES:END -->
