---
id: TASK-069
title: Grup ici yerlesim icin uretici kurallarini ve ankrajlari derle
status: Done
assignee: []
created_date: '2026-09-24 07:37'
updated_date: '2026-09-24 13:41'
labels:
  - layout
  - docs
milestone: m-1
dependencies:
  - TASK-067
  - TASK-066
references:
  - hardware/gopo.kicad_pcb
  - hardware/gopo.kicad_sch
  - design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
  - >-
    design_decisions/output/URETICI_YERLESIM_KURALLARI_VE_ANKRAJLARI_TASK069_20260924.md
  - hardware/docs/reports/task-069-20260924/inventory.json
  - hardware/docs/reports/task-069-20260924/verify.py
priority: high
ordinal: 151000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB üzerindeki 15 grubun güncel üye/pad/net envanterini çıkar; üreticinin datasheet, layout guideline ve varsa evaluation-board yerleşiminden uygulanacak kuralları ref/pin bazında derle. Kaynak sayfa/şekil/revizyonlarını kaydet; üretici şartı ile proje tercihlerini ayır. Bu aşama grup içi göreli yerleşim hazırlığıdır. Kart dışındaki gruplar burada hazırlanabilir; kart içine son taşıma TASK-063/TASK-065/TASK-008 kapsamıyla koordine edilir. J3/FPC ve H1-H4 ankrajları korunur. J9 eski koordinatı sabit değildir; TASK-063/083 ile Ethernet yanında son konumu ve kablo alanı belirlenir. Eksik resmi kaynakları temin et; bulunamayan kuralları üretici önerisi gibi sunma.

Yeni yüz hedefleri J7/U2 F.Cu, J8 B.Cu; U2 anteni PCB dışında, USB-C'ye RF/mekanik koşulları sağlayan yakınlıkta. TASK-065 eski USB-C/MCU bottom atamaları tarihsel başlangıçtır. Slot tanımı TASK-083'te çözülür. Ayrıntılı güncel öncelikler: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 15 grubun tüm footprint üyeleri ve grup dışındaki J3/J9/H1-H4 ankrajları güncel PCB ile eşleştirilmiş; eski J1 yerine güncel USB-C J7, panel SW3 yerine J9 kullanılmış.
- [x] #2 Her grup için üretici kaynağı, revizyon, sayfa/şekil, kritik pin ilişkisi, yerleşim kuralı ve doğrulama yöntemi design_decisions altında tek tabloda; üreticinin sayısal limit vermediği yerde proje hedefi ayrı işaretli.
- [x] #3 J3 kilidi/FPC zarfı, J9 kablo alanı, anten keepout, J8 bottom/sol kenar ve TASK-065 yükseklik/yüz kısıtları listelenmiş; yüz kararı kesinleşmemiş gruplar açıkça belirtilmiş.
- [x] #4 USB-C–PD/C3, U11/D5–U6/V_X, LM74801–INA226/J4, J3–backlight, MCU–I2C/Ethernet/enkoder ve TP bağlantı yönleri için komşuluk tablosu hazırlanmış.
- [x] #5 Başlangıç grup üyeliği, x/y/açı/yüz/kilit, mevcut izler ve DRC/parity çıktısı kaydedilmiş; TASK-058 D5–U11 FB izi envantere alınmış. Tamamlanmamış routing nedeniyle bağlantısız öğeler sıfır şartı konmamış.
- [x] #6 Kaynak/ankraj tablosunda tarihsel yüzler ile hedef yüzler ayrı; J7/U2 top ve J8 bottom, J9 taşınabilir ankraj, LCD dışı uzun parçalar ve buck/boost–MCU bölge ayrımı açık.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — TASK-065 tamamlandı: buck/boost, RTC, USB-C, Ethernet,
INA226/panel çıkışı, AP33772S ve ESP32 blokları B.Cu; backlight/J3 F.Cu.
Bu yüz atamalarını başlangıç olarak koru. D5.2–U11.9 FB izi B.Cu'da
2,584607 mm; sonraki taşımalarda birlikte taşı. C33/J8 karşı yüz pinleri,
J9 proje model ataması ve top 1,80 mm bütçe için
`design_decisions/output/LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md` esas alınmalı.

24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir.

24.09.2026 — TASK-069 tamamlandı:
- 15 PCB grubunun (137 footprint) ve 6 mekanik ankrajın (H1-H4, J3, J9, toplam 143 footprint) üretici yerleşim kılavuzları, pin ilişkileri, mekanik ankrajları ve bloklar arası komşuluk/koridor haritası eksiksiz derlendi.
- Üretici veri sayfaları (TI, Diodes Inc, AOS, Espressif, NXP, Microchip, Korchip, Taiwan Semi, Waveshare vb.) incelenerek üretici şartları ile proje mühendislik tercihleri tek tabloda netleştirildi.
- Mekanik sınırlar ve keepout'lar tanımlandı: J3 FPC kilitli ankrajı (98.0, 109.3), J9 enkoder kablo/lehim alanı, U2 ESP32 anteni 15 mm keepout'u, J8 RJ45 THT lehim çıkıntısı (~2.2 mm) altındaki anakart B.Cu MUTLAK KEEPOUT'u ve TASK-065 LCD altı top bileşen zarfı <= 1.80 mm kuralı kayda geçirildi.
- 15 blok arası güç/sinyal komşuluk ve arayüz koridorları matrisi hazırlandı. Tarihsel yüzler ile hedef yüzler (J7/U2 top, J8/buck/boost bottom) ayrıştırıldı.
- Başlangıç envanteri ve TASK-058 D5.2-U11.9 FB izi (4 segment, 2.5846 mm) doğrulandı; DRC 145/145, unconnected 360/360, parity 0 teyit edildi.
- Karar ve Kanıt: design_decisions/output/URETICI_YERLESIM_KURALLARI_VE_ANKRAJLARI_TASK069_20260924.md, hardware/docs/reports/task-069-20260924/inventory.json, verify.py.
<!-- SECTION:NOTES:END -->
