# PD_INT seviye bölücüsü: 12k/20k → 10k+2k0 / 2×10k (23 Eylül 2026)

Görev: TASK-043. Amaç BOM'daki tekil 12k (R8, CRCW040212K0FKED) ve 20k
(R9, TC0250B2002TCC) kalemlerini kaldırmak.

## Devre

AP33772S INT (U1 pin 9, `PD_INT_5V`) → R8 → `PD_INT_3V3` → ESP32-C6 GPIO20
(U2 pin 26); `PD_INT_3V3` → R9 → GND.

- AP33772S INT **push-pull** çıkış (DS46176, "FLIP, INT, OTP, LED Pins"):
  VOH 4.37–4.85–5.33 V (VCC = 5 V), sink/source ≥ 2 mA. Bölücü yükü
  ~30 kΩ → 0.18 mA, sorun değil.
- ESP32-C6 (MINI-1 datasheet): VIH ≥ 0.75 × VDD, VIH maks = VDD + 0.3 V.
- +3.3V rayı AOZ1284, R39 10k2 / R40 3k24 (±1 %), VFB 0.788–0.812 V
  (25 °C): **3.22–3.42 V**. Buradan pencere: giriş **2.565 V ≤ V ≤ 3.52 V**.

## En kötü durum (VOH ve direnç toleransları üst üste)

| Seçenek | V maks | V min | Tipik (4.85 V) | Sonuç |
|---|---|---|---|---|
| Eski: 12k (±1 %) / 20k (±0.1 %) | 3.345 V | 2.720 V | 3.03 V | uygun |
| İlk öneri: 10k / 2×10k (±0.1 %) | **3.556 V** | 2.911 V | 3.23 V | VIH maks'ı 36 mV aşıyor |
| **Seçilen:** 10k (±0.1 %) + 2k0 (±1 %) / 2×10k (±0.1 %) | 3.336 V | 2.728 V | 3.03 V | uygun |

İlk öneri tipik durumda sorunsuz, ancak VOH üst sınırı ile rayın alt sınırı
birlikte gelirse girişi VDD + 0.3 V'un üstüne taşıyor. Enjeksiyon akımı
Thevenin 6.7 kΩ ile ihmal edilebilir olsa da spesifikasyon dışı kalmamak
için oran 0.625'te tutuldu.

## Uygulama

- R8: 12k → 10k, TC0250B1002TCC (R27/R56 ile aynı seçim).
- **R64 (yeni)**: 2k0, ERJ2RKF2001X (R52 ile aynı seçim), R8 ile seri.
- R9: 20k → 10k, TC0250B1002TCC.
- **R65 (yeni)**: 10k, TC0250B1002TCC, R9 ile seri; alt ucu D1/PWR_FLAG
  GND teline bağlandı (#PWR04 kalktı).

BOM: 12k ve 20k kalemleri kalktı, iki 0402 direnç eklendi. Netlist farkı
yalnız beklenen: `PD_INT_3V3` = R64.2, R9.1, TP8.1, U2.26; yeni netler
`Net-(R64-Pad1)` (R8.2–R64.1) ve `Net-(R65-Pad1)` (R9.2–R65.1); GND'de
R9.2 yerine R65.2. ERC 0 hata / 0 uyarı.
