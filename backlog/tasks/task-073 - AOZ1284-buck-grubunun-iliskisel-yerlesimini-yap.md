---
id: TASK-073
title: AOZ1284 buck grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/AOZ1284.pdf
  - hardware/datasheets/TLV431x_Rev10-2025.pdf
  - hardware/datasheets/FPI0705-220K.pdf
  - design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md
priority: high
ordinal: 155000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: AOZ1284 3.3V BUCK. Güncel kapsam: U5, U6, L1, D2, C12-C19, R38-R41, R43, R50, R51. U5 buck güç katını giriş kapasiteleri, diyot, bobin, çıkış kapasiteleri ve FB/COMP ilişkisine göre düzenle. U6/R43/R50/R51 ortak referansını TPS55340 D5 bağlantısıyla birlikte ele al.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Giriş kapasiteleri–U5–D2 yüksek di/dt döngüsü ve L1/çıkış yolu çizilmiş; FB/COMP için sessiz dönüş ve termal bakır alanı ayrılmış.
- [x] #2 U6 pad1 REF, pad2 EN_CTRL, pad3 GND olarak doğrulanmış; R50/R51 REF düğümü kısa tutulmuş, R43 ısı yayılım alanı ayrılmış.
- [x] #3 U11/D5 yönündeki ortak V_X bağlantısı için komşuluk belirlenmiş; güç katının tüm kritik elemanları aynı yüz düzeninde tutulmuş.
- [x] #4 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [x] #5 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes
<!-- SECTION:NOTES:BEGIN -->
TASK-072 devri (24.09.2026): D5.1 EN_CTRL (62,97;57,60), D5.2 BOOST_FB
ve U11.9 FB hattı B.Cu'da; U6.2 EN_CTRL (80,885;54,602), R50.1
(82,185;60,57) ve R51/U6 REF bu hassas sınırın karşı tarafında.
`design_decisions/output/TPS55340_YERLESIM_TASK072_20260924.md` içindeki
sessiz GND ve V_X koridorunu buck yerleşiminde koru. Boost C28 uzak
çıkış deposunun x=82,00; y=64,00 konumunu buck güç alanıyla birlikte
yeniden değerlendir; D4–C27 kısa çıkış yolu ve D5–U11 FB izini bozma.

24.09.2026 — Uygulandı. 19 üyeli B.Cu buck grubunda U5–D2 LX
pad mesafesi 2,20 mm, U5–L1 6,05 mm, L1–C16 4,64 mm oldu.
U6.1 REF/U6.2 EN_CTRL/U6.3 GND padleri kontrol edildi; R50/R51 REF
uçları arası 1,88 mm. R43'ün V_PRE/EN_CTRL yönleri ve ısıl alanı
C28 ve buck sınırıyla uzlaştırıldı. D5–U11 4 segment BOOST_FB izi
2,584607 mm ve B.Cu'da korundu. DRC 146→146, unconnected 360→360,
schematic parity 0→0; yeni courtyard/clearance/short/edge ihlali 0.
Önce/sonra x/y/açı/yüz ve pad-net listesi, DRC JSON'ları, açıklamalı
yakın plan ve KiCad B.Cu katman çıktısı:
`hardware/docs/reports/task-073-20260924/`.
Üretici kaynak/pin kontrolü, routing/via koridorları, mevcut ihlaller,
TASK-069 tablo istisnası ve C28 son routing notu:
`design_decisions/output/AOZ1284_YERLESIM_TASK073_20260924.md`.
<!-- SECTION:NOTES:END -->
