---
id: TASK-074
title: LM74801 cikis anahtari grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 11:08'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/LM7480-Q1.pdf
  - hardware/datasheets/sqjb60ep.pdf
priority: high
ordinal: 156000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: LM74801 CIKIS ANAHTARI + IDEAL DIYOT. Güncel kapsam: U12, Q5, C30-C32, D6, R54-R56, R58. U12 ve Q5 çift MOSFET pinlerini, gate sürme/sense yollarını ve çıkış güç akışını temel alarak yerleştir. INA226 ve J4 tarafına güç çıkış koridoru bırak.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 U12 A/DGATE/C–Q5B S/G/D ve HGATE/OUT–Q5A G/S ilişkisi gerçek pad-net haritasıyla belgelenmiş; gate/sense hatları yüksek akım bakırından ayrı çıkarılabilir.
- [x] #2 C32 VS/GND pinlerine yakın; C31 ve hassas kontrol elemanlarının MOSFET ısısı ve SW gürültüsünden uzaklığı kaydedilmiş.
- [x] #3 Q5 güç/termal bakırı ve INA226/J4 bağlantı yönü ayrılmış; bileşen polariteleri kontrol edilmiş.
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
24.09.2026 — LM74801 çıkış anahtarı ve ideal diyot grubunun 10 üyesi (U12, Q5, C30–C32, D6, R54–R56, R58) F.Cu katmanında ortak source (common-source) topolojisi, gate sürme, dV/dt yumuşak açılış, charge pump kapasitesi ve çıkış gücü akışına göre ilişkisel olarak yerleştirildi.

Önce/sonra görünüm, oklarla planlanan güç/DGATE/HGATE/sense/charge pump koridorları, üretici kural kontrolü (TI LM7480-Q1 §12.1/§12.2) ve devir notları:
`design_decisions/output/LM74801_YERLESIM_TASK074_20260924.md`.
Tam x/y/açı/yüz ve pad/net/mesafe envanteri:
`hardware/docs/reports/task-074-20260924/verification.json`.

Q5 (SQJB60EP) 0° açıyla yönlendirildi; üst kenarda Drain A (PD_VBUS_SENSED) ve Drain B (SW_OUT) yüksek akım koridorları, alt kenarda gate/source leaded bacakları (Pins 1–4) ayrıldı.
U12 (117.5, 56.5; 0°) Pin 1 (DGATE) ve Pin 2 (SRC_COMMON) doğrudan Q5.4 ve Q5.3'e yöneltildi (3.94 mm ve 5.02 mm); U12.8 (HGATE) Q5.2'ye yöneltildi (9.09 mm).
C31 (220nF) charge pump kapasitesi TI kuralına uygun olarak Q5 ısıl alanından uzağa (sağ tarafa) konumlandırıldı (3.67 mm).
C32 (100nF) VS bypass kapasitesi U12.10 ve GND pinlerine (3.40 mm / 2.57 mm) yerleştirildi.
D6 Zener koruması Q5A Gate–Source arasına bağlandı; R54–C30 dV/dt devresi C30 referans yazısı lehim maskesinden kaçırılarak yerleştirildi.
DRC önce/sonra 146/146, unconnected 360/360, schematic parity 0/0; yeni courtyard veya açıklık ihlali 0 (minimum aralık 0.350 mm).
<!-- SECTION:NOTES:END -->
