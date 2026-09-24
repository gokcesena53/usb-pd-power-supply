---
id: TASK-086
title: Tum bloklarla kaba PCB alan planini hazirla
status: To Do
assignee: []
created_date: '2026-09-24 13:06'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-010
  - TASK-069
references:
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 168000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
İki turlu yerleşimin ilk turu. Üretici/katman kuralları ve grup envanteriyle kartın tamamı için kaba alan planı hazırla. Portlar kadar güç bloklarını da baştan hesaba kat. Mevcut göreli grup çalışmaları girdidir; bunların tamamının Done olması kaba planın ön koşulu değildir. Son mekanik seçimi TASK-063, ince yerleşimi TASK-008 yapar.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J7 top, J8 bottom/USB-C altı, U2 top/anten dışarı, J9 Ethernet yanı hedefleriyle tüm 15 grubun gerçek XY zarfları ve yüz/yükseklikleri aynı kart planında gösterilmiş; küçük parçaların nihai konumu henüz kilitlenmemiş.
- [ ] #2 LCD/FPC/H1-H4, anten, kablo/fiş ve slot için ayrılan hacimler; buck/boost ve çıkış/ölçüm alanları; güç/sinyal/via/ısıl koridorları birlikte gösterilmiş. Güç blokları kalan boşluğa sonradan sıkıştırılmamış.
- [ ] #3 En az iki aday düzen değerlendirilmiş; en az biri tüm zorunlu geometrik/elektriksel kısıtları sağlıyor veya sağlanamayan kısıt ölçülü olarak raporlanıp TASK-063'e devredilmiş. Uygun çözüm yoksa görev Done yapılmamış.
- [ ] #4 Ethernet altı başlangıçta kullanılmayan alan kabul edilmiş; sığma yalnız bu hacme bağlıysa bağımlılık açıkça işaretlenmiş ve TASK-080 doğrulaması olmadan uygulanabilirlik iddiası yapılmamış.
- [ ] #5 Top/bottom alan planı, blok zarf/yön/bağlantı tablosu, varsayımlar ve tercih gerekçesi kayıtlı; slot tipi bekleniyorsa olası mekanik zarf ayrılmış, freze uygulanmamış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
