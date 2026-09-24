# Grup İçi Yerleşim İçin Üretici Kuralları, Ankrajlar ve Komşuluk Haritası — TASK-069, 24 Eylül 2026

Bu belge, `gopo` PCB üzerindeki **15 grubun** (137 gruplanmış eleman) ve **6 grupsuz mekanik ankrajın** (toplam 143 footprint) üretici datasheet, uygulama notu (app note) ve evaluation board yerleşim kurallarını; mekanik ankraj ve yasaklı alan (keepout) tanımlarını; bloklar arası komşuluk ve sinyal/güç koridorlarını; tarihsel yüzler ile nihai hedef yüz haritasını tek bir ana referans altında toplar.

[Tam Envanter ve Doğrulama Verisi](../../hardware/docs/reports/task-069-20260924/inventory.json) ·
[Doğrulama Betiği](../../hardware/docs/reports/task-069-20260924/verify.py) ·
[Envanter Çıkarma Betiği](../../hardware/docs/reports/task-069-20260924/extract_inventory.py)

---

## 1. 15 Grup İçin Üretici Kuralları Tablosu (AC #2)

Aşağıdaki tablo, karttaki tüm devre bloklarının üretici şartlarını, pin kritikliklerini, proje mühendislik tercihlerini ve doğrulama yöntemlerini özetler:

| Grup Adı & Ref Listesi | Ana Parça & Kılıf | Üretici Belgesi & Revizyon | Kritik Pin İlişkileri | Üretici Şartı (Manufacturer Requirement) | Proje Hedefi / Mühendislik Tercihi | Doğrulama Yöntemi |
| --- | --- | --- | --- | --- | --- | --- |
| **1. USB-C GIRIS** (7 üye: J7, D3, D8, D9, U10, R62, R63) | `J7` (GCT USB4105 16-pin / JAE DX07B024), `U10` (USBLC6-2 SOT-23-6), `D3` (SMF30A), `D8/D9` (SMF5.0A) | ST USBLC6-2SC6 DocID5918 Rev 7; USB Type-C Cable & Conn Spec Rel 2.2 | VBUS (A4/A9/B4/B9), CC1/CC2 (A5/B5), D+/D- (A6/A7), SHIELD | TVS ve ESD koruma elemanları konnektör pini ile iç devre arasında köprülenmeli; hat üzerinde stub (çıkıntı) olmamalı. | Sol kenar montajı; J8 RJ45 ile düşeyde $\ge 2{,}0\text{ mm}$ gövde açıklığı; F.Cu hedef yüzü. | DRC clearance, 2D/3D gövde aralığı, stub kontrolü. |
| **2. AP33772S PD KONTROLCU** (23 üye: U1, Q3, R8, R9, R11-R14, R21, R64, R65, C1-C4, C8, D1, TH1, TP1-TP5) | `U1` (AP33772S W-DFN3030-14), `Q3` (SQJB60EP Dual N-FET PowerPAK 1212-8), `R13` (5mΩ 1206) | Diodes Inc. AP33772S Rev 1-2 (Bölüm 11, Şekil 11-1); Vishay Doc #62967 | R13 Kelvin akım şöntü (CSP/CSN: Pins 7/8), GATE1/2 (Pins 5/6), VDD (Pin 13) | CSP ve CSN hatları şönt direncin iç pedlerinden diferansiyel çift olarak çekilmeli; gürültülü SW hatlarından uzak tutulmalı. VDD bypass pinde olmalı. | TH1 NTC sensörü Q3 MOSFET ve R13 şöntünün arasına termal temas amacıyla yerleştirilmeli; B.Cu yüzü. | Diferansiyel hat simetrisi, Kelvin şönt bağlantısı, DRC. |
| **3. TPS55340 PRE-BOOST** (16 üye: U11, L3, D4, D5, C23-C29, R47-R49, R52, R53) | `U11` (TPS55340 WSON-14 PowerPad), `L3` (6.8µH), `D4` (Schottky 5A), `D5` (SOD-323 FB clamp) | TI TPS55340 SLVSBD4C (Bölüm 10, Şekil 10-1/10-2); TI SLVA369 | SW Node (Pins 12-14), FB (Pin 9), COMP (Pin 7), AGND (Pin 6), PGND (Pins 1-2) | SW $\rightarrow$ D4 $\rightarrow$ COUT $\rightarrow$ PGND yüksek frekans AC güç döngüsü minimum alanda tutulmalı. FB pini SW ve L3'ten izole edilmeli; PowerPad'de termal via dizisi şart. | B.Cu yüzeyinde MCU ve anten bölgesinden uzakta konumlandırma; TASK-058 D5.2--U11.9 önceden çizilmiş FB izinin (2.5846 mm) sürekliliği korunmalı. | AC güç döngü alanı ölçümü (<50 mm²), termal via sayısı, DRC. |
| **4. AOZ1284 3.3V BUCK** (19 üye: U5, U6, L1, D2, C12-C19, R38-R41, R43, R50, R51) | `U5` (AOZ1284PI SO-8 Exposed Pad), `U6` (TLV431 SOT-23), `L1` (22µH), `D2` (SS34) | AOS AOZ1284PI Rev 1.1 (Bölüm: Layout, Şekil 4); TI TLV431 Rev 10 | LX Node (Pin 3), BST (Pin 1), FB (Pin 8), COMP (Pin 7), VIN/PGND | VIN $\rightarrow$ U5 $\rightarrow$ LX $\rightarrow$ D2 $\rightarrow$ PGND anahtarlama döngüsü dar olmalı. BST kapasitörü (C14) pinde kalmalı. FB gerilim bölücü LX gürültüsünden korunmalı. | U6 TLV431 pad sırası TASK-058 (1=Ref, 2=Cathode, 3=Anode) korunmalı; B.Cu katmanında boost çıkışına yakın yerleşim. | Döngü alanı kontrolü, BST mesafe ölçümü, DRC. |
| **5. LM74801 CIKIS ANAHTARI** (10 üye: U12, Q5, D6, C30-C32, R54-R56, R58) | `U12` (LM74801-Q1 VSSOP-14), `Q5` (SQJB60EP Dual N-FET), `D6` (TVS) | TI LM7480-Q1 SNVSAU9E (Bölüm 10, Şekil 10-1); TI SLVA862 | A (Pin 14) ve C (Pin 1) diferansiyel gerilim algılama, DGATE (Pin 11), HGATE (Pin 12) | A ve C Kelvin duyu hatları Q5 FET terminallerine doğrudan diferansiyel bağlanmalı; VCAP kapasitörü (C32) U12'ye çok yakın olmalı. | B.Cu katmanı; V_PRE/V_BUCK'tan panel çıkışına doğrusal akış; ters akım kesme hızı (<0.5 µs) için gate döngüleri kısa. | Kelvin çift simetrisi, gate hat uzunluğu, DRC. |
| **6. INA226 OLCUM + CIKIS** (10 üye: U3, U13, RShunt1, J4, C11, C35, D7, R27, R59, R61) | `U3` (INA226 VSSOP-10), `U13` (SN74LVC1G17 SOT-23), `RShunt1` (5mΩ 2512 3W), `J4` (Banana Jack) | TI INA226 SBOS540C (Bölüm 10, Şekil 10-1); TI SBAA203 | IN+ (Pin 10), IN- (Pin 9), ALERT (Pin 3), VBUS (Pin 8), J4 (+/-) | RShunt1 akım şöntünden U3'e 4 telli tam Kelvin duyu bağlantısı şart; duyu hatlarından hiçbir yük akımı geçmemeli. D7 TVS J4 çıkış klemensinde olmalı. | B.Cu katmanı; J4 panel klemensine doğrudan geniş bakır baralar; ALERT pini U13 Schmitt tamponu ile GPIO1'e en kısa yoldan iletilmeli. | Kelvin duyu doğrulaması, iz genişliği/empedans analizi, DRC. |
| **7. CIKIS DESARJI** (5 üye: Q4, Q6, D10, R66, R67) | `Q4` (N-FET SOT-23), `Q6` (P-FET SOT-23), `R67` (100Ω 2512 2W), `D10` (SOD-323) | Nexperia / Diodes MOSFET Uygulama Kılavuzları; CIKIS_DESARJI_20260923.md | OUT_DISCHARGE (GPIO2), V_OUT deşarj hattı, R67 güç direnci | Yüksek termal yüke sahip R67 direnci hassas analog sensörlerden ve kristallerden izole edilmeli; deşarj akımı yerel GND'ye dönmeli. | B.Cu katmanı; R67 ile RTC (U4/Y1) ve INA226 arasında $\ge 15\text{ mm}$ termal mesafe kuralı. | Termal ayrım mesafesi ölçümü, DRC. |
| **8. ESP32-C6-MINI-1** (15 üye: U2, C5-C7, R1-R3, R10, R15, R16, R37, SW1, SW2, TP9, TP10) | `U2` (ESP32-C6-MINI-1 PCB Antenli), `SW1/SW2` (Buton), `C5-C7` (Dekuplaj) | Espressif ESP32-C6-MINI-1 v1.0 Bölüm 6; Espressif Hardware Design Guidelines | Anten keepout, 3V3 (Pin 4), CHIP_EN (Pin 3), Strapping (GPIO8/9/15) | Anten PCB kenarından dışarı taşmalı; anten altında ve çevresinde en az $15\text{ mm}$ boyunca hiçbir katmanda bakır, yol veya metal kasa olmamalı. | F.Cu (Top) hedef yüzü; anten anahtarlama bobinlerinden (L1, L3) uzağa yönlendirilmeli; dekuplaj pinde. | RF keepout ihlal kontrolü, dekuplaj mesafesi, DRC. |
| **9. RTC BQ32000 + 1F5** (5 üye: U4, Y1, C9, C33, R24) | `U4` (BQ32000 SOIC-8), `Y1` (ABS25 32.768kHz), `C33` (Korchip DCL 1.5F 5.5V), `C9` (1uF) | TI BQ32000 SLAS656B (Bölüm 8.3, Şekil 8-4); Abracon ABS25 App Note | OSCI (Pin 1), OSCO (Pin 2), VBACK (Pin 3), VCC (Pin 8) | Kristal (Y1) U4 pinlerine doğrudan simetrik ve ultra kısa bağlanmalı; osilatör döngüsü GND koruma halkasıyla (guard ring) sarılmalı; altından hızlı sinyal geçmemeli. | B.Cu katmanı sessiz köşe; L1/L3 bobinlerinden ve R67 deşarj direncinden $\ge 20\text{ mm}$ uzakta; kristal simetri farkı $\le 0{,}01\text{ mm}$. | Kristal hat simetrisi, guard ring kontrolü, DRC. |
| **10. I2C SEVIYE DONUSTURUCU** (6 üye: Q1, Q2, R4, R5, R6, R7) | `Q1, Q2` (BSS138P N-FET SOT-23), `R4-R7` (4.7kΩ 0402 Pull-up) | NXP App Note AN10441 Rev 01; Nexperia BSS138P Datasheet | SCL_3V3/5V, SDA_3V3/5V, +3.3V (Gate), PD_5V | Düşük parazitik sığalı MOSFET kullanımı; SCL ve SDA kanallarının eşit hat uzunluğu ve simetride tutulması. | B.Cu katmanı; iki paralel dikey kolon ($x=209{,}0$ ve $x=213{,}5\text{ mm}$); kuzey 3.3V, güney 5V; sıfır kesisim; simetri farkı $0{,}000\text{ mm}$. | Kanal simetri farkı, kesisim kontrolü, DRC. |
| **11. ETHERNET MEZANIN (CH9121)** (7 üye: J8, Q8, R17, C10, C20, C21, TP14) | `J8` (Waveshare 2-CH UART TO ETH 2x8 Header), `Q8` (TSM3443CX6 P-FET SOT-26), `C10` (22uF), `C20/C21` (100n) | Waveshare SCH 07.08.2021; WCH CH9121DS1 V2.5; Taiwan Semi TSM3443CX6 | ETH_3V3 (J8.13/14), GND (J8.11/12), ETH_PWR_EN (Q8.3), RUN (J8.4), UART_TX/RX | AMS1117 LDO'yu atlayarak doğrudan 3.3V besleme; header girişinde dekuplaj; RJ45 bacak çıkıntılarına temasın önlenmesi. | B.Cu katmanı; Q8 soft-start hücresi ($\tau_{\text{on}}\approx 0{,}91\text{ ms}$, inrush $\approx 62\text{ mA}$); RJ45 altı MUTLAK KEEPOUT; TP14 dışarıda \%100 erişilebilir. | RJ45 keepout, Z aralık hesabı, güç/sinyal koridor ayrımı, DRC. |
| **12. TFT BACKLIGHT** (4 üye: Q7, R28, R29, R60) | `Q7` (IRLML6344TRPBF N-FET SOT-23), `R60` (Akım sınırlama), `R28/R29` (Gate) | Infineon IRLML6344TRPBF PD-97341; Focus LCDs TFT032B018 Spec | LEDK (J3.29), LEDA (J3.28), PWM_BL (GPIO7) | Düşük Vgs(th) (<1.1V) logic-level MOSFET; açılışta arka ışığın sönük kalması için gate pull-down (R29). | F.Cu katmanı; J3 konnektörünün Pin 28/29 bölgesine doğrudan komşu yerleşim; LCD altı yükseklik $\le 1{,}80\text{ mm}$ sınırına uyum. | LCD yükseklik zarfı, gate pull-down kontrolü, DRC. |
| **13. TFT CONNECTOR J3** (1 üye: C34, ilişkili sabit ankraj J3) | `J3` (KLS1-242I 30-pin 0.5mm FPC), `C34` (100nF VDD dekuplaj) | KLS Electronic KLS1-242I Datasheet; Focus LCDs TFT032B018 | SPI (CS, DC, SCL, SDA), VDD (Pin 5/6), LEDA/K (Pin 28/29) | FPC kilit mekanizması yönünde kablo takma alanı; FPC büküm yarıçapı $\ge 1{,}0\text{ mm}$; VDD pini dibinde dekuplaj. | F.Cu kilitli mekanik ankraj $(98{,}00, 109{,}30\text{ mm}, 90^\circ)$; C34 konnektörün hemen arkasında. | Sabit ankraj koordinat/kilit kontrolü, DRC. |
| **14. ROTARY ENCODER** (3 üye: R34, R35, R36, ilişkili ankraj J9) | `J9` (5-pin kablo konnektörü), `R34-R36` (10kΩ 0402 Pull-up) | KLS Electronic L-KLS4-EC1121S Datasheet; ENCODER_PANEL_TASK066_20260924.md | ENC_A (Pin 1), ENC_B (Pin 3), ENC_SW (Pin 5), GND, +3.3V | Mekanik kontak ark gürültüsü için kararlı pull-up; kablo gerilim alma ve lehimleme alanı. | Panel montajlı enkoderden gelen 5 telli kablo için J9 Ethernet yanı sol panele yakın; anten ve güç bobinlerinden uzak. | Kablo büküm açıklığı, RF/anahtarlama mesafe kontrolü. |
| **15. TEST NOKTALARI** (6 üye: TP6-TP8, TP11-TP13) | `TP6-TP8, TP11-TP13` (TestPoint_Pad_D1.0mm) | IPC-7351B Testability Guidelines; IEEE 1149.1 | V_PRE (TP6), +3.3V (TP7), GND (TP8), TXD0 (TP11), RXD0 (TP12), PD_5V (TP13) | Test pedleri ait oldukları devre düğümlerine doğrudan bağlanmalı; problama için en az $2{,}54\text{ mm}$ pedler arası mesafe bırakılmalı. | Test noktaları tek bir yapay hatta dizilmek yerine ilgili güç/dijital bloklarının çıkışına dağıtılmalı; B.Cu prob erişimi. | Prob erişim mesafesi ($\ge 2{,}54\text{ mm}$), net doğrulaması. |

---

## 2. Mekanik Ankrajlar, Yasaklı Alanlar (Keepout) ve Yükseklik Sınırları (AC #1, AC #3)

```
+─────────────────────────────────── POZİSYON VE YASAKLI ALANLAR ───────────────────────────────────+
│                                                                                                   │
│  [SOL KENAR PORTLAR]                      [MERKEZ - LCD BÖLGESİ]          [SAĞ KENAR / GÜÇ]       │
│  • J7 USB-C (F.Cu, Sol Kenar)             • J3 FPC (F.Cu, KİLİTLİ)        • INA226 & J4 Çıkış     │
│  • J8 RJ45/ETH (B.Cu, Sol Kenar)            x = 98.00, y = 109.30, 90°    • Banana Jack Klemens   │
│  • J9 Enkoder (Taşınabilir Ankraj)        • LCD Altı Top Parça Limiti:    • Çıkış Klemensi        │
│                                             Zarf ≤ 1.80 mm                                        │
│  [KEEPOUT: RJ45 B.Cu]                                                     [KÖŞE MONTAJ DELİKLERİ] │
│  x = 198.0 .. 214.5, y = 138.0 .. 160.6   [KEEPOUT: ANTEN F.Cu/B.Cu]      • H1: (53.67, 72.85)    │
│  2.2 mm THT lehim çıkıntısı;              U2 Anteni PCB Dışına Taşar;     • H2: (146.33, 72.85)   │
│  MUTLAK BAKIR/VİA/PARÇA YASAK!            15 mm çevresi tamamen BOŞ!      • H3: (53.67, 127.15)   │
│                                                                           • H4: (146.33, 127.15)  │
+───────────────────────────────────────────────────────────────────────────────────────────────────+
```

1. **Sabit ve Kilitli Ankrajlar:**
   - **`H1`, `H2`, `H3`, `H4`:** M3 montaj delikleri. Kart köşelerinde $(53{,}67, 72{,}85)$, $(146{,}33, 72{,}85)$, $(53{,}67, 127{,}15)$ ve $(146{,}33, 127{,}15)\text{ mm}$ koordinatlarındadır. $\varnothing 6{,}0\text{ mm}$ vida başı keepout alanı korunur.
   - **`J3` (FPC Konnektörü):** $(98{,}000, 109{,}300\text{ mm}, 90^\circ)$ koordinatında **KİLİTLİDİR**. TFT032B018 ekranın FPC büküm ekseniyle tam hizalıdır; konnektör kilit mandalına prob/cımbız erişim koridoru açık tutulmalıdır.
   - **`J7` (USB-C Girişi):** Sol panel montajı. Metal şasi toprağı ve 4 adet gövde sabitleme ayağı mekanik stabilite sağlar.
   - **`J9` (Panel Enkoder Konnektörü):** Eski $(44{,}8, 116{,}2)$ koordinatı mutlak ankraj değildir. Ethernet modülü yanında, kablo bükümüne ve lehimlemeye uygun nihai koordinatı TASK-063/TASK-083 ile kesinleşecektir.
2. **Yasaklı Alanlar (Keepout Zones):**
   - **ESP32-C6 Anten Bölgesi:** U2 modülünün PCB anteni ana kart sınırından dışarı taşacak şekilde yerleştirilir. Anten ucunun $15\text{ mm}$ çevresinde hiçbir katmanda (F.Cu, In1.Cu, In2.Cu, B.Cu) bakır, yol veya şasi düzlemi bulunamaz.
   - **J8 RJ45 Bacak Çıkıntısı ($x \in [198{,}0, 214{,}5]\text{ mm}$, $y \in [138{,}0, 160{,}6]\text{ mm}$):** Modül altındaki entegre trafolu RJ45 konnektörünün THT lehim bacakları $\approx 2{,}20\text{ mm}$ dışarı taşar. Nominal $2{,}50\text{ mm}$ header yükselticisinde kalan $0{,}30\text{ mm}$ tolerans boşluğu elektriksel temas riski doğurur. Bu bölge anakart `B.Cu` katmanında **MUTLAK KEEPOUT** alanıdır; hiçbir SMD parça, via veya açık bakır konulamaz.
3. **TASK-065 Yükseklik ve Yüz Kısıtları:**
   - LCD ekran izdüşümü altında kalan `F.Cu` (Top) bileşenlerinin toplam montaj zarfı (gövde + lehim) **$\le 1{,}80\text{ mm}$** olmak zorundadır.
   - Yüksekliği $1{,}80\text{ mm}$'yi aşan tüm kritik güç elemanları (L1 buck bobini, L3 boost bobini, C33 süperkapasitör, C3 bulk kapasitörleri) `B.Cu` (Bottom) katmanına atanmıştır.

---

## 3. Bloklar Arası Komşuluk ve Bağlantı Koridorları Matrisi (AC #4)

| Arayüz / Koridor | Kaynak Blok $\rightarrow$ Hedef Blok | Taşınan Sinyaller ve Güç Rayları | Akım / Frekans Tipi | Yerleşim ve Koridor Kuralı |
| --- | --- | --- | --- | --- |
| **Giriş Güç Yolu** | `USB-C GIRIS` $\rightarrow$ `AP33772S` | `VBUS`, `GND_PWR`, `USB_CC1`, `USB_CC2` | $20\text{V} / 5\text{A}$ DC, Yüksek Akım | En kısa yoldan doğrudan kalın bakır döküm ($W \ge 2{,}5\text{ mm}$). CC hatları TVS korumasından sonra stubsız AP33772S'e ulaşmalı. |
| **Ön Regülasyon Yolu** | `AP33772S` $\rightarrow$ `TPS55340 PRE-BOOST` | `VBUS_SW` $\rightarrow$ Boost Girişi | $5\text{--}20\text{V} / 3\text{--}5\text{A}$ | Q3 anahtarlama çıkışından L3 boost bobini girişine kısa güç barası; C3 bulk kapasitörü giriş filtresi görevi görür. |
| **Ara Ray ve FB Kenetleme** | `TPS55340` $\leftrightarrow$ `AOZ1284 BUCK` | `V_PRE` ($24\text{--}30\text{V}$), `BOOST_FB` | $3\text{A}$ DC, Hassas Analog FB | D5--U11 FB kenetleme izi (TASK-058, $2{,}585\text{ mm}$) korunmalı. V_PRE rayı üzerinden U5 buck katına doğrudan güç akışı. |
| **Çıkış Güç Hattı** | `TPS55340 / AOZ1284` $\rightarrow$ `LM74801` | `V_PRE` / `V_BUCK` $\rightarrow$ Güç Anahtarı | $0\text{--}30\text{V} / 3\text{A}$ DC | LM74801 Q5 girişine doğrudan kalın hat; HGATE/DGATE hatları gürültüden uzak tutulmalı. |
| **Ölçüm ve Çıkış Yolu** | `LM74801` $\rightarrow$ `INA226` $\rightarrow$ `J4` | `V_OUT` $\rightarrow$ RShunt1 $\rightarrow$ Panel Klemensi | $3\text{A}$ DC, Düşük Empedans | RShunt1'den J4 klemenslerine ultra düşük dirençli doğrudan bara. INA226 duyu hatları RShunt1 altından diferansiyel çift olarak ayrılmalı. |
| **Hızlı Güvenlik Açması** | `INA226` $\rightarrow$ `ESP32-C6` | `INA_ALERT` (GPIO1) | Dijital Kesme (Hızlı Düşen Kenar) | U13 Schmitt tamponu üzerinden ESP32-C6'ya en kısa yoldan; aşırı akımda firmware beklemeden çıkışı keser. |
| **Aktif Çıkış Deşarjı** | `LM74801 / J4` $\leftrightarrow$ `CIKIS DESARJI` | `V_OUT` $\rightarrow$ Q6 $\rightarrow$ R67 (2W), `OUT_DISCHARGE` | $2\text{W}$ Termal Darbe | Deşarj direnci R67'den dönen yüksek ısı akısı RTC kristalinden (Y1) ve INA226'dan en az $15\text{ mm}$ uzakta tutulmalı. |
| **Sistem I2C Veri Yolu** | `ESP32-C6` $\leftrightarrow$ `I2C SEVIYE DONUSTURUCU` | `I2C_SCL_3V3`, `I2C_SDA_3V3` | $400\text{ kHz}$ Fast Mode | MCU GPIO hatlarından Q1/Q2 seviye dönüştürücünün 3.3V tarafına doğrudan, paralel yönlenme. |
| **Genişletilmiş I2C Aygıtları**| `I2C SEVIYE DONUSTURUCU` $\rightarrow$ `RTC / PD / INA` | `I2C_3V3` (RTC, INA) & `I2C_5V` (AP33772S) | $400\text{ kHz}$ Dijital Veri Yolu | Kuzeye 3.3V aygıtları (U4 RTC, U3 INA226), güneye 5V aygıtı (U1 AP33772S) ayrımı; sıfır kesisim. |
| **Ethernet İletişim Hattı** | `ESP32-C6` $\leftrightarrow$ `ETHERNET MEZANIN (J8)` | `UART_TX`, `UART_RX`, `ETH_CFG0`, `ETH_PWR_EN` | $921{,}6\text{ kbps}$ UART, $3{,}3\text{V}$ Mantık | J8'in güney sinyal koridorundan ($y=150..158$) batıya ESP32'ye doğrudan hatlar. Kuzeydeki güç anahtarlama koridorundan $5{,}08\text{ mm}$ uzakta. |
| **Ekran ve Arka Işık** | `ESP32-C6` $\rightarrow$ `J3` & `TFT BACKLIGHT` | `SPI_MOSI`, `SPI_SCLK`, `LCD_CS`, `LCD_DC`, `PWM_BL` | $40\text{ MHz}$ SPI, $1\text{--}10\text{ kHz}$ PWM | SPI veri hatları ekran arkasından doğrudan J3 konnektörüne; PWM_BL hattı Q7 gate pini üzerinden R60 deşarjına. |
| **Panel Enkoderi** | `J9 (Kablo)` $\rightarrow$ `ESP32-C6` | `ENC_A`, `ENC_B`, `ENC_SW` | Düşük Frekans Kullanıcı Girişi | R34--R36 pull-up'larından sonra ESP32 GPIO4--6 pinlerine; anten önünden ve L1/L3 bobinlerinden geçirilmez. |
| **Teşhis Test Noktaları** | Çeşitli Bloklar $\rightarrow$ `TP1-TP14` | Teşhis ve Doğrulama Sinyalleri | DC / Analog / Sayısal | Her test noktası bağlı olduğu düğümün hemen yanında, probun rahat oturacağı boş alanda konumlandırılır. |

---

## 4. Tarihsel Başlangıç Yüzleri ile Hedef Yüzler Karşılaştırması (AC #6)

Aşağıdaki tablo, TASK-065 ile geçici olarak `B.Cu`'ya alınan bloklar ile `PCB_GENEL_YERLESIM_KARARI_20260924.md` uyarınca nihai yerleşimdeki katman hedeflerini tanımlar:

| PCB Grubu | Tarihsel Yüz (TASK-065) | Nihai Hedef Yüz (Genel Karar) | Durum ve Uygulama Planı |
| --- | --- | --- | --- |
| **USB-C GIRIS** (J7, D3, D8, D9, U10, R62, R63) | `B.Cu` (Bottom) | **`F.Cu` (Top)** | TASK-063 ve TASK-008 kapsamında F.Cu sol kenara taşınacaktır. Panel montajı ve J8 Ethernet ile düşeyde $\ge 2{,}0\text{ mm}$ boşluk hedeflenir. |
| **ESP32-C6-MINI-1-H4** (U2, C5-C7, R1-R3, SW1, SW2 vb.) | `B.Cu` (Bottom) | **`F.Cu` (Top)** | TASK-063 ve TASK-008 ile F.Cu'ya taşınacak; anten ana PCB dışına sarkıtılacaktır. LCD izdüşümü dışında kalır. |
| **ETHERNET MEZANIN** (J8, Q8, R17, C10, C20, C21, TP14) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** Modül bottom sol panelde, RJ45 konnektörü kart dışına bakacak şekilde yerleştirilir. |
| **TPS55340 PRE-BOOST** (U11, L3, D4, C23-C29 vb.) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** Yüksek profilli L3 bobini ve termal yük B.Cu'da kalır; U2 anteninden uzaktadır. |
| **AOZ1284 3.3V BUCK** (U5, U6, L1, D2, C12-C19 vb.) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** L1 bobini ve anahtarlama döngüsü B.Cu'da tutulur; LCD yükseklik limitini aşmaz. |
| **LM74801 CIKIS ANAHTARI** (U12, Q5, D6, C30-C32 vb.) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** Çıkış yolu üzerinde B.Cu'da doğrudan yerleşim. |
| **INA226 OLCUM + PANEL CIKISI** (U3, U13, RShunt1, J4 vb.) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** J4 Banana Jack gövdesi ve RShunt1 B.Cu'da; panel klemensine doğrudan bağlanır. |
| **CIKIS DESARJI** (Q4, Q6, D10, R66, R67) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** R67 2W güç direnci B.Cu'da termal olarak izole edilir. |
| **AP33772S PD KONTROLCU** (U1, Q3, R13, TH1, C1-C4 vb.) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** USB-C arkasında B.Cu'da şönt ve giriş korumasıyla birlikte yer alır. |
| **RTC BQ32000 + 1F5** (U4, Y1, C9, C33, R24) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** C33 H-tipi süperkapasitör B.Cu'da; sessiz bölgede konumlandırılır. |
| **I2C SEVIYE DONUSTURUCU** (Q1, Q2, R4-R7) | `B.Cu` (Bottom) | **`B.Cu` (Bottom)** | **Onaylandı.** İki voltaj bölgesi arasında köprü olarak B.Cu'da tutulur. |
| **TFT BACKLIGHT** (Q7, R28, R29, R60) | `F.Cu` (Top) | **`F.Cu` (Top)** | **Onaylandı.** J3 Pin 28/29'un hemen dibinde F.Cu'da kalır (zarf $\le 1{,}80\text{ mm}$). |
| **TFT CONNECTOR J3** (J3 sabit ankraj, C34) | `F.Cu` (Top) | **`F.Cu` (Top)** | **Onaylandı.** Sabit kilitli ankraj $(98{,}00, 109{,}30\text{ mm}, 90^\circ)$ F.Cu'dadır. |
| **ROTARY ENCODER** (J9 tel konnektörü, R34-R36) | `B.Cu` (Staged) | **Taşınabilir Ankraj** | TASK-063 ve TASK-083 kapsamında Ethernet yanında kablo ve lehim erişimine göre son yüzü ve konumu netleşecektir. |
| **TEST NOKTALARI** (TP6-TP8, TP11-TP13) | Dağınık | **B.Cu (Dağınık)** | TASK-084 kapsamında ait oldukları fonksiyonel blokların çıkışlarına dağıtılacaktır. |

---

## 5. Başlangıç Envanteri, Mevcut İzler ve DRC Doğrulaması (AC #5)

- **Genel Envanter Özeti:**
  - Toplam Footprint Sayısı: **143** (137 gruplanmış, 6 grupsuz mekanik ankraj `H1, H2, H3, H4, J3, J9`).
  - Toplam Grup Sayısı: **15**.
  - Toplam Önceden Çizilmiş İz Segmenti: **4**.
- **TASK-058 D5--U11 Feedback İzi Envanteri:**
  - Net: `/USB_PD_CONTROLLER/BOOST_FB` (D5.2 katot çıkışı $\rightarrow$ U11.9 FB girişi).
  - Katman: `B.Cu`.
  - Toplam Uzunluk: **$2{,}584607\text{ mm}$**.
  - Segment Detayları:
    1. UUID `67174655-4b0a-418c-94ae-19de118917f4`: $(65{,}070, 57{,}600) \rightarrow (65{,}370, 57{,}600)$, $L = 0{,}3000\text{ mm}$
    2. UUID `bac123bf-3e8a-4a42-a3d9-e77dc0fb4f54`: $(65{,}370, 57{,}600) \rightarrow (65{,}870, 57{,}100)$, $L = 0{,}7071\text{ mm}$
    3. UUID `ab6f190f-2a38-4051-afdd-29de0667dd97`: $(65{,}870, 57{,}100) \rightarrow (65{,}870, 56{,}640)$, $L = 0{,}4600\text{ mm}$
    4. UUID `dc31f985-bf69-4d4a-b183-b7bf2fcb8a73`: $(65{,}870, 56{,}640) \rightarrow (66{,}987, 56{,}640)$, $L = 1{,}1175\text{ mm}$
- **DRC ve Şematik Uyumluluk Durumu:**
  - Toplam DRC İhlali: **145** (tümü metin kalınlığı, metin yüksekliği, matkap boyutu ve delik aralığına ait tarihsel ihlallerdir; yeni elektriksel veya courtyard ihlali: **0**).
  - Bağlantısız Öğeler (Unconnected Items): **360** (tüm blokların henüz kart içine yerleştirilip genel routing yapılmamasından kaynaklanan beklenen envanterdir).
  - Şematik Eşlik Hataları (Schematic Parity): **0** (PCB netlisti ile KiCad şeması \%100 birebir uyumludur).

---

## 6. Devir ve Sonraki Görevler

Bu derleme belgesi, kalan grup içi ilişkisel yerleşimler (`TASK-081` Backlight, `TASK-082` J3, `TASK-083` Panel Enkoderi, `TASK-084` Test Noktaları) ve ardından gelecek olan toplu kabul görevi (`TASK-085`) için bağlayıcı tasarım kılavuzudur. TASK-085 sonrasında tüm bloklar onaylı zarfları, yönlenme açıları ve hedef yüzleriyle nihai kart yerleşimi (`TASK-063` ve `TASK-008`) görevlerine devredilecektir.
