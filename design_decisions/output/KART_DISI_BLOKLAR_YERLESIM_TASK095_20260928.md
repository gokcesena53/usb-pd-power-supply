# TASK-095 — Kart dışında bekleyen blokların yeniden yerleşimi

28.09.2026: TASK-094 sonrasında park edilmiş 26 komponent ana PCB içine alındı. AP33772S bloğu 23, encoder pull-up bloğu 3 üyedir. Geçici park alanında elektriksel komponent kalmadı. Panel encoder mekanik modeli kart dışında kalması gereken panel parçasıdır.

## Yerleşim kararı

AP33772S bloğu B.Cu üzerinde encoder kablo hacmi ile TPS55340 boost bölgesi arasına yerleştirildi. R11 giriş şöntü Ethernet modülünün güneyinde; Q3 onun güneyinde; C3 giriş tarafında, C8 Q3 çıkışı ile boost girişi arasında. U1 ve bypass/filtre elemanları Q3 altında, bölücü ve gösterge elemanları kartın güney kenarındadır. TH1 güç MOSFET yakınında kaldı. R34–R36, J9 altında Y=125,5 mm üzerinde 2,5 mm adımla sıralandı.

Tüm 26 parça B.Cu yüzünde kaldı; yeni çift yüzlü güç döngüsü oluşturulmadı. C8 0 dereceye, R34–R36 ortak 90 dereceye getirildi. Yeni dar alana uyarlamak için blok içi koordinatlar yeniden düzenlendi; grup üyeliği ve pad-net eşleşmeleri korundu.

J7 USB, J8 Ethernet, J9, MECH_ENC, J3/FPC, H1–H4 ve diğer footprint konumları/açıları/yüzleri korunmuştur. Edge.Cuts ve tasarım kuralları değişmedi. Yalnız J8 referans yazısı yeni R11 ile çakışmaması için taşındı; Q3/R11/R64/R65 referansları da yeni konumlara uyarlandı.

## Son koordinatlar

| Ref | X (mm) | Y (mm) | Açı | Yüz |
|---|---:|---:|---:|---|
| C1 | 73.500 | 125.500 | 0° | B.Cu |
| C2 | 72.000 | 122.800 | 0° | B.Cu |
| C3 | 72.400 | 107.000 | 180° | B.Cu |
| C4 | 72.500 | 118.500 | 0° | B.Cu |
| C8 | 82.700 | 116.900 | 0° | B.Cu |
| D1 | 83.500 | 120.500 | 180° | B.Cu |
| Q3 | 78.500 | 110.000 | 0° | B.Cu |
| R11 | 76.500 | 103.000 | 0° | B.Cu |
| R12 | 77.500 | 115.500 | 90° | B.Cu |
| R13 | 82.500 | 122.500 | 0° | B.Cu |
| R14 | 81.200 | 120.500 | 0° | B.Cu |
| R21 | 75.800 | 125.500 | 0° | B.Cu |
| R34 | 62.500 | 125.500 | 90° | B.Cu |
| R35 | 65.000 | 125.500 | 90° | B.Cu |
| R36 | 67.500 | 125.500 | 90° | B.Cu |
| R64 | 80.500 | 125.500 | 0° | B.Cu |
| R65 | 82.800 | 125.500 | 0° | B.Cu |
| R8 | 78.200 | 125.500 | 0° | B.Cu |
| R9 | 85.100 | 125.500 | 0° | B.Cu |
| TH1 | 73.500 | 111.000 | 90° | B.Cu |
| TP1 | 71.500 | 101.300 | 0° | B.Cu |
| TP2 | 82.000 | 102.500 | 0° | B.Cu |
| TP3 | 90.800 | 103.600 | 0° | B.Cu |
| TP4 | 70.000 | 127.500 | 0° | B.Cu |
| TP5 | 74.000 | 113.500 | 0° | B.Cu |
| U1 | 76.500 | 120.500 | 180° | B.Cu |

## Elektriksel yerleşim ve routing devri

Aşağıdaki değerler pad merkezleri arasındaki düz mesafedir; bitmiş iz uzunluğu veya elektriksel performans ölçümü değildir.

| Bağlantı | Mesafe (mm) |
|---|---:|
| U1.20-C4.1 | 3.730 |
| U1.12-C1.1 | 3.768 |
| U1.15-C2.1 | 3.648 |
| R11.2-Q3.7 | 7.711 |
| Q3.5-C8.1 | 6.039 |
| U1.23-R12.1 | 2.540 |
| R12.2-Q3.2 | 7.714 |

TASK-087 için güç akışı J7 → R11 → Q3 → C8 → boost girişidir. R11 iki ucundan U1 algılama pinlerine bağımsız Kelvin bağlantıları çekilmeli; algılama izleri yüksek akım bakırından ayrılmalıdır. U1 CC1/CC2 hatları J7/ESD yönüne sol-kuzey koridorundan götürülmeli. C4/V5V, C1/V18 ve C2/IFB pin bağlantıları en kısa doğrudan rotalarla ve yakın GND dönüşüyle tamamlanmalı. Q3 gate yolu R12 üzerinden, güç/SW bakırından uzak tutulmalı. R34–R36 +3.3V ortak beslemesi ve encoder sinyalleri J9 yönüne çıkarılmalı.

Mevcut dört D5–U11 FB iz segmentinin UUID, koordinat, genişlik ve netleri değişmedi. Diğer bağlantılar henüz route edilmemiştir; 360 bağlantısız öğe TASK-087 işidir.

## Mekanik ve DRC doğrulaması

Encoder/J9 alt yüz kablo hacmi PCB X=57,8..70, Y=102..123, STEP Z=−17..−0,5 mm olarak korundu. Taşınan modeller bu hacme, encoder modeline ve sabit tüm komponent modellerine karşı kontrol edildi. Taşınan modellerin kendi aralarındaki katı kesişimleri de denetlendi.

- Taşınan 21 modelli parçanın sabit modellerle en büyük kesişim hacmi: **0.000000 mm³**; kendi aralarında çakışma: **0**. Beş test noktası düz PCB pedidir, ayrı yükseltilmiş katı modeli yoktur.
- Kablo servis hacmine minimum model mesafesi: **1.400 mm**.
- Encoder modeline minimum mesafe: **7.036 mm**.
- Taşınan 26 footprint’in tüm pad merkezleri kapalı kart poligonunun içinde; DRC pad kenarı/bakır açıklıklarını denetledi. Yalnız pad merkezine bakılarak kenar uygunluğu iddia edilmedi.
- Sol kenarda en az 0,254 mm ve mevcut daha sıkı genel 0,500 mm kuralı korundu; J9 ve yeni sol kenar değişmedi.
- DRC hata **15 → 15**, uyarı **153 → 153**; yeni ihlal **0**. Mevcut 15 hata U2 kart kenarı ihlalleridir.
- Şematik parite farkı **0**; bağlantısız öğe **360 → 360**.
- Üst/alt SVG katmanları ve 3D renderleri kontrol edildi.

Model kontrolü nominal geometriler içindir; gerçek lehim çıkıntıları, Ethernet model toleransı, kablo demeti ve kutu/fiş kabulü önceki numune görevlerinde sürer. Bu yerleşim tamamlanması genel routing veya üretim kabulü değildir.

## Kanıtlar

- [Son alt yüz 3D](../../hardware/docs/reports/task-095-20260928/bottom.png)
- [Son üst yüz 3D](../../hardware/docs/reports/task-095-20260928/top.png)
- [Sayısal doğrulama](../../hardware/docs/reports/task-095-20260928/verification.json)
- [Katı kontrolü](../../hardware/docs/reports/task-095-20260928/solid-check.json)
- [Önce/sonra koordinatlar](../../hardware/docs/reports/task-095-20260928/placement.json)
- [Son DRC](../../hardware/docs/reports/task-095-20260928/final-drc.json)

Doğrulanan PCB SHA256: `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6`. Başlangıç yedekleri ve tekrar üretim betikleri aynı rapor dizinindedir.
