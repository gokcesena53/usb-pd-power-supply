# Devre bağlantı incelemesi — 9 Eylül 2026

**Sonuç: Şema mevcut haliyle çalışır ve üretime hazır değildir.** Tüm kayıtlı şema dosyaları, hiyerarşi, dışa aktarılan netlist ve ERC raporu incelendi. Şema değiştirilmedi. Bu inceleme elektriksel ağ bağlantılarını kapsar; fiziksel donanım testi veya simülasyon değildir. PCB dosyası boş olduğundan PCB izleri, akım taşıma kapasitesi, creepage/clearance ve yerleşim doğrulanamaz. KiCad editöründe kaydedilmemiş değişiklikler varsa bu rapora dahil değildir.

## 1. ERC özeti

KiCad 10 ile yeniden çalıştırılan ERC: **35 hata, 280 uyarı, toplam 315 kayıt**. Bunlar 315 bağımsız devre arızası değildir; aynı eksiklik birden fazla kayıt oluşturabilir.

| Kategori | Adet |
|---|---:|
| Bağlantısız pin | 20 |
| Sürülmeyen giriş | 6 |
| Güç çıkışı tarafından sürülmeyen güç pini | 5 |
| Bağlantısız etiket | 3 |
| Hiyerarşik etiket uyuşmazlığı | 1 |
| Bağlantı grid'i dışında pin/tel | 254 |
| Açık tel ucu | 17 |
| Tek pine bağlı etiket | 5 |
| Aynı ağda birden fazla ad | 2 |
| Footprint kütüphane bağlantısı | 1 |
| Sembol/kütüphane farkı | 1 |

Ham kanıtlar: [ERC metin raporu](erc.rpt), [ERC JSON](erc.json), [netlist](connectivity.xml). Global etiketin tek kullanımı, dört yönlü birleşim, SPICE modeli ve footprint filtresi kontrolleri proje ayarlarında yok sayılıyor. Bunların yapılmış olduğu varsayılmadı. Fiziksel pinin bir ağda görünmesi, ilgili parçanın seçiminin ve tüm çalışma koşullarının doğru olduğunu tek başına kanıtlamaz.

## 2. Kesin bağlantı hataları ve eksikler

| Öncelik | Yer | Kanıt / mevcut bağlantı | Sonuç ve gerekli işlem |
|---|---|---|---|
| Kritik | USB_PD_CONTROLLER, R11 | R11 pin 1 açıkta; pin 2 `PD_VBUS_SENSED` üzerinde. USB VBUS ağı yalnızca konnektör, TP1 ve U1 ISENP pinine gidiyor. | Giriş güç yolu kesik; U1 VCC ve güç MOSFET'lerinin giriş tarafı VBUS'tan beslenemiyor. R11'in giriş tarafı VBUS/ISENP ağına bağlanmalı. |
| Kritik | USB-C → U1 | `USB_CC1` yalnızca USB konnektör A5; `USB_CC2` yalnızca B5. U1 pin 17 ve 16 ayrı açık ağlarda. | USB-C bağlantı algılama ve PD haberleşmesi çalışmaz. U1 CC1/CC2 kendi isimli USB ağlarına ulaşmalı. |
| Kritik | POWER GENERATION / +3.3V | U5 AOZ1284PI'nin yalnızca GND bağlantısı var. VIN, EN, SS, FSW, COMP, BST, LX ve FB açık. +3.3V ağında regülatör çıkışı veya tanımlı harici besleme girişi yok. | ESP32, RTC, INA228 ve ekran lojik beslemesi üretilmiyor. Regülatörün destek elemanları ve besleme yolu tamamlanmalı. |
| Yüksek | USB_PD_CONTROLLER, R4–R7 | R4.1, R5.2, R6.2 ve R7.2 açıkta; dirençlerin diğer uçları ilgili besleme rayına bağlı. | SCL/SDA seviye çeviricisinin hem 3.3 V hem 5 V tarafındaki pull-up'lar ağlara ulaşmıyor. INA228 de aynı 3.3 V I²C ağını kullanıyor. |
| Yüksek | USB_PD_CONTROLLER, R8 | U1.9 `PD_INT_5V` üzerinde tek başına. R8.1 açık; R8.2 → R9.1 → ESP32 GPIO20 bağlantısı mevcut. | PD kesmesi MCU'ya ulaşmaz. R8.1, `PD_INT_5V` ağına bağlanmalı. |
| Yüksek | MCU, RTC_SCL | U2.7/GPIO7 yalnızca `/MCU/RTC_SCL` ağında. U4.3/SCL ve R25.2 farklı `Net-(U4-SCL)` ağında. RTC yanındaki etiket (247.65, 109.22 mm) boşta. | RTC ile I²C haberleşmesi kurulamaz. Etiket gerçek SCL teline taşınmalı veya tel tamamlanmalı. |
| Yüksek | USER INTERFACE, Q6 | Q6.3/D açıkta. `BL_SINK` yalnızca R30–R33 uçlarına bağlı. | Aydınlatmanın akım dönüş yolu yok. Q6 drain, BL_SINK ağına bağlanmalı. |
| Yüksek | USER INTERFACE, BACKLIGHT_3V0 | Bu ağda yalnızca J3.38 var. | Ekran aydınlatmasının besleme kaynağı tanımlanmamış. Uygun kaynak/sürücü tamamlanmalı. |
| Orta | USB_PD_CONTROLLER, D1 | D1 anodu GND; katodu R14 üzerinden U1 LED çıkışına bağlı. | Mevcut pozitif lojik sürüşte LED ters kutuplu kalır. LED polaritesi düzeltilmeli. |
| Yüksek | POWER OUTPUT | Sayfa boş. OUT_POS üzerinde INA228 ölçüm pinleri ve şönt bulunuyor, fiziksel çıkış konnektörü yok. | Kullanılabilir cihaz çıkışı ve dönüş bağlantısı tamamlanmamış. |

CC hatlarındaki somut geometri hatası: hiyerarşik etiketler (64.77, 63.50) ve (64.77, 66.04) mm; ilgili tel uçları (64.77, 64.77) ve (64.77, 67.31) mm. Her ikisinde **1.27 mm kayma** var. Üstelik ana sayfadaki USB_PD_CONTROLLER sayfa pinleri de bağlanmamış. Bu nedenle yalnızca etiketleri yaklaştırmak, hiyerarşi bağlantısı da tamamlanmadıkça yeterli olmayabilir; sayfalar arasında tek, tutarlı bağlantı yöntemi kullanılmalı.

AP33772S'nin CC, harici I²C pull-up, INT ve LED işlevleri üretici pin tablosuyla karşılaştırıldı. INT yüksek seviyede aktiftir. [Diodes AP33772S, sayfa 3](https://www.diodes.com/datasheet/download/AP33772S.pdf).

## 3. ERC dışındaki önemli bulgular

**J1 referansı iki farklı parçada kullanılıyor.** MCU sayfasındaki 3 pin UART konnektörü ile USB_C_INPUT sayfasındaki DX07B024JJ1R1500 USB-C konnektörü aynı referansa sahip. XML'de J1 bileşen kaydı UART konnektörü olarak çıkarken J1.A4/J1.A5 gibi USB pinleri de ağlarda bulunuyor. Bu durum BOM ve PCB aktarımını belirsiz hale getirir. Bileşenler benzersiz numaralandırılmalı, ardından netlist yeniden alınmalı. Mevcut ERC bunu raporlamamış olması nedeniyle manuel saptanan ayrı bir bulgudur.

**Q3/Q4 sembolleri gerçek IRF7855 pin numaralarıyla uyumlu değil.** Kullanılan genel sembol G=1, S=2, D=3. Gerçek SO-8 IRF7855 için S=1/2/3, G=4, D=5/6/7/8 eşlemesi gerekir. Footprint de henüz atanmamış. Yalnızca SO-8 footprint eklemek yeterli değildir; sembol-pin eşlemesi düzeltilmelidir. MOSFET'in RDS(on) garantisi VGS=10 V koşulundadır; AP33772S'nin gerçek gate sürüşünde kayıp/ısınma ayrıca doğrulanmalıdır. [Infineon IRF7855](https://www.infineon.com/assets/row/public/documents/24/49/infineon-irf7855-datasheet-en.pdf).

**ESP32 BOOT kurtarma yolu güvenilirliği:** GPIO9 için 10 kΩ pull-up ve BOOT butonu var. Ancak GPIO8 yalnızca R15 ve TP9'a gidiyor; tanımlı pull-up yok. Normal flash boot ile zorlanmış download modu aynı koşula sahip değil: download için GPIO8=1 ve GPIO9=0 gerekir. Bu yüzden BOOT butonuyla programlama/kurtarma garanti edilemiyor. GPIO8 başlangıç seviyesi tanımlanmalı. Ekrana ayrılan GPIO4/5/15 de strapping işlevleri taşıdığından ekranın reset sırasındaki yükleri doğrulanmalı; bunları doğrudan yanlış GPIO seçimi diye sınıflandırmıyorum. [Espressif, Boot Configurations](https://documentation.espressif.com/esp32-c6-wroom-1_wroom-1u_datasheet_en.html).

**INT bölücüsü:** Kopukluk giderildiğinde nominal oran 20/(12+20)=0.625; 5 V giriş yaklaşık 3.125 V olur. En yüksek kaynak çıkışı, direnç toleransı ve 3.3 V rayının alt sınırı birlikte kontrol edilmelidir. Bu satır, bağlantı kopukluğundan ayrı bir tasarım toleransı kontrolüdür.

**AOZ1284PI exposed pad VIN'dir.** Sembolün pin 9/VIN tanımı doğru yöndedir; PCB'de bu pad alışkanlıkla GND'ye bağlanmamalıdır. Şu anda açıktır. [AOS datasheet, sayfa 2](https://www.aosmd.com/sites/default/files/res/datasheets/AOZ1284PI.pdf).

## 4. Footprint ve doğrulanamayan parçalar

- UART J1 footprint kimliği `DS1021-1X3SF11-B:CONNFLY_DS1021-1X3SF11-B`; kayıtlı footprint kütüphanesinin adı ise `CONNFLY_DS1021-1X3SF11-B`. Kütüphane öneki eşleşmiyor.
- Q6 yalnızca genel `Q_NMOS_GSD`; gerçek parça ve footprint seçilmemiş. 3.3 V gate ile hedef aydınlatma akımı için uygunluğu teyit edilemez.
- J3 genel 40 pin konnektör; gerçek ekran modeli/datasheet belirtilmediği için besleme, SPI, mod seçimi ve LED anot/katot pin eşlemesi kesin teyit edilemez. NC işaretli pinlerin ekranın mod seçimi girişleri olup olmadığı kontrol edilmeli.
- RShunt = 5 mΩ için 01005 footprint atanmış. Örneğin 5 A'da I²R = 0.125 W olur. Seçili üretici parçası, akım/güç/tolerans değeri olmadan bu footprint onaylanamaz. Şönt için uygun güç paketi ve Kelvin bağlantısı gereklidir. Bu 5 A örnektir; doğrulanmış sistem çalışma akımı olarak alınmadı.
- C5 = 22 µF için 01005 atanmış. Gerçek kapasitör bulunabilirliği, DC bias altındaki etkin kapasitesi ve gerilim sınıfı doğrulanmalı. VBUS tarafındaki C3/C8 için de hedef PD gerilimine uygun gerçek parça seçimi eksik.
- R8/R9/R14'e `Capacitor_SMD:C_01005_0402Metric` atanmış. İki pad olması elektriksel bağı otomatik bozmaz; buna rağmen direnç parçasının land pattern'iyle uyumu doğrulanmalı ve doğru footprint sınıfı kullanılmalı.
- U1'e başka üretici adını taşıyan QFN footprint atanmış. İsim tek başına hata kanıtı değildir; pad ölçüleri ve exposed-pad numarası AP33772S mekanik çizimiyle eşleştirilmeden üretim onayı verilemez.
- Encoder footprint dosyasında açıkça `MECHANICAL POSITION UNRESOLVED` ve konumlandırma özellikleri için `Y UNRESOLVED` notları var. Elektriksel ağ doğru olsa da mekanik footprint tamamlanmış sayılmaz. SW3 için sembol/kütüphane uyumsuzluğu da mevcut; terminal isimlerinin gerçek satın alınan parçayla eşleşmesi ayrıca teyit edilmeli.

## 5. Bağlantı düzeyinde doğru bulunan bölümler

| Bölüm | Doğrulanan ağ |
|---|---|
| Encoder | SW3.1/A → R34.2 → U2.20/GPIO22; SW3.3/B → R35.2 → U2.21/GPIO23; SW3.4/S1 → R36.2 → U2.19/GPIO21. Dirençlerin diğer uçları +3.3V; SW3.2/C ve SW3.5/S2 GND. |
| Encoder yazılım şartı | Pull-up'lar 10 kΩ; RC debounce eklenmemiş. Quadrature durum çözümleme ve buton debounce yazılımda gerekli. |
| Native USB | USB D+ A6/B6 → R2 22Ω → U2.14/GPIO13; USB D− A7/B7 → R3 22Ω → U2.13/GPIO12. D+/D− yer değiştirmemiş. J1 referans çakışması saklı tutulmak kaydıyla ağlar izlenebiliyor. |
| UART | U2.25/GPIO16 → UART_TX → MCU J1.1; U2.24/GPIO17 → UART_RX → MCU J1.2; J1.3 GND. |
| EN/RESET | U2.3 → 10 kΩ pull-up; 1 µF → GND; RESET butonu → GND. |
| RTC SDA/INT | GPIO6 → U4.4/SDA ve R26 pull-up; GPIO2 → U4.2/INT ve R24 pull-up. RTC SCL ise yukarıdaki nedenle hatalı. |
| RTC besleme | VDD → +3.3V; VSS → GND; BT1+ → R22 → VBACKUP, C10 → GND. EVI 10 kΩ ile GND. Pil kimyası ve firmware backup/şarj ayarları belirtilmediği için ayrıca incelenmeli. |
| INA228 | VS → +3.3V, GND ortak; A0/A1 → GND; IN+ şönt giriş tarafı, IN− ve VBUS şönt çıkış tarafı; ALERT → GPIO3 + 10 kΩ pull-up. SCL/SDA doğru ortak ağlarda fakat ağın pull-up'ları kopuk. |
| BSS138 topolojisi | Q1/Q2 gate → +3.3V, source → 3.3 V I²C, drain → 5 V I²C. Yön doğru; dört pull-up bağlantısı tamamlanmalı. |
| AP33772S yardımcı pinleri | V18 → 100 nF → GND; IFB → 100 nF → GND; V5V → 1 µF → GND; OTP → NTC → GND; VOUT ölçümü R13 üzerinden PD_VOUT. |
| Güç MOSFET ağları | Q3/Q4 source uçları ortak; gate uçları ortak ve R12 üzerinden PWR_EN'e bağlı. Ağ topolojisi mevcut; gerçek paket pin eşlemesi ayrıca hatalı. |
| Ekran SPI | SCLK=GPIO4, MOSI=GPIO5, CS=GPIO10, DC=GPIO11, RESET=GPIO15; PWM=GPIO1 → R28 → Q6 gate; R29 gate pull-down mevcut. Ekran tarafı gerçek panel datasheet'i olmadan onaylanamaz. |

INA228 ölçüm pinleri [TI datasheet](https://www.ti.com/lit/ds/symlink/ina228.pdf), RTC pinleri [Micro Crystal RV-3028-C7](https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3028-C7.pdf) ile karşılaştırıldı. AP33772S'nin kullanılmayan DP/DN pinleri, nem algılama kullanılmıyorsa açık bırakılabilir; bunları sırf açık oldukları için hata saymadım.

## 6. ERC kayıtlarının yorumu ve düzeltme sırası

254 grid uyarısı otomatik olarak 254 kopukluk anlamına gelmez. Bazı pin/teller 0.635 mm gibi alt grid konumlarında elektriksel olarak doğru birleşiyor. Kopukluk kararında netlist esas alındı. Pilin VBACKUP ağı için `power_pin_not_driven` kaydı, pasif pil sembolünün güç çıkışı sayılmamasından kaynaklanabilir; pil bağlantısı netlistte mevcut. Buna karşılık +3.3V ve PD giriş güç yolundaki eksikler gerçektir; PWR_FLAG eklemek bunları onarmaz.

`TYPE-C KONNEKTÖRÜ` metni açıklama yerine global etiket olarak kullanılmış ve USB_VBUS ile aynı ağa düşmüş. Elektriksel kısa devre oluşturduğu gösterilmedi, fakat ağ adı belirsizliği yaratıyor. INA_ALERT üzerinde boş yerel etiket de var. Ana sayfanın USB_VBUS sayfa pini alt sayfa etiketiyle eşleşmiyor.

Önerilen sıra: (1) benzersiz referanslar ve gerçek sembol/paket pin eşlemeleri; (2) R11/CC bağlantıları ve besleme üretimi; (3) I²C pull-up, INT ve RTC SCL; (4) ekran aydınlatması ve güç çıkışı; (5) boot/ekran/footprint belirsizlikleri; (6) ERC ve netlistin yeniden doğrulanması, ardından PCB tasarımı ve donanım testi.

Önceki yanıttaki “encoder devresinde ERC ihlali yok” ifadesi fazla genişti: encoderin ağ bağlantıları doğrulandı, ancak grid ve sembol/kütüphane uyarıları vardır. Bu rapor o ayrımı düzeltiyor.
