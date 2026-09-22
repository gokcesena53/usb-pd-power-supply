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

## U1 AP33772S — Mouser/DigiKey

Özdisan indeksinde stoksuz dahil hiç geçmiyor; PD 3.1 EPR sink kontrolcüsü kategorisi Özdisan'da yok. Muadil arayışı tavanı da değiştirir (bkz. `CIKIS_GERILIMI_28V_TAVANI_20260922.md`), bu yüzden parça korunuyor ve ikinci kaynaktan alınıyor. Stok ve fiyat satın alma öncesi doğrulanacak.

## U2 ESP32-C6-WROOM-1 — Mouser/DigiKey

Özdisan "WiFi Modülleri" kategorisinde ESP32-C6 yok (22.09.2026). Stoktakiler:

- **ESP32-C3-MINI-1-N4** (445): native USB var ama GPIO sayısı yetmiyor (tasarım ~22 GPIO kullanıyor), Wi-Fi 6 / 802.15.4 yok.
- **ESP32-WROOM-32E-N4** (466): aynı 18 × 25,5 mm gövde ama pin dizilişi farklı ve native USB yok (USB-UART köprüsü gerekir).

İkisi de şema, footprint ve firmware değişikliği isterdi; modül korunuyor. Flash varyantı satın alma öncesi sabitlenecek (TASK ile izlenen ayrı karar değil, DesignNote'ta duruyor).

## Kontrol

Alan güncellemesi sonrası şema: ERC 0 hata / 0 uyarı, `netlist farki: YOK`, `field_geometry` farkı boş (hiçbir sembol oynamadı).
