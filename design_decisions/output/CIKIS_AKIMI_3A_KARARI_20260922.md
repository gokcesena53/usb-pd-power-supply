# Maksimum çıkış akımı: 3 A (22 Eylül 2026)

Handoff'ta (`USB_PD_REV_C_tasarim_kararlari_handoff.md` §1) maksimum çıkış akımı **5 A varsayılmıştı** ve "kesinleşmedi — değişirse şönt, FET ve SOA hesapları yeniden yapılmalı" notu vardı. Kullanıcı kararı: **maksimum çıkış akımı 3 A**. Bu belge kararın hesaplara etkisini ve `todo.txt`'de kapanan/güncellenen maddeleri kaydeder. Şemada değişiklik yapılmadı: 5 A için seçilmiş bütün parçalar 3 A'de marjlı kalıyor.

## Yol direnci ve düşüm (USB_VBUS → OUT_POS)

Kaynak: `design_decisions/reports/sqjb60ep-20260921/result.md` §4.

| Eleman | Direnç | 5 A (eski varsayım) | 3 A |
|---|---|---|---|
| R11 (AP33772S şöntü) | 5 mΩ | 25 mV | 15 mV |
| Q5A+Q5B (SQJB60EP, 2 × 12 mΩ) | 24 mΩ (125 °C'de 38,2 mΩ) | 120 mV (191 mV) | **72 mV (115 mV)** |
| RShunt1 (INA226 şöntü) | 5 mΩ | 25 mV | 15 mV |
| **Toplam** | 34 mΩ (125 °C'de 48,2 mΩ) | 170 mV (241 mV) | **102 mV (145 mV)** |

- **Çıkış kolu kaybı (Q5):** 5 A'de 0,60–0,96 W idi, 3 A'de **0,22–0,34 W** (die başına 0,11–0,17 W). SQJB60EP'nin onaylı ≤4 mΩ spesifikasyonundan sapması (3 kat) 3 A'de pratik bir sorun olmaktan çıktı: ≤4 mΩ FET'lerle toplam düşüm 3 A'de 54 mV olurdu, SQJB60EP ile 102 mV.
- **3,3 V / 3 A çıkış:** Adaptörün 25 °C'de ~3,40 V, 125 °C'de ~3,45 V (artı kablo düşümü) vermesi gerekir. PPS APDO'ları 3,3 V'tan başlayıp 20 mV adımla yükseldiği için bu gerilim istenebilir; kompanzasyon firmware'de (todo: "AP33772S FAULT izleme ... PPS 20 mV adımlarıyla kablo düşümü kompanzasyonu").

## Şönt ve INA226 (RShunt1)

Kaynak: `design_decisions/reports/ina226-20260921/result.md` §2.

| | 5 mΩ (mevcut) | 10 mΩ (seçenek) |
|---|---|---|
| 3 A'de şönt düşümü | 15 mV (tam skalanın %18'i) | 30 mV (%37) |
| 3 A'de kayıp | 45 mW | 90 mW |
| Akım LSB (2,5 µV / R) | 500 µA | 250 µA |
| Ofset (±10 µV) | ±2 mA | ±1 mA |
| Yol düşümüne katkı | — | +15 mV (toplam 117 mV) |

**Karar: RShunt1 5 mΩ'da kalıyor** (BVT-I-R005-1.0, Özdisan stoklu). 10 mΩ düşük akım çözünürlüğünü iki katına çıkarır ama 3,3 V çıkışta adaptör payını azaltır ve yeni parça seçimi ister. Düşük akım çözünürlüğü (±2 mA) ekranda yetersiz kalırsa 10 mΩ'a geçiş PCB'de ayak değişmeden yapılabilir (aynı 2512).

**Firmware için yeni INA226 ayarları (5 mΩ, 3 A):**

```
Current_LSB = 125 uA              (tam skala 4.096 A, 2^15 adim)
CAL = 0.00512 / (125e-6 x 0.005) = 8192   -> 05h = 0x2000
Power_LSB   = 25 x Current_LSB = 3.125 mW
SOL esigi (3.5 A) = 3.5 A x 5 mOhm / 2.5 uV = 7000   -> 07h = 0x1B58
Mask/Enable: SOL=1, LEN=1, APOL=0, CNVR=0 -> 06h = 0x8001 (degismedi)
```

SOL eşiği nominalin ~%17 üstünde (3,5 A) önerildi; kesin değer firmware tarafında seçilebilir. Eski 6 A / 250 µA ayarı 5 A varsayımına göreydi.

## Diğer parçalar

5 A'e göre seçilen parçalar 3 A'de fazladan marj taşıyor; değişiklik gerekmiyor:

- J7 USB4105-GF-A (5 A), J4 klemens, SQJB60EP, BVT-I-R005 (2,5 W), R11: aynı kalıyor.
- USB PD tarafı: AP33772S'in PDO/APDO isteklerinde çalışma akımı 3 A ile sınırlanmalı; bu `todo.txt` FIRMWARE bölümüne eklendi.
- Dahili kol (Q3, ~1,4 A) ve ön-boost/buck zinciri çıkış akımından bağımsız; etkilenmez.

## todo.txt'de yapılanlar

Kapatılan (bu belgeye taşındı):

- **"Maksimum çıkış akımı kesinleştir (varsayım 5 A)"** → 3 A; RShunt1 5 mΩ'da kaldı (yukarıda).
- **"3.3 V tam yükte adaptör başlığını doğrula"** → 3 A'de yol düşümü 102 mV (125 °C'de 145 mV); gereken ~3,40–3,45 V PPS ile istenebilir. Ölçümle teyit prototip doğrulamasına kalıyor (PPS geçiş testleri zaten listede).

Güncellenen (açık kalıyor, 5 A → 3 A):

- Prototip: "28 V EPR, 5 A yükte ... tepe < 34 V" → 3 A.
- Prototip: "AP74502Q açılışı ... 5 A rezistif yük (SOA)" → 3 A.
- Firmware: INA226 kalibrasyon/SOL değerleri yukarıdaki 3 A ayarlarıyla değiştirildi.
- Firmware: yeni madde — PDO/APDO isteklerinde çalışma akımı ≤3 A.
