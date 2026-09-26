# Genel PCB yerleşimi — 24 Eylül 2026

25.09.2026 kesinleştirme: Ethernet, sol panelden bakıldığında USB-C'nin
**tam altında, aynı Y merkezinde** olmalıdır. Son merkez Y=88,500 mm;
J9 X=58,000 mm üzerinde düz 5 pin sırasıdır. Güncel uygulama ve ölçüler:
[Port hizası ve enkoder düzeltmesi](PORT_HIZASI_ENKODER_DUZELTME_20260925.md).

Kullanıcıyla kararlaştırılan yerleşim hedefidir. Bu kayıt task planını
günceller; PCB taşıması, routing veya yeni DRC/3D kanıtı değildir.

## Mekanik ve elektriksel düzen

- Mevcut 99,40 × 61,04 mm dış hat, H1–H4 ve J3/FPC ankrajları korunur.
- J7 USB-C top (F.Cu), sol kenarda; J8 Ethernet bottom (B.Cu), USB-C'nin
  altında ve aynı sol panelde. x/y/z ilişkisi kesitte gösterilir. İki fiş
  aynı anda takılıyken ≥2 mm gövde açıklığı proje hedefidir; RJ45 mandalı,
  karşı yüze geçen sabitleme ayakları ve header pinleri ayrıca kontrol edilir.
- U2 ESP32-C6-MINI-1 top; anten kısmı ana PCB dışında. RF/mekanik koşulları
  sağlayan USB-C'ye yakın uygulanabilir konum seçilir. Antenin sağ kenarda
  olması zorunluluğu kaldırıldı. USB-C yakınlığı anten boşluğundan öncelikli
  değildir. Modül bağlantı tarafının kart içine bakması değerlendirilir.
- U2/J7 gövdeleri LCD toleranslı izdüşümü dışında tutulur. LCD altında J3
  dışındaki top parçaların gövde+lehim toplam zarfı ≤1,80 mm kalır. J8 top
  pinleri LCD dışında veya metal+lehim ≤1,50 mm kesim/montaj şartıyla tanımlı
  olmalıdır. LCD mesafesi kendiliğinden artırılmaz.
- J9 enkoder pedleri Ethernet yanında; eski koordinatı kesin ankraj değildir.
  LCD dışında havya/prob erişimi, lehim, kablo bükümü ve gerilim alma alanı
  ayrılır; mevcut beş tel pin haritası korunur. Kablo anten önünden ve
  buck/boost/backlight anahtarlama bölgelerinden geçirilmez.
- Slotun fiziksel PCB yarığı mı yoksa boş kablo/lehime erişim alanı mı olduğu
  henüz cevaplanmadı; TASK-083'te takip edilir. Netleşmeden Edge.Cuts'a yarık
  eklenmez. Yarık seçilirse freze ölçüsü, bakır açıklığı ve kalan et kalınlığı
  belirlenir.
- AOZ1284 buck ve TPS55340 boost B.Cu üzerinde, U2/anten bölgesinden uzakta;
  bobinler ve SW/LX alanları MCU/anten altına getirilmez. U2 bypass/bulk
  kapasiteleri MCU yanında kalır. Mesafeler ölçülür; üretici şartı olmayan
  evrensel bir mm sınırı konmaz.
- LM74801/MOSFET, şönt, INA226 ve J4 kısa/doğrudan çıkış yolu oluşturur.
  Kelvin ölçüm yolu güç akımından ayrı; FB/COMP/sense ve ortak V_X yolları
  anahtarlama bölgelerinden uzak tutulur. D5–U11 FB sürekliliği korunur.

## Ethernet altının kullanımı

25.09.2026 kullanıcı isteğiyle modül altındaki uygun hacim aktif komponent
yerleşimi için kullanılacaktır. Önceki boş bırakma tercihi yerine Ethernet
yardımcı hücresi ve bağlantısı uygun düşük profilli gruplar değerlendirilir.
Güncel analiz: `ETHERNET_ALTI_ALAN_ANALIZI_20260925.md`. Genel yerleşimin bu
hacme bağımlılığı ve henüz numuneyle doğrulanmamış kabuller açıkça kaydedilir.
Projedeki nominal 2,5 mm aralık ve yaklaşık 2,2 mm RJ45 lehim çıkıntısı numune
garantisi değildir. RJ45 pim keepout'u, header/mekanik pin bölgesi ve modül
kartının altı ayrı XY/Z haritasında gösterilir. Bottom flip sonrası keepout
yüzü doğrulanır. Genel ≤2 mm parça yüksekliği kabulü geçersizdir.

Önce Q8/R17/C10/C20/C21 gibi Ethernet'e ait düşük profilli, az ısınan
elemanlar değerlendirilir. Her adayın maksimum gövde+lehim yüksekliği,
karşıdaki çıkıntı, tolerans ve kalan boşluğu yazılır. Sıcak güç elemanları
buraya sıkıştırılmaz; test/servis erişimi ve modül dışı alternatif korunur.
TASK-053 numunesi son mekanik doğrulamaya girdidir.

## İş sırası ve kabul

1. TASK-010 üretici/katman/DRC kuralları ve TASK-069 grup envanteri.
2. **TASK-086 ilk tur:** güç blokları dahil bütün devrelerin gerçek alanlarıyla
   kaba kart planı. İki aday incelenir; en az biri zorunlu koşulları sağlamalı.
   Küçük parçalar kesin kilitlenmez; Ethernet altı başlangıçta boş kabul edilir.
3. TASK-083 J9 kablo/slot ölçülerini, TASK-080 yerel J8 hacim/keepout haritasını
   verir. Bu görevler TASK-063 son konumunu beklemez. **TASK-063 mekanik
   konumların tek karar sahibidir**; LCD, portlar, U2, J9 ile birlikte kaba
   plandaki güç/ölçüm zarflarını ve koridorlarını değerlendirir.
4. TASK-070–084 grup hazırlıkları ve TASK-085 grup devrinden sonra
   **TASK-008 ikinci tur:** ince yerleşim ve gerçek iz/via veya ölçülü kritik
   güzergâh denemeleri. Gereken mekanik değişiklik TASK-063'te tekrar doğrulanır.
5. **TASK-087:** önce kritik hatlar, sonra kalan routing, güç bakırı/via'lar
   ve dolgular tamamlanır. Bağlantısız öğe 0, schematic parity 0 istenir.
6. TASK-053 numune ölçüleri ve TASK-054 son kutu/mekanik kabulü ile
   **TASK-088 üretim öncesi elektriksel/mekanik kabul** tamamlanır.
   TASK-014 Gerber üretimi bu kabulü bekler; tahmini modül ölçüsüyle geçilmez.
7. TASK-015 prototip/dizgi sonrası **TASK-089 son kutuda RF** ve
   **TASK-090 eşzamanlı yükte besleme/termal** performansını ölçer.

Yerleşim denemesi numune beklerken yapılabilir; son üretim kabulü numune
ölçümlerini bekler. Prototip performans testlerinin sayısal planı üretimden
önce hazırlanır, fiziksel sonuçlar ancak prototipte alınır. RF test planının
sahibi TASK-054, besleme/termal bütçesinin sahibi TASK-008; TASK-088 bu
girdilerin TASK-089/090'a devrini kontrol eder.

Mezanin altında fiziksel olarak uygun üst üste yerleşim, tüm modülü kapsayan
2D courtyard ile çakışabilir. Yalnız XY/Z, tolerans ve 3D kanıtı olan belirli
J8–parça çiftlerine sınırlı courtyard istisnası kabul edilir. Elektriksel
clearance, kısa devre, bağlantısızlık ve RJ45 keepout'u kapatılmaz; genel
bir DRC muafiyeti verilmez. TASK-080 kanıtı TASK-010 kural politikasıyla
uygulanır ve TASK-088'de incelenir.

## İsterlerin görev ve kanıt karşılığı

| İster | Sorumlu görev / kabul kanıtı |
| --- | --- |
| USB-C top, Ethernet bottom ve USB-C altında | TASK-063 yüz/koordinat ve panel kesiti; TASK-054 numune/fiş kontrolü |
| Ethernet yanında enkoder pedleri ve uygun slot/alan | TASK-083 ölçülü girdi; TASK-063 son konum ve erişim |
| MCU top, anten dışarı, RF koşullarını sağlayan USB-C yakınlığı | TASK-063 aday karşılaştırması/keepout; TASK-089 son kutu RF testi |
| Ethernet altında uygun komponentler | TASK-080 XY/Z haritası; TASK-008 ref/boşluk listesi; TASK-053 gerçek ölçü |
| Buck ESP32'den uzak | TASK-086 bölge ayrımı; TASK-008 bobin/SW mesafeleri ve besleme bütçesi; TASK-090 ölçüm |
| Düzenli ve route edilebilir bağlantılar | TASK-086 blok yönleri; TASK-008 kritik güzergâh denemesi; TASK-087 tamamlanmış routing |

Bu isterler uygulanmadan/ölçülmeden karşılanmış sayılmaz; görevlerin
güncellenmesi tasarımın fiziksel doğrulaması değildir.

Öncelik: mekanik/RF sınırları → kısa kritik akım döngüleri ve GND dönüşü →
kritik sinyal koridorları → ratsnest sadeliği. Blok giriş/çıkışları birbirine
çevrilir; güç bakırı, sinyal, via ve termal alan ayrılır. Vida başları,
FPC kilidi, BOOT/RESET, test noktaları ve kablo lehim erişimi korunur.

Son kabul: top/bottom ve 3D inceleme, kritik güzergâh denemesi,
ref/x/y/açı/yüz listesi, DRC farkı, schematic parity 0 ve yeni açıklanmamış
geometrik ihlal olmaması. Kanıtlı courtyard istisnaları, mevcut ihlaller
ve bağlantısız öğeler ayrı raporlanır. Yerleşim
bitişi, genel routing veya üretime hazır kart onayı değildir.

## Önceki kayıtlarla ilişki

Bu karar TASK-065/070/077 raporlarının USB-C/ESP32 bottom hedefini,
TASK-063 sağ kenar anten şartını ve TASK-054 eski kart/arka panel/genel
≤2 mm varsayımlarını değiştirir. Tamamlanmış görevlerin tarihsel kanıtı
korunur; yeni yüzlere taşıma ve yeniden kontrol TASK-063/008'dedir.
LCD yükseklik sınırları geçerlidir.

Kaynaklar: `LCD_YUKSEKLIK_BOTTOM_TASK065_20260924.md`,
`KART_DIS_HATTI_LCD_20260924.md`, `ENCODER_PANEL_TASK066_20260924.md`,
`ETHERNET_MODULU_ANALIZI_20260923.md` ve
[Espressif modül yerleşim kılavuzu](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32c6/pcb-layout-design.html#general-principles-of-pcb-layout-for-modules-positioning-a-module-on-a-base-board).
