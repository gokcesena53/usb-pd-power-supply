---
id: TASK-092
title: Kalan komponentlerin kart ici yerlesimini tamamla
status: Done
assignee: []
created_date: '2026-09-25 07:34'
updated_date: '2026-09-25 14:55'
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
    design_decisions/output/KALAN_KOMPONENTLER_YERLESIM_TASK092_20260925.md
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
- [x] #1 Güncel envanterdeki her ref x/y/açı/yüz ve grup bilgisiyle kayıtlı; geçici olarak kart dışında bekleyen komponent kalmamış, kasıtlı anten/port taşmaları ayrı belirtilmiş.
- [x] #2 TASK-091 port ankrajları, J3/FPC, H1-H4, LCD yükseklik limitleri, J9 kablo alanı ve U2 anten boşluğu korunmuş; top/bottom ve 3D incelemede açıklanmamış mekanik çakışma yok.
- [x] #3 Buck/boost B.Cu üzerinde anten/MCU bölgesinden uzak; çıkış anahtarı-şönt-INA226-J4 akışı, dekuplaj ve FB/COMP/Kelvin sessiz alanları korunmuş. Güç/GND, USB/CC, I2C/SPI/UART ve termal via koridorları gösterilmiş.
- [x] #4 Ethernet altındaki her parça TASK-080 XY/Z/keepout haritasına göre ref ve maksimum yükseklik/açıklık ile doğrulanmış; BOOT/RESET, test noktaları, montaj ve lehim erişimi korunmuş.
- [x] #5 Önce/sonra görünüm ve DRC farkı kaydedilmiş; schematic parity 0, yeni açıklanmamış clearance/short/courtyard ihlali 0; grup üyelikleri ve yerel izler korunmuş, D5-U11 FB kesintisiz ve en fazla 10 mm.
- [x] #6 Yerleşim tablosu, güncel alan planı, kritik güzergâhlar ve çözülmemiş kısıtlar TASK-008 incelemesine devredilmiş; bağlantısız öğeler routing işi olarak ayrıca raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 — TASK-092 Tamamlandı:
1. Envanter & Kart Dışı Durumu:
   - 143 footprint tamamı kart sınırları içinde ($X \in [50{,}300, 149{,}700]\text{ mm}$, $Y \in [69{,}480, 130{,}520]\text{ mm}$).
   - Kart dışı bekleyen komponent = 0 (yalnızca U2 RF anteni kasıtlı olarak kuzeye taşar).
   - Tam liste `hardware/docs/reports/task-092-20260925/after-inventory.json` dosyasına yazıldı.
2. Ankrajlar & Mekanik Korumalar:
   - J7, J8, J9, J3, H1-H4 ve Ethernet besleme hücresi (Q8, R17, C21, C20, C10, TP14) taban durumla 0,000 mm sapma ile korundu.
   - B.Cu RJ45 keepout ($X \in [51{,}35, 69{,}85]$, $Y \in [80{,}60, 97{,}00]$) içinde J8 harici 0 komponent var.
   - F.Cu LCD koridorunda ($X \in [63{,}52, 141{,}62]$, $Y \in [72{,}28, 127{,}72]$) tüm elemanlar $Z \le 1{,}35\text{ mm} \le 1{,}80\text{ mm}$ kısıtını sağlar.
3. Güç Akışı & Kritik Yollar:
   - Soldan sağa doğrusal akış korundu: J7 -> AP33772S -> Boost -> Buck -> LM74801 -> INA226/Şönt -> J4.
   - J4 vidalı klemens 90° dikey oryantasyonla (146,0; 104,0) yerleştirildi; 3,9 mm PTH padleri doğu kart kenarından 1,75 mm açıklık marjına sahiptir.
   - D5-U11 `/USB_PD_CONTROLLER/BOOST_FB` net izi 4 segmentle taşındı; toplam uzunluk 2,585 mm <= 10,0 mm kuralına uygundur.
4. FreeCAD 3D Katı Kesişim Analizi:
   - `hardware/docs/reports/task-092-20260925/solid-check.json`: J8 mezanin ve tüm komşu 3D katı modelleri kesişim hacmi 0,000000 mm3 (PASSED).
5. DRC ve Parite Doğrulaması:
   - Toplam hata: 15 (tamamı U2 anten kenar kuralı ihlali; 0 yeni hata).
   - Yeni açıklanmamış clearance/short/courtyard ihlali: 0.
   - Şematik paritesi: 0 fark.
   - Bağlantısız öğeler: 360 adet (taban çizgi korundu; routing için TASK-087'ye devredildi).
6. Raporlar & Çıktılar:
   - `hardware/docs/reports/task-092-20260925/final-drc.json`
   - `hardware/docs/reports/task-092-20260925/after-inventory.json`
   - `hardware/docs/reports/task-092-20260925/verification.json`
   - `hardware/docs/reports/task-092-20260925/solid-check.json`
   - `hardware/docs/reports/task-092-20260925/final-top.svg`
   - `hardware/docs/reports/task-092-20260925/final-bottom.svg`
   - `design_decisions/output/KALAN_KOMPONENTLER_YERLESIM_TASK092_20260925.md`
<!-- SECTION:NOTES:END -->
