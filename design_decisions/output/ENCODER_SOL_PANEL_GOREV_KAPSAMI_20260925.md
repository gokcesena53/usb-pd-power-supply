# Sol panel encoder yerleşimi — 25 Eylül 2026

Bu kayıt kullanıcı tarafından netleştirilen yeni görev kapsamıdır; yerleşimin uygulanmış veya doğrulanmış olduğunu belirtmez.

- Encoder: `hardware/datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf`. Panele mekanik montaj yapılır; J9'a beş kablo ile bağlanır. SW3 ana PCB'ye lehimlenmez.
- Sol panelden bakıldığında şaft daire olarak görülür. Şaft ekseni sol panele diktir ve PCB top düzlemine paraleldir; encoder tabanı ile PCB top düzlemi 90 derecedir.
- Şaft ekseninin yüksekliği `Z_enc = (Z_USB_giris_merkezi + Z_RJ45_giris_merkezi) / 2` olarak belirlenir. Referans, metal gövdelerin üst sınırları değildir. Aynı montaj koordinat sistemindeki gerçek kablo giriş merkezleri kullanılmalıdır.
- **Uygulama sırasındaki kullanıcı düzeltmesi:** Encoder düz dış panele monte edilir; şaft dışarı taşabilir. Önceki şaft uç yüzünü USB kablo giriş yüzüyle aynı düzleme getirme şartı kaldırılmıştır. Kablo giriş merkezlerinin orta yüksekliği ve J7/J8 sabitliği korunur.
- Encoder, kullanıcının üstten görünüşte portların solunda/J9 tarafında tarif ettiği bölgeye yerleştirilir. Sayısal panel-yanal mesafe verilmemiştir; mevcut J9 bölgesi ve mekanik zarf esas alınarak ölçülü aday seçilir. Kart eksen yönleri ile ekranın sol yönü karıştırılmamalıdır; üst ve sol panel görünüşünde işaretlenir.
- **J7 USB ve J8 Ethernet/RJ45'in mevcut konumları, açıları ve yüzleri değiştirilmeyecek.** İşe başlarken güncel karttan ankrajlar alınır; eski rapor koordinatlarına geri dönülmez. Önceki USB'yi sola taşıma ve RJ45 ile giriş yüzlerini hizalama isteği, bu son talimatla yürütülecek kapsamdan çıkarılmıştır; bu işlemler tamamlanmış sayılmaz.
- Mekanik gövde kalınlığı 3 mm'dir. Encoder panel montajı, gövde/şaft/bağlantı uçları ve kablo zarfı bu kalınlıkla kontrol edilir. Düz panel montajında nominal şaft çıkıntısı 12,5 − 3 = 9,5 mm'dir. Sabit portlarla uygulanabilir panel montajı çelişirse portlar taşınmadan ölçülü çelişki kullanıcıya sunulur.
- Encoder ve gerekli sol kenar değişikliğinden etkilenen komponentler, ilişkili devre blokları halinde kart dışında ayrı geçici alanlara taşınır. Blok üyeliği, göreli yerleşim, netler ve mevcut yerel bağlantılar korunur; taşınması zorunlu sınır bağlantıları belgelenir. Etkilenmeyen bloklar korunur.
- Encoder konumu tamamlandıktan sonra yalnızca sol taraftaki Edge.Cuts değiştirilir. Üst/alt/sağ kenarlar, mevcut montaj delikleri ve sabit ankrajlar korunur; çelişki halinde kapsam kendiliğinden genişletilmez.
- Yeni sol kenarda bakır-kenar açıklığı en az **10 mil = 0,254 mm** olmalıdır. Geçerli daha sıkı kurallar korunur; 0,250 mm, 10 mil kabul edilmez. Mevcut ihlaller başlangıç DRC'siyle ayrılır; açıklanmamış yeni ihlal kabul edilmez.
- Geçici alana alınan blokların yeniden kart içine yerleştirilmesi ayrı sonraki görevdir. Encoder/sol kenar görevi kapsamında otomatik yapılmaz.

Mevcut STEP modeli `hardware/libraries/L-KLS4-EC1121S-E5A-F12.5.3dshapes/L-KLS4-EC1121S-E5A-F12.5.step` PDF ile doğrulanarak kullanılabilir; eksik veya yanlışsa düzeltilir. Panel parçasının mekanik montaj gösterimi, SW3'ü elektriksel PCB footprint'i haline getirmemelidir. Sayısal açıklık/kesişim raporu ve ölçülü görseller birlikte teslim edilir.

Önceki TASK-066/083/092 kayıtları tarihsel sonuçlardır. Yeni çalışma başladığında J9 ve etkilenen blokların nihai konumları bu kapsamın yeni raporuyla güncellenir. Bu kayıt fiziksel değişiklik yapmaz.
