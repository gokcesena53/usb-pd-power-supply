# Stokta olmayan parçalar: tedarik / muadil kararları

Tarih: 2026-09-22 · Görev: TASK-002 · Durum: karar

Özdisan indeksinde (21–22.09.2026) stokta olmayan üç parça için karar. Kaynak tablo: `hardware/docs/output/BOM_OZDISAN_REV_C_20260921.xlsx`.

## L1 — SRI0704-220M → **FPI0705-220K** (Core Master, Özdisan 507505)

AOZ1284 buck bobini (V_PRE → +3.3V, 500 kHz). Tasarımdaki SRI0704-220M (22 µH / 0,11 Ω / 1,95 A, 7,3 × 7,3 × 4,5 mm) Özdisan'da yok; aynı serinin başka değerleri stokta.

Yük: 3,3 V rayında ölçülen tepe talep ~0,7 A (ESP32-C6 Wi-Fi TX + TFT + arka ışık ~80 mA; eski 0,74 A tahmini boost'lu arka ışığı içeriyordu, o devre kalktı). 22 µH'de dalgalanma 0,265 A tepe-tepe → tepe akım ~0,83 A.

Taranan stok (Özdisan "Sabit İndüktörler" 468, 22 µH, 35 sonuç) içinden adaylar:

| Parça | L / DCR / IDC | Gövde | Fiyat | Stok | Not |
|---|---|---|---|---|---|
| **FPI0705-220K** | 22 µH / 0,11 Ω / 2,3 A | 7,8 × 7,0 × 5,0 | 8,28 TL | 3.467 | **Seçilen** |
| FPI1005-220M | 22 µH / 0,07 Ω / 3,4 A | 10 × 9 × 5,4 | 10,56 TL | 10.468 | Elektriksel en iyi, +%40 alan |
| 74404084220 (Würth) | 22 µH / 0,069 Ω / 2,1 A (Isat 3 A) | 8 × 8 × 4,2 | 26,38 TL | 500 | 3 kat pahalı |
| SMPI06050-220M | 22 µH / 0,115 Ω / 5 A | 7,7 × 6,6 × 5,0 | 15,05 TL | 200 | Stok düşük |
| IHLP2525CZER220M11 | 22 µH / 0,135 Ω / 2,9 A | 6,5 × 6,6 × 3,0 | 62,21 TL | 747 | En küçük, en pahalı |
| TPY0705-220M | 22 µH / 0,35 Ω / 2,0 A | 7,0 × 7,0 × 4,6 | 13,55 TL | 1.221 | **Mevcut footprint'e birebir uyuyor**, DCR 3 katı |
| SRI0704-330M | 33 µH / 0,25 Ω / 1,2 A | 7,3 × 7,3 × 4,5 | 15,05 TL | 13.335 | Aynı ayak, DCR ve marj kötüleşiyor |

Gerekçe: FPI0705-220K, tasarımın DCR'ını (0,11 Ω) birebir korur — iletim kaybı ve verim değişmez. IDC 1,95 → 2,3 A çıkar; tepe akıma göre 2,8 kat marj. Gövde eskisinden 0,5 mm daha uzun ve 0,5 mm daha yüksek, alan etkisi ihmal edilebilir. Adaylar içinde en ucuzu ve stoğu üretim için yeterli.

Reddedilenler: TPY0705-220M footprint değişikliği istemezdi ama 0,35 Ω DCR ile kaybı üçe katlıyordu (0,7 A'de 0,17 W). SRI0704-330M da aynı ayakta kalırdı; 1,2 A IDC ile marj 1,45 kata iniyordu. FPI1005 elektriksel olarak daha iyi ama 10 × 9 mm.

Footprint: `hardware/libraries/Inductor_Custom.pretty/L_CoreMaster_FPI0705_7.8x7.0mm_H5.0.kicad_mod` (spec DWG MY0212071: land L 8,5 toplam, G 2,0 boşluk, H 7,5 ped genişliği → 7,5 × 3,25 mm iki ped, merkez ±2,625). Datasheet: `hardware/datasheets/FPI0705-220K.pdf`.

## L3 — B82422H1682K000 → **SRI0704-6R8M** (Core Master, Özdisan 587796)

TPS55340 pre-boost bobini (PD_VOUT → V_PRE 5,02 V, 600 kHz). TASK-001, 23.09.2026.

Eski parça yetersizdi: B82422H1682K000 (1210 çip) 6,8 µH ama **0,35 A / 570 mΩ**; hesaplanan tepe akımın (1,24 A) çok altında. Özdisan stoğu da 10 adete inmiş.

Gereksinim, TPS55340 datasheet'inin (SLVSBD4E) 11–16 numaralı denklemleriyle hesaplandı. Vin(min) 3,3 V PPS, Vout 5,02 V, VD 0,45 V, fsw 600 kHz, V_PRE yükü 0,6 A (3,3 V rayının 0,7 A'i + kontrolcü/bias), η 0,85:

- D = 0,397 · IL(ort) = 1,07 A · dalgalanma 0,32 A · **tepe 1,24 A** (geçici pay ile ~1,5 A)
- KIND 0,3 için L(min) = 6,78 µH → şemadaki **6,8 µH doğru değer**
- TPS55340 anahtar akım limiti 5,25–7,75 A. TI'nin en muhafazakâr önerisi (Isat > limit) bu kartta 12 × 12 mm sınıfı bobin gerektirirdi; görevdeki ≥3 A şartı (tepe akımın 2,4 katı) benimsendi.

| Parça | L / DCR / IDC | Gövde | Fiyat | Stok | Not |
|---|---|---|---|---|---|
| **SRI0704-6R8M** | 6,8 µH / 0,04 Ω / 3,5 A | 7,3 × 7,3 × 4,5 | 15,05 TL | 657 | **Seçilen**; KiCad'de hazır footprint |
| FPI0705-100M | 10 µH / 0,058 Ω / 3,4 A | 7,8 × 7,0 × 5,0 | 8,28 TL | 735 | L1 ile ortak footprint; L değişimi RHP sıfırını %32 aşağı taşır |
| FPI0504-6R8M | 6,8 µH / 0,065 Ω / 2,7 A | 5,2 × 5,8 × 4,5 | 5,64 TL | 108 (+3000) | En küçük ve ucuz; stok düşük |
| SRI0605B-6R8M | 6,8 µH / 0,08 Ω / 2,8 A | 6,6 × 6,2 × 5,0 | 17,56 TL | 1.583 | DCR iki katı |
| 74437356068 (Würth) | 6,8 µH / 0,049 Ω / 5,1 A | 8,5 × 8 × 3 | 56,15 TL | 34 | Akım limitinin üstünde ama stok yetersiz |

Gerekçe: 6,8 µH korunduğu için kompanzasyon (R52/C) yeniden doğrulanmıyor; adaylar içinde DCR en düşük (0,04 Ω → 1,07 A rms'de 46 mW) ve akım en yüksek. Footprint `Inductor_SMD:L_7.3x7.3_H4.5` KiCad'de hazır, yeni çizim gerekmedi. Datasheet: `hardware/datasheets/SRI0704-6R8M.pdf`.

## U1 AP33772S — Mouser/DigiKey

Özdisan indeksinde stoksuz dahil hiç geçmiyor; PD 3.1 EPR sink kontrolcüsü kategorisi Özdisan'da yok. Muadil arayışı tavanı da değiştirir (bkz. `CIKIS_GERILIMI_28V_TAVANI_20260922.md`), bu yüzden parça korunuyor ve ikinci kaynaktan alınıyor. Stok ve fiyat satın alma öncesi doğrulanacak.

## U2 — ESP32-C6-MINI-1-H4 (23.09.2026, TASK-041)

Modül varyantı kesinleşti: **ESP32-C6-MINI-1-H4** — 4 MB flash (Quad SPI), −40…105 °C, 13,2 × 16,6 × 2,4 mm, PCB anten. Tedarik yine Mouser/DigiKey (Özdisan'da ESP32-C6 yok).

WROOM-1'den farkı: MINI-1 **IO10 ve IO11'i dışarı vermiyor** (datasheet v1.5, Tablo 3-1). Tasarım 22 GPIO kullanıyordu; yeniden atama:

- TFT_CS: GPIO10 → **GPIO14** (pin 19)
- TFT_DC: GPIO11 → **GPIO7** (pin 16)

Kalan atamalar korundu. Kullanılan küme GPIO 0–9 ve 12–23 olup modülün verdiği kümeyle birebir örtüşüyor; **boşta GPIO kalmadı**. Strapping pinleri (GPIO4/5/8/9/15) tasarımdaki rolleriyle değişmedi.

Şema tarafı: IO8/IO9 WROOM'da sağ kenardaydı, MINI-1'de sol kenarda. Bu yüzden strap/boot ağları (R37 pull-up + R15/TP9 test noktası, R10 pull-up + SW1) U2'nin sol altına taşındı ve iki pull-up tek bir +3.3V sembolünü paylaşan kısa bir raya bağlandı. USB seri dirençleri yerinde kaldı; yalnız taşıdıkları sinyal yer değiştirdi (R2 → D−, R3 → D+). Footprint `RF_Module:ESP32-C6-MINI-1` (KiCad standart).

Kontrol: netlist'te her net U2 dışındaki üyelerini korudu (yalnız pin numaraları değişti), GND'ye modülün tüm toprak pedleri katıldı, ERC 0 hata / 0 uyarı, okunabilirlik denetiminde yeni bulgu yok. Firmware pin haritası `software/FIRMWARE_GEREKSINIMLERI.md` içinde güncellendi.

## U2 ESP32-C6-WROOM-1 — Mouser/DigiKey (22.09.2026, tarihsel)

Özdisan "WiFi Modülleri" kategorisinde ESP32-C6 yok (22.09.2026). Stoktakiler:

- **ESP32-C3-MINI-1-N4** (445): native USB var ama GPIO sayısı yetmiyor (tasarım ~22 GPIO kullanıyor), Wi-Fi 6 / 802.15.4 yok.
- **ESP32-WROOM-32E-N4** (466): aynı 18 × 25,5 mm gövde ama pin dizilişi farklı ve native USB yok (USB-UART köprüsü gerekir).

İkisi de şema, footprint ve firmware değişikliği isterdi; modül korunuyor. Flash varyantı satın alma öncesi sabitlenecek (TASK ile izlenen ayrı karar değil, DesignNote'ta duruyor).

## Kontrol

Alan güncellemesi sonrası şema: ERC 0 hata / 0 uyarı, `netlist farki: YOK`, `field_geometry` farkı boş (hiçbir sembol oynamadı).
