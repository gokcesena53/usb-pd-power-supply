# KiCad 10 PCB Layout — Adım Adım Uygulama Rehberi

Proje: `masaüstü güç kaynağı.kicad_pcb`  
Başlangıç: yaklaşık **93 × 60 mm**, **4 katman**

Sırayı bozma: mekanik → kurallar → 5 A yolu → Kelvin → buck → backlight → USB → sinyaller → zone → DRC.

## 1. Başlangıç ve mekanik kilitleme

1. KiCad Project Manager'dan PCB dosyasını aç.
2. `File → Save As…` ile çalışma kopyası oluştur veya Git'e kaydet.
3. Sağdaki `Appearance` panelinden `Ratsnest` ve `Board Shape` görünürlüğünü aç.
4. Grid'i **0.25 mm** yap.
5. `Edge.Cuts` katmanını seç; `Inspect → Measure Tool` ile kartı ölç.
6. USB-C ve RJ45'in sol kenarda, ESP32 anteninin sağ kenarda olduğunu doğrula. LCD yerleşimi ve kart ölçüsü için bkz. `KART_DIS_HATTI_LCD_20260924.md`; encoder panele monte edilir.
7. ESP32 anteninin önü ve altı için boş bölge bırak.
8. J1, J4, ESP32, TFT konektörü, encoder ve montaj deliklerini seç; `E → Locked` ile kilitle.
9. `Inspect → Design Rules Checker → Run DRC` çalıştır ve başlangıç durumunu kaydet. Routing başlamadığı için unconnected uyarıları normaldir.

## 2. Dört katmanı ayarla

1. `File → Board Setup…` aç.
2. `Board Stackup → Physical Stackup` seç.
3. Copper layer sayısını **4** yap.
4. Katman görevleri:
   - `F.Cu`: bileşenler, kritik sinyaller ve ana güç polygonları
   - `In1.Cu / GND_PLANE`: kesintisiz GND
   - `In2.Cu / POWER_PLANE`: güç dağıtımı
   - `B.Cu`: yardımcı sinyaller ve GND dolgu
5. Başlangıç kalınlığını 1.6 mm bırak. Üreticiden gerçek core/prepreg/Dk bilgisi gelince stackup'ı güncelle.
6. `Apply → OK` seç.

## 3. Net class'ları oluştur

1. `File → Board Setup → Design Rules → Net Classes` aç.
2. Şu sınıfları ekle:

| Sınıf | İz | Clearance | Via / delik |
|---|---:|---:|---:|
| `SIGNAL` | 0.20 mm | 0.15 mm | 0.60 / 0.30 mm |
| `POWER_3V3` | 0.60 mm | 0.20 mm | 0.70 / 0.35 mm |
| `MAIN_5A` | polygon | 0.25 mm | 1.00 / 0.50 mm |
| `USB_DIFF` | stackup hesabı | üretici hesabı | mümkünse via yok |

3. Netleri ata:
   - `MAIN_5A`: `USB_VBUS`, `PD_VBUS_SENSED`, `PD_VOUT`, `OUT_POS`
   - `POWER_3V3`: `+3.3V`, `BACKLIGHT_4V2`
   - `USB_DIFF`: USB `D+` ve `D-`
   - Diğer sinyaller: `SIGNAL`
4. `Apply → OK` seç.

`MAIN_5A` için genişlik tek bir ince track değeriyle belirlenmemeli. Kısa ve geniş polygon kullan; nihai sıcaklık artışını gerçek bakır kalınlığıyla doğrula.

## 4. L2 GND düzlemini oluştur

1. `In1.Cu / GND_PLANE` katmanını seç.
2. `Place → Add Filled Zone` seç.
3. Net olarak `GND` seç.
4. Kart dış hattını takip eden zone çiz; son noktada çift tıkla.
5. `B` tuşuyla doldur.
6. ESP32 anten alanına `Place → Add Rule Area` ekle; bu bölgede copper pour, track ve via'yı yasakla.
7. `B` tuşuna tekrar bas.

Kontrol: L2 tek parça GND olmalı ve anten altında bakır bulunmamalı.

## 5. Ana 5 A yolunu çiz

Akış: `J1 USB_VBUS → R11 → Q4/Q3 → RShunt → OUT_POS → J4`

1. `F.Cu` katmanını seç.
2. Kilitli konektörleri oynatmadan R11, Q4/Q3 ve RShunt'ı kısa bir güç hattı oluşturacak şekilde `M` ile hizala.
3. `Place → Add Filled Zone` ile `USB_VBUS` netine bağlı yerel polygonu J1'den R11'e çiz.
4. Şematikteki net adlarını izleyerek R11 → Q4/Q3 → RShunt için ayrı doğru-net polygonları çiz.
5. RShunt çıkışından `OUT_POS` polygonunu J4'e götür.
6. Pad girişlerinde dar boyun bırakma.
7. L3'te paralel güç alanı gerekirse aynı nete bağlı zone oluştur.
8. L1-L3 geçişinde tek via kullanma; akım yolunun enine yayılmış çoklu via yerleştir. Routing sırasında `V` via ekler.
9. `B` ile zone'ları doldur.
10. `Highlight Net` aracıyla her netin sürekliliğini kontrol et.

Kontrol: J1-J4 arasında ince sinyal izi şeklinde 5 A bağlantısı kalmamalı; Q3/Q4 ve shunt çevresinde ısı yayacak bakır olmalı.

## 6. INA228 Kelvin bağlantılarını çiz

1. RShunt'ın giriş ve çıkış güç padlerini belirle.
2. INA228 `IN+` izini doğrudan shunt giriş padinin kenarından başlat.
3. `IN−` izini doğrudan shunt çıkış padinin kenarından başlat.
4. İki izi kısa, yakın ve benzer geometride INA228'e götür.
5. Yük akımının bu sense izlerinden geçmesine izin verme.
6. İzleri buck `LX_SW`, backlight `SW` ve MOSFET güç yollarından uzak tut.
7. INA228 bypass kapasitörünü besleme pinine çok yakın bağla; GND padinden L2'ye kısa via kullan.

Kontrol: `Highlight Net` ile IN+ ve IN− ayrı ayrı seçildiğinde her biri yalnızca kendi shunt padine ulaşmalı.

## 7. AOZ1284PI buck bölümünü route et

1. U buck, D2, L1, giriş ve çıkış kapasitörlerini sıkı bir grup halinde tut.
2. `PD_VOUT → giriş kapasitörü → VIN/EP` bağlantısını kısa ve geniş çiz.
3. Exposed pad'i **VIN/PD_VOUT** ağına bağla. GND via bağlama.
4. Pin 1 `LX → D2 → GND` çevrimini en küçük alanla çiz.
5. `LX → L1 → çıkış kapasitörü → +3.3V` yolunu kısa ve geniş çiz.
6. `LX_SW` bakırını gereksiz büyütme.
7. BST kapasitörünü pin 2 BST ile pin 1 LX'in hemen yanına bağla.
8. FB divider sense noktasını çıkış kapasitörünün pozitif padinden al.
9. FB ve COMP izlerini LX, D2 ve L1'den uzak geçir.
10. SS, FSW ve EN direnç/kapasitörlerini kendi pinlerine kısa bağla.
11. `B` ile doldur.

Pin kontrolü: `1=LX, 2=BST, 3=GND, 4=FSW, 5=COMP, 6=FB, 7=SS, 8=EN, EP=VIN`.

## 8. Backlight güç katını route et

1. U7, L2, C20 ve C21'in yakınlığını kontrol et.
2. `+3.3V → C20 → U7/L2 giriş` bağlantısını kısa tut.
3. U7 switching pininden L2'ye giden bakırı küçük tut.
4. `L2 → C21 → BACKLIGHT_4V2` yolunu kısa ve geniş çiz.
5. Feedback'i C21 pozitif padinden al; SW alanından uzak geçir.
6. PWM/EN hattını SW hattına uzun süre paralel götürme.

## 9. USB D+ ve D− çiftini route et

1. Üretici stackup'ı kesinleşince 90 ohm diferansiyel hat genişliği/aralığını üreticinin hesaplamasıyla belirle.
2. Bu değerleri `USB_DIFF` sınıfına gir.
3. J1 → U9 ESD koruma elemanı arasını önce çiz.
4. U9 → ESP32 USB pinleri arasını diferansiyel çift aracıyla birlikte çiz.
5. F.Cu üzerinde kal; mümkünse via kullanma.
6. Altında kesintisiz L2 GND referansı bulunsun.
7. 45 derece/yumuşak dönüş kullan; çift aralığını sabit tut.
8. Hatları buck, backlight ve MOSFET switching bölgelerinden uzak geçir.

## 10. Düşük hızlı sinyalleri tamamla

1. Önce tüm IC bypass kapasitörlerini route et: besleme pini → kapasitör → kısa GND via.
2. ESP32 +3.3V bağlantılarını tamamla.
3. RTC SDA/SCL ve battery-cell hatlarını route et.
4. TFT SPI hatlarını doğrudan ve düzenli götür.
5. Encoder A/B/switch hatlarını route et.
6. Boot/reset hatlarını tamamla.
7. GND, PD_VOUT, +3.3V ve OUT_POS test noktalarını erişilebilir bırak.

## 11. L3 güç ve L4 GND zone'larını ekle

1. `In2.Cu / POWER_PLANE` katmanında yalnız gerekli güç netleri için ayrı local zone'lar oluştur.
2. Farklı net zone'ları arasında kural clearance'ını koru.
3. `B.Cu` üzerinde GND zone oluştur.
4. Kart çevresine ve switching bloklarının GND dönüşlerine stitching via'ları ekle.
5. Genel başlangıç aralığı 2–3 mm olabilir; anten keepout içine via koyma.
6. `B` ile tüm zone'ları doldur.

## 12. Bağlantıları ve DRC'yi bitir

1. `Inspect → Design Rules Checker → Run DRC` seç.
2. Önce `Unconnected Items` listesini aç.
3. Her satıra çift tıkla; eksik bağlantıyı route et.
4. `B` ile zone doldur ve tekrar DRC çalıştır.
5. Ratsnest çizgisi ve unconnected sayısı **0** olana kadar devam et.
6. Hataları şu sırayla düzelt:
   1. Short circuit
   2. Clearance violation
   3. Unconnected
   4. Track/via outside board
   5. Anten keepout ihlali
   6. Courtyard overlap
   7. Silkscreen over pad/copper
   8. Silkscreen edge ve text-size uyarıları
7. Bir uyarıyı `Exclude` etmeden önce gerçek hata olmadığını doğrula.

Hedef: **0 short, 0 clearance, 0 unconnected, 0 courtyard ve 0 edge hatası.**

## 13. 3D ve üretim kontrolü

1. `View → 3D Viewer` veya `Alt+3` aç.
2. USB-C, J4, TFT, encoder ve pil yuvasının mekanik erişimini kontrol et.
3. ESP32 anten önündeki boşluğu kontrol et.
4. Son DRC'yi çalıştır.
5. `File → Fabrication Outputs → Gerbers` ile dört bakır, mask, silk ve Edge.Cuts katmanlarını plot et.
6. `Generate Drill Files` ile PTH/NPTH delikleri üret.
7. `File → Fabrication Outputs → Component Placement` ile `.pos` dosyası üret.
8. Şematik editöründe `Tools → Generate BOM` ile BOM üret.
9. Gerber Viewer'da Edge.Cuts, drill, mask ve iç katmanları görsel olarak incele.

## Her oturumda kısa çalışma döngüsü

1. Bir blok seç.
2. Yerleşimini kontrol et.
3. Kritik güç/sinyal yolunu route et.
4. GND dönüşünü kontrol et.
5. `B` ile doldur.
6. DRC çalıştır.
7. Hataları düzelt.
8. Kaydet.

## Şimdi yapılacak ilk iş

1. Yalnız `J1 → R11 → Q4/Q3 → RShunt → J4` 5 A yolunu çiz.
2. Sonra RShunt → INA228 Kelvin hatlarını çiz.
3. Bu iki bölümün DRC kontrolü tamamlandıktan sonra AOZ1284PI buck'a geç.
