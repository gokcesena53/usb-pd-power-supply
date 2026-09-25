---
id: TASK-092
title: Kalan komponentlerin kart ici yerlesimini tamamla
status: To Do
assignee: []
created_date: '2026-09-25 07:34'
updated_date: '2026-09-25 08:10'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-091
  - TASK-085
  - TASK-093
references:
  - hardware/gopo.kicad_pcb
  - >-
    design_decisions/output/GRUP_DEVIR_VE_KONSOLIDE_DOGRULAMA_TASK085_20260925.md
  - design_decisions/output/KABA_ALAN_PLANI_TASK086_20260925.md
  - design_decisions/output/ETHERNET_ALTI_ALAN_ANALIZI_20260925.md
  - design_decisions/output/PORT_HIZASI_ENKODER_DUZELTME_20260925.md
priority: high
ordinal: 174000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-091 ile Ethernet USB-C altına alındıktan sonra kalan komponentleri mevcut kart sınırları içinde nihai konumlarına yerleştir. TASK-085 grup envanteri ve TASK-086 kaba planını yeni port konumuna göre güncelle. USB-C/PD çevresi, TPS55340 boost, AOZ1284 buck, LM74801 çıkış anahtarı, INA226/şönt/J4, aktif deşarj, MCU çevresi, RTC, I2C seviye dönüştürücü, TFT/backlight, enkoder çevresi ve test noktalarını kapsa. Grup içi ilişkileri koruyup grup sınırlarında gerekli düzeltmeleri yap. Bu görev fiziksel yerleşim uygulamasıdır; TASK-008 kritik elektriksel yerleşim, akım/termal bütçe ve güzergâh kabulünün takip kaydı olarak kalır. Genel routing TASK-087 kapsamındadır.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Güncel envanterdeki her ref x/y/açı/yüz ve grup bilgisiyle kayıtlı; geçici olarak kart dışında bekleyen komponent kalmamış, kasıtlı anten/port taşmaları ayrı belirtilmiş.
- [ ] #2 TASK-091 port ankrajları, J3/FPC, H1-H4, LCD yükseklik limitleri, J9 kablo alanı ve U2 anten boşluğu korunmuş; top/bottom ve 3D incelemede açıklanmamış mekanik çakışma yok.
- [ ] #3 Buck/boost B.Cu üzerinde anten/MCU bölgesinden uzak; çıkış anahtarı-şönt-INA226-J4 akışı, dekuplaj ve FB/COMP/Kelvin sessiz alanları korunmuş. Güç/GND, USB/CC, I2C/SPI/UART ve termal via koridorları gösterilmiş.
- [ ] #4 Ethernet altındaki her parça TASK-080 XY/Z/keepout haritasına göre ref ve maksimum yükseklik/açıklık ile doğrulanmış; BOOT/RESET, test noktaları, montaj ve lehim erişimi korunmuş.
- [ ] #5 Önce/sonra görünüm ve DRC farkı kaydedilmiş; schematic parity 0, yeni açıklanmamış clearance/short/courtyard ihlali 0; grup üyelikleri ve yerel izler korunmuş, D5-U11 FB kesintisiz ve en fazla 10 mm.
- [ ] #6 Yerleşim tablosu, güncel alan planı, kritik güzergâhlar ve çözülmemiş kısıtlar TASK-008 incelemesine devredilmiş; bağlantısız öğeler routing işi olarak ayrıca raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 — Ethernet altını aktif kullanma isteği TASK-093 ile uygulanacak. Güncel sıra TASK-091 → TASK-093 → TASK-092 → TASK-008 → TASK-087. TASK-093 yerleştirilmiş refleri, ayrılan routing/servis hacmini ve yükseklik varsayımlarını devreder; kalan komponentler bu yerleşim etrafında tamamlanır.

Son ankraj duzeltmesi: J7=(53.975,88.5,-90,F.Cu), J8=(102.5,79.61,0,B.Cu), J9=(58,104,-90,F.Cu). Portlar ayni Y=88.5 merkezinde. Ethernet orta brut seridi X=69.85..98.69 Y=77.5..99.5; eski Y=99.89..121.89 haritasi gecersiz. Son karar PORT_HIZASI_ENKODER_DUZELTME_20260925.md; USB delik/ayak izdususunu da dikkate al.
<!-- SECTION:NOTES:END -->
