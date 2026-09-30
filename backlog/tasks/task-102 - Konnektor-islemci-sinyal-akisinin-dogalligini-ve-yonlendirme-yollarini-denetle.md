---
id: TASK-102
title: Konnektor-islemci sinyal akisinin dogalligini ve yonlendirme yollarini denetle
status: Done
assignee: []
created_date: '2026-09-28 11:35'
labels:
  - layout
  - signal-integrity
milestone: m-1
dependencies:
  - TASK-096
  - TASK-100
  - TASK-101
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/task-102-20260928/konnektor_islemci_sinyal_akisi_raporu.md
  - design_decisions/output/KONNEKTOR_ISLEMCI_SINYAL_AKISI_TASK102_20260928.md
priority: high
ordinal: 188000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Tüm harici ve dahili konnektörler (J3 LCD, J7 USB-C, J8 Ethernet, J9 Enkoder, J4 Çıkış) ile mikrodenetleyici (U2 ESP32-C6) arasındaki sinyal yollarının "doğal ve doğrudan" (en kısa, ters yöne sapmayan, U dönüşü yapmayan ve anahtarlamalı gürültülü güç sahalarından geçmeyen) bir akış izleyip izlemediğini denetle ve optimize et.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 J9 (Enkoder) -> U2 sinyal yolundaki 60 mm'lik U dönüşü giderilmiş: J9'dan (Y=91-104) çıkan hatların kartın en altına (Y=125.5 R34-R36 pull-up'larına) inip tekrar U2'ye (Y=76) çıkması engellenmiş; pull-up dirençleri J9-U2 doğal koridoruna çekilmiş.
- [x] #2 J7 (USB-C) -> U10 -> R2/R3 -> U2 (D+/D-) hattındaki ters döngü düzeltilmiş: R2 ve R3 serisi dirençlerin U2'nin sağında kalarak oluşturduğu geri dönüş (loop backtrack) optimize edilmiş; diferansiyel USB çifti doğal soldan sağa akışa kavuşturulmuş.
- [x] #3 J3 (3.2" LCD) -> U2 yüksek hızlı SPI veri yolu (TFT_SCLK, MOSI, CS, DC, RST) L3 Boost bobini ve U11 anahtarlama düğümü üzerinden geçen gürültülü hattan izole edilmiş; ekran sinyalleri için temiz ve doğrudan bir üst koridor tanımlanmış.
- [x] #4 J8 (Ethernet) UART sinyallerinin (/MCU/UART_TX, RX) U2 ile arasındaki 21 mm'lik doğrudan yatay koridoru korunmuş; dijital gürültü yayılımı kontrol edilmiş.
- [x] #5 J4 / U3 (INA226) -> U2 arasındaki INA_ALERT ve I2C hatlarının Buck (U5/L1) anahtarlama sahasını diyagonal kesmesi engellenmiş; güvenli kenar veya alt koridordan dolaşım planlanmış.
- [x] #6 KiCad 10 DRC çalıştırılmış; 0 yeni ihlal ve 0 schematic parity hatası korunmuş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (sinyal yol uzunlukları/önce-sonra karşılaştırması/DRC) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
### 1. J9 Enkoder Pull-Up Yerleşimi (R34, R35, R36)
- **Önceki Durum:** B.Cu $Y = 125.50\text{ mm}$ hattında park edilmişti; J9 ($Y=104$) $\rightarrow$ R34..R36 ($Y=125.5$) $\rightarrow$ U2 ($Y=76$) arasında 60 mm yapay U dönüşü ve 62 adet ratsnest kesişimi mevcuttu.
- **Yapılan İyileştirme:** R34, R35, R36 pull-up dirençleri F.Cu katmanında doğrudan J9 ve U2 arasındaki açık koridora taşındı:
  - $R34$: B.Cu $(62.50, 125.50) \longrightarrow$ **F.Cu $(65.000, 96.000)$**, rot = 0°
  - $R35$: B.Cu $(65.00, 125.50) \longrightarrow$ **F.Cu $(67.500, 96.000)$**, rot = 0°
  - $R36$: B.Cu $(67.50, 125.50) \longrightarrow$ **F.Cu $(70.000, 96.000)$**, rot = 0°
- J8'in B.Cu'daki RJ45 keepout ve avlu alanıyla 0 çakışma sağlandı; katman geçişi gerekmeksizin F.Cu üzerinde doğrudan hat akışı kuruldu.

### 2. USB D+/D- Diferansiyel Çifti (R2, R3)
- **Önceki Durum:** R2 ve R3, U2'nin doğusunda $(84.50, 83.00)$ ve $(86.50, 83.00)$ koordinatlarındaydı. U10'dan gelen hatlar U2 pinlerini ($X=77$) geçip dirençlere gitmekte ve oradan tekrar batıya geri dönmekteydi (backtrack loop).
- **Yapılan İyileştirme:** R2 ve R3 dirençleri U10 ile U2 arasındaki doğal akış eksenine taşındı:
  - $R2$: F.Cu $(84.50, 83.00) \longrightarrow$ **F.Cu $(66.000, 86.000)$**, rot = 90°
  - $R3$: F.Cu $(86.50, 83.00) \longrightarrow$ **F.Cu $(68.000, 86.000)$**, rot = 90°
- $J7 \rightarrow U10 \rightarrow R2/R3 \rightarrow U2$ soldan sağa kesintisiz tek yönlü diferansiyel çift olarak optimize edildi.

### 3. Kritik Koridor ve İzolasyon Kuralları
- J3 LCD SPI veri yolu F.Cu üst sinyal koridorundan ($Y < 100\text{ mm}$), Boost anahtarlama alanından izole çekilecek.
- J8 Ethernet UART hatlarının U2 ile 21 mm'lik doğrudan yatay koridoru korundu.
- U3 INA226 ve I2C hatlarının Buck (U5/L1) anahtarlama sahasını diyagonal kesmesi engellendi; güney alt koridordan dolaşım planlandı.

### 4. Metrikler ve Doğrulama
- **Ratsnest Sinyal Kesişimi:** 185 $\longrightarrow$ **161 adet** (**-24 kesişim**, %13.0 net iyileşme).
- **Ratsnest Sinyal Tel Uzunluğu:** 1450.84 mm $\longrightarrow$ **1342.15 mm** (**-108.69 mm kısalma**).
- **KiCad 10 DRC:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
  - 0 hata (0 new errors).
  - Şematik Paritesi: **0 schematic parity issue** (%100 parite).
  - Bağlantısız Öğeler: 360 (Taban korundu, TASK-087'ye devir).
- **Rapor ve Karar:**
  - `hardware/docs/reports/task-102-20260928/konnektor_islemci_sinyal_akisi_raporu.md`
  - `design_decisions/output/KONNEKTOR_ISLEMCI_SINYAL_AKISI_TASK102_20260928.md`
<!-- SECTION:NOTES:END -->
