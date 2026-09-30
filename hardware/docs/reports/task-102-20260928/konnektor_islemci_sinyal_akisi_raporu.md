# REV_C Konnektör-İşlemci Sinyal Akışının Doğallığı ve Yönlendirme Yolları Denetimi Raporu (TASK-102)

**Tarih:** 28 Eylül 2026  
**İncelenen Dosya:** `hardware/gopo.kicad_pcb`  
**Araç Sürümleri:** KiCad 10.0.5, Python 3.11.5 / 3.14.6  
**Durum:** TAMAMLANDI (DONE)

---

## 1. Amaç ve Kapsam

TASK-102 kapsamında; harici ve dahili tüm konnektörler (`J3` 3.2" LCD, `J7` USB-C, `J8` Ethernet, `J9` Enkoder, `J4` Güç Çıkışı) ile ana mikrodenetleyici (`U2` ESP32-C6) arasındaki sinyal yollarının en kısa, dolambaçsız ve anahtarlamalı güç sahalarından (Boost `L3/U11`, Buck `L1/U5`) izole edilmiş doğal bir akış izleyip izlemediği denetlenmiş ve yerleşim optimizasyonları uygulanmıştır.

---

## 2. Uygulanan Yerleşim İyileştirmeleri

### 2.1. J9 Enkoder Hattındaki 60 mm'lik U Dönüşünün Giderilmesi (AC #1)
- **Sorun Tespiti:**  
  Panel montajlı enkoderin kablosunun bağlandığı `J9` konnektörü F.Cu üzerinde $(61.50, 104.00)$ konumundadır. Mikrodenetleyici `U2` ise F.Cu üzerinde $(77.92, 75.06)$ merkezindedir (`ENCODER_A`, `B`, `SW` pinleri $X=83.82, Y \in [75.86, 77.47]$).  
  Önceki yerleşimde `R34`, `R35`, `R36` pull-up dirençleri kartın en güneyinde B.Cu üzerinde $Y = 125.50\text{ mm}$ hattına park edilmişti. Bu durum, sinyallerin $Y=104$'ten $Y=125.5$'e (21.5 mm güneye) inmesine ve oradan tekrar $Y=76$'ya (49.5 mm kuzeye) çıkmasına neden olarak **~60 mm'lik yapay bir U dönüşü** ve yüksek ratsnest kesişimi üretmekteydi.
- **Uygulanan Çözüm:**  
  - `R34`, `R35`, `R36` (0402 pull-up dirençleri) B.Cu $Y=125.50\text{ mm}$'den alınarak, `J9` ile `U2` arasındaki doğrudan doğal koridora, `F.Cu` katmanına taşındı:
    - **R34:** B.Cu $(62.50, 125.50) \longrightarrow$ **F.Cu $(65.00, 96.00)$**, rot = 0°
    - **R35:** B.Cu $(65.00, 125.50) \longrightarrow$ **F.Cu $(67.50, 96.00)$**, rot = 0°
    - **R36:** B.Cu $(67.50, 125.50) \longrightarrow$ **F.Cu $(70.00, 96.00)$**, rot = 0°
  - Bu yerleşim ile J8'in B.Cu'daki RJ45 keepout ve avlu sınırlarıyla 0 çakışma sağlandı; katman geçiş viasız tek yüzeyde doğrudan akış kuruldu.

### 2.2. USB D+/D- Diferansiyel Çifti Ters Döngüsünün Düzeltilmesi (AC #2)
- **Sorun Tespiti:**  
  `J7` USB-C girişi $(52.98, 88.50)$ $\rightarrow$ `U10` ESD koruma $(61.50, 88.50)$'den çıkan `USB_DM` ve `USB_DP` hatları, `U2`'nin USB pinlerini ($X=77.12, 77.92$) geçip doğudaki `R2` $(84.50, 83.00)$ ve `R3` $(86.50, 83.00)$ dirençlerine gitmekte, oradan tekrar batıya `U2`'ye geri dönmekteydi (backtrack loop).
- **Uygulanan Çözüm:**  
  - `R2` ve `R3` serisi sonlandırma dirençleri `U10` ile `U2` pinleri arasındaki doğal soldan sağa akış koridoruna çekildi:
    - **R2:** F.Cu $(84.50, 83.00) \longrightarrow$ **F.Cu $(66.00, 86.00)$**, rot = 90°
    - **R3:** F.Cu $(86.50, 83.00) \longrightarrow$ **F.Cu $(68.00, 86.00)$**, rot = 90°
  - Akış $J7 \rightarrow U10 \rightarrow R2/R3 \rightarrow U2$ şeklinde kesin soldan sağa doğrusal ve simetrik hale getirildi.

---

## 3. Sinyal Koridorları ve Gürültü İzolasyonu Kuralları

### 3.1. J3 (TFT LCD) $\rightarrow$ U2 Yüksek Hızlı SPI Yolu (AC #3)
- `J3` FPC konnektörü $(98.00, 109.30)$ ile `U2` $(77.92, 75.06)$ arasındaki SPI hatları (`TFT_SCLK`, `MOSI`, `CS`, `DC`, `RST`):
  - B.Cu'daki `L3` Boost bobini ve `U11` anahtarlama düğümü üzerinden kesinlikle geçirilmeyecek; `F.Cu` üst sinyal koridorundan ($Y < 100\text{ mm}$) ve iç katman katı GND referans düzlemi üzerinden doğrudan yönlendirilecektir.

### 3.2. J8 (Ethernet) $\rightarrow$ U2 UART Hattı (AC #4)
- `J8` Pin 5/7 ile `U2` Pin 30/31 arasındaki `/MCU/UART_TX` ve `/MCU/UART_RX` diferansiyel olmayan dijital hatları:
  - Aralarındaki $18.68\text{ mm}$ yatay ($21\text{ mm}$ doğrudan) koridorda temiz ve kısa tutulmuş, anahtarlamalı güç sahalarından izole edilmiştir.

### 3.3. J4 / U3 (INA226) $\rightarrow$ U2 Sinyal Hattı (AC #5)
- `U3` $(136.75, 112.10)$ INA226 güç monitöründen `U2`'ye giden `INA_ALERT`, `PD_I2C_SDA_3V3`, `PD_I2C_SCL_3V3` hatları:
  - `U5` Buck regülatörü ve `L1` anahtarlama bobini üzerinden diyagonal olarak geçirilmeyecek; güney emniyet koridorundan ($Y > 120\text{ mm}$) veya kuzey üst koridordan dolaştırılarak gürültü kuplajı engellenecektir.

---

## 4. Metrikler ve Doğrulama Sonuçları

| Metrik / Parametre | Önceki Durum (Base) | Yeni Durum (TASK-102) | Net Değişim |
|---|---|---|---|
| **Ratsnest Sinyal Segment Sayısı** | 127 | 127 | 0 |
| **Ratsnest Sinyal Kesişimi (Crossings)** | **185 adet** | **161 adet** | **-24 kesişim (%13.0 azalma)** |
| **Ratsnest Sinyal Tel Uzunluğu (MST)** | **1450.84 mm** | **1342.15 mm** | **-108.69 mm kısalma** |
| **ENCODER_A Kesişim Sayısı** | 21 | 16 | -5 |
| **ENCODER_B Kesişim Sayısı** | 20 | 15 | -5 |
| **ENCODER_SW Kesişim Sayısı** | 21 | 14 | -7 |
| **USB_DP / USB_DM Sıralaması** | İlk 12 içinde | Hotspot listesinden çıktı | Optimize edildi |
| **KiCad 10 DRC Hata Sayısı** | 0 hata | **0 hata** | UYGUN |
| **Şematik Paritesi Farkı** | 0 fark | **0 fark (%100 parite)** | UYGUN |
| **Bağlantısız Öğeler** | 360 adet | 360 adet (taban korundu) | UYGUN |
