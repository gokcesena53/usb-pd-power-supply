# Çıkış deşarjı: R59 bleed → SW_EN kontrollü aktif deşarj (23 Eylül 2026)

Görevler: TASK-049 (şema), TASK-050 (prototip doğrulaması). Ön adım
TASK-048: I2C seviye dönüştürücü mcu sayfasına taşındı, deşarj bloğu
usb_pd_controller'da boşalan yere kondu.

## Sorun

R59 (OUT_POS–GND, 10 kΩ, 1/3 W 0805) tek deşarj yoluydu:

| | R59 = 10 kΩ |
|---|---|
| 28 V'ta sürekli kayıp | 78 mW |
| INA226 akım hatası | R59 şöntün yük tarafında: 28 V'ta +2,8 mA (ofset ±2 mA, 22 LSB) |
| 100 µF yük, 28 V → 1 V | 3,3 s |
| 1000 µF yük, 28 V → 1 V | 33 s |

OUT_POS'ta kartın kendi kapasitesi yok (C29 PD_VOUT'ta); boşalan enerji
kullanıcı yükündedir. Q5'in DGATE tarafı (LM74801, V(A−C) karşılaştırıcısı)
ters akımı engellediği için gerilim düşürmede (28 → 5 V) çıkış yük boşalana
kadar eski gerilimde kalır; firmware'in voltaj değiştirme sırası tıkanır.

## LM74801'in kendi özelliği yok

SNOSD95C incelendi: HGATE kapalıyken yalnız kendi gate'ini OUT'a bağlar,
VSNS–SW anahtarı EN low iken *açıktır* (ters mantık, bölücü akımı için),
shutdown'da OUT'ta aşağı çeken yol yoktur. C pini boşta bırakılırsa
LM74801 çift yönlü iletir; bu, çıkış enerjisini PD_VBUS'a geri verir ve USB
PD'de yasaktır. Deşarj harici yapılmalıdır.

## Karar

Kullanıcı kararı: ekstra GPIO kullanılmayacak (ESP32-C6-MINI-1'de boş GPIO
yok). SW_EN (U13 = OUT_EN AND ~ALERT) transistörlü NOT kapısıyla ters
çevrilip deşarj FET'ini sürer.

```
SW_OUT ─ R66 100k ─┬─ DISCH_G ─┬──────────── Q6.G
                   │           D10 BZT52C12 (K üstte) ─ GND
                   Q4.D
SW_EN ─────────── Q4.G     Q4.S ─ GND
OUT_POS ─ R67 1k 2W ─ Q6.D   Q6.S ─ GND
OUT_POS ─ R59 100k ─ GND   (pasif yedek)
```

| Durum | SW_EN | Q4 | DISCH_G | Q6 |
|---|---|---|---|---|
| Çıkış açık | H | açık | ~0 V | kapalı |
| OUT_EN low | L | kapalı | min(V_OUT, 12 V) | açık |
| INA226 ALERT | L | kapalı | yukarıda | açık |
| Kart güçsüz (U13 beslenmiyor) | L | kapalı | yukarıda | açık |

- **R66 SW_OUT'tan beslenir:** çıkış kapalıyken SW_OUT şönt (5 mΩ) üzerinden
  OUT_POS ile aynı gerilimdedir, deşarjı yükteki enerji sürer (USB çekilince
  de çalışır). Şönt öncesi olduğu için çıkış açıkken R66–Q4 akımı
  (28 V'ta 0,28 mA) INA226 ölçümüne girmez.
- **D10** gate'i ≤12 V'ta tutar (BSS138P VGS maks ±20 V). D6 ile aynı parça.
- **Çakışma:** SW_EN yükselince Q4 ns'de açılır, U12 HGATE ise CdVdT ile
  ms'de; Q6 önce kapanır. Kapanışta Q6 gate'i R66 × Ciss ≈ 100 kΩ × 50 pF
  ≈ 5 µs'de dolar; o sırada Q5 açık kalsa akımı R67 sınırlar (28 mA).
- **R59 100k** Q6 eşiğinin (~1,5–2 V) altında kalan gerilimi boşaltır ve
  INA226 Vbus girişini tanımlı tutar. INA226 ofset katkısı 0,28 mA.

## Parça seçimi

| Ref | Parça | Özdisan (23.09.2026) | Gerekçe |
|---|---|---|---|
| Q4, Q6 | BSS138P,215 (Nexperia) | 737689, stok 73553 | Q1/Q2 ile aynı kalem. 60 V > D7 kenetleme 48,4 V; VGS(th) 0,9–1,5 V (Q4 3,3 V ile sürülüyor); RDS(on) 2 Ω @5 V |
| D10 | BZT52C12 (PANJIT) | 560765 | D6 ile aynı |
| R66, R59 | CRCW0603100KFKTBBC 100k 0603 | 1089735, stok 8494 | 75 V çalışma gerilimi |
| R67 | PS122WF1001T4E 1k 2512 2 W anti-surge | 746122, stok 93571 | aşağıda |

**R67 değeri.** GPIO olmadığı için çıkış kapalıyken OUT_POS'a dış kaynak
bağlanırsa deşarj kapatılamaz; R67 bunu sürekli taşımalı.

| R67 (2 W) | 28 V sürekli | 30,4 V (OV eşiği) | 1000 µF 28 → 5 V | Özdisan |
|---|---|---|---|---|
| 470 Ω | 1,67 W (%83) | 1,97 W (%98) | 0,81 s | var (HP122WF4700T4E) — marj yok |
| 560 Ω | 1,40 W (%70) | 1,65 W (%83) | 0,97 s | stokta yok |
| **1 kΩ** | **0,78 W (%39)** | **0,92 W (%46)** | **1,72 s** | **var** |

1 kΩ ile deşarj: 100 µF 28 → 5 V 0,17 s; 1000 µF 28 → 2 V 2,64 s
(R59'un 33 s'ine göre ~13–20 kat hızlı). Enerji 1000 µF/28 V'ta 0,39 J.

**Q1/Q2 değişmedi.** 2N7002K (VGS(th) maks 2,5 V) 3,3 V gate'li I2C seviye
dönüştürücüde 5V→3V3 yönünde en kötü durumda ~0,4 V gate üstü sürüş
bırakıyor; BSS138P (maks 1,5 V) daha iyi. Yeni FET'ler Q1/Q2'nin parçasına
uyduruldu; Q1/Q2'nin sembol alanları (Description "50V", Value "BSS138",
parametrik TBD'ler) BSS138P datasheet'ine göre düzeltildi.

## Firmware etkisi

`software/FIRMWARE_GEREKSINIMLERI.md` §3: voltaj düşürürken OUT_EN low
sonrası INA226 Vbus hedefin altına inene kadar beklenir; Vbus 100 ms'de
%5'ten az düşerse "harici kaynak bağlı" uyarısı verilir (deşarj
kapatılamaz, R67 sürekli ~1 W ısınır).

## Açık

- Prototip ölçümleri: TASK-050 (deşarj süreleri, çakışma, R67 sıcaklığı 30 dk
  30,4 V dış kaynakla).
- PCB: R59 0805 → 0603, R67 2512 için bakır alanı (TASK-006/008).
