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

## Eski ERC ihlalleri (todo: "MEVCUT ERC İHLALLERİ")

### PD_I2C_SDA_5V dangling + R6 pin 2 + Q2 pin 3 bağlı değil (2026-09-17)

Üçü tek hataydı: SDA seviye dönüştürücüsü kopuktu. R6.2 ve Q2.D PD_I2C_SDA_5V'ye bağlandı (SCL tarafı R5/Q1 ile simetrik).

Kontrol (22.09 netlist): `PD_I2C_SDA_5V` = Q2.3 (D), R6.2, U1.4 (SDA); `PD_I2C_SCL_5V` = Q1.3, R5.2, U1.5 (SCL). Simetrik ve bağlı.

## Depo (todo: "DEPO / LİSANS")

### sym-lib-table'da harici mutlak yol kalmadı

DS1021 kaydı temizlenmişti (2026-09-16). 22.09'da tekrar bakıldı: `hardware/sym-lib-table`'da `/home`, `C:` veya DS1021 geçen kayıt yok.

## Todo'da maddesi olmayan, bu dönemde tamamlanan şema işleri

Ayrıntılar `CHANGES.TXT`'de:

- RTC: RV-3028-C7 + CR2032 → BQ32000DR + Y1 ABS25 kristal + C33 1,5 F süper kapasitör (commit `f0438c3`).
- Özdisan BOM seçimleri tüm sembol alanlarına aktarıldı; onaylı footprint/değer değişiklikleri (commit `f0438c3`). Tablo: `hardware/docs/output/BOM_OZDISAN_REV_C_20260921.xlsx`.
- Ekran: NHD-2.4 → TFT032B018, J3 KLS 30p FPC, boost + CAT4104 yerine Q7/R60 PWM backlight (22.09, henüz commit edilmedi).
