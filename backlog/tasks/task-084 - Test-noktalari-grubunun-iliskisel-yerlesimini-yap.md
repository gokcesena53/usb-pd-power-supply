---
id: TASK-084
title: Test noktalari grubunun iliskisel yerlesimini yap
status: To Do
assignee: []
created_date: '2026-09-24 07:38'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-069
references:
  - hardware/gopo.kicad_pcb
priority: medium
ordinal: 166000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PCB grubu: TEST NOKTALARI. Güncel kapsam: TP6-TP8, TP11-TP13. Test noktalarını ait oldukları net ve ölçülecek blokla ilişkilendir; tek bir estetik sıraya dizme. Grup üyeliği korunabilir, konumlar ölçüm işlevine göre dağıtılabilir. Diğer gruplardaki TP1-TP5/TP9/TP10/TP14 için de erişim kontrolü yap.

TASK-069 kaynak/ankraj tablosunu uygula. Grup içi x/y/açı ilişkisini routing yapılabilir bir yerleşime dönüştür; mevcut grup üyeliklerini koru. Kart dışındaki blok için nihai kart konumu bu görevin kapsamı değildir. Sabit ankraj istisnalarını koru; yüz seçimini TASK-065 ile koordine et, sonraki flip/taşıma için kontrol notu bırak. Şema/topoloji/BOM değişikliği veya kartın genel routing işlemi bu görev kapsamında değildir. Mevcut yerel izleri eleman hareketiyle birlikte koru ve bağlantısını doğrula.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Tüm TP'lerin net/blok/ölçüm amacı ve prob yaklaşma yüzü tabloya alınmış; altı grup üyesi uygun blok çıkışına yönlendirilmiş.
- [ ] #2 Prob ucu çapı ve gerekli erişim boşluğu belirtilmiş, mevcut GND prob referansı tanımlanmış; LCD/J8 kapalı alanları ve yüksek akım yollarıyla çakışma gösterilmemiş.
- [ ] #3 TASK-069 üretici kuralları ref/pin bazında kontrol edilmiş; istisnalar gerekçeli. Giriş/çıkış/GND ve hassas sinyal çıkış yönleri, gerekli bakır/via/iz koridorları açıklamalı yakın plan üzerinde gösterilmiş.
- [ ] #4 Grup üyeliği/net/polarite ve sabit ankrajlar korunmuş; yeni courtyard/clearance ihlali yok, schematic parity 0. Önce/sonra görünüm, x/y/açı/yüz listesi ve DRC farkı Implementation Notes içinde bağlantılı; mevcut ihlaller ve bağlantısız öğeler ayrı raporlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
