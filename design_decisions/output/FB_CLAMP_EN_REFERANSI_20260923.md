# U5 EN + U11 FB clamp: ortak V_X referansı (23 Eylül 2026)

İki pinin gerilimini V_PRE'den sınırlayan devre tek bir referansta
birleştirildi. Bunlar AOZ1284'ün (U5) EN pini ve TPS55340 pre-boost'un (U11)
FB pini. Referans artık +3.3V'a bağlı değil. Analiz 0…60 °C için yapıldı.

## Eski devre ve sorunları

| Blok | Devre | Sorun |
|---|---|---|
| U5 EN | V_PRE → R43 1k0 → EN_CTRL; U6 TL431 (K=REF) 2.495 V; R42 100k | R43 28 V'ta 0.65 W harcıyordu (2 W parça gerekiyordu). |
| U11 FB clamp | BAT54: anot BOOST_FB, katot V_CL; V_CL = +3.3V → R50 820R → R51 1k0 → GND ≈ 1.81 V | Clamp referansı +3.3V'tan geliyordu, +3.3V ise V_PRE'den (U5). Açılışta ya da 3.3 V çöktüğünde V_CL ≈ 0 V olur, D5 FB'yi aşağı çeker ve boost duty'yi artırır. BAT54'ün Schottky kaçağı FB'ye ofset olarak girer (1 µA × 30.1 kΩ = 30 mV V_PRE sapması). |

Değerlendirilen seçenekler:

- **Clamp bölücüsünü TL431'den beslemek (910R/2k4).** Bölücünün 0.75 mA'lik
  akımı, R43'ün verebildiği akımdan TL431'in Imin değerini (≤1 mA) düştükten
  sonra kalan paya sığmıyor. Açılışta pay sınırda kalıyor.
- **D5 katodunu doğrudan 2.495 V'a bağlamak.** FB ≈ 2.8 V olur;
  −40 °C'de ve Vref'in üst toleransında ~2.95 V'a çıkar, 3 V sınırına fazla
  yakın.

Karşılaştırma simülasyonu:
`design_decisions/reports/fb-clamp-20260923/fb_clamp.cir`
(CFG 0 = eski, 1 = doğrudan, 2 = 910R/2k4).

## Yeni devre

```
                     V_PRE (4.3 V … 34 V)
  ────────┬──────────────────────────────────┬──────────
         ┌┴┐ R48 30k1                       ┌┴┐ R43 4k7 (2512)
         └┬┘                                └┬┘
          │            D5 BAS16H             │      EN_CTRL = V_X ≈ 1.605 V
 U11 FB ◄─●──────────────▶|──────────────────●───────────────► U5 EN
         ┌┴┐ R49 9k76              ┌─────────┴──────┐ K
         └┬┘                      ┌┴┐ R50 2k87  ┌───┴───┐
         GND                      └┬┘    REF    │U6 TLV431
                                   ●────────────┤       │
                                  ┌┴┐ R51 9k76  └───┬───┘ A
                                  └┬┘               │
                                  GND              GND
```

- V_X = 1.24 × (1 + 2.87/9.76) = **1.605 V** (nominal).
- Normal çalışmada FB = 1.229 V, V_X'in altında kalır. D5 ters kutupludur
  ve regülasyona etki etmez.
- Pass-through'da (V_PRE > 5 V) FB, V_X + Vf seviyesine sınırlanır. D5'ten
  gelen akımı U6 yutar.
- R42 kalktı: REF bölücüsü (12.6 kΩ) EN'i zaten GND'ye çekiyor.
- V_X, V_PRE'den türetiliyor. Boost anahtarlamaya başlamadan önce
  (V_PRE ≈ PD_VOUT − Vf) de mevcut, yani 3.3 V'a bağımlılık kalmadı.

## Datasheet sınırları

| Pin / parça | Sınır | Kaynak |
|---|---|---|
| U11 FB | abs max 3.0 V; VREF 1.204–1.254 V; IFB ≤20 nA | TPS55340 §6.1, §6.5 |
| U11 VIN | abs max 34 V | TPS55340 §6.1 |
| U5 EN | açık ≥1.2 V, kapalı ≤0.4 V; önerilen 1.2–5 V; abs max 6 V; açık bırakılamaz | AOZ1284 Electrical Char., Enable |
| U6 TLV431BQ | Vref 1.221–1.265 V (tam aralık); IK 0.1–15 mA (abs ±20); VKA ≤6 V; Iref ≤0.5 µA; \|zKA\| ≤0.4 Ω; ΔVref/ΔVKA −2.7 mV/V | TI SLVS139Z §5.1, §5.3, §5.7 |
| U6 pinout (DBZ) | **1 = REF, 2 = K, 3 = A** | TI SLVS139Z Table 4-1 |
| D5 BAS16HT1G | Vf ≤715 mV @1 mA (25 °C), ~−1.6 mV/°C (Şekil 2); IR 55 °C tipik ~0.04 µA (Şekil 3); VR 100 V | onsemi BAS16HT1/D Rev. 11 |

## Worst-case (0…60 °C)

Varsayımlar:
- Dirençler: ±1 % + 100 ppm/°C × 35 °C = ±1.35 %.
- V_PRE: anahtarlama öncesi 4.3 V, sürekli çalışmada 29.4 V (28 V + 5 %),
  geçicide 34 V.
- U5 EN giriş akımı datasheet'te verilmiyor; ≤10 µA varsayıldı.
- TLV431BQ'nun tam aralık toleransı (−40…125 °C) kullanıldı, 0…60 °C için
  kötümser.

**V_X = 1.566 … 1.652 V.** Hesap: bölücü oranı 0.2862…0.3021 + Iref·R50 + zKA
+ ΔVref/ΔVKA.

| # | Kontrol | Worst case | Sınır | Sonuç |
|---|---|---|---|---|
| 1 | U5 EN açık | V_X min 1.566 V | ≥1.2 V | ✓ 0.37 V pay |
| 2 | U5 EN üst sınır | V_X max 1.652 V | ≤5 V (abs 6) | ✓ |
| 3 | U11 FB, V_PRE 34 V, 0 °C, V_X max | 1.652 + 0.746 = **2.40 V** | abs 3.0 V | ✓ 0.60 V pay |
| 4 | U11 FB, 29.4 V sürekli | ≈2.39 V | 3.0 V | ✓ |
| 5 | Regülasyonda D5 iletmez | FB max 1.254 − V_X min 1.566 = −0.31 V (ters) | iletim için +0.2…0.4 V | ✓ |
| 6 | D5 kaçağının V_PRE'ye etkisi | 0.5 µA (tipiğin 10 katı) × 30.1 kΩ = −15 mV | V_PRE bandı 4.82–5.23 V | ✓ ihmal |
| 7 | U6 min akım, V_PRE 4.3 V | 0.556 − 0.133 − 0.010 = 0.41 mA | ≥0.1 mA | ✓ 4× |
| 8 | U6'nın regüle ettiği en düşük V_PRE | 2.81 V | U5 UVLO 2.9 V | ✓ |
| 9 | U6 max akım, 34 V (D5 dahil) | 7.0 + 0.89 − 0.12 = 7.8 mA; 12.8 mW | ≤15 mA | ✓ 1.9× |
| 10 | R43 kaybı | 0.17 W (29.4 V), 0.23 W (34 V) | 1 W (2512) | ✓ 4× |
| 11 | D5 zorlanması | VR ≤1.7 V, IF ≤0.9 mA | 100 V / 200 mA | ✓ |
| 12 | Açılış rampası | V_X ≈ 0.73·V_PRE > FB = 0.245·V_PRE | D5 iletmez | ✓ |
| 13 | U6 kararlılığı | V_X'te kondansatör yok | dahili kompanze (SLVS139Z §8.1) | ✓ |

Satır 3'ün hesabı: FB Thevenin gerilimi 34 × 0.2499 = 8.50 V, direnci
7.27 kΩ, D5 akımı ≈ 0.84 mA. Vf, 715 mV (25 °C max) + 25 °C × 1.6 mV = 0.746 V.

Önerilen devrenin simülasyonu:
`design_decisions/reports/fb-clamp-20260923/fb_clamp_tlv431.cir`.
Bu dosya çalıştırılmadı.

## Uygulanan şema değişikliği (usb_pd_controller)

| Ref | Eski | Yeni | Özdisan (23.09.2026) |
|---|---|---|---|
| U6 | TL431AIDBZR, `Reference_Voltage:TL431DBZ` | **TLV431BQDBZT**, `Power_Path_Custom:TLV431xDBZ` (yeni proje sembolü, pinout SLVS139Z) | 1587549, stok 1134 |
| D5 | BAT54T1G, SOD-123, `Device:D_Schottky` | **BAS16HT1G**, SOD-323, `Device:D` | 344295, stok 6290 |
| R43 | 1k0 PS122WF1001T4E 2 W | **4k7 CQ121WF4701T4E** 1 W %1 2512 | 605074, stok 10274 |
| R50 | 820R, +3.3V → V_CL | **2k87 0402WGF2871TCE**, EN_CTRL → U6 REF | 506262, stok 7770 |
| R51 | 1k0, V_CL → GND | **9k76 0402WGF9761TCE**, U6 REF → GND | 506310, stok 17170 |
| R42 | 100k EN_CTRL → GND | **kaldırıldı** | – |

Netlist farkı (`verify.py --against`, ERC 0/0) yalnızca beklenen netleri
içeriyor:

- `EN_CTRL` = D5.1 (K), R43.2, R50.1, U5.8 (EN), U6.2 (K)
- yeni `Net-(U6-REF)` = R50.2, R51.1, U6.1 (REF)
- `V_CL` neti kalktı
- +3.3V'tan R50.1, GND'den R42.2 çıktı

Eski TL431 sembolünde pin 1 = K, pin 2 = REF idi. TLV431 DBZ'de sıra
tersine dönüyor. K ile REF artık kısa devre olmadığı için yeni proje sembolü
zorunlu.

## Açık kalemler

- **PCB:** U6 SOT-23'ün pad sırası değişti (REF/K) ve D5'in footprint'i
  SOD-123 yerine SOD-323 oldu. PCB güncellemesinde iki parça yeniden
  yerleşecek ve yollar yenilenecek.
- **Bring-up'ta ölçülecekler:** V_X (4.3 V, 5 V, 28 V'ta), pass-through'da
  28 V'ta FB ve açılışta V_PRE aşımı. AOZ1284'ün EN giriş akımı
  datasheet'te yok; varsayım ≤10 µA.
