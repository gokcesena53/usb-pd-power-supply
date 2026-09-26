---
id: TASK-086
title: Tum bloklarla kaba PCB alan planini hazirla
status: Done
assignee: []
created_date: '2026-09-24 13:06'
updated_date: '2026-09-25 09:55'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-010
  - TASK-069
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
  - design_decisions/output/KABA_ALAN_PLANI_TASK086_20260925.md
priority: high
ordinal: 168000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
İki turlu yerleşimin ilk turu. Üretici/katman kuralları ve grup envanteriyle kartın tamamı için kaba alan planı hazırla. Portlar kadar güç bloklarını da baştan hesaba kat. Mevcut göreli grup çalışmaları girdidir; bunların tamamının Done olması kaba planın ön koşulu değildir. Son mekanik seçimi TASK-063, ince yerleşimi TASK-008 yapar.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 J7 top, J8 bottom/USB-C altı, U2 top/anten dışarı, J9 Ethernet yanı hedefleriyle tüm 15 grubun gerçek XY zarfları ve yüz/yükseklikleri aynı kart planında gösterilmiş; küçük parçaların nihai konumu henüz kilitlenmemiş.
- [x] #2 LCD/FPC/H1-H4, anten, kablo/fiş ve slot için ayrılan hacimler; buck/boost ve çıkış/ölçüm alanları; güç/sinyal/via/ısıl koridorları birlikte gösterilmiş. Güç blokları kalan boşluğa sonradan sıkıştırılmamış.
- [x] #3 En az iki aday düzen değerlendirilmiş; en az biri tüm zorunlu geometrik/elektriksel kısıtları sağlıyor veya sağlanamayan kısıt ölçülü olarak raporlanıp TASK-063'e devredilmiş. Uygun çözüm yoksa görev Done yapılmamış.
- [x] #4 Ethernet altı başlangıçta kullanılmayan alan kabul edilmiş; sığma yalnız bu hacme bağlıysa bağımlılık açıkça işaretlenmiş ve TASK-080 doğrulaması olmadan uygulanabilirlik iddiası yapılmamış.
- [x] #5 Top/bottom alan planı, blok zarf/yön/bağlantı tablosu, varsayımlar ve tercih gerekçesi kayıtlı; slot tipi bekleniyorsa olası mekanik zarf ayrılmış, freze uygulanmamış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
25.09.2026 (TASK-086):
1. 99.40 x 61.04 mm kart alanı üzerinde iki aday kaba alan planı (Aday A ve Aday B) modellendi.
2. Aday A (Doğrusal Batı->Doğu güç akışı, Kuzeybatı U2 ESP32-C6 / 22 mm kısa USB 2.0 diferansiyel çifti, J7 top-sol, J8 bottom-sol, J9 sol kablo koridoru, Kuzeydoğu sessiz RTC köşesi 26.5 mm izolasyon) teknik ve geometrik üstünlükleriyle seçildi; Aday B (72 mm uzun USB hattı, karmaşık döngüler) elendi.
3. 15 grubun gerçek XY zarfları ve katman dağılımları kart yüzeyinde bütçelendi; güç blokları için geniş ve kesintisiz alanlar ayrıldı.
4. J8 Mezanin modülü altı Bölge 3 (RJ45 THT bacak çıkıntıları) mutlak keepout olarak ayrıldı; Bölge 2 orta boşluğu başlangıçta kullanılmayan alan kabul edildi.
5. Aday A ve Aday B SVG görselleştirmeleri (floorplan_candidate_a.svg, floorplan_candidate_b.svg) ve sayısal analiz (floorplan_analysis.json) hardware/docs/reports/task-086-20260925/ klasöründe üretildi. DRC 126 (0 hata, 126 metin uyarısı), unconnected 360, schematic parity 0, ERC 0. Karar belgesi: design_decisions/output/KABA_ALAN_PLANI_TASK086_20260925.md.
<!-- SECTION:NOTES:END -->
