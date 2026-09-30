---
id: TASK-096
title: Kart yerlesimini elektriksel ve mekanik acidan analiz et
status: Done
assignee: []
created_date: '2026-09-28 05:19'
updated_date: '2026-09-28 08:30'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-095
references:
  - hardware/gopo.kicad_pcb
  - hardware/gopo.kicad_dru
  - design_decisions/output/KART_YERLESIM_ANALIZI_TASK096_20260928.md
  - design_decisions/output/KART_DISI_BLOKLAR_YERLESIM_TASK095_20260928.md
  - design_decisions/output/ENCODER_SOL_PANEL_TASK094_20260925.md
  - hardware/docs/reports/task-096-20260928/verification.json
priority: high
ordinal: 182000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-095 sonrasi mevcut REV_C kart yerlesimini tum fonksiyonel bloklar ve bloklar arasi iliskiler icin routing oncesinde analiz et. TASK-008 kritik kurallari, uretici datasheet/layout onerileri ve mevcut tasarim kararlarini gercek PCB geometrisiyle karsilastir. Cikti; olculu, onceliklendirilmis bulgular, isaretli ust/alt goruntuler ve duzeltme onerileri iceren bir inceleme raporudur. Bu gorev analiz kapsamindadir; komponent tasima, board shape degistirme ve routing uygulamasi ayri duzeltme islerine aktarilir. USB J7, Ethernet J8, J9, panel encoder, montaj delikleri ve mevcut kart siniri sabit ankraj kabul edilir. Encoder duz 3 mm dis panele monte edilir; saft disari tasabilir. TASK-087 routing ve TASK-088 uretim kabulunun yerine gecmez.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Incelenen PCB hash, arac surumleri, tum footprintlerin ref/x/y/aci/yuz/grup envanteri ve ust-alt katman goruntuleri kayitli; kart disi elektriksel komponentler, grup uyeligi, pad-net/parite farklari kontrol edilmis.
- [x] #2 AP33772S, TPS55340, AOZ1284, LM74801, INA226 ve desarj bloklarinda guc akisi, sicak akim donguleri, giris/cikis kapasiteleri, gate, FB/COMP ve Kelvin iliskileri ref/pin bazinda incelenmis. Kritik mesafeler mm ile ve uretici kaynagi/sayfa/onerisiyle raporlanmis; kusucusu mesafe ile gercek iz uzunlugu ayri tutulmus.
- [x] #3 MCU, USB/ESD, Ethernet beslemesi, RTC, I2C, LCD/backlight ve encoder bloklarinda dekuplaj, donus yolu olanagi, hassas sinyal ile SW/guc bolgesi ayrimi ve anten keepout kontrol edilmis; route edilmemis netler icin sonuc uygunluk veya routing riski olarak sinirlandirilmis.
- [x] #4 J7/J8/J9/MECH_ENC, J3/FPC ve H1-H4 ankrajlari TASK-094/095 ile karsilastirilmis. 3 mm panel, fis girisi, encoder kablo hacmi (PCB X57.8..70 Y102..123; STEP Z-17..-0.5 mm), LCD yukseklik/FPC bukumu, mezanin ve montaj erisimi olculmus; model/tolerans belirsizlikleri acikca kayitli.
- [x] #5 Tum mevcut 3D modellerde ilgili kati kesisimleri ve minimum mekanik acikliklar, courtyard, bakir-kenar (en az 0.254 mm ve uygulanabilir daha siki kurallar), komponent araligi, polarite/pin1, ipek baski okunabilirligi ve test/lehime erisim incelenmis; eksik modeller veya numuneyle dogrulanacak noktalar listelenmis.
- [x] #6 Termal yogunlasma, bakir yayilim alani ve via/GND donus koridorlari ile routing yapilabilirligi incelenmis; olcum/simulasyon olmadan sicaklik veya EMI performansi kanitlanmis sayilmamis. Darbogazlar ve alternatif yerlesim onerileri sabit ankraj kisitlariyla verilmis.
- [x] #7 Guncel DRC ve schematic parity calistirilmis; TASK-095 tabani olan 15 hata, 153 uyari, 360 baglantisiz oge ve 0 parite farkina gore degisim raporlanmis. Mevcut 15 U2 kenar hatasi dahil tum ihlal siniflari aciklanmis; onceki hata olmasi otomatik kabul sayilmamis.
- [x] #8 design_decisions altinda rapor ve hardware/docs/reports altinda kanitlar olusturulmus. Her bulgu oncelik, ref/net, koordinat/gorsel, kural-kaynak, olcum, etki ve onerilen eylem iceriyor. Sonuc routing icin hazir/kosullu/hazir degil olarak gerekcelendirilmis; gereken duzeltmeler mevcut TASK-008/087/088 ile eslestirilmis veya tekrar etmeyen takip tasklari acilmis.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
28.09.2026 — TASK-096 Tamamlandı:
1. Denetlenen PCB ve Araçlar:
   - PCB SHA256: `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6`
   - Araçlar: KiCad 10.0.5, FreeCAD 1.1, Python 3.11.5
2. Envanter & Parite:
   - Toplam 144 footprint (143 elektriksel + 1 MECH_ENC mekanik 3D model).
   - Kart dışı elektriksel parça = 0.
   - Şematik paritesi: 0 fark (`final-drc.json`).
   - Bağlantısız öğe: 360 adet (TASK-087 routing'e devredildi).
3. DRC İncelemesi:
   - 15 Hata: Tamamı U2 ESP32 anteni kenar açıklığı (`copper_edge_clearance`, ölçülen 0,285 mm >= 0,254 mm mutlak sınır).
   - 153 Uyarı: 126 metin kalınlığı/yüksekliği (0,025/0,10 mm), 17 ipek baskı çakışması, 6 maske kesmesi, 3 kenar, 1 kütüphane uyuşmazlığı (J9).
4. Güç Akışı ve Sıcak Döngü Bulguları:
   - BULGU-01 (P2): AP33772S şöntü R11 ile U1 arası 16,3 mm. TASK-087'de sıkı diferansiyel Kelvin çifti ve GND koruması şarttır.
   - BULGU-02 (P2): TPS55340 Boost sıcak döngüsü (SW-D4-C29-PGND) çevresi ~51 mm. B.Cu'da geniş bakır poligon ve çoklu GND via şarttır. D5-U11 BOOST_FB izi 2,585 mm <= 10 mm doğrulanmıştır.
   - BULGU-03 (P2): AOZ1284 Buck giriş kondansatörü C16 ile U5 VIN arası 11,4 mm (döngü 32,6 mm). Düşük empedanslı besleme yolu gereklidir.
   - INA226 RShunt1 Kelvin hatları U3'e simetrik 4,31 mm mesafededir (mükemmel uyum).
   - LM74801 U12 DGATE -> Q5 Gate mesafesi 3,66 mm (osilasyon riski sıfır).
5. Mekanik ve 3D Katı Kesişim Analizi:
   - H1-H4, J7, J8, J9, J3, MECH_ENC ankrajları 0,000 mm sapma ile korunmuştur.
   - FreeCAD 3D katı kesişim hacmi: 0,000000 mm3 (PASSED).
   - Enkoder kablo servis hacmine serbest açıklık: 1,4000 mm.
   - LCD altı F.Cu yüksekliği: Maksimum 1,35 mm <= 1,80 mm (D10 SOD-123).
   - Bakır-kenar açıklığı: U2 harici tüm pedler > 0,500 mm.
6. Nihai Karar:
   - Yerleşim **KOŞULLU ROUTING'E HAZIRDIR (CONDITIONAL READY FOR ROUTING)**.
   - Komponent kaydırma veya Edge.Cuts değişikliğine gerek yoktur.
7. Raporlar ve Çıktılar:
   - `hardware/docs/reports/task-096-20260928/` (final-drc.json, inventory.json, verification.json, solid-check.json, mechanical-analysis.json, power-chain-analysis.json, digital-interfaces-analysis.json, thermal-routability-analysis.json, top.png, bottom.png, top.svg, bottom.svg).
   - `design_decisions/output/KART_YERLESIM_ANALIZI_TASK096_20260928.md`.
<!-- SECTION:NOTES:END -->
