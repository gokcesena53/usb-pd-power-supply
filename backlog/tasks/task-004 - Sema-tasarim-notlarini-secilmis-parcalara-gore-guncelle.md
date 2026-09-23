---
id: TASK-004
title: Şema tasarım notlarını seçilmiş parçalara göre güncelle
status: Done
assignee: []
created_date: '2026-09-22 18:45'
updated_date: '2026-09-23 05:12'
labels:
  - schematic
milestone: m-0
dependencies: []
priority: medium
ordinal: 99000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
usb_pd_controller AOZ1284 bölgesindeki eski not ("Cout: 10V X7R ... >=44uF", "L/D exact MPN and footprints require selection", "L: Isat >=2A") güncel değil: L1 SRI0704-220M, D2 SS2060FL, C15 hibrit + C16 seçildi.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 AOZ1284 notu seçilmiş parçalara göre yeniden yazıldı
- [x] #2 Diğer sayfalardaki notlar tarandı, eskiyenler düzeltildi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
usb_pd_controller (AOZ1284 blogu): COMP notu yeni degerlerle yazildi (Rc=51k, Cc=15n -> fC ~20 kHz, CO ~89 uF); 'L/D exact MPN ... require selection' notu secilen parcalarla degistirildi (L1 FPI0705-220K 22uH/0.11 ohm/2.3 A, D2 SS2060FL 60V/2A, Cout C15 47uF hibrit 35V + C16 47uF X5R 16V); 'Cout: 10V X7R' yanlis dielektrik/gerilim bilgisi kaldirildi; blok basligi 'V_PRE 5..28V INPUT' olarak duzeltildi.
mcu: cerceve disinda kalmis alti eski inceleme sorusu kaldirildi (PORT gosterimi, pin atamasi, bosta kalan pinlere test point, decoupling, programlama yontemi, encoder secimi) - hepsi cozulmus durumda. Blok basligi ESP32-C6-MINI-1-H4 olarak guncellendi (TASK-041).
Diger sayfalar tarandi: usb_c_input (VBUS limit, CC/Rd notlari), userinterface (backlight, TFT, encoder) ve mcu RTC notlari guncel; degisiklik gerekmedi.
Kanit: metin degisikligi; ERC 0 hata / 0 uyari, 'netlist farki: YOK', render ile kontrol edildi. Cok satirli notun capasi en alt satirda oldugu icin bir not 3.81 mm asagi alindi.
<!-- SECTION:NOTES:END -->
