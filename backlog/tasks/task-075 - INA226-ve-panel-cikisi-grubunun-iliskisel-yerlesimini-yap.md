---
id: TASK-075
title: INA226 ve panel cikisi grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 12:02'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/ina226.pdf
priority: high
ordinal: 157000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: INA226 OLCUM + PANEL CIKISI. Güncel kapsam: U3, U13, RShunt1, J4, D7, C11, C35, R27, R59, R61. RShunt1–U3 Kelvin ölçümü, LM74801'den gelen güç akışı, J4 panel kablo pedleri ve U13 koruma mantığını birlikte yerleştir. R59'un güncel şemadaki işlevini esas al.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 RShunt1 güç yolu ile IN+/IN- Kelvin çıkışları ayrılmış; U3 girişlerine simetrik, kısa ve gürültü bölgesinden uzak güzergâh ayrılmış.
- [x] #2 C11/C35 ait oldukları IC besleme pinlerine yerleştirilmiş; U13/ALERT/kapatma ilişkisi netlerden doğrulanmış.
- [x] #3 J4 OUT_POS/GND kablo lehim ve erişim alanı, D7 koruma dönüşü ve 3 A güç bakırı koridoru gösterilmiş; termal/iz hesabı TASK-008 kapsamına aktarılmış.
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
24.09.2026 — INA226 akım/güç ölçümü ve panel çıkışı grubunun 10 üyesi (U3, U13, RShunt1, J4, D7, C11, C35, R27, R59, R61), TI INA226 Kelvin algılama kuralları, 3 A çıkış güç akışı, TVS koruma kenetlemesi, U13 donanım kapatma mantığı ve panel kablo lehimleme alanına göre ilişkisel olarak yerleştirildi.

Önce/sonra görünüm, planlanan güç/Kelvin/ALERT/SW_EN koridorları, 3 A güç yolu ve termal değerlendirme, TVS koruması ve devir notları:
`design_decisions/output/INA226_PANEL_CIKISI_YERLESIM_TASK075_20260924.md`.
Tam x/y/açı/yüz ve pad/net/mesafe envanteri:
`hardware/docs/reports/task-075-20260924/verification.json`.

RShunt1 (5m0 2512 B.Cu) 0° açı ile SW_OUT batıdan girecek, OUT_POS doğudan çıkacak şekilde yerleştirildi (45 mW kayıp).
U3 (INA226 TSSOP-10 B.Cu) -90° (270°) açı ile RShunt1'in kuzeyine yerleştirildi; U3.10 (IN+) ve U3.9 (IN-) hatları 4,310 mm tam eşit simetrik Kelvin diferansiyel çifti oluşturdu. U3.8 (VBUS) 4,01 mm mesafeyle bağlandı.
C11 (100n 0402) U3.6 (VS) ve U3.7 (GND) pinlerinin hemen dibine (2,97 mm) yerleştirildi.
J4 (1x02 pitch 7,8 mm) ön panel 1,5 mm² silikon kablo lehimlemesi için 3,9 mm TH ped çevresinde geniş erişim alanıyla doğuya yerleştirildi.
D7 (SMBJ30A SMB TVS) ve R59 (100k 0603 bleed) J4 klemensinin hemen bitişiğine, OUT_POS ve GND arasına paralel bağlandı (D7–J4: 6,78 mm / 8,96 mm).
U13 (74LVC1G08 SOT-23-5) donanım koruma mantığı 0° açı ile B.Cu'da konumlandırıldı; U3.3 (INA_ALERT) hattı R27 (10k 0402 pull-up, 4,74 mm) üzerinden U13.2'ye bağlandı. U13.1 (OUT_EN) R61 (4k7 pull-down, 2,87 mm) ile toprağa çekildi. C35 (100n bypass, 1,88 mm) U13.5 dibine kondu. U13.4 çıkışı SW_EN barasına yöneltildi.
DRC önce/sonra 145/145, unconnected 360/360, schematic parity 0/0; yeni courtyard veya açıklık ihlali 0 (minimum 2D aralık 0,390 mm).
<!-- SECTION:NOTES:END -->
