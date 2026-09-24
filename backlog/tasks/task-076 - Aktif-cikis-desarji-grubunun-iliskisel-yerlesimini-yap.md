---
id: TASK-076
title: Aktif cikis desarji grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 11:54'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/BSS138P.pdf
priority: high
ordinal: 158000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: CIKIS DESARJI (R59 yerine aktif). Güncel kapsam: Q4, Q6, D10, R66, R67. Güncel aktif deşarj şemasındaki Q4/Q6 sürme, D10 clamp ve R67 akım/ısı yolunu temel al. Bu grubun adı tarihsel R59 ifadesi içerir; ölçüm grubundaki R59'u yanlışlıkla taşıma. İlgili BSS138P üretici belgesini temin et.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Q4/Q6 gate-source ağı ve D10 yönü pad-net üzerinden doğrulanmış; OUT_POS/GND bağlantı yönleri ölçüm/çıkış grubuna bakıyor.
- [x] #2 R67 kayıp hesabına göre ısı yayılım alanı ayrılmış ve INA226/RTC gibi hassas bloklara etkisi not edilmiş.
- [x] #3 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [x] #4 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
24.09.2026 — Aktif çıkış deşarjı grubunun 5 üyesi (Q4, Q6, D10, R66, R67) Q4/Q6 sürme, D10 kenetleme, R67 güç yolu ve U13 SW_EN mantık kontrolüne göre ilişkisel olarak yerleştirildi.

Önce/sonra görünüm, planlanan güç/DISCH_G/SW_EN/SW_OUT koridorları, R67 kayıp hesabı (0,78 W / 0,92 W), ısı yayılımı, hassas blok (INA226/RTC) kısıtları ve devir notları:
`design_decisions/output/CIKIS_DESARJI_YERLESIM_TASK076_20260924.md`.
Tam x/y/açı/yüz ve pad/net/mesafe envanteri:
`hardware/docs/reports/task-076-20260924/verification.json`.

R67 (2512 2W) 0° açı ile OUT_POS batıya (INA226/J4 yönüne) dönük konumlandırıldı.
Q6 (BSS138P F.Cu) 180° açı ile Pin 3 (Drain) doğrudan R67.2 pad'ine baktırıldı (y=57,5 mm doğrusal ekseninde 2,60 mm aralık).
D10 (BZT52C12 SOD-123) 90° açı ile Katot (DISCH_G) güneye, Anot (GND) kuzeye açıldı; Q6.1/D10.1 ve Q6.2/D10.2 paralel kesişimsiz koridorlar oluşturdu (3,63 mm).
R66 (100k 0603) -90° (270°) açı ile Pin 1 (SW_OUT) kuzeye, Pin 2 (DISCH_G) güneye bağlandı (3,60 mm).
Q4 (BSS138P B.Cu) 0° açı ile Pin 1 (SW_EN) batıya (U13 logic çıkışına) baktırıldı; DISCH_G doğuya tek bir ara via (x≈192, y≈60,5) ile aktarılacak şekilde yerleştirildi (4,08 mm).
DRC önce/sonra 146/145 (D10 referans silk kırpılması çözüldü, yeni ihlal 0), unconnected 360/360, schematic parity 0/0; yeni courtyard veya açıklık ihlali 0 (minimum 2D aralık 0,690 mm).
<!-- SECTION:NOTES:END -->
