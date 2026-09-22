# REV_C şema — tamamlanan todo maddeleri (22 Eylül 2026)

`todo.txt` içindeki şema ile ilgili maddeler 22.09.2026'da şema dosyaları, netlist ve git geçmişi üzerinden yeniden kontrol edildi. Tamamlandığı doğrulanan maddeler buraya taşındı ve `todo.txt`'den çıkarıldı. Her maddede kontrolün neye dayandığı yazılıdır.

Kontrol anındaki durum: ERC 0 hata / 2 uyarı (`isolated_pin_label` OUT_EN, `lib_symbol_mismatch` U6 TL431DBZ); ikisi de `todo.txt`'de açık madde olarak duruyor.

## Parça seçimi (todo: "REV_C — TBD PARÇA SEÇİMİ")

### Q5/Q6 (M1/M2) ve Q3/Q4 → SQJB60EP-T1_GE3 (2026-09-21)

Parça dual; her sırt sırta çift tek pakete indi: Q3 = dahili kol (unit A/B), Q5 = çıkış kolu (unit A/B). Q4/Q6 referansları kalktı. Dahili kol handoff 3.2 #2'yi tam karşılıyor. Çıkış kolunda sapma var: RDS(on) 12 mΩ, onaylanan ≤4 mΩ'un 3 katı. Ayrıntı: `design_decisions/reports/sqjb60ep-20260921/result.md`.

Kontrol: Q3 ve Q5 şemada `Power_Supply_Custom:SQJB60EP`, MPN `SQJB60EP-T1_GE3`. Kapanan kısım yalnız şemadaki parça seçimi. **Footprint hâlâ boş**; PowerPAK SO-8L Dual footprint'i ve PCB güncellemesi `todo.txt`'de açık.

### D4 boost Schottky (40–60 V, 3 A, düşük VF) → SX36_R1_00001

Özdisan BOM çalışmasında seçildi (2026-09-21): PANJIT SX36, 60 V / 3 A, SMA. SS34 Özdisan'da yalnız SMC kılıfta olduğu için SMA'da 60 V'luk parça seçildi; V_PRE ~28 V için pay var.

Kontrol: D4 Value `SX36`, MPN `SX36_R1_00001`, footprint `Diode_SMD:D_SMA`.

### C29 sönümleme bulk (47 µF, 35–50 V, ESR 50–100 mΩ, seramik değil) → EEHZA1V470P

Panasonic ZA hibrit polimer: 47 µF / 35 V, ESR 60 mΩ @100 kHz, ripple 1,3 A. Handoff 3.3 #12 (C_DAMP) şartına birebir uyuyor.

Kontrol: C29 `Device:C_Polarized`, MPN `EEHZA1V470P`, footprint `Capacitor_SMD:CP_Elec_6.3x5.8`, pin 1 PD_VOUT'ta.

Aynı bölümdeki **L3 kapanmadı**: şemadaki B82422H1682K000 bir 1210 çip bobin; Isat ≥3 A şartını karşılamıyor.

## Şema / kütüphane (todo: "REV_C — ŞEMA / KÜTÜPHANE")

### Blok A ve Blok B yerleşimi KiCad'de düzenlendi (2026-09-17)

İki satırlı ve planar yerleşim; netlist değişmedi, KiCad'de kontrol edildi.

Not: todo maddesi commit olarak `9c3d219`'u gösteriyordu. Bu nesne depoda yok (geçmiş yeniden yazılmış). İşin karşılığı olan commit `9b1325a` ("powergeneration, poweroutput: Blok A ve B çizimini yeniden düzenle"), maddeyi kapatan commit `7b93e79`. Bloklar daha sonra `usb_pd_controller` sayfasına taşındı.

### AP74502Q sembolü Diodes datasheet'iyle karşılaştırıldı (2026-09-22)

Önceden Diodes datasheet'i indirilemediği için pinout TI LM74502'den alınmıştı. Datasheet (DS47093 Rev. 2) artık `hardware/datasheets/AP74502Q_AP74502HQ.pdf`.

| Pin | Datasheet | Sembol | Sonuç |
|---|---|---|---|
| 1 | EN/UVLO | EN/UVLO | aynı |
| 2 | GND | GND | aynı |
| 3 | NC | NC | aynı |
| 4 | VCAP | VCAP | aynı |
| 5 | VIN | VS | ad farklı, işlev aynı |
| 6 | GATE | GATE | aynı |
| 7 | OVLO | OV | ad farklı, işlev aynı |
| 8 | SRC | SRC | aynı |

Pin numaraları ve işlevleri birebir tutuyor; netlist'e etkisi yok. C31'in VCAP–VIN arasına bağlanması da datasheet'le uyumlu (VCAP–VIN abs max 15 V).

Yeni açık nokta: datasheet paketi "SOT28" (TA8) diye adlandırıyor; şemadaki footprint `Package_TO_SOT_SMD:TSOT-23-8_HandSoldering`. Paket ölçüsü doğrulanmadı; `todo.txt`'ye ayrı madde olarak eklendi.

### C3 footprint'i gözden geçirildi (0805 2,2 µF / 50 V, DC bias altında 1 µF hedefi)

Özdisan BOM çalışmasında (2026-09-21) değerlendirildi. 0805 50 V X7R'de Özdisan stoğunda yalnız 1 µF var; ±%10 toleransla 0,9 µF'a iner ve cSnkBulk ≥1 µF alt sınırını ihlal eder. 2,2 µF / 50 V X5R (CL21A225KB9LNNC) vSafe5V'ta ~2 µF efektif kalıyor (1–10 µF aralığında), bu yüzden 0805 korundu; 1206'ya geçiş gerekmedi.

Kontrol: C3 Value `2u2`, MPN `CL21A225KB9LNNC`, footprint `C_0805_2012Metric`. Bu karar analize dayanıyor, ölçülmedi; prototipte USB_VBUS efektif kapasitesi zaten `todo.txt` "PROTOTİP DOĞRULAMA" bölümünde ölçülecek.

### Tüm güç zinciri tek A3 sayfasında (usb_pd_controller)

PD kontrolcü + VBUS şönt/anahtar, AP74502Q çıkış anahtarı, INA ölçüm + panel çıkışı, TPS55340 ön-boost, AOZ1284 buck ve I2C seviye dönüştürücü. Boş kalan sayfalar (powergeneration, poweroutput, powersensing, CALC_MCU, CALC_USB_C_INPUT, calc_usb_pd_controller) kaldırıldı.

Kontrol: commit `5cb020c`; `usb_pd_controller.kicad_sch` kâğıt boyutu A3; proje 6 sayfa (kök, USB_C_INPUT, USB_PD_CONTROLLER, MCU, USER INTERFACE, USER).

### VBUS dağıtımı tek sayfada toplandı

AP33772S bloğu ile VBUS şönt/çıkış anahtarı birleştirildi; AP74502Q çıkış anahtarı poweroutput'tan, INA228 ölçümü powersensing'ten taşındı. PD_VBUS_SENSED ve SW_OUT sayfa içi yerel etiket oldu.

Kontrol: commit `43ca484` (o aşamada A2; sonra `5cb020c` ile A3'e geçildi).

### U3 INA228AIDGSR → INA226AIDGSR (2026-09-21)

Pin ve paket birebir aynı; lib_symbols önbelleği, U3 alanları, blok başlığı ve PCB'deki Value/MPN güncellendi. Netlist farkı yok, ERC değişmedi. Gerekçe: `design_decisions/reports/ina226-20260921/result.md`.

Kontrol: U3 `Sensor_Energy:INA226`, MPN `INA226AIDGSR`. Firmware sürücüsünün yeniden yazılması `todo.txt` FIRMWARE bölümünde açık.

## Karar bekleyenler (todo: "REV_C — KARAR BEKLEYEN")

### SQJB60EP PowerPAK SO-8L Dual footprint'i çizildi (2026-09-22)

`hardware/libraries/Package_SO_Custom.pretty/Vishay_PowerPAK_SO-8L_Dual.kicad_mod` (yeni kütüphane, `fp-lib-table`'a eklendi). Q3 ve Q5'in Footprint alanı bu footprint'e ayarlandı.

Kaynak: Vishay doc 63817 (`sqjb60ep.pdf` s.9). Todo'da çözülemeyen ölçüler sayfa 300 dpi render edilip ölçü okları ölçülerek çözüldü (ölçek 6,75 ve 7,75 ile doğrulandı). Orijin keep-out merkezi:

- Drain gövdesi 1,73 × 3,99: x ±0,25…±1,98, y −3,075…+0,915 ("0,9150" = drain alt kenarı).
- Üst kulakçık 0,47 × 0,41: x ±1,98…±2,45, drain üst kenarıyla hizalı.
- Orta kulakçık 0,585 × 0,51: x ±1,98…±2,565, y ±0,255.
- S/G pedleri 0,41 × 0,72: x ±0,635/±1,905, y +2,355…+3,075 ("3,0750" = dış kenar, "2,1100" = en dış pedin dış kenarı).

Pin sırası datasheet s.1 ile: 1 S1, 2 G1, 3 S2, 4 G2 (soldan sağa), sol drain D1 = 7-8, sağ drain D2 = 5-6. Eş drain pinleri 6 ve 8, gövdenin yalnız bakır (mask/paste'siz) kopyası; paste ikilenmez, PCB güncellemesinde eksik ped çıkmaz. Courtyard = keep-out 6,75 × 7,75.

Kontrol: netlist farkı yok, alan geometrisi/görünürlüğü değişmedi. PCB güncellemesi todo'da açık.

### OUT_EN için GPIO: RTC I2C'si PD/INA226 bus'ına alındı, OUT_EN = GPIO6 (2026-09-22)

AP33772S (0x52) ve INA226 (0x40, A0=A1=GND) zaten `PD_I2C_SDA_3V3`/`PD_I2C_SCL_3V3` (GPIO19/18) üzerindeydi; ayrı olan tek bus RTC'ninkiydi (GPIO6/7). BQ32000 (0x68) bu bus'a alındı, R25/R26 pull-up'ları kaldırıldı (bus pull-up'ı R4/R7 4k7). Boşalan GPIO6 (MTCK) OUT_EN'e atandı: strapping değil, pad JTAG açılsa bile giriş pini olduğu için çip sürmez. GPIO7 (MTDO) boş, no-connect.

Kontrol: beklenen netlist farkı yalnız `RTC_SCL`/`RTC_SDA` → `PD_I2C_SCL_3V3`/`PD_I2C_SDA_3V3` (+U4.6/U4.5), `OUT_EN` = R57.1 + U2.6, `U2.7` boşta, R25/R26 kalktı. ERC: `isolated_pin_label` (OUT_EN) kapandı, 0 hata / 1 uyarı (TL431).

### U12 EN = OUT_EN AND ~ALERT: U13 74LVC1G08 (2026-09-22)

Sorun: EN düğümünde R27 10k (+3.3V) pull-up ile R58 100k pull-down vardı, OUT_EN buna R57 10k ile bağlıydı. OUT_EN low iken EN ≈ 3,3 × 9,1k / 19,1k = 1,57 V, AP74502Q `VEN_UVLO_RISING` en fazla 1,32 V -> çıkış OUT_EN ile kapatılamıyordu; açılışta GPIO6'nın dahili 45k pull-up'ı da EN'i yukarıda tutuyordu. Yalnız INA226 ALERT çıkışı kesebiliyordu.

Çözüm (kullanıcı kararı): U13 SN74LVC1G08DBVR (Özdisan 503098, stok 5805) INA226 bloğunda; A = OUT_EN, B = INA_ALERT, Y -> `SW_EN` -> U12 EN.

- R61 4k7 OUT_EN pull-down: reset boyunca GPIO6 zayıf pull-up'ıyla 3,3 × 4,7 / 49,7 = 0,31 V (< VIL 0,8 V).
- R27 10k ALERT pull-up'ı olarak kaldı; GPIO3 artık doğrudan ALERT'i okuyor.
- R58 100k EN'de kaldı: 3,3 V yokken LVC Ioff ile çıkış yüksek empedans, EN low (AP74502Q'nun iç 3 µA sink'i de aynı yönde).
- R57 kaldırıldı. C35 100n U13 dekuplajı.
- EN yüksek iken 3,3 V (itme-çekme çıkış), eşiğin 2,5 katı.
- Sembol: `Power_Path_Custom:74LVC1G08`, KiCad `74xGxx:74LVC1G08` gövdesiyle 2,54 mm pinli kompakt kopya (orijinali 28 × 20 mm, blok içine sığmıyordu).

Kontrol: beklenen netlist farkı yalnız `SW_EN` (R58.1, U12.1, U13.4), `INA_ALERT` (R27.2, U13.2, U2.26, U3.3), `OUT_EN` (R61.1, U13.1, U2.6) ve +3.3V/GND'ye U13/C35/R61 eklenmesi. ERC 0 hata / 1 uyarı (TL431). Okunabilirlik denetiminde yeni bulgu yok.

### USB-C giriş koruması yeniden ele alındı; AQ3130E eklenmedi (2026-09-22)

Soru: VBUS'ta SMBJ30A varken ESD için AQ3130E-01ETG (ya da Özdisan muadili) eklenmeli mi? AP33772S datasheet'i (DS46176 Rev.10) ile tekrar bakıldı:

- AP33772S CC1/CC2 mutlak maksimum 34 V ve "VBUS short protection on CC1/CC2 up to 34V": konnektörde VBUS'a komşu CC pinlerinin 28 V'a kısa devresine çip kendisi dayanır. Figure 1'de CC hatlarında TVS/ESD elemanı yok; VBUS'ta yalnız 10 µF var.
- **VBUS: ek eleman gerekmez.** 8 kV IEC kontak deşarjı ~1,2 µC (150 pF); C3 2,2 µF / 50 V X5R (28 V'ta ~0,5 µF efektif) R11 5 mΩ üzerinden VBUS'ta, sıçrama ~2,4 V. SMBJ30A (VRWM 30 V, VC 48,4 V @12,4 A) surge için kalır. 28 V'ta iletmeyip 34 V altında kırpan TVS fiziksel olarak yok; 28 V/3 A tepe ölçümü prototip listesinde.
- **CC hatlarında hata vardı:** CC1/CC2 5,5 V'luk U10 TPD4EUSB30'a bağlıydı. EPR'de CC-VBUS kısa devresinde U10 iletime geçip yanar, AP33772S'nin 34 V dayanımını boşa çıkarır. Orijinal (11.09) tasarımda CC'de 28 V'luk AQ3130E'ler vardı.
- **Rd eksikti:** Figure 1 ve metin CC1/CC2'de harici 5,1 kΩ Rd gösteriyor; dahili Rd değeri hiçbir tabloda yok. Şemada (ve depo geçmişinde) Rd hiç olmamıştı; kaynak sink'i görmez, VBUS açılmazdı.

Uygulanan (kullanıcı onayı, 5 madde):

1. R62/R63 5k1 %1 0402 (HP02WAF5101TCE, Özdisan 603919) CC1/CC2 -> GND.
2. CC1/CC2 U10'dan ayrıldı.
3. D8/D9 SMF30A-TKS (Özdisan 639352, SOD-123FL, VRWM 30 V) CC1/CC2 -> GND, **DNP**. Sıfır biasta ~400 pF (datasheet Fig.6) cReceiver 200–600 pF sınırını AP33772S ile birlikte aşabilir; IEC testi geçmezse ve CC BMC ölçümü uygunsa takılır.
4. VBUS değişmedi; D3 CC1 etiketine yer açmak için 35,56 mm sağa taşındı, açıklaması "600W SMB" olarak düzeltildi. Sayfaya yerleşim notu: D3/C3 J7 dibinde, CC izleri kısa.
5. U10 TPD4EUSB30 (stokta yoktu) -> USBLC6-2SC6 (Özdisan 402751, stok 7375), referans korundu, yalnız D+/D-. Flow-through pin çiftleri (1-6, 3-4) proje sembolünde KiCad 10 `jumper_pin_groups` ile iç bağlı tanımlandı (netlist'te doğrulandı: USB_DM = J7.A7/B7, R3, U10.1, U10.6). VBUS referans pini +3.3V'a (USB_VBUS 28 V olabilir).

Kontrol: beklenen netlist farkı yalnız USB_CC1 (D8.1, J7.A5, R62.1, U1.17), USB_CC2 (D9.1, J7.B5, R63.1, U1.16), USB_DM/DP (U10 pin numaraları), +3.3V'a U10.5, GND'ye R62/R63/D8/D9/U10.2. ERC 0 hata / 1 uyarı (TL431), okunabilirlik 0 bulgu. Betik önce projenin scratchpad kopyasında doğrulandı.

### Ters akım: U12 AP74502Q -> LM74801-Q1 (2026-09-22)

Doğrulama (todo: "AP74502Q'nun ters akım korumasını datasheet'ten doğrula"): **karşılamıyordu.** AP74502Q (DS47093) bir "reverse battery polarity and overvoltage protection controller"dır (LM74502 sınıfı); akım/ileri gerilim algılayan pini yoktur, gate yalnız EN/UVLO, VCAP UVLO ve OV ile kapanır. Çıkış açıkken sırt sırta FET'ler çift yönlü iletir. Ters akım yolu OUT_POS -> şönt -> Q5 -> PD_VBUS_SENSED -> doğrudan adaptör VBUS'ı (Q3 bu yolda değil).

Uygulanan (kullanıcı kararı, seçenek A): U12 = **LM74801QDRRRQ1** (TI SNOSD95C; Özdisan 1044371, stok 912). Referans korundu (`swap_lib`), sembol `Power_Path_Custom:LM74801-Q1` (pinout Table 6-1), footprint `Package_SON:WSON-12-1EP_3x3mm_P0.5mm_EP1.5x2.5mm` (TI DRR0012E land pattern: ped 0,62 x 0,25 @ ±1,39, EP 1,3 x 2,5; KiCad pedleri bunu kapsıyor). EP (RTN) datasheet gereği boşta.

Ortak-source bağlantı (datasheet §9.5.2 / Figure 10-25):

- Q5A (giriş, D1 = PD_VBUS_SENSED) <- **HGATE** (GATE_DRV): yük anahtarı, OV ve EN kesmesi; R54/C30 yavaş açılış ve D6 12 V kırpma korundu. HGATE 55 µA (AP74502Q 60 µA).
- Q5B (çıkış, D2 = SW_OUT) <- **DGATE** (yeni net): ideal diyot. V(A-C) -4,5 mV'ta (-6,4…-1,3) 0,5 µs'de kapanır; 12 mΩ'da ~0,1-0,5 A ters akımda keser, sonra gövde diyotu bloke eder. İleri yönde 177 mV'ta (gövde diyotu) yeniden açılır. LM74800 (lineer regülasyon, sıfır DC ters akım) stokta yok.
- A = OUT = SRC_COMMON, C = SW_OUT, VS/VSNS/SW = V_PRE (CAP = VS + ~13 V; V_PRE pass-through'da ≈ VBUS olduğundan HGATE-OUT ≥ 10 V), CAP-VS = C31 220n, EN = SW_EN (U13), OV = OV_SENSE.
- **OV eşiği**: V(OVR) 1,231 V (1,195-1,267). R55 232k ile 28,9-30,7 V çıkıyordu; 28 V EPR +%5 = 29,4 V'ta yanlış tetikleme riski. R55 **237k** (0402WGF2373TCE, Özdisan 506427): 30,4 V (29,5-31,3 V).
- AP74502Q Özdisan'da stokta değildi; madde tedarik listesinden de düştü.

Kontrol: beklenen netlist farkı DGATE (Q5.4, U12.1), GATE_DRV (Q5.2, D6, R54, U12.8), SRC_COMMON (+U12.2 A, U12.9 OUT), SW_OUT (+U12.12 C), V_PRE (+U12.3/4/10), Net-(U12-CAP) (C31), OV_SENSE (U12.5), SW_EN (U12.6), GND (U12.7), RTN boşta. ERC 0 hata; tek kesişme önceden kabul edilmiş kapı hattı/SRC kesişmesi. V_PRE etiketi ve C32 büyüyen gövdeye yer açmak için sola alındı.

### U12 kılıfı (2026-09-22)

AP74502Q için: Diodes SOT28 önerilen ped 0,45 x 0,9 mm, 0,65 adım, ±1,1 sıra; şemadaki TSOT-23-8_HandSoldering (0,4 mm ped) lehimlenir ama dar, standart TSOT-23-8 uygun olurdu. U12 LM74801'e (WSON-12) geçtiği için madde kapandı.

### C15 hibrit + AOZ1284 kompanzasyonu (2026-09-22)

Datasheet (AOZ1284 Rev 1.0) formülleri: fSW = 500 kHz (R38 100k), VOUT = 0,8 x (1 + 10k2/3k24) = 3,32 V, GEA 200 µA/V, GCS 4,5 A/V. CO ≈ 89 µF (C15 47 µF hibrit + C16 47 µF X5R 1210 @3,3 V ~37 µF + küçük seramikler).

- Eski (R41 12k7, C19 18n): fC ≈ 5 kHz, sıfır 696 Hz (< fC/5), C15 ESR sıfırı 1/(2π·47 µF·60 mΩ) ≈ 56 kHz (fC'nin 10 katı üstünde, ek kutup gerekmez). **Kararlı** ama yavaş: 0,3 A yük basamağında ~100 mV çökme.
- Yeni (kullanıcı kararı): **R41 51k** (0402WGF5102TCE, Özdisan 359892), **C19 15n** (CL05B153KO5NNNC, Özdisan 521922; 12n stokta yok). fC ≈ 20 kHz (< fSW/10), sıfır 208 Hz, ESR sıfırı yine fC üstünde; beklenen çökme ~25 mV. C19'un 18n tedarik sorunu da kapandı.

## Eski ERC ihlalleri (todo: "MEVCUT ERC İHLALLERİ")

### PD_I2C_SDA_5V dangling + R6 pin 2 + Q2 pin 3 bağlı değil (2026-09-17)

Üçü tek hataydı: SDA seviye dönüştürücüsü kopuktu. R6.2 ve Q2.D PD_I2C_SDA_5V'ye bağlandı (SCL tarafı R5/Q1 ile simetrik).

Kontrol (22.09 netlist): `PD_I2C_SDA_5V` = Q2.3 (D), R6.2, U1.4 (SDA); `PD_I2C_SCL_5V` = Q1.3, R5.2, U1.5 (SCL). Simetrik ve bağlı.

### TL431DBZ lib_symbol_mismatch (2026-09-22)

KiCad 10 `Reference_Voltage:TL431DBZ` sembolünde pin uzunlukları 2,54'ten 1,27 mm'ye inmiş ve bir çizgi eklenmiş; pin uç konumları (`at`) aynı. usb_pd_controller'daki `lib_symbols` önbelleği kütüphaneden yenilendi.

Kontrol: netlist farkı yok, U6 render'da değişmeden bağlı. **ERC 0 hata / 0 uyarı** (REV_C'de ilk kez tamamen temiz).

## Depo (todo: "DEPO / LİSANS")

### sym-lib-table'da harici mutlak yol kalmadı

DS1021 kaydı temizlenmişti (2026-09-16). 22.09'da tekrar bakıldı: `hardware/sym-lib-table`'da `/home`, `C:` veya DS1021 geçen kayıt yok.

## Todo'da maddesi olmayan, bu dönemde tamamlanan şema işleri

Ayrıntılar `CHANGES.TXT`'de:

- RTC: RV-3028-C7 + CR2032 → BQ32000DR + Y1 ABS25 kristal + C33 1,5 F süper kapasitör (commit `f0438c3`).
- Özdisan BOM seçimleri tüm sembol alanlarına aktarıldı; onaylı footprint/değer değişiklikleri (commit `f0438c3`). Tablo: `hardware/docs/output/BOM_OZDISAN_REV_C_20260921.xlsx`.
- Ekran: NHD-2.4 → TFT032B018, J3 KLS 30p FPC, boost + CAT4104 yerine Q7/R60 PWM backlight (22.09, henüz commit edilmedi).
