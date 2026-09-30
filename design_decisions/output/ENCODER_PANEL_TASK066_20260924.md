# SW3 panel montajı ve J9 kablo pedleri — 24 Eylül 2026

Görev: TASK-066. SW3, `L-KLS4-EC1121S-E5A-F12.5`, kutunun ön panelinde
kalır; karta beş ayrı kabloyla bağlanır. Bu karar TASK-062'deki panel montaj
kararını şema ve PCB'ye uygular.

## Şema ve bağlantı

- SW3: `Footprint` boş, `on_board no`, `in_pos_files no`, `in_bom yes`.
  Enkoder satın alınan bir panel parçası olarak BOM'da kalır.
- J9: `Connector_Generic:Conn_01x05`; karta lehimlenen beş tel için PCB
  özelliğidir, satın alınacak header değildir. BOM/pozisyon dosyasından hariçtir.
- Footprint:
  `Connector_Wire:SolderWire-0.25sqmm_1x05_P4.2mm_D0.65mm_OD1.7mm`.
  Ped aralığı 4,2 mm, bitmiş delik nominal çapı 0,65 mm; kare ped pin 1'dir.
- R34/R35/R36 10k pull-up'ları ve MCU pin atamaları korunur. Görev açıklamasında
  geçen RC filtre mevcut şemada **yoktur**; bu değişiklikte RC veya TVS eklenmedi.

| J9 pedi | SW3 pini | İşlev | Kart neti | MCU |
| --- | --- | --- | --- | --- |
| 1 | 1 / A | Faz A | ENCODER_A | U2.28 / GPIO22 |
| 2 | 2 / C | Enkoder ortak ucu | GND | — |
| 3 | 3 / B | Faz B | ENCODER_B | U2.29 / GPIO23 |
| 4 | 4 / D (S1) | Basma kontağı | ENCODER_SW | U2.27 / GPIO21 |
| 5 | 5 / E (S2) | Basma kontağı dönüşü | GND | — |

İki GND pedi ayrı tellerle ilgili enkoder uçlarına gider; kablo beş tellidir.
PCB netlistinde SW3.1…5 yerine aynı pin sırasıyla J9.1…5 geçer; diğer
bağlantılar değişmez. Şemadaki SW3 kablo tesisatını da tarif eder.

## Kablo, gürültü ve ESD kararı

- Kutu içinde, **en fazla 150 mm**, beş adet esnek çok telli izole bakır tel:
  nominal 0,14 mm²; iletken demeti dış çapı en fazla 0,5 mm, izolasyon dış
  çapı en fazla 1,5 mm. Bu çaplar 0,65 mm delik ve footprint'in 1,7 mm
  izolasyon zarfı için seçim şartıdır; numunede lehimlenebilirlik doğrulanır.
- Beş tel kısa, birlikte ve hafif bükülmüş demet halinde taşınır. GND telleri
  sinyal tellerinin yanında tutulur; güç/buck/boost anahtarlama düğümleri,
  indüktörler ve LCD backlight akım döngüsünden uzak geçirilir. Kablo lehim
  noktalarından çekilmez: kutu içindeki bir klips/kelepçe gerilim alma sağlar.
- Kart tarafında mevcut 10k pull-up'lar korunur. Firmware, geçerli quadrature
  durum geçişlerini kontrol etmeli ve butona debounce uygulamalıdır. AB fazlarını
  uzun, bağımsız zaman kilitleriyle süzmek yerine geçiş dizisi doğrulanır.
  Firmware algoritması bu donanım görevinin kapsamında uygulanmadı.
- **ESD varsayımı:** plastik kutu ve yalıtkan düğme, dışarıdan erişilemeyen mil,
  kontaklar ve kablo lehimleri. Panel metalinin devre GND'sine kendiliğinden
  bağlanacağı varsayılmadı; beş tel arasında şasi/kalkan hattı yoktur.
- Bu iç kablo bağlantısına harici TVS konulmadı. Yalıtkan düğme, kısa kablo ve
  debounce bir IEC ESD dayanım kanıtı değildir; yazılım elektriksel hasara
  karşı koruma sağlamaz. Metal mil/çerçeve erişilebilir kalırsa veya kablo
  kutu dışına çıkarılırsa bu varsayım geçersiz olur ve J9 girişinde harici
  koruma tasarımı yeniden değerlendirilir. Mevcut MCU pin korumasına sistem
  ESD dayanımı atfedilmiyor.
- Montaj, 100 detent/her yön, 100 basma, güç yük geçişlerinde 10 dakika sahte
  olay/reset gözlemi ve son kutunun ESD testi **TASK-068**'de takip edilir.
  Test başarısızlığında seri direnç/RC/TVS seçimi ölçümle yapılıp şemaya işlenir.

SW3 datasheet'i dişli panel somunu tanımlamaz. Enkoder gövdesi kutuya özel
bir tutucu ile sabitlenmeli; kablolar veya mil mekanik taşıyıcı olarak
kullanılmamalıdır. Tutucunun 3D tasarımı bu PCB bağlantı değişikliğine dahil değildir.

## PCB yerleşimi ve LCD boşluğu

J9 ön yüzde, sol şeritte; pad 1 mutlak koordinatı **(58,00; 91,60) mm**,
açı −90°. Ped merkezleri x=58,00; y=91,60 / 95,80 / 100,00 / 104,20 / 108,40.
AA merkezine göre x=−42,00; y=−8,40…+8,40 mm. İpek baskıda her pedin işlevi yazılıdır.

- J9 footprint grafik sınırı x=56,555…59,445, y=89,975…110,025 mm.
- LCD modülünün sol sınırı x=63,72 mm: **4,275 mm** yatay boşluk vardır;
  modülün ±0,2 mm toleransında da en az 4,075 mm kalır.
- Kablo bükümü/lehimi sol şeritte tutulur, x=63,52 mm'yi aşmaz. Bu nedenle
  J3 yüksekliğine dayanarak LCD altında tel sıkıştırılmıyor.
- THT tellerin alt yüz çıkıntıları kesilir; TASK-063'te USB/RJ45 ve TASK-065'te
  alt yüz yerleşimi yapılırken J9 delikleri ve kablo alanı korunur.
- H1–H4, diğer footprint UUID/konum/yön/katman/ped netleri korunmuştur.
  Genel kart yerleşimi ve iz çekimi henüz tamamlanmamıştır.

## Doğrulama

Kanıtlar: `hardware/docs/reports/task-066-20260924/`.

| Kontrol | Önce | Sonra |
| --- | --- | --- |
| ERC hata / uyarı | 0 / 0 | 0 / 0 |
| Net sayısı | 120 | 120 |
| DRC schematic parity | 0 | 0 |
| DRC yerleşim/üretim ihlalleri | 149 | 148 |
| DRC bağlantısız öğe | 361 | 361 |

Netlist karşılaştırması yalnız ENCODER_A/B/SW ve GND'de SW3 → J9 pin değişimini
doğrular. J9 için yeni DRC ihlali yoktur; şema okunabilirlik denetimi sıfır
bulgu vermiştir. Şema yakın planı, PCB katman çizimi ve 3D görüntü incelendi.
Kablo ve LCD'nin 3D modelleri kartta yoktur; gerçek kablo büküm zarfı için
yukarıdaki mekanik sınırlar ve prototip doğrulaması geçerlidir.

`update_pcb.py --keep-tracks`, şemada olmayan board-only H1–H4'ü de sildiği için
bu dört footprint özgün bloklarıyla geri kondu; UUID/konumları tekrar doğrulandı.
SW3 PCB'den çıkarıldı. Kalan 148 DRC ihlali ve 361 bağlantısız öğe genel
yerleşim/routing işleridir; bu çalışma tam kart DRC geçişi değildir.

## Kaynaklar

- `hardware/datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf`: A/C/B ve D/E kontakları,
  enkoder gövdesi ve mil çizimi.
- `hardware/datasheets/TFT032B018.pdf` ve
  `KART_DIS_HATTI_LCD_20260924.md`: LCD izdüşümü ve toleransı.
- KiCad 10 kurulu `Connector_Wire.pretty` kütüphanesindeki yukarıda belirtilen
  standart solder-wire footprint: ped, delik ve kablo zarfı.
