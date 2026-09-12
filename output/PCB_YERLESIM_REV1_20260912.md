# PCB yerleşim revizyonu 1

Tarih: 12 Eylül 2026

## Kart yapısı

- Taslak boyut: **93 × 60 mm**
- Katman sayısı: **4**
- L1: bileşenler ve kritik sinyaller
- L2 / `GND_PLANE`: kesintisiz GND zone
- L3 / `POWER_PLANE`: güç dağıtımı için ayrıldı
- L4: düşük hızlı sinyaller ve ek GND dolgu
- Köşeler: 2 mm yuvarlatılmış
- PCB bileşeni: 100
- J5/J6 banana jack: panel tipi; PCB üzerinde yerleştirilmedi, J4 üzerinden kablolanacak

## Yapılan yerleşim düzeltmeleri

1. ESP32-C6-WROOM-1 90 derece döndürüldü ve anten sağ kart kenarına yönlendirildi.
2. Anten bölgesi x=107–113 mm, y=21–39 mm civarında tutuldu. J4 metal klemens anten bölgesinden yaklaşık 26 mm yatay ayrıldı.
3. Encoder alt-sağ bölgeye yatay yerleştirildi; anten bölgesiyle düşey ayrım artırıldı.
4. J1 USB-C, U9 ve D3/D4/D5 koruma elemanları sol kart kenarında tek giriş kümesi hâline getirildi.
5. USB-PD ana güç sırası J1 → R11 → Q4/Q3 → RShunt → J4 doğrultusunda kuruldu.
6. INA228, RShunt yakınına ve Kelvin izleri çıkarılabilecek yönde yerleştirildi.
7. AOZ1284PI bloğu U5, L1, D2, C12/C13 ve C15/C16 çevresinde kompaktlaştırıldı. FB/COMP elemanları anahtarlama bölgesinin sessiz tarafına alındı.
8. RV-3028-C7 pile yaklaştırıldı ve anahtarlamalı güç elemanlarından uzaklaştırıldı.
9. TFT konnektörü alt kart kenarında tutuldu; TPS61023, CAT4104 ve backlight pasifleri doğrudan konnektörün üzerinde kümelendi.
10. Bütün bileşenler ilk revizyonda üst yüzde bırakıldı.

## DRC sonucu

- Yerleştirilmemiş bileşen: **0**
- Eksik PCB footprinti: **0**
- Courtyard/bileşen çakışması: **0**
- Pad veya farklı net kısa devresi: **0**
- Bakır açıklık ihlali: **0**
- Kart kenarı bakır ihlali: **0**
- Açık bağlantı: **274** — routing henüz başlamadığı için beklenen durum
- Kalan yerleşim uyarıları: silkscreen yazıları ve iki metin yüksekliği

DRC raporu: `reports/layout-20260911/placement-final-drc.rpt`

## Sonraki routing sırası

1. J1–R11–Q4/Q3–RShunt–J4 5 A güç yolu
2. INA228 Kelvin IN+/IN− bağlantıları
3. AOZ1284PI yüksek di/dt giriş ve catch-diode döngüsü
4. TPS61023 boost döngüsü ve CAT4104 akım yolu
5. USB D+/D− diferansiyel çifti
6. +3.3 V güç dağıtımı
7. ESP32, TFT, RTC ve encoder sinyalleri
8. GND via stitching, zone fill ve silkscreen temizliği

Üretici stack-up bilgisi alınmadan USB diferansiyel iz genişliği kesinleştirilmemelidir. 5 A yolunun nihai polygon genişliği de bakır kalınlığı ve izin verilen sıcaklık artışıyla hesaplanacaktır.

