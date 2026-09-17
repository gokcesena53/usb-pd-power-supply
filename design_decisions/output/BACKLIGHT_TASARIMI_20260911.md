# TFT arka ışık tasarımı — 11 Eylül 2026

Uygulama: USER INTERFACE sayfası. Eski Q5/R30–R33 ağı kaldırıldı; R28/R29 PWM girişinde yeniden kullanıldı. Kaynaksız BACKLIGHT_3V0 adı gerçek beslemeyi ifade eden BACKLIGHT_4V2 ile değiştirildi. Bu gerilim ekranın logic beslemesine uygulanmaz.

## Gereksinim ve mimari

NHD-2.4-240320AF-CSXP datasheet sayfa 6: nominal arka ışık akımı toplam 160 mA, maksimum 200 mA; 160 mA'de Vf 2.7–3.4 V, tipik 3.0 V. J3.38 ortak anot, J3.34–37 dört ayrı katottur. Gerilim değeri referanstır; LED akımı sınırlandırılmalıdır.

+3.3V → U7 TPS61023DRLR senkron boost → BACKLIGHT_4V2 → J3.38 → dört LED kolu → U8 CAT4104V-GT3 bağımsız akım kanalları → GND.

U7 gerilimi, U8 LED akımını regüle eder. U8 EN/PWM mevcut TFT_BL_PWM sinyalini alır. Ortak katot MOSFET'i yerine dört ayrı akım kanalı kullanılması akım paylaşımını LED Vf farklılıklarından ayırır.

## Hesap ve parça seçimleri

| İşlev | Eleman | Seçim / hesap |
|---|---|---|
| Boost | U7 | TPS61023DRLR, SOT-563; VIN=+3.3V, EN=+3.3V |
| FB üst | R44 | 604 kΩ, %0.1, 0402 |
| FB alt | R45 | 100 kΩ, %0.1, 0402 |
| Çıkış | BACKLIGHT_4V2 | Vout=0.595×(1+604/100)=4.1888 V nominal PWM modu |
| DC tolerans hesabı | R44/R45 + Vref | 580–610 mV referans sınırlarıyla yaklaşık 4.076–4.302 V; ripple/transient dahil değil |
| Bobin | L2 | 2.2 µH, Würth 74438357022, MAPI-4030 |
| Giriş kapasitörü | C20 | 22 µF nominal / 16 V / X7R / 1206; 3.3 V altında etkili ≥10 µF şartı |
| Çıkış kapasitörü | C21 | 22 µF nominal / 16 V / X7R / 1206; 4.3 V altında etkili 4–30 µF şartı |
| LED sürücü | U8 | CAT4104V-GT3, SOIC-8 |
| Akım ayarı | R46 | 3.24 kΩ, %0.1, 0402 |
| U8 bypass | C22 | 100 nF / 16 V / 0402 |
| PWM seri direnç | R28 | 100 Ω / 0402 |
| PWM pull-down | R29 | 100 kΩ / 0402 |

CAT4104 datasheet'in ampirik bağıntısı R[kΩ]=117×I[mA]^(-0.978)+0.05 kullanıldı. R46=3.24 kΩ için yaklaşık 39.77 mA/kanal ve 159.09 mA toplam elde edilir. Bu nominal tahmindir; entegre akım toleransı ve sıcaklık etkisi dahil değildir. RSET üzerinde yaklaşık 1.2 V, dirençte yaklaşık 0.444 mW bulunur. %0.1 direnç, toplam LED akımının %0.1 hassasiyetli olduğu anlamına gelmez.

En düşük hesaplanan rail ile en yüksek LED Vf arasındaki pay 4.076−3.4=0.676 V'tur. CAT4104 uygulama bölümü 400 mV akım regülasyon payı ister. Kalan yaklaşık 276 mV pay, iletken/konnektör düşümü ve ripple için ayrılır; açılış overshoot ve yük adımı ölçülmelidir. 4.2 V, LED jonksiyonuna zorla uygulanan gerilim değildir: LED Vf'si dışındaki gerilim CAT4104 üzerinde düşer.

## Boost boyutlandırması

TPS61023 desteklenen L aralığı 0.37–2.9 µH. 2.2 µH ±%20 bu aralığa uyar. Nominal ideal duty 1−3.3/4.1888 ≈%21.22. Frekans yaklaşık 1 MHz tipiktir; datasheet bu koşullar için garantili alt frekans sınırı vermediğinden aşağıdaki ripple hesabı tipik frekansla yapılmıştır.

Muhafazakâr hesap senaryosu: VIN=3.0 V, VOUT=4.302 V, IOUT=0.20 A, verim %85 mühendislik varsayımı, L=2.2×0.7=1.54 µH. Sonuç: D≈%30.26; IL_avg≈0.337 A; ΔIL≈0.590 A; IL_peak≈0.632 A. Hafif yükte PFM/DCM davranışı nedeniyle bu CCM bağıntıları dalga şeklinin garantisi değildir.

74438357022 güncel üretici çiziminde Isat %10 düşüm için 4.6 A tipik, %30 düşüm için 9.2 A tipik, DCR 26 mΩ maksimumdur. Normal yük hesabına geniş pay sunar; bu tek başına bütün arıza koşullarının doğrulanması değildir. Bobin üretici tarafından verilen 4030 footprint ailesiyle eşleştirildi.

TPS61023 çıkışında efektif en az 4 µF gerekir. Seçilen efektif 4–30 µF aralığı, datasheet'in >40 µF için önerdiği feed-forward ekini gerektirmeyen tasarım hedefidir. Kesin C20/C21 MPN'leri ve DC-bias eğrileri henüz seçilmedi; bu alan satın alma/üretim öncesi tamamlanmalıdır. Nominal 22 µF'nin bias altında korunacağı varsayılmadı. Kompanzasyon entegre içindedir; fiziksel yük adımı testi gereklidir.

## PWM, açılış ve güç bütçesi

U8 EN/PWM VIH≥1.3 V ve VIL≤0.4 V ister. ESP32 3.3 V çıkışı uygundur. R29, MCU pini yüksek empedanstayken arka ışığı kapalı tutar. R28 giriş kenarı/paraziti için seridir. U7 EN doğrudan +3.3V olduğundan rail MCU komutundan bağımsız kurulur; parlaklık U8 üzerinden kontrol edilir. Ekran kapalıyken boost rail gerilimli kalır.

Firmware önerisi: 1 kHz, %1–99 duty; tam kapalı %0, tam açık %100. %1'de yüksek süre 10 µs, datasheet'in 5 µs minimumunu karşılar; %99'da düşük süre 10 µs, 1 µs minimumdan uzundur. Firmware bu çalışmada değiştirilmedi.

Tam parlaklıkta LED gücü tipik yaklaşık 3.0×0.159≈0.477 W. U8 kanal kaybı yaklaşık (4.189−3.0)×0.159≈0.189 W; IC besleme akımı buna eklenir. Vf=2.7 V ve yüksek rail ile kayıp artar. Datasheet SOIC-8 için verdiği 160°C/W değerini iki inç kare ısı yayma bakırı koşulunda belirtir; boş PCB için bu termal direnç garanti edilemez.

Nominal rail, 159 mA LED ve 6 mA sürücü bütçesiyle, %85 boost verimi varsayımı altında +3.3V girişinden yaklaşık 247 mA gerekir. 200 mA çıkış tasarım noktasında 3.0 V giriş senaryosu yaklaşık 337 mA verir. Önceki 0.4 A elektronik yük tahminine muhafazakâr olarak eklenirse yaklaşık 0.74 A; mevcut 1 A buck hedefinin altındadır. Yük tahminindeki olası çift sayım ve gerçek Wi-Fi/PWM geçişleri prototipte kontrol edilir. Ana 5 A çıkış yükü bu devreden geçmez.

## Pin bağlantıları

| Entegre pin | Bağlantı |
|---|---|
| U7.1 FB | R44/R45 orta noktası |
| U7.2 EN, U7.3 VIN | +3.3V |
| U7.4 GND | GND |
| U7.5 SW | L2.1, yerel BL_BOOST_SW |
| U7.6 VOUT | BACKLIGHT_4V2, C21+, R44 üst, U8 VIN, J3.38 |
| U8.1–4 LED1–4 | J3.34–37, ayrı BL_K1–4 netleri |
| U8.5 GND | GND |
| U8.6 EN_PWM | TFT_BL_PWM → R28; R29 pull-down |
| U8.7 VIN | BACKLIGHT_4V2, C22 bypass |
| U8.8 RSET | R46 → GND |

## Doğrulama ve yerleşim

Son ERC: **0 hata, 0 uyarı**. Yeni devrede 12 kritik net grubu kontrol edildi. Arka ışık değişikliği dışında önceki elemanların birbirine bağlantıları korundu. Mevcut PD sayfasındaki #FLG01'in eksik yatay besleme bağlantısı da geri bağlandı. ERC kontrolleri kapatılmadı.

PCB henüz boş. C20/U7/L2 ve U7/C21/GND yüksek frekans döngüleri kısa tutulmalı; SW alanı küçük olmalı. R44/R45 FB hattı SW'den uzak, çıkış kapasitöründen alınmalı. R46 dönüşü U8 GND'ye temiz bir yoldan gitmeli. Sürücü ısısı, her kol akımı, ilk açılış, %0/%1/%50/%100 PWM ve 3.3 V rail yük adımı prototipte doğrulanmalıdır.

Kaynaklar: [TPS61023](https://www.ti.com/lit/ds/symlink/tps61023.pdf), [CAT4104](https://www.onsemi.com/download/data-sheet/pdf/cat4104-d.pdf), [Würth 74438357022](https://www.we-online.com/components/products/datasheet/74438357022.pdf), yerel NHD-2.4-240320AF-CSXP datasheet sayfa 4–6.

[Güncel ERC](<C:/Users/Slayer/Desktop/masaüstü güç kaynağı/reports/backlight-20260911/erc.rpt>) · [Bağlantı kontrol kaydı](<C:/Users/Slayer/Desktop/masaüstü güç kaynağı/reports/backlight-20260911/validation.json>)
