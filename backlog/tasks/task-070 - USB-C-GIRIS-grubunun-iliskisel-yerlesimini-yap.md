---
id: TASK-070
title: USB-C GIRIS grubunun iliskisel yerlesimini yap
status: Done
assignee: []
created_date: '2026-09-24 07:38'
updated_date: '2026-09-24 12:25'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/USBLC6-2.pdf
  - hardware/datasheets/SMF_THINKING.pdf
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
priority: high
ordinal: 152000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: USB-C GIRIS. Güncel kapsam: J7, D3, D8, D9, R62, R63, U10. J7 konnektörü esas alınarak VBUS ve CC koruma elemanlarını girişe, U10 USB ESD elemanını veri hattı girişine yerleştir. AP33772S grubundaki C3 ile komşuluk ihtiyacını kaydet; üyeliğini değiştirme.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 J7–koruma–devre yönü ve U10 D+/D- flow-through pad eşlemesi netlerden doğrulanmış; ESD GND dönüşü için doğrudan bakır/via alanı ayrılmış.
- [x] #2 D3/C3 komşuluğu ve CC1/CC2 koruma yolları AP33772S göreviyle eşleştirilmiş; J7 için TASK-063 mekanik ankrajı korunmuş.
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
24.09.2026 — J7 konnektör ankrajı korunarak USB-C GIRIS grubunun 7 üyesi (J7, D3, D8, D9, R62, R63, U10) B.Cu'da giriş koruma, flow-through veri akışı ve ESD dönüş koridorlarına göre ilişkisel yerleştirildi.

Önce/sonra görünüm, oklarla planlanan güç/CC/veri/GND koridorları, üretici kural kontrolü (USBLC6-2, SMF30A, SMBJ30A) ve devir notları:
`design_decisions/output/USB_C_GIRIS_YERLESIM_TASK070_20260924.md`.
Tam x/y/açı/yüz ve pad/net/mesafe envanteri:
`hardware/docs/reports/task-070-20260924/verification.json`.

U10 180° yönlendirmesiyle konnektör tarafı (1/3) ve sistem tarafı (6/4) padleri netlerle birebir eşleşti (stub yok); pin 2 GND dönüşü ve doğrudan via alanı ayrıldı.
D3.1 USB_VBUS ile C3.1 PD_VBUS_SENSED'in doğrudan aynı net olmadığı (Q3 anahtarı/algılama topolojisi) ve CC1/CC2 koruma yolları TASK-071 (AP33772S) görevine devredildi.
J7 mekanik ankrajı (41,05; 77,32; -90°; B.Cu) TASK-063 için korundu.
DRC önce/sonra 146/146, unconnected 360/360, schematic parity 0/0; yeni ihlal 0.

24.09.2026 — Kullanıcı genel yerleşim kararı: design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md. Önceki bottom USB-C/ESP32 ve karşı sağ kenarda anten şartlarının yerini J7 top, U2 top/anten dışarı ve J8 bottom alır. Bu kayıt plan güncellemesidir; PCB uygulaması veya yeni doğrulama kanıtı değildir. Tamamlanan grup/yükseklik çalışmasının tarihsel kanıtı korunur; J7/U2 top'a taşıma ve yeniden doğrulama TASK-063/008 kapsamındadır.
<!-- SECTION:NOTES:END -->
