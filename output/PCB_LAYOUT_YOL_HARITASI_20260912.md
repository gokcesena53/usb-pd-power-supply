# PCB layout yol haritası

Mevcut durum: Şematik tamamlandı, ERC temiz, footprintler atandı, 93 × 60 mm dört katmanlı ilk yerleşim hazır. Routing henüz başlamadı.

## Aşama 1 — Mekanik yapıyı kilitle

KiCad'de önce `Edge.Cuts` ve mekanik bileşenleri kontrol et.

- Kart: 93 × 60 mm
- USB-C: sol kart kenarı
- ESP32 anteni: sağ kart kenarı
- TFT FPC konektörü: alt kenar
- Encoder: alt-sağ
- J4 klemens: üst kenar
- CR2032: alt-sol
- Banana jack'ler: panel üzerinde, J4'e kabloyla bağlı
- Kasa ölçüleri geldiğinde montaj deliklerini ekle
- Encoder mil merkezi ve mekanik tespit deliklerini üretici çizimiyle doğrula

Tamamlanma ölçütü: Konnektörler kasa açıklıklarıyla uyuşuyor ve hiçbir mekanik parça sonradan taşınmayacak.

## Aşama 2 — Board Setup ve üretici stack-up

KiCad: `File → Board Setup → Board Stackup → Physical Stackup`

Başlangıç yapısı:

| Katman | Kullanım | Başlangıç bakırı |
|---|---|---|
| F.Cu / L1 | Bileşenler ve kritik routing | 2 oz aday |
| In1.Cu / L2 | Kesintisiz GND | 1 oz |
| In2.Cu / L3 | Güç dağıtımı | 1 oz |
| B.Cu / L4 | Düşük hızlı sinyaller ve GND | 2 oz aday |

Toplam kalınlık için 1,6 mm başlangıç kabulüdür. USB empedansı için PCB üreticisinden gerçek prepreg/core kalınlıkları ve Dk değeri alınmalıdır.

Tamamlanma ölçütü: Üretici stack-up'ı KiCad'e girilmiş ve USB için empedans geometrisi hesaplanmış.

## Aşama 3 — Net class oluştur

KiCad: `Board Setup → Design Rules → Net Classes`

| Net class | Ağlar | Başlangıç kuralı |
|---|---|---|
| `MAIN_5A` | `USB_VBUS`, `PD_VBUS_SENSED`, `PD_VOUT`, `OUT_POS` | İz yerine polygon; 0,25 mm clearance; 1,0/0,5 mm via başlangıcı |
| `POWER_3V3` | `+3.3V`, `BACKLIGHT_4V2` | 0,6 mm başlangıç izi; 0,7/0,35 mm via |
| `USB_DIFF` | `USB_DP`, `USB_DM` | 90 Ω diferansiyel; genişlik/aralık stack-up hesabından |
| `SIGNAL` | SPI, I²C, GPIO, encoder | 0,20 mm iz; 0,15 mm clearance |

`MAIN_5A` genişliği nihai değer değildir. Polygon genişliği bakır kalınlığı, yol uzunluğu ve izin verilen sıcaklık artışına göre doğrulanmalıdır.

Tamamlanma ölçütü: Bütün kritik ağlar doğru net class'a atanmış.

## Aşama 4 — 5 A ana güç yolunu çiz

İlk route edilecek yol:

`J1 USB_VBUS → R11 → Q4/Q3 → RShunt → OUT_POS → J4`

- L1 üzerinde geniş polygon kullan.
- Uygun bölgelerde aynı yolu L3 üzerinde paralel polygonla destekle.
- L1–L3 geçişlerinde tek via yerine via dizisi kullan.
- Dar boğazları pad çıkışlarında kontrol et.
- Q3/Q4 çevresinde ısı yayılım alanı bırak.
- `PD_VOUT` ile `OUT_POS` RShunt dışında birleşmemeli.

Tamamlanma ölçütü: Güç yolu kesintisiz, dar boğazsız ve 5 A sıcaklık artışı hesabıyla doğrulanmış.

## Aşama 5 — INA228 Kelvin ölçümünü çiz

Routing sırası:

1. RShunt giriş padinden ayrı bir ince hatla INA228 `IN+` pinine git.
2. RShunt çıkış padinden ayrı bir ince hatla INA228 `IN−` pinine git.
3. Ölçüm hatlarını yük akımı polygonunun kenarından veya ortasından alma; doğrudan şönt padinden çıkar.
4. İki hattı birbirine yakın, benzer uzunlukta ve anahtarlama düğümlerinden uzak tut.
5. INA228 bypass kapasitörünü besleme pinlerinin yanında tut.

Tamamlanma ölçütü: Yük akımı Kelvin izlerinden geçmiyor ve her ölçüm izi şöntün kendi padinden başlıyor.

## Aşama 6 — AOZ1284PI buck bölümünü çiz

Öncelik sırası:

1. `C12/C13 → U5 VIN/EP → GND` giriş döngüsü
2. `U5 LX → D2 → GND` catch-diode döngüsü
3. `U5 LX → L1 → C15/C16 → GND` çıkış döngüsü
4. BST–LX arasındaki C14
5. FB ve COMP hatları

Kurallar:

- `LX_SW` alanını küçük tut.
- FB/COMP izlerini LX_SW ve L1'den uzak tut.
- U5 exposed pad `PD_VOUT/VIN` ağıdır. Altındaki termal via'ları GND'ye bağlama.
- U5 VIN termal via'ları yalnız uygun VIN bakırına bağlanmalı.
- Güç GND bağlantılarını kısa ve geniş yap.

Tamamlanma ölçütü: Üç kritik akım döngüsü minimum alanlı ve FB/COMP sessiz bölgede.

## Aşama 7 — Backlight boost bölümünü çiz

Sıra:

1. `+3.3V → C20 → L2 → U7 SW`
2. `U7 → C21 → BACKLIGHT_4V2`
3. `BACKLIGHT_4V2 → U8 → TFT backlight katotları`
4. U7 feedback dirençleri
5. U8 PWM ve akım ayar bağlantıları

- Boost SW bakırını küçük tut.
- C20 ve C21 GND bağlantılarını kısa via ile L2'ye indir.
- Backlight akım yolunu TFT konektörüne kısa götür.

Tamamlanma ölçütü: Boost giriş/çıkış döngüleri kompakt ve feedback hattı SW düğümünden uzak.

## Aşama 8 — USB D+/D− çiftini çiz

- J1'den U9 ESD'ye, oradan ESP32'ye git.
- Mümkünse tamamını L1 üzerinde tut.
- Via kullanma; zorunluysa iki hatta aynı sayıda ve simetrik via kullan.
- Sürekli L2 GND referansı altında kal.
- Keskin 90 derece köşe kullanma.
- Çift aralığını güzergâh boyunca değiştirme.
- Q3/Q4, L1/L2 indüktörleri ve switching node'lardan uzak tut.

Tamamlanma ölçütü: D+/D− kesintisiz GND referanslı, 90 Ω diferansiyel ve uzunluk uyumlu.

## Aşama 9 — +3.3 V ve düşük hızlı sinyaller

Sıra:

1. ESP32 beslemesi ve bypass kapasitörleri
2. RTC beslemesi ve I²C
3. TFT SPI
4. Encoder A/B/SW
5. BOOT ve RESET
6. Test noktaları

- SPI ve I²C hatlarını L1 veya L4 üzerinde taşı.
- Katman değiştirirken dönüş yolu için yakına GND via koy.
- RTC ve VBACKUP hattını buck/boost alanından uzak tut.

Tamamlanma ölçütü: Bütün kontrol ağları bağlı ve her katman geçişinin dönüş yolu mevcut.

## Aşama 10 — GND ve güç zone'ları

- L2'yi kesintisiz GND zone olarak doldur.
- L3 üzerinde `PD_VOUT`, `OUT_POS`, `+3.3V` ve `BACKLIGHT_4V2` bölgelerini oluştur.
- L4 boş alanlarını GND ile doldur.
- Kart çevresinde 2–3 mm aralıklı GND stitching via kullan.
- Güç devrelerinin yakınında daha sık GND via kullanılabilir.
- ESP32 anten keepout alanında hiçbir katmanda zone, via, iz veya bileşen bırakma.

Tamamlanma ölçütü: Zone fill sonrası izole bakır adası yok ve L2 GND düzlemi kesilmemiş.

## Aşama 11 — Son kontroller

1. `Inspect → Design Rules Checker`
2. Açık bağlantı sayısını sıfıra indir.
3. Clearance, kısa devre, courtyard ve kart kenarı hatalarını sıfıra indir.
4. Silkscreen yazılarını bileşen ve padlerden temizle.
5. 3D Viewer ile USB, TFT, encoder, pil ve klemens mekaniklerini kontrol et.
6. ESP32 anten keepout alanını bütün katmanlarda kontrol et.
7. 5 A bakır sıcaklık artışını ve via akımını hesapla.
8. ERC ve PCB–şematik parity kontrolünü tekrar çalıştır.

Tamamlanma ölçütü: ERC/DRC temiz, açık bağlantı sıfır ve mekanik çakışma yok.

## Aşama 12 — Üretim çıktıları

- Gerber
- Drill dosyaları
- IPC-356 veya netlist
- BOM
- Pick-and-place
- Assembly drawing
- Stack-up ve kontrollü empedans notları
- 3D STEP

Gerber üretildikten sonra her katman ayrı ayrı görsel olarak incelenmelidir.

## Mevcut projede sıradaki somut işlem

İlk yapılacak routing işi **5 A ana güç yolu ve INA228 Kelvin bağlantılarıdır**. Bunlar tamamlandıktan sonra buck güç döngüsüne geçilmelidir.

