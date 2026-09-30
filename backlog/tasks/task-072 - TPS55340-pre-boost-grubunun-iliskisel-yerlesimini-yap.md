---
id: TASK-072
title: TPS55340 pre-boost grubunun iliskisel yerlesimini yap
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
  - hardware/datasheets/TPS55340.pdf
  - hardware/datasheets/BAS16HT1G.pdf
  - hardware/datasheets/SRI0704-6R8M.pdf
  - design_decisions/output/FB_CLAMP_EN_REFERANSI_20260923.md
priority: high
ordinal: 154000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: TPS55340 PRE-BOOST. Güncel kapsam: U11, L3, D4, D5, C23-C29, R47-R49, R52, R53. Güç döngüsü, SW düğümü, FB/COMP ve termal pad önceliğiyle U11 grubunu düzenle. AOZ1284 grubundaki U6 ortak EN_CTRL/V_X referansına komşuluk ayır. TASK-058 ile oluşturulan D5–U11 FB izini başlangıçta envantere al ve eleman hareketiyle birlikte tutarlı taşı.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 U11/L3/D4/giriş-çıkış kapasiteleri için anahtarlama akım döngüsü çizilmiş; SW bakır alanı ve termal via alanı ayrılmış; FB/COMP bu bölgeden uzak tutulmuş.
- [x] #2 D5 anot–U11 FB bağlantısı mevcut netleriyle kesintisiz ve toplam iz uzunluğu ≤10 mm; yeni konumda ölçülüp kaydedilmiş.
- [x] #3 U6/R50/R51 ortak referansıyla D5 arasındaki grup sınırı ve sessiz GND dönüşü AOZ1284 göreviyle uzlaştırılmış.
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
24.09.2026 — U11/D5 ve dört parçalı B.Cu BOOST_FB izi ankraj bırakılarak
16 üyeli B.Cu grubunun ilişkisel yerleşimi yapıldı. Kart dışı geçici blok
alanı korundu. Önce/sonra görünüm, oklarla işaretli güç/GND/FB/COMP
koridorları, üretici §10.1–10.3 kural kontrolü ve istisnalar:
`design_decisions/output/TPS55340_YERLESIM_TASK072_20260924.md`.
Tam x/y/açı/yüz ve pad/net/UUID envanteri:
`hardware/docs/reports/task-072-20260924/verification.json`.
D5.2–U11.9: 4 aynı UUID'li iz, 2,584607 mm, via yok, ≤10 mm.
DRC önce/sonra 146/146; unconnected 360/360; schematic parity 0/0.
Mevcut 146 ihlal ve 360 bağlantısız öğe karar dosyasında ayrı sayıldı;
yeni courtyard/clearance/short/mask ihlali 0.
TASK-069 tablosu henüz tamamlanmadığından TI kaynağı doğrudan bu grubun
kararında ref/pin bazında uygulandı. C28 ve ortak U6/R50/R51 sınırı
TASK-073/085'e devredildi; güç ve termal via routing'i bu görevin dışında.
<!-- SECTION:NOTES:END -->
