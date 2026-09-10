# AOZ1284PI — şema öncesi hesap raporu

Kaynak: [AOS AOZ1284PI Rev.1.1, March 2025](https://www.aosmd.com/sites/default/files/res/datasheets/AOZ1284PI.pdf). PDF denklemleri görüntüden kontrol edildi. Girdi: PD_VOUT=5–28 V; çıktı +3.3V; tasarım yükü 1 A, beklenen tepe 0.4 A. Ana çıkışın 5 A yükü bu hesapta yok.

## DATASHEET VALUE

Pinler: 1 LX, 2 BST, 3 GND, 4 FSW, 5 COMP, 6 FB, 7 SS, 8 EN; exposed pad VIN (KiCad pad 9).

VIN 3–36 V; FB 0.8 V (0.788–0.812 V); f=200–2000 kHz; minimum on-time 150 ns; maksimum duty tabloda %87 (1 MHz koşulu). BST–LX: 100 nF. EN çalışma 1.2–5 V; mutlak maksimum 6 V, OFF <0.4 V. ISS=2–3 µA, tipik 2.5 µA; CSS minimum 850 pF.

RF[kΩ]=50000/f[kHz]−5. Tabloda 500 kHz→100 kΩ; denklem aynı frekansta 95 kΩ verir. GEA elektriksel tabloda 170 µA/V, kompanzasyon metninde 200 µA/V; GCS=4.5 A/V, GVEA=500.

Seramikler X5R/X7R; diyot Schottky, VRRM>VINmax ve akım kapasitesi>yük. Sayfa 10/11/12 denklemleri aşağıdaki hesaplarda kullanıldı.

## ENGINEERING CHOICE

| Eleman / parametre | Tasarım tercihi |
|---|---|
| FSW | R38=100 kΩ, 1%; tablodaki yaklaşık 500 kHz bölgesi. 28 V'ta minimum on-time sınırına yaklaşmamak için MHz bölgesi seçilmedi. |
| L1 | 22 µH; tolerans hedefi ±20%, normal çalışma için Isat≥2 A ve Irms≥1.5 A, en yüksek parça sıcaklığında. Gerçek parça/DC kayıpları henüz seçilmedi. |
| D2 | Schottky, en az 60 V / 2 A sınıfı; gerçek VF, sızıntı, termal ve surge özellikleri MPN seçimine bağlı. |
| Cin | C12/C13: 2×10 µF, 50 V X7R; 28 V'ta toplam etkin C≥10 µF şartı. C14: 100 nF/50 V yakın bypass. |
| Cout | C15/C16: 2×47 µF, 10 V X7R; 3.3 V'ta toplam etkin C≥44 µF şartı. Nominal 94 µF'nin etkin 44 µF olduğu varsayılmıyor; bu bir satın alma/doğrulama koşulu. |
| FB | R39 üst=10 kΩ, R40 alt=3.20 kΩ; %0.1 direnç hedefi. |
| SS | C18=10 nF; hesaplanan nominal ramp yaklaşık 3.2 ms. |
| BST | C17=100 nF/16 V, BST ile LX arasında. Gerilim sınıfı LX'in toprağa göre genliğiyle değil iki uç arasındaki farkla ilişkilidir. |
| COMP | R41/C19 seri topoloji yerleştirilecek, değerleri UNRESOLVED. |
| EN | R42=100 kΩ pulldown; EN_CTRL yerel etiketiyle erişim. 1.2–5 V sağlayan kaynak/devre UNRESOLVED. Böylece eksik EN tasarımı yanlışlıkla yüksek gerilime bağlanmıyor. |

## CALCULATED VALUE

100 kΩ için denklem f=476.190 kHz verir. Aşağıdaki nominal hesaplar bu daha düşük değeri kullanır; tablo 500 kHz der. Gerçek frekans/tolerans garantisi **UNRESOLVED**; bu iki sayı arasında kalacağı iddia edilmiyor.

İdeal D=Vo/Vin; ΔIL=Vo(1−Vo/Vin)/(fL); Ipk=Io+ΔIL/2.

| Giriş | Duty | ΔIL, pp | Ipk @1 A | IL,rms | ton |
|---|---:|---:|---:|---:|---:|
| 5 V | %66.000 | 0.10710 A | 1.05355 A | 1.00048 A | 1386 ns |
| 28 V | %11.786 | 0.27788 A | 1.13894 A | 1.00321 A | 247.5 ns |

22 µH, maksimum nominal ripple hedefi 0.30 A için hesaplanan Lmin=20.38 µH'den büyüktür. L −%20 olduğunda ripple=0.34734 A, peak=1.17367 A; 2 A Isat şartının bu normal çalışma peak'ine marjı %70.4'tür. 0.4 A yükte aynı şartta peak=0.57367 A. Bu Isat hesabı kısa devre dayanımını kanıtlamaz: IC'nin akım sınırı 1 A'ya ayarlanmış değildir; 5 A minimum/6 A tipik sınır ve belirtilmeyen maksimum nedeniyle hata anı indüktör dayanımı **UNRESOLVED**.

Gösterilen duty/on-time değerleri ideal hesaptır. Gerçek VF, DCR ve anahtar kayıpları duty'yi artırır; gerçek parçalar olmadan kayıplı sonuç uydurulmadı. 5 V'ta ideal %66 duty, datasheet'in %85 önerilen Vo/Vin sınırının altındadır. 28 V'ta nominal ton>150 ns; frekansın kesin aralığı teyit edilmeden worst-case on-time garantisi verilemez.

Diyot minimum ters gerilimi 28 V'tan büyük olmalı. Ortalama akım Io(1−D): 5 V'ta 0.340 A, 28 V'ta 0.88214 A; en yüksek normal peak yukarıda 1.174 A. Seçim hedefi 60 V/2 A, fakat Pdiode≈0.88214×VF W olduğundan gerçek termal yeterlilik VF/MPN/PCB olmadan **UNRESOLVED**.

Cin RMS=Io√(D(1−D)): 5 V'ta 0.47371 A; 28 V'ta 0.32244 A. Tüm giriş aralığında en kötü nokta 6.6 V, 0.5 A. ≥0.6 A RMS kapasite hedeflendi. Etkin 10 µF ile kapasitif giriş ripple: 5 V'ta 47.124 mV, 28 V'ta 21.833 mV; en kötü 6.6 V'ta 52.5 mV. ESR/ESL ve kaynak geçişleri dahil değildir.

Etkin Cout=44 µF ile kapasitif ripple: 5 V'ta 0.639 mV, 28 V'ta 1.658 mV. L −%20 için 2.072 mV. ESR katkısı ΔIL×ESR olarak ayrıca eklenir. Cout RMS, L −%20'de 0.10027 A; ≥0.15 A RMS hedefi. Tam yük geçişi, ESR/ESL ve etkin C dağılımı henüz **UNRESOLVED**.

FB: 0.8×(1+10000/3200)=**3.3000 V**. Bölücü akımı 250 µA; 1 µA FB bias'ın gerilim etkisi yaklaşık 10 mV. %0.1 direnç ve referans uçlarıyla bias hariç 3.2456–3.3546 V. Bias işareti ve diğer regülasyon etkileri için son tolerans bütçesi gerekir.

SS: sabit akım ve 0.8 V hedefinden t≈CSS×0.8/ISS=3.2 ms; ISS uçlarıyla 2.667–4.000 ms (kapasitör toleransı hariç). Datasheet'in 850 pF için yaklaşık 200 µs örneği bu basit modelle 272 µs verir; ramp zamanı tahmindir, garanti değildir.

COMP için seçilen örnek hedef fc=10 kHz < f/10; RL=3.3 Ω, etkin Co=44 µF, fp1=1/(2πCoRL)=1096.1 Hz.

Rc=fc×Vo/VFB×2πCo/(GEA×GCS):

- GEA=170 µA/V → Rc=14.907 kΩ.
- GEA=200 µA/V → Rc=12.671 kΩ.

Sayfa 12, Cc=1.5/(2πRc fp1) verir; sonra “basitleştirilmiş” olarak CoRL/Rc yazar. Bunlar 1.5 katsayısı nedeniyle eşdeğer değildir:

- 170 µA/V: Cc=14.610 nF veya 9.740 nF.
- 200 µA/V: Cc=17.189 nF veya 11.459 nF.

Her iki sıfır konumu 10 kHz/5'in altındadır; buna rağmen doğru GEA, Cc denklemi ve gerçek etkin Cout/ESR netleşmeden nihai R41/C19 değerlerini seçmiyorum: **UNRESOLVED**. İki farklı denklemin arasından gerekçesiz seçim yapılmadı.

EN için yalnızca sabit oranlı bölücü bütün aralıkta mümkün değil: 5 V'ta k≥1.2/5=0.24, 28 V'ta k≤5/28=0.17857 gerekir. Doğrudan bağlantı veya böyle bir bölücü uygulanmayacak. Datasheet EN bias akımını/zener boyutlandırmasını vermediğinden yeni clamp devresi tahmin edilmedi. EN_CTRL için doğrulanmış harici 1.2–5 V kaynak gereklidir; +3.3V'a bağlamak kendi kendine başlangıç döngüsü yaratır.

## Paket kontrolü

Mevcut SOIC-8-1EP footprint: body 3.9×4.9 mm, pitch 1.27 mm; merkez pad 9=2.71×3.7 mm. Bunlar SO8_EP1 gövde/EP ile uyumludur. KiCad standart dış pad'leri 1.895×0.6 mm; AOS önerisi 2.20×0.80 mm (90° döndürülmüş görünüm) olduğundan land pattern birebir aynı değildir. Kullanıcının yalnız sayfa düzenleme sınırı içinde standart footprint korunur; montaj land-pattern onayı **UNRESOLVED**. Merkez pad 9 kesinlikle PD_VOUT/VIN'e bağlanacak, GND'ye değil.

## Uygulama sınırı

Güç katı ve belirlenebilen destek bağlantıları kurulacak. EN kaynağı ve COMP değerleri çözümlenmeden bu şema çalıştırılabilir/üretime hazır tasarım olarak sunulmayacak. Tüm MPN'ler seçilmemiştir; L/D footprint'leri parça seçimine kadar boş kalacaktır. Diğer sayfalar değiştirilmeyecek.
