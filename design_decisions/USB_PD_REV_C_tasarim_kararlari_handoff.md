# USB-C PD Masaüstü Güç Kaynağı — REV_C Tasarım Kararları (Agent Handoff)

**Tarih:** 2026-09-16
**Kaynak:** Zg ile yapılan tasarım inceleme oturumu (claude.ai, "USB TYPE C PD Project")
**Hedef revizyon:** REV_B → REV_C

---

## 0. Agent için çalışma kuralları

1. Bu doküman **onaylanmış kararları** içerir. Aşağıdaki "Reddedilen alternatifler" (Bölüm 9) listesindeki çözümleri yeniden önermeyin veya uygulamayın.
2. Referans designator'lar (Q3, Q4, C3, D3, R43, C12, C13, C16 vb.) REV_B şemasından alınmıştır. Değişiklik yapmadan önce her birinin şemada doğru parçaya karşılık geldiğini **doğrulayın**. Uyuşmazlık varsa değiştirmeyin, raporlayın.
3. Değeri veya MPN'i **TBD** olarak işaretlenmiş parçalar için MPN uydurmayın. Şemaya generic parça + `TBD` notu ile yerleştirin (Bölüm 8'deki gereksinimleri parça alanına yazın).
4. Her değişikliği sayfa bazında ayrı commit / değişiklik kaydı olarak yapın ve sonunda Bölüm 10'daki kontrol listesini raporlayın.
5. Parça tedariki LCSC üzerinden planlanıyor. Yeni parça eklerken LCSC stok durumunu not edin.

---

## 1. Tasarım varsayımları

| Parametre | Değer |
|---|---|
| PD controller | AP33772S (sink) |
| VBUS aralığı | vSafe5V attach → PPS 3.3 V … EPR 28 V |
| Kullanıcı çıkış voltajı | **3.3 V – 28 V** (5 V altı yalnızca PPS ile, adaptörün APDO minimumuna bağlı) |
| Maksimum çıkış akımı | **5 A varsayıldı** (kesinleşmedi — değişirse şönt, FET ve SOA hesapları yeniden yapılmalı) |
| Dahili yük | 3.3 V / ~1 A (ESP32, ekran + backlight boost, INA228 vb.) |
| MCU | ESP32 |

---

## 2. Yeni mimari (özet)

```
J1 (USB-C) ── D3 (AQ3130E, ESD) + SMBJ30A (surge) ── USB_VBUS ── C3 ── AP33772S R_SENSE
                                                                         │
                         ┌───────────────────────────────────────────────┤  (dallanma noktası
                         │                                               │   şöntün ARKASINDA)
                         ▼                                               ▼
  KOL A — DAHİLİ BESLEME                               KOL B — KULLANICI ÇIKIŞI
  Q3/Q4 (küçük dual NMOS, AP33772S sürer)             M1 ⇄ M2 back-to-back (AP74502Q sürer)
         │                                                     │
      PD_VOUT (+47 µF sönümleme bulk)                     INA228 şönt
         │                                                     │
  TPS55340 pre-boost (5.02 V)                              OUT_POS ── J4/J5
         │
       V_PRE = max(5 V, PD_VOUT − V_D) ──► AP74502Q VIN
         │
  AOZ1284 buck ── 3.3 V rail
```

**Temel fikir:**
- Kullanıcı akımı artık Q3/Q4'ten geçmez, sadece M1/M2 üzerinden akar (yol kaybı yarıya iner).
- Q3/Q4, cSnkBulk (≤10 µF) uyumu, Hard Reset/detach izolasyonu ve dahili rail kısa devre koruması için **kalır** ama küçültülür.
- Pre-boost, PD_VOUT 5 V'un altına indiğinde (3.3 V PPS) dahili rail'i ayakta tutar; üstünde pass-through çalışır.
- AP74502Q'nun VIN'i V_PRE'den beslendiği için 3.3 V çıkışta da POR eşiğinin (≤3.9 V) üzerinde kalır.

---

## 3. Sayfa bazında değişiklikler

### 3.1 `usb_c_input` / VBUS giriş

| # | İşlem | Referans | Detay |
|---|---|---|---|
| 1 | EKLE | D_TVS (yeni) | **SMBJ30A** (tek yönlü, 600 W, VRWM 30 V). Yer yoksa SMAJ30A. J1'e yakın, kısa toprak dönüşü. |
| 2 | KORU | D3 | AQ3130E-01ETG (ESD diyotu) yerinde kalır, SMBJ30A ile paralel. |
| 3 | DEĞİŞTİR | C3 | 1 µF/50 V → **2.2 µF/50 V X7R** (cSnkBulk minimum 1 µF'ı DC bias altında garanti etmek için). USB_VBUS'ta toplam efektif kapasite 5 V'ta **≤10 µF** kalmalı. |
| 4 | NOT | Ferrite bead | 5 A yoluna **bead konmayacak**. İstenirse USB_VBUS'ta 0 Ω doldurulmuş opsiyonel footprint bırakılabilir (DNP bead). TVS'ler bead'in konnektör tarafında olmalı. |

### 3.2 `usb_pd_controller`

| # | İşlem | Referans | Detay |
|---|---|---|---|
| 1 | DOĞRULA | AP33772S R_SENSE | Şöntün **iki kolun dallandığı noktanın önünde** olduğundan emin olun (OCP ve PPS akım ölçümü toplam akımı görmeli). Konum farklıysa raporlayın, topolojiyi buna göre düzenleyin. |
| 2 | DEĞİŞTİR | Q3, Q4 | IRF7855 → **küçük dual NMOS, 40–60 V, ≥2 A** (TBD, Bölüm 8). Q3/Q4 çıkışı artık sadece `PD_VOUT` (dahili kol) netini besler. |
| 3 | AYIR | Net | `PD_VOUT` ile `OUT_POS` / INA228 arasındaki bağlantıyı **kaldırın**. Kullanıcı çıkış kolu Q3/Q4'ün önünden (USB_VBUS, şönt sonrası) beslenecek. |

### 3.3 `powergeneration`

| # | İşlem | Referans | Detay |
|---|---|---|---|
| 1 | EKLE | U_BOOST (yeni) | **TPS55340PWPR** (HTSSOP-14 PowerPAD). Giriş: `PD_VOUT`, çıkış: yeni net `V_PRE`. |
| 2 | EKLE | L_BOOST | 6.8–10 µH, Isat ≥3 A, düşük DCR (pass-through'da buck giriş akımını sürekli taşır). **TBD** |
| 3 | EKLE | D_BOOST | Schottky 40–60 V, 3 A, düşük VF (SS34/SS36 sınıfı). **TBD** |
| 4 | EKLE | R_FREQ | **78.7 kΩ** (≈600 kHz). f_sw 350 kHz altına düşürülmemeli (foldback recovery). |
| 5 | EKLE | FB bölücü | R_TOP **30.1 kΩ** (V_PRE→FB), R_BOT **9.76 kΩ** (FB→AGND) → V_PRE ≈ 5.02 V |
| 6 | EKLE | **FB clamp (ZORUNLU)** | FB abs max 3 V; pass-through'da FB ≈ 6.8 V'a çıkar. ~~BAT54 + 3V3 bölücü (V_CL ≈ 1.81 V)~~ → **23.09.2026: BAS16H**, anot FB, katot `EN_CTRL` (V_X = 1.605 V, U6 TLV431; #14 ile ortak). 34 V / 0 °C worst-case FB 2.40 V. Ayrıntı: `design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md`. |
| 7 | EKLE | C_SS | 47 nF |
| 8 | EKLE | Kompanzasyon | R3 = 2 kΩ, C4 = 100 nF (başlangıç değeri, en düşük VIN'de ölçümle optimize edilecek). C5 opsiyonel/DNP. |
| 9 | EKLE | C_IN_BOOST | 10 µF/50 V X7R + VIN pinine yakın 100 nF |
| 10 | EKLE | C_OUT_BOOST | ≥2 × 10 µF/50 V X7R (`V_PRE`), AOZ1284 giriş kapasiteleriyle birleştirilebilir |
| 11 | BAĞLA | EN | EN → VIN'e 100 kΩ ile (her zaman aktif). SYNC → AGND, NC → AGND, PowerPAD → AGND. |
| 12 | EKLE | C_DAMP | `PD_VOUT`'a **47 µF, 35–50 V, ESR ~50–100 mΩ** (hybrid polymer veya düşük ESR elektrolitik). Seramik bu işi görmez. PD_VOUT toplam kapasitesi **≤100 µF** (cSnkBulkPd). **TBD MPN** |
| 13 | TAŞI | AOZ1284 girişi | AOZ1284 VIN: `PD_VOUT` → **`V_PRE`**. C12/C13 `V_PRE` netine taşınır. |
| 14 | TAŞI | R43 / TL431 (EN bias) | Beslemesi `V_PRE`'den alınır. ~~R43 ≈ 1 kΩ, TL431 2.495 V~~ → **23.09.2026: R43 4k7, U6 TLV431BQ, R50 2k87 / R51 9k76 REF bölücü → V_X 1.605 V; R42 kaldırıldı.** R43 28 V'ta 0.15 W. |
| 15 | DÜZELT | C16 | **47 µF footprint `C_0402_1005Metric` hatalı** (47 µF 0402'de üretilmiyor). 1206/1210'a çevirin; Cout efektif ≥44 µF hedefi için gerekirse 2 × 22 µF paralel. |
| 16 | KALDIR | — | Buck giriş koluna önerilmiş olan ferrite bead + sönümleme düzeni **iptal** (topoloji değişti). |

### 3.4 `powersensing` / `poweroutput` — Kullanıcı çıkış anahtarı (yeni blok)

| # | İşlem | Referans | Detay |
|---|---|---|---|
| 1 | EKLE | U_SW | **AP74502QTA8-7** (Diodes). Alternatif: **LM74502DDFR** (TI, pin uyumlu). **Her ikisine uyan ortak footprint** kullanın (TI'nın daha uzun pad'li land pattern'i). |
| 2 | EKLE | M1, M2 | Back-to-back (ortak source) N-kanal, **60 V, ≤4 mΩ, 5×6 DFN, Vgs ±20 V**. **TBD** (Bölüm 8). M1 drain → USB_VBUS (şönt sonrası dallanma), M2 drain → INA228 şönt girişi. Yönelimi AP74502Q datasheet tipik uygulamasına göre bağlayın. |
| 3 | BAĞLA | VIN (pin 5) | **`V_PRE`** (USB_VBUS değil). |
| 4 | BAĞLA | SRC (pin 8) | M1/M2 ortak source düğümü |
| 5 | BAĞLA | GATE (pin 6) | M1/M2 gate'lerine doğrudan |
| 6 | EKLE | D_GS | **12 V zener (BZT52C12)** GATE–SRC arası (GATE–SRC abs max 15 V koruması). |
| 7 | EKLE | CdVdT + RG | GATE düğümü → **RG 1 kΩ** → **CdVdT 22 nF/50 V** → GND (seri kol). ≈2.7 V/ms soft-start. |
| 8 | EKLE | C_VCAP | **220 nF/25 V**, VCAP (pin 4) – VIN arası |
| 9 | EKLE | C_VIN | 100 nF/50 V, VIN – GND |
| 10 | EKLE | OVLO bölücü | **Eşik ≈30 V** (kullanıcı çıkışı artık AP33772S OVP'sinin arkasında değil). Direnç değerlerini AP74502Q OVLO eşiğine göre hesaplayın. **TBD değer** |
| 11 | BAĞLA | EN/UVLO (pin 1) | ESP32 GPIO → **10 kΩ seri** → EN; EN → **100 kΩ** → GND (varsayılan kapalı); **INA228 ALERT** (open-drain) doğrudan EN düğümüne (wired-OR). ESP32 **strapping olmayan** bir GPIO kullanın. INA_ALERT ayrıca ESP32 input'una da gitmeye devam etsin. |
| 12 | KORU | INA228 | Şönt M2 sonrası, OUT_POS öncesi. |
| 13 | EKLE | D_OUT | OUT_POS'a **SMBJ30A** (endüktif yük geri tepmesi). |
| 14 | EKLE (ops.) | R_BLEED | OUT_POS → GND 10 kΩ (≥0.25 W) veya SHDN/EN low iken açılan küçük deşarj FET'i. |

### 3.5 `mcu` / firmware arayüzü

- Yeni sinyal: `OUT_EN` (ESP32 GPIO → AP74502Q EN, 10 kΩ seri + 100 kΩ pull-down).
- `INA_ALERT` hem `OUT_EN` düğümüne wired-OR hem de ESP32 interrupt girişine.
- AP33772S INT/STATUS okuması firmware için gerekli (Hard Reset / detach / FAULT).

---

## 4. Firmware gereksinimleri (şema dışı, dokümante edilmeli)

1. **Açılış:** `OUT_EN` low. AP33772S varsayılan olarak 5 V ile açılır (VSELMIN default 5 V).
2. **VSELMIN:** Boot sonrası **≤3.2 V** yapılmalı (aksi halde 3.3 V isteğinde Q3/Q4 kapanır → ESP32 reset döngüsü).
3. **Voltaj isteği:** 5 V altı yalnızca **PPS** ile; istek adaptörün APDO minimumunun altındaysa gönderilmez.
4. **PPS operating current** = kullanıcı yükü + dahili tüketim (3.3 V'ta ~1.4 A).
5. **Çıkış açma:** `OUT_EN` high → ≥25 ms bekle → INA228 ile çıkış voltajını doğrula.
6. **Voltaj değiştirme:** `OUT_EN` low → yeni PDO/APDO isteği → PS_RDY → AP33772S voltaj kaydı ile doğrula → kullanıcı onayı → `OUT_EN` high.
7. **Fixed PDO geçişlerinde** Accept–PS_RDY arası toplam tüketim ≤2.5 W (Wi-Fi TX ertele, backlight kıs).
8. **Hard Reset / detach interrupt:** `OUT_EN` hemen low.
9. **INA228 ayarları:** ALATCH = 1, CNVR = 0, SOVL ≈ 6 A eşdeğeri (donanım aşırı akım), SUVL ≈ −0.3 A (ters akım), BOVL dinamik (istenen voltaj + marj), ADCRANGE uygun aralıkta.
10. **UVP / FAULT:** AP33772S FAULT kaydı izlenmeli; UVP durumunda yeniden pazarlık. 3.3 V'ta kablo düşümü için PPS 20 mV adımlarıyla kompanzasyon.
11. **Hata sonrası:** ALERT latch → arayüzde hata → kullanıcı onayıyla DIAG_ALRT temizle → `OUT_EN` high.

---

## 5. Koruma katmanları (referans)

| Katman | Eleman | Görev |
|---|---|---|
| 1 | INA228 ALERT → EN | Donanım aşırı akım (~6 A) + ters akım, sub-ms |
| 2 | AP74502Q OVLO | Çıkış aşırı voltaj (~30 V) |
| 3 | Firmware (INA228) | Kullanıcı akım limiti, BOVL |
| 4 | AP33772S OCP/OVP/UVP | Toplam giriş; dahili kolu (Q3/Q4) keser |

---

## 6. Kritik tasarım notları (agent değiştirmemeli)

- **Q3/Q4 kaldırılmayacak ve tek MOSFET'e düşürülmeyecek** (cSnkBulk ≤10 µF, Hard Reset/detach izolasyonu, dahili kısa devre koruması).
- **TPS55340 FB clamp devresi zorunlu.** Clamp olmadan PD_VOUT >~12 V'ta FB pini hasar görür.
- **GATE–SRC 12 V zener zorunlu.**
- **AP74502Q VIN'i V_PRE'den** beslenecek, USB_VBUS'tan değil.
- **47 µF sönümleme bulk'ı PD_VOUT'ta zorunlu** (5 A'de çıkış anahtarı açıldığında kablo endüktansı kaynaklı tepeyi 34 V altında tutmak için; AP33772S VCC ve TPS55340 VIN abs max 34 V).
- **Boost asenkron (Schottky'li) olmalı** — pass-through davranışı buna dayanıyor.

---

## 7. BOM özet değişiklikleri

| Durum | Parça |
|---|---|
| Yeni | TPS55340PWPR, AP74502QTA8-7 (alt: LM74502DDFR), SMBJ30A ×2, BZT52C12, BAS16H (eski BAT54), L_BOOST (TBD), D_BOOST (TBD), M1/M2 (TBD), C_DAMP 47 µF (TBD), pasifler |
| Değişen | C3 → 2.2 µF/50 V; Q3/Q4 → küçük dual NMOS (TBD); C16 footprint → 1206/1210; R43 güç rating kontrolü |
| Kaldırılan | IRF7855 (Q3/Q4 olarak); 5 A yolundaki ferrite bead planı |
| Aynen kalan | AP33772S, AOZ1284, D3 (AQ3130E), INA228, EN bias (besleme V_PRE'ye taşındı; 23.09.2026 TL431 → TLV431, FB clamp ile ortak) |

---

## 8. Açık kalemler (TBD) ve gereksinimleri

| Kalem | Gereksinim | Not |
|---|---|---|
| Q3/Q4 (dahili kol) | Dual NMOS, 40–60 V, ≥2 A, AP33772S gate sürüşüyle uyumlu Vgs | LCSC'den seçilecek |
| M1/M2 (çıkış kolu) | 60 V, ≤4 mΩ @10 V, 5×6 DFN, Vgs ±20 V; 28 V × ~1–5 A × ~10 ms SOA | LCSC'den seçilecek |
| L_BOOST | 6.8–10 µH, Isat ≥3 A, düşük DCR | LCSC |
| D_BOOST | Schottky 40–60 V, 3 A | LCSC |
| C_DAMP | 47 µF, 35–50 V, ESR 50–100 mΩ | LCSC |
| AP74502Q OVLO bölücü | ≈30 V eşik | Datasheet OVLO eşiğinden hesaplanacak |
| Maksimum çıkış akımı | Varsayım 5 A | Kesinleşmeli |
| AP33772S R_SENSE konumu | Dallanma noktasının önünde | Şemadan doğrulanacak |

---

## 9. Reddedilen alternatifler (yeniden önermeyin)

| Alternatif | Red sebebi |
|---|---|
| SMBJ40A (VBUS TVS) | 44 V'a kadar iletmez, AP33772S'i korumaz |
| SMAJ30CA (çift yönlü) | Negatif ringing'i −33 V'a kadar geçirir |
| Ferrite bead 5 A yolunda | Isıl marj, DC bias'ta empedans kaybı, kazanç yok |
| LTC4368 çıkış anahtarı | UV/OV istenmedi, maliyet |
| LTC4365 çıkış anahtarı | Pre-boost + V_PRE beslemesiyle gereksiz kaldı |
| LTC3115-1 buck-boost | LCSC ~10.8 $, stok yetersiz |
| LM3481 buck olarak | Low-side kontrolcü, buck yapamaz |
| LM3481 SEPIC tek kademe | Yüksek stres, zor kompanzasyon, 9–28 V'ta düşük verim |
| LM3481 boost | TPS55340 ile değiştirildi (entegre FET, düşük VIN'de harici FET sorunu yok) |
| Q3/Q4'ü tamamen kaldırmak / tek MOSFET | cSnkBulk ihlali, Hard Reset/detach, kısa devre koruması |
| Seri yol (Q3/Q4 → M1/M2) | Paralel kol ile değiştirildi (kayıp yarıya iner) |

---

## 10. Prototip doğrulama listesi (şemaya "test notu" olarak da eklenebilir)

1. 5 V profilde tam yükte AOZ1284 ve TPS55340 kararlılığı; attach anında USB_VBUS efektif kapasite ≤10 µF.
2. 3.3 V PPS'te tam dahili yükte V_PRE regülasyonu (5.02 V) ve boost döngü kararlılığı.
3. 5.5–28 V pass-through'da TPS55340 SW pininde anahtarlama olmadığı ve **FB < 3 V**.
4. 28 V EPR, 5 A yükte çıkış anahtarı açılışında **USB_VBUS / PD_VOUT tepe < 34 V**.
5. AP74502Q açılışı: 1000 µF kapasitif yük (inrush) ve 5 A rezistif yük (SOA); 3.3 V çıkışta gate voltajı ve zener clamp.
6. INA228 ALERT → EN kapanma gecikmesi (kısa devre testi).
7. 5→12, 5→28, 28→5, 5→3.3 V geçişlerinde ESP32 3.3 V rail'i ve AP33772S UVP davranışı (birden fazla adaptörle).
8. Hard Reset ve kablo çekme sırasında çıkış kapasitelerinin VBUS'ı beslemediği.
