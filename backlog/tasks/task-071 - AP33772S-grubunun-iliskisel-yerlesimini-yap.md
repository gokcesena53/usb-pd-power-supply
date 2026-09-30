---
id: TASK-071
title: AP33772S grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 08:56'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/AP33772S.pdf
  - hardware/datasheets/sqjb60ep.pdf
priority: high
ordinal: 153000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: AP33772S PD KONTROLCU + VBUS SONT / ANAHTAR. Güncel kapsam: U1, Q3, R11, TH1, D1, C1-C4, C8, R8, R9, R12-R14, R21, R64, R65, TP1-TP5. U1 çevresini besleme bypass, PD/CC, şönt ölçümü ve Q3 güç anahtarı ilişkisine göre düzenle. Güncel pad-net atamalarını esas al; eski notlardaki ref ve değerleri kopyalama.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 U1 bypass kapasiteleri ilgili besleme/GND pinlerine yöneltilmiş; CC yolları USB-C grubuna bakan taraftan çıkıyor.
- [x] #2 R11 algılama bağlantıları Kelvin olarak çıkarılabilecek; Q3 gate yolu, güç bakırı ve TH1 termal konumu üretici kaynağına göre gerekçelendirilmiş.
- [x] #3 C3 için J7/D3 yakınlığı grup sınırında korunmuş; güç giriş/çıkış yönü ve test noktalarının erişimi çizimde gösterilmiş.
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
24.09.2026 — AP33772S PD denetleyici grubunun 23 üyesi (U1, Q3, R11, TH1, D1, C1–C4, C8, R8, R9, R12–R14, R21, R64, R65, TP1–TP5) B.Cu'da yüksek akım güç yolu, Kelvin algılama, gate sürüşü, bypass/filtre kapasiteleri ve CC çıkış yönlerine göre ilişkisel olarak yerleştirildi.

Önce/sonra görünüm, oklarla planlanan güç/CC/Kelvin/gate/NTC koridorları, üretici kural kontrolü (AP33772S, SQJB60EP, Isabellenhütte) ve devir notları:
`design_decisions/output/AP33772S_YERLESIM_TASK071_20260924.md`.
Tam x/y/açı/yüz ve pad/net/mesafe envanteri:
`hardware/docs/reports/task-071-20260924/verification.json`.

U1 180° yönlendirmesiyle CC1/CC2 (pad 17/16) doğrudan sol kenara (USB-C J7 tarafına) açıldı; C4 1uF (pin 20) 3.73 mm ve C1 100nF (pin 12) 3.11 mm mesafeyle LDO pinlerine yöneltildi.
R11 5m0 şönt (rot=0) ile Q3 Drain 1 arası 2.26 mm güç yolu ayrıldı; R11.1–U1.1 ve R11.2–U1.24 Kelvin algılama hatları bağımsız tutuldu.
TH1 NTC termistörü (56.0, 145.2) Q3 gövdesine yaklaştırılarak FET aşırı sıcaklık izlemesi sağlandı.
C3 2.2uF cSnkBulk kapasitesi R11.2/Q3.7 düğümünde giriş tarafına yakın konumlandırıldı.
DRC önce/sonra 146/146, unconnected 360/360, schematic parity 0/0; yeni courtyard veya açıklık ihlali 0 (minimum aralık 0.215 mm).
<!-- SECTION:NOTES:END -->
