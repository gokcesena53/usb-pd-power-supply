# Tüm şematik bağlantı kontrolü ve mühendislik açıklaması

**Tarih:** 11 Eylül 2026  
**Proje:** masaüstü güç kaynağı — KiCad 10  
**Kapsam:** USB-C giriş, USB-PD denetleyici, 3,3 V buck, MCU, RTC, encoder, TFT/backlight, güç ölçümü ve iki çıkış konektörü

## Sonuç

Kök şemadan yeniden üretilen netlistte **102 bileşen, 361 pin ve 102 net** denetlendi. KiCad ERC sonucu **0 hata / 0 uyarı**dır. Datasheet ve tasarım amacı açısından kritik görülen **89 pin-net eşleşmesinin tamamı geçti**. Netsiz kütüphane pini ve istem dışı tek elemanlı net bulunmadı. USB 3.x ve kullanılmayan yardımcı fonksiyonlara ait **32 pin bilinçli NC** bırakılmıştır.

Bu sonuç şematik bağlantı doğruluğunu gösterir. PCB dosyası boş olduğundan yerleşim, akım taşıma, diferansiyel empedans, termal tasarım, creepage/clearance ve DRC henüz doğrulanamaz.

## Son kontrolde düzeltilen gerçek hatalar

| Konum | Önceki durum | Yapılan düzeltme | Elektriksel sonuç |
|---|---|---|---|
| USB-PD, `#FLG01` | `PD_VBUS_SENSED` güç bayrağı yatay telden kopuktu | Tel pin üzerine bağlandı | VCC güç kaynağı ERC tarafından doğru görülüyor |
| Backlight, L2 | Tel L2'nin üzerinden kesintisiz geçiyor, bobin devre dışında kalıyor ve U7 SW doğrudan +3.3V'a bağlanıyordu | Tel L2'nin iki padinde kesildi | `+3.3V → L2 → BL_BOOST_SW/U7.5` seri yolu oluştu; SW-giriş kısa devresi kaldırıldı |
| Backlight, R28 | Tel R28'in üzerinden kesintisiz geçiyor, 100 Ω seri direnç devre dışında kalıyordu | Tel R28'in iki padinde kesildi | `TFT_BL_PWM → R28 → U8.EN_PWM`; R29 aynı düğümden GND'ye pull-down |
| USB ESD sayfası | Eklenen elemanlar 0,254 mm kadar 50 mil grid dışında kalmıştı | 28 öğe 1,27 mm gride oturtuldu | Görsel/bağlantı tutarlılığı düzeltildi |
| Güç ölçümü RShunt | 5 mΩ / 1 W çıkış şöntüne 01005/0402 sınıfı footprint atanmıştı | `R_2512_6332Metric` yapıldı | Güç şöntü için fiziksel olarak uygulanabilir geçici paket sağlandı |

RShunt için 2512 seçimi geçicidir. Üretimden önce 5 mΩ, en az 1 W, düşük TCR ve tercihen Kelvin ölçüme uygun kesin MPN/footprint seçilmelidir.

## Blokların çalışma mantığı ve bağlantı kontrolü

### 1. USB-C giriş ve ESD

J1 yalnız USB 2.0 ve USB-PD sink işlevi için kullanılır. A/B yüzlerindeki VBUS pinleri `USB_VBUS`, D+ pinleri `USB_DP`, D− pinleri `USB_DM`, CC pinleri `USB_CC1/USB_CC2`, bütün GND ve shield uçları GND üzerindedir. SuperSpeed TX/RX ve SBU pinleri bilinçli NC'dir.

| Koruma | Bağlantı | Kontrol sonucu |
|---|---|---|
| U9 TPD4E05U06-Q1 pin 1 | USB_DP | Geçti |
| U9 pin 2 | USB_DM | Geçti |
| U9 pin 3 ve 8 | GND | Geçti |
| D3 AQ3130E | USB_VBUS ↔ GND | Geçti |
| D4 AQ3130E | USB_CC1 ↔ GND | Geçti |
| D5 AQ3130E | USB_CC2 ↔ GND | Geçti |

U9'un 5,5 V çalışma gerilimli düşük kapasitans kanalları yalnız D+/D− için kullanıldı. CC hatlarına 28 V çalışma gerilimli çift yönlü TVS kondu; böylece AP33772S'nin CC pinlerinde belirtilen yüksek gerilim kısa-devre dayanımı düşük gerilimli bir TVS ile bozulmadı. D3 ESD'yi toprağa yönlendirir; 39–44 V civarı datasheet klemp seviyesi AP33772S mutlak maksimumlarının üstünde olduğundan uzun süreli surge garantisi değildir.

### 2. USB-PD denetleyici ve ana güç yolu

Güç akışı `J1/USB_VBUS → R11 5 mΩ → PD_VBUS_SENSED → Q4/Q3 back-to-back MOSFET → PD_VOUT` şeklindedir. Q3 ve Q4 ortak source ve ortak `PD_GATE` kullanır; bu topoloji kapalı durumda iki yöndeki gövde diyodu iletimini engeller. AP33772S PWR_EN, R12 üzerinden iki gate'i sürer.

| AP33772S bağlantısı | Net / eleman | Kontrol sonucu |
|---|---|---|
| U1.1 ISENP | USB_VBUS | Geçti |
| U1.24 VCC | PD_VBUS_SENSED | Geçti |
| U1.16 / U1.17 | USB_CC2 / USB_CC1 | Geçti |
| U1.4 / U1.5 | 5 V tarafı SDA/SCL | Geçti |
| U1.20 V5V | PD_5V, C4 bypass | Geçti |
| U1.22 VOUT | R13 üzerinden PD_VOUT algılama | Geçti |
| U1.23 PWR_EN | R12 üzerinden PD_GATE | Geçti |
| U1.3 ve exposed GND | GND | Geçti |

Q1/Q2 BSS138 dönüştürücüleri 5 V I²C ile 3,3 V I²C alanlarını ayırır; gate'leri +3.3V, source'ları 3,3 V tarafında, drain'leri 5 V tarafındadır. İki tarafta da pull-up vardır. PD interrupt hattı MCU'ya `PD_INT_3V3` olarak ulaşır.

**Açık risk:** IRF7855'in düşük RDS(on) değeri esas olarak 10 V gate sürüşü için verilir. AP33772S'nin gerçek gate seviyesiyle kayıp ve SOA doğrulanmadan bu MOSFET üretim seçimi sayılamaz.

### 3. AOZ1284PI 3,3 V buck

Bu kademe yalnız iç elektroniği besler. Ana çıkışın 5 A akımı bu buck'tan geçmez. Tasarım 5–28 V giriş, yaklaşık 1 A tasarım yükü ve +3.3V çıkış içindir.

| AOZ1284PI pini | Şematik bağlantı | Datasheet amacı | Sonuç |
|---|---|---|---|
| 1 LX | `LX_SW`; D2 ve L1 | Anahtarlama düğümü | Geçti |
| 2 BST | C17 100 nF; diğer ucu LX | Bootstrap | Geçti |
| 3 GND | GND | Kontrol toprağı | Geçti |
| 4 FSW | R38 100 kΩ → GND | Frekans ayarı | Geçti |
| 5 COMP | R41 12,7 kΩ seri C19 18 nF → GND | Döngü kompanzasyonu | Geçti |
| 6 FB | R39 10 kΩ / R40 3,20 kΩ bölücü | 0,8 V geri besleme | Geçti |
| 7 SS | C18 10 nF → GND | Soft-start | Geçti |
| 8 EN | TL431 tabanlı 2,495 V clamp | EN, 6 V mutlak sınırın altında | Geçti |
| EP / pad 9 VIN | PD_VOUT, C12/C13/C14 | VIN ve termal pad; GND değildir | Geçti |

R38 için datasheet bağıntısı yaklaşık 476 kHz verir; datasheet tablosu 100 kΩ için yaklaşık 500 kHz gösterir. 22 µH ile hesaplanan ripple 5 V'ta yaklaşık 0,107 A, 28 V'ta yaklaşık 0,278 A'dır. −%20 L köşesinde 28 V ripple yaklaşık 0,347 A ve 1 A yükte peak yaklaşık 1,174 A olur. L1 için en az 2 A Isat ve 1,5 A Irms hedefi konmuştur. D2 gereksinimi 60 V / 2 A Schottky'dir.

FB bölücüsü `0,8 × (1 + 10k/3,2k) = 3,300 V` verir. C18 için soft-start nominal yaklaşık 3,2 ms, datasheet akım aralığıyla yaklaşık 2,67–4 ms'dir. EN doğrudan 28 V'a bağlanmamıştır; R43 ve U6 ile sınırlandırılır. Bu ağ harici UVLO sağlamaz.

**Açık seçimler:** L1 ve D2 kesin MPN/footprint; giriş/çıkış MLCC'lerin 28 V ve 3,3 V DC-bias altındaki etkili kapasitesi; kompanzasyonun yük adımı ve loop ölçümü.

### 4. MCU, USB veri ve programlama

ESP32-C6-WROOM-1 besleme pinleri +3.3V, bütün GND/EP pinleri GND'dir. USB D+ ve D−, sırasıyla R2/R3 22 Ω seri direnç üzerinden modülün GPIO13/USB_D+ ve GPIO12/USB_D− pinlerine gider. Boot/reset pull-up ağları ve UART servis konektörü bağlıdır.

TFT kontrolü: GPIO4=SCLK, GPIO5=MOSI, GPIO10=CS, GPIO11=DC, GPIO15=RST, GPIO1=TFT_BL_PWM. Encoder: GPIO22=A, GPIO23=B, GPIO21=SW. INA228 alert GPIO3'e, RTC interrupt GPIO2'ye, PD interrupt GPIO20'ye gider.

Boot strap olarak kullanılan ESP32 pinlerine bağlanan çevre birimlerinin reset anındaki seviyeleri prototipte kontrol edilmelidir. Bu bir bağlantı kopukluğu değildir; açılış davranışı doğrulamasıdır.

### 5. RTC ve pil

RV-3028-C7 VDD=+3.3V, VSS=GND, SDA/SCL I²C hattında ve INT açık-kollektör pull-up ile MCU'ya bağlıdır. VBACKUP, CR2032 pozitifinden R22 1 kΩ üzerinden gelir; C10 100 nF ile bypass edilir. EVI kullanılmadığı için R23 ile GND'ye çekilir; CLKOUT bilinçli NC'dir.

CR2032 birincil hücre olduğundan RTC trickle-charge işlevi firmware/EEPROM ayarında kapalı tutulmalıdır. BT1 için seçilen footprint fiziksel pil yuvası datasheet'iyle son kez karşılaştırılmalıdır.

### 6. TFT ve dört kanallı backlight

TFT logic +3.3V ile beslenir. Arka ışık ayrı akım kontrollü yoldadır: `+3.3V → L2 2,2 µH → U7 TPS61023 → BACKLIGHT_4V2 → J3.38 ortak anot → dört LED kolu → U8 CAT4104 → GND`.

U7 FB bölücüsü R44=604 kΩ ve R45=100 kΩ ile yaklaşık 4,189 V ayarlar. U8 RSET=3,24 kΩ yaklaşık 39,8 mA/kanal, toplam yaklaşık 159 mA hedefler. U8 pin 1–4 ayrı katotlara, pin 7 BACKLIGHT_4V2'ye, pin 5 GND'ye bağlıdır. PWM yolu `TFT_BL_PWM → R28 100 Ω → U8.6`; R29 100 kΩ bu düğümü GND'ye çeker.

Backlight bir gerilimle doğrudan sürülmez; CAT4104 dört kolun akımını düzenler. U7'nin görevi sürücünün akım regülasyonu için gerekli headroom'u üretmektir. L2 ve R28 bağlantılarındaki regresyon bu son kontrolde giderilmiştir.

### 7. Güç ölçümü

`PD_VOUT → RShunt 5 mΩ → OUT_POS` yolu üzerinden ana çıkış akımı ölçülür. INA228 VIN+=PD_VOUT, VIN−=OUT_POS ve VBUS=OUT_POS'tur. Bu polarite pozitif çıkış akımında pozitif şönt gerilimi verir. U3 +3.3V ile beslenir; adres pinleri GND'dedir; SDA/SCL ortak 3,3 V I²C hattındadır.

5 A'da 5 mΩ üzerinde 25 mV ve 0,125 W oluşur. 1 W rating termal pay sağlar, fakat ölçüm doğruluğu için Kelvin sense yönlendirmesi ve düşük TCR kesin parça gerekir. INA228 ölçüm yapar; akımı sınırlayan bir CC döngüsü değildir.

### 8. Power output

İki fiziksel çıkış kararı uygulanmıştır:

| Konektör | Bağlantı |
|---|---|
| J4.1 DG142R klemens | OUT_POS |
| J4.2 DG142R klemens | GND |
| J5 108-0902-001 banana jack | OUT_POS |
| J6 108-0903-001 banana jack | GND |

J4/J5/J6 aynı iki elektriksel çıkışı paralel sunar. Mevcut haliyle çıkış **PD'den geçen gerilimdir**; ayarlı CV/CC laboratuvar çıkışı değildir. Harici ters besleme, çıkış kapatma, donanımsal OVP/OCP, deşarj ve yük anahtarı henüz yoktur. Bu nedenle power-output bloğu geliştirme aşamasındadır.

## Global label yön denetimi

Toplam 72 global label örneği tarandı. TFT ve encoder kaynakları user-interface tarafında `output`, MCU tarafında `input`; INA/RTC/PD interrupt kaynakları çevre birimi tarafında `output`, MCU tarafında `input`; I²C hatları `bidirectional`; güç rayları `passive` olarak tanımlıdır. USB veri/CC hatlarındaki TVS ve konnektör uçlarının `passive` olması, veri uçlarının `bidirectional` tanımıyla uyumludur.

## Üretim öncesi kapanması gereken konular

1. **Eksik footprintler:** D1, D2, J1, L1, SW1, SW2, TH1 ve TP1–TP10. J1 için benzer USB-C footprint'i rastgele atanmayıp DX07B024JJ1R1500 mekanik çizimine göre kesin footprint hazırlanmalıdır.
2. **Kesin güç parçaları:** D2, L1, R11, R43 ve RShunt için MPN, güç/sıcaklık derating ve tedarik doğrulaması.
3. **MOSFET gate uyumu:** IRF7855 ile AP33772S sürüş geriliminin RDS(on), kayıp ve SOA kontrolü.
4. **Kapasitör DC-bias:** Buck ve boost bulk MLCC'lerinin gerçek etkili kapasiteleri üretici eğrisiyle doğrulanmalıdır.
5. **Power output güvenliği:** Ayarlı CV/CC isteniyorsa ayrı güç katı; her durumda OVP/OCP, ters akım ve kontrollü kapatma mimarisi.
6. **PCB:** Koruma elemanı yerleşimi, USB diferansiyel çift, yüksek di/dt döngüleri, Kelvin şönt, 5 A bakır genişliği, termal via ve DRC.
7. **Prototip testleri:** PD açılış/yeniden başlatma, 5 V ve 28 V buck yük adımı, COMP kararlılığı, backlight PWM/ısıl, USB IEC ESD ve VBUS surge.

0402 boyutu sinyal dirençleri ve küçük bypass kapasitörlerinde kullanıldı. R11/R43/RShunt ile buck/boost bulk kapasitörlerini 0402'ye zorlamak elektriksel ve termal olarak uygun değildir; bu parçalar değer, gerilim, ripple ve güç gereksinimine göre daha büyük tutulmuştur.

## Doğrulama kanıtları

- `reports/full-connectivity-20260911/erc-final.rpt`: KiCad ERC, 0 hata / 0 uyarı.
- `reports/full-connectivity-20260911/audit-summary.json`: otomatik denetim özeti.
- `reports/full-connectivity-20260911/all-pin-connections.csv`: 361 pinin tamamının net ve footprint tablosu.
- `reports/full-connectivity-20260911/global-label-directions.csv`: global label yönleri.
- `reports/full-connectivity-20260911/project-final.xml`: denetlenen kök netlist.

ERC proje ayarlarında daha önce tanımlanmış dört genel kategori yok sayılmaktadır: tek örnekli global label, dört bağlantı noktasının birleşmesi, SPICE model uyarısı ve footprint-filter eşleşmesi. Sonuçtaki 0/0 değeri bu mevcut proje ayarlarıyla elde edilmiştir; bu çalışma sırasında yeni bir ERC bastırması eklenmemiştir.
