# INA226AIDGSR, INA228AIDGSR yerine kullanılabilir mi?

**Tarih:** 2026-09-21
**Kapsam:** U3 (kullanıcı çıkışı akım/gerilim ölçümü), `usb_pd_controller` sayfası
**Sonuç:** Kullanılabilir, uygulandı. Üç noktada bilinçli marj kaybı var (§3).

---

## 1. Uyumluluk

Pinout ve paket birebir aynıdır; TI INA228'i INA226'nın pin uyumlu üst modeli
olarak çıkarmıştır. İki datasheet'in "Pin Configuration and Functions"
tablolarından doğrulandı (`hardware/datasheets/ina226.pdf` SBOS547C,
`ina228.pdf` SLYS021A):

| Pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| INA228 | A1 | A0 | ALERT | SDA | SCL | VS | GND | VBUS | IN− | IN+ |
| INA226 | A1 | A0 | Alert | SDA | SCL | VS | GND | VBUS | IN− | IN+ |

- Paket: her ikisi de **DGS (VSSOP-10), 3.00 × 4.90 mm** → `Package_SO:TSSOP-10_3x3mm_P0.5mm` ayağı değişmez, PCB yerleşimi etkilenmez.
- Besleme: her ikisi de 2.7–5.5 V → C11 (100n) ve +3.3V beslemesi aynı kalır.
- Adresleme: her ikisinde de A0/A1 → GND/SCL/SDA/VS ile 16 adres, taban 0x40. Şemada A0/A1 GND'de, adres **0x40** değişmedi.
- ALERT: her ikisinde de açık drenajlı, varsayılan aktif-düşük → R27 (10k pull-up) ve `INA_ALERT` wired-OR düzeni aynen çalışır.
- KiCad kütüphanesinde `INA228` zaten `INA226`'yı `extends` eder; sembol gövdesi ve pinleri bayt bayt aynı çıktı (yalnız Datasheet/Description/ki_keywords alanları farklı).

Devrede **hiçbir tel, hiçbir pasif ve hiçbir net değişmez**. Değişim tamamen
parça seviyesindedir.

## 2. Ölçüm başarımı — RShunt1 = 5 mΩ ile

| | INA228 (ADCRANGE=1) | INA226 |
|---|---|---|
| Şönt tam skala | ±40.96 mV → ±8.19 A | ±81.92 mV → ±16.38 A |
| Şönt LSB | 78.125 nV → **15.6 µA** | 2.5 µV → **500 µA** |
| Şönt ofset (maks) | ±1 µV → ±0.2 mA | ±10 µV → **±2 mA** |
| Kazanç hatası (maks) | ±0.05 % | ±0.1 % |
| VBUS LSB | 195.3 µV | 1.25 mV |
| VBUS aralığı | 0–85 V | **0–36 V** |
| Çözünürlük | 20 bit | 16 bit |
| Enerji / şarj birikimi | var | **yok** |
| Die sıcaklık sensörü | var | **yok** |

Pratik sonuç:

- **Yüksek akımda fark yok.** 5 A'de bağıl hata INA228'de ~%0.07, INA226'da
  ~%0.3. Panelde gösterilecek değer için ikisi de fazlasıyla yeterli.
- **Düşük akımda fark büyük.** 10 mA'de (50 µV şönt düşümü) INA226'nın ±2 mA
  ofseti **±%20** hata demektir; INA228'de aynı nokta ±%2'dir. Tezgâh
  beslemesiyle uyku akımı ölçme senaryosu (µA–mA mertebesi) INA226 ile
  yapılamaz.
- **Ölçüm penceresi yarı yarıya israf oluyor.** 5 A'de şönt düşümü 25 mV;
  INA226'nın 81.92 mV tam skalasının yalnız %30'u. İstenirse RShunt1 10 mΩ'a
  çıkarılarak akım LSB'si 250 µA'e iner, karşılığında 5 A'de kayıp 125 mW →
  250 mW ve yol düşümü 25 mV → 50 mV olur. **Bu değişiklik yapılmadı**;
  maksimum çıkış akımı kesinleşmeden şönt hesabı yeniden açılmamalı (handoff §8).

## 3. Marj kayıpları

### 3.1 Gerilim dayanımı: 85 V → 40 V (abs max)

| | IN+ / IN− / VBUS abs max | çalışma aralığı |
|---|---|---|
| INA228 | 85 V | 0–85 V |
| INA226 | **40 V** | 0–36 V |

Tasarımın maksimum çıkış gerilimi **28 V** (EPR). 36 V çalışma sınırına 8 V
marj kalır — sürekli rejimde sorun yok.

Riskli pencere D7 (SMBJ30A, OUT_POS): VRWM 30 V, VBR 33.3–36.8 V, VC 48.4 V
@12.4 A. Yani bir endüktif geri tepme/surge olayında D7 kırpmaya başlamadan
önce INA226'nın 40 V abs max'ı aşılabilir.

**Bu kabul edilebilir bir risk sayıldı**, çünkü kart zaten daha düşük bir abs
max ile yaşıyor: AP33772S VCC abs max **34 V** ve o da aynı sınıf bir TVS'nin
(D3, SMBJ30A) arkasında. Handoff §10.4'teki "tepe < 34 V" doğrulama maddesi
tam olarak bu marjı ölçmek için var; o test geçerse INA226'nın 40 V'u zaten
güvenli tarafta kalır.

**Sert sınır:** çıkış gerilimi bir gün 28 V'un üzerine çıkarılırsa (USB PD EPR
spesifikasyonu 48 V'a izin verir) INA226 doğrudan elenir. Bu karar 28 V tavana
bağlıdır.

### 3.2 ALERT: dört ayrı limit → tek limit

INA228'de SOVL/SUVL/BOVL/BUVL ayrı kayıtlardır ve hepsi aynı anda etkindir.
INA226'da **tek bir Alert Limit Register (07h)** vardır ve Mask/Enable ile beş
fonksiyondan (SOL, SUL, BOL, BUL, POL) yalnız biri seçilebilir — datasheet
§6.3.1.2: *"Only one of these alert functions can be enabled and monitored at a
time."*

Handoff §4.9 üç limit istiyordu. Karşılıkları:

| İstenen | INA226'da | Karşılayan |
|---|---|---|
| SOVL ≈ 6 A (aşırı akım) | **SOL olarak korunur** | INA226 ALERT → EN (koruma katmanı 1) |
| BOVL (çıkış aşırı gerilim) | düşer | **Zaten yedekli:** AP74502Q OVLO, 232k/10k ile ~30.25 V (koruma katmanı 2) |
| SUVL ≈ −0.3 A (ters akım) | düşer | AP74502Q ideal diyot kontrolcüsünün ters akım koruması — **doğrulanmalı** (todo) + firmware ile yavaş yedek |

Yani mimarinin birincil katmanı (donanım aşırı akım) aynen korunuyor, bus OV
zaten çift yedekliydi, kaybedilen tek şey ters akımın **ikinci** donanım
katmanı. Mask/Enable varsayılanları bu kullanım için doğru: APOL=0 (aktif
düşük, açık drenaj) ve LEN=1 (mandallı) ile `INA_ALERT` → `OUT_EN` wired-OR
düzeni değişmeden çalışır.

### 3.3 ALERT gecikmesi: 75 µs → ~140–280 µs

INA228'in "fast alert response" değeri 75 µs'tir. INA226'da ALERT her şönt
dönüşümünün sonunda değerlendirilir; en kısa dönüşüm süresi 140 µs (AVG=1).
Şönt-sürekli modda gecikme ~140 µs, şönt+bus sürekli modda ~280 µs olur.

Kısa devre testinde (handoff §10.6) M1/M2 bu 2–4 kat uzamış süreyi SOA içinde
taşımalıdır. Yedek katman AP33772S OCP'sidir. **Prototipte ölçülmeli.**

## 4. Firmware etkisi

Register haritası tamamen farklıdır, sürücü yeniden yazılmalıdır:

- INA228: `00h CONFIG, 01h ADC_CONFIG, 02h SHUNT_CAL, 04h VSHUNT(24b), 05h VBUS,
  06h DIETEMP, 07h CURRENT, 08h POWER, 09h ENERGY, 0Ah CHARGE, 0Bh DIAG_ALRT,
  0Ch–11h limitler`
- INA226: `00h Config, 01h Shunt Voltage, 02h Bus Voltage, 03h Power,
  04h Current, 05h Calibration, 06h Mask/Enable, 07h Alert Limit,
  FEh Mfg ID (0x5449), FFh Die ID (0x2260)`

Önerilen kalibrasyon noktası (5 mΩ şönt için):

```
Current_LSB = 250 µA            (8.19 A tam skala, 2^15 adım)
CAL = 0.00512 / (Current_LSB × R_SHUNT)
    = 0.00512 / (250e-6 × 0.005) = 4096          -> 05h = 0x1000
Power_LSB = 25 × Current_LSB = 6.25 mW
SOL eşiği (6 A) = 6 A × 5 mΩ / 2.5 µV = 12000    -> 07h = 0x2EE0
Mask/Enable: SOL=1, LEN=1, APOL=0, CNVR=0        -> 06h = 0x8001
```

Kaybedilenler firmware'e devrolur: enerji/şarj (mAh, Wh) sayacı artık akım
ölçümlerinin yazılımda integrali ile tutulmalı; die sıcaklığı okunamaz.

## 5. Uygulanan şema değişikliği

`hardware/usb_pd_controller.kicad_sch`:

- `lib_symbols` önbelleğindeki `Sensor_Energy:INA228` girdisi, sistem
  kütüphanesinden alınan `Sensor_Energy:INA226` ile değiştirildi.
- U3: `lib_id`, `Value` (INA228 → INA226), `Datasheet`, `Description`,
  `MPN` (INA228AIDGSR → **INA226AIDGSR**) güncellendi.
- Blok başlığı: "INA228 OLCUM + PANEL CIKISI" → "INA226 OLCUM + PANEL CIKISI".

`hardware/gopo.kicad_pcb`: U3'ün `Value` ve `MPN` alanları güncellendi.
Footprint aynı olduğu için pad, yerleşim ve yollar **değişmedi**.

Doğrulama:

```
ERC: 2 ihlal (0 hata, 2 uyari)   <- değişim öncesiyle aynı
     1 isolated_pin_label  (OUT_EN, bilinen açık kalem)
     1 lib_symbol_mismatch (TL431DBZ/U6, bilinen açık kalem)
netlist: 105 net
netlist farki: YOK
readability: 9 bulgu            <- değişim öncesiyle aynı, U3 ile ilgisiz
```

Yeni `lib_symbol_mismatch` oluşmadı: gömülü önbellek doğrudan sistem
kütüphanesinden alındı.

## 6. Ne yapılmadı

- **RShunt1 5 mΩ'da bırakıldı.** 10 mΩ'a çıkarmak düşük akım çözünürlüğünü
  iyileştirir ama maksimum çıkış akımı kesinleşmeden şönt/FET/SOA hesabı
  yeniden açılmamalı.
- **BOM yeniden üretilmedi.** `hardware/docs/output/BOM_REV_C_20260918.xlsx`
  hâlâ INA228AIDGSR yazıyor; şemadan yeniden üretilmeli.
- **LCSC stok/fiyat doğrulanmadı** (çevrimdışı). INA226AIDGSR yaygın bir
  parçadır ve genellikle INA228AIDGSR'den ucuzdur, ama sipariş öncesi
  bakılmalı (handoff §0.5).
