---
id: TASK-064
title: LCD FPC büküm yolunu ve J3 konumunu belirle
status: Done
assignee: []
created_date: '2026-09-23 20:34'
updated_date: '2026-09-24 10:15'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-062
references:
  - design_decisions/output/LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md
  - hardware/datasheets/KLS1-242I.pdf
  - hardware/datasheets/TFT032B018.pdf
  - hardware/userinterface.kicad_sch
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 107000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TFT032B018'in FPC'si modülün arkasına doğru bükülerek kart üzerindeki J3'e (KLS L-KLS1-242I-2.0-30, 30p 0,5 mm flip ZIF, yatay) girer. J3'ün konumu ve açısı FPC'nin çıkış kenarı, uzunluğu, minimum büküm yarıçapı ve kontak yüzüne göre belirlenmeli; yanlış konumda FPC gerilir, ters yüze kıvrılır veya ZIF kapağı kapanmaz.

Büküm sonrası kontak yüzü J3'ün kontak yüzüyle eşleşmeli (KLS1-242I çift temaslı, ancak pin 1 yönü ters dönmemeli). Numune doğrulaması TASK-012'de.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Datasheet'ten FPC çıkış kenarı, serbest uzunluğu, kalınlığı ve kontak yüzü okunmuş; büküm yarıçapı ≥ üretici minimumu (yoksa ≥ 1 mm) alınmış
- [x] #2 J3 konumu ve açısı büküm geometrisinden hesaplanmış; FPC'nin J3 içine girme boyu datasheet ekleme derinliği ±0,3 mm içinde
- [x] #3 Büküm sonrası J3 pin 1 ile LCD FPC pin 1 eşleşiyor; ZIF kapağının açılıp kapanacağı alan (önünde ve üstünde) boş
- [x] #4 Büküm çizimi (yan kesit) design_decisions/ altında; sonuç TASK-012 numune kontrolüne girdi olarak bağlanmış
- [x] #5 J3 PCB'de sabitlenmiş (locked) ve LCD modül izdüşümüne göre konumu User katmanında işaretli
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
TFT032B018 ve KLS1-242I mekanik cizimlerinden FPC boylari, kontak/pin-1 yonu ve ekleme derinligini cikar. En az 1 mm bukum yaricapiyla J3 konumunu hesapla; yan kesit ve User katmani zarflarini olustur, J3u kilitle. Netlist/parity ve mekanik bosluklari dogrula; tolerans ve numune maddelerini TASK-012ye bagla.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 - TFT032B018 ve KLS1-242I datasheet'leri üzerinden FPC büküm geometrisi ve J3 konumu hesaplandı, PCB'de uygulandı.

1. Datasheet ve Geometri Verileri:
   - LCD Modülü: 77.70 x 55.04 x 2.40 mm, AA 64.80 x 48.60 mm (Landscape montaj, AA merkez orijini (100, 100) mm). Modül X: [63.72, 141.42] mm, Y: [72.48, 127.52] mm.
   - FPC Çıkışı: Sağ kısa kenardan (X = 141.42 mm), modül alt kenarından 10.47 ± 0.50 mm ofsetle başlar (Y = 117.05 mm).
   - FPC Boyutları: Serbest düz boy 44.67 ± 0.50 mm, uç genişliği 15.50 ± 0.10 mm (30 pin, 0.5 mm pitch, W = 0.35 mm). İletken kontak boyu 2.5 ± 0.3 mm, PI takviye boyu 5.0 ± 0.3 mm, takviyeli kalınlık 0.30 ± 0.03 mm (maks 0.40 mm).
   - Büküm Yarıçapı: Üretici büküm çiziminde loop çıkıntısı 1.00 mm (Apex X = 142.42 mm, R ≈ 1.2..1.75 mm >= 1.0 mm). Kart kenarına 7.28 mm pay kalır, H2/H4 montaj deliklerine girmez.

2. J3 Konum ve Ekleme Derinliği Hesabı:
   - Büküm sonrası FPC uç noktası: X_tip = 141.42 - 41.00 = 100.42 mm.
   - FPC merkez hattı Y: Y_center = 127.52 - (10.47 + 25.97) / 2 = 109.30 mm.
   - KLS1-242I ekleme derinliği: 2.10 mm stop, 1.30 mm kontak noktası.
   - J3 Footprint: (at 98.00 109.30 90), locked yes.
   - Giriş ağzı X = 102.55 mm, dahili stop X = 100.45 mm.
   - Ekleme boyu: 102.55 - 100.42 = 2.13 mm (Nominal 2.10 mm'ye göre fark +0.03 mm; ±0.3 mm tolerans kriteri sağlandı).

3. Pin 1 ve Kontak Yüzü Doğrulaması:
   - J3 rot 90° olduğunda: Pin 1 Y = 102.05 mm (üstte), Pin 30 Y = 116.55 mm (altta).
   - FPC arkaya katlandığında Pin 1 üstte kalır; J3 Pin 1 ile birebir eşleşir.
   - KLS1-242I çift kontaklıdır; FPC altın parmakları aşağıya (F.Cu) bakarak J3 alt kontaklarına oturur.

4. Doğrulama ve DRC:
   - KiCad 10 CLI DRC: `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
   - Schematic parity: 0 issue.
   - Courtyard overlap: 0, Clearance: 0.

5. Dwgs.User Katmanı ve Çizimler:
   - J3 gövde zarfı (kesikli dikdörtgen [97.90, 100.03] - [102.55, 118.57]), Pin 1 / Pin 30 işaretleri, FPC şerit sınırları ve büküm döngüsü apex çizgisi Dwgs.User katmanına eklendi.
   - Yan kesit çizimi ve ayrıntılı tolerans analizi `design_decisions/output/LCD_FPC_BUKUM_VE_J3_KONUMU_20260924.md` dosyasına yazıldı.
   - TASK-012 numune doğrulama maddelerine FPC büküm, ekleme boyu ve Pin 1 polarite kontrol adımları bağlandı.
   - CHANGES.TXT güncellendi.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
TFT032B018 LCD FPC büküm geometrisi ve J3 konnektör konumu belirlendi. J3 konnektörü PCB üzerinde (X = 98.00 mm, Y = 109.30 mm, rot 90°) konumuna yerleştirildi ve locked olarak kilitlendi. FPC büküm yarıçapı R >= 1.0 mm (loop çıkıntısı +1.0 mm, apex X = 142.42 mm), J3 içi ekleme boyu 2.13 mm (datasheet nominal 2.10 mm, sapma +0.03 mm) olarak doğrulandı. Pin 1 ve kontak yönü netlist parity 0 ile eşleşti. Dwgs.User katmanına J3 zarfı ve büküm yolu işlendi. Yan kesit karar dosyası oluşturuldu, TASK-012 ve CHANGES.TXT güncellendi.
<!-- SECTION:FINAL_SUMMARY:END -->
