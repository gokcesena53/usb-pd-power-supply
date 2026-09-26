---
id: TASK-094
title: Sol panel encoder yerlesimini ve sol kart kenarini duzenle
status: Done
assignee: []
created_date: '2026-09-25 13:21'
updated_date: '2026-09-26 10:52'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf
  - design_decisions/output/ENCODER_SOL_PANEL_GOREV_KAPSAMI_20260925.md
  - design_decisions/output/ENCODER_SOL_PANEL_TASK094_20260925.md
  - hardware/docs/reports/task-094-20260925/verification.json
priority: high
ordinal: 177000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Encoderi J9 bolgesinde 3 mm duz dis panele monte edilecek sekilde yerlestir, J9 kablo baglantisini koru. Son kullanici karariyla saft disari tasabilir; onceki USB agziyla saft ucu esitligi kaldirildi. Saft merkezi USB/RJ45 kablo giris merkezlerinin orta yuksekliginde, encoder tabani PCB topa 90 derece. J7/J8 mevcut konum/aci/yuzleri sabit. Etkilenen bloklari kart disina park et; encoder konumu tamamlandiktan sonra yalniz sol Edge.Cuts duzenle. Geri yerlestirme TASK-095 kapsaminda sonraki istir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 J7/J8 ankrajlarinda sifir degisim; etkilenen bloklar envanterli gecici kart disi alanlarda, etkilenmeyen bloklar korunmus.
- [x] #2 Encoder yerlestirildikten sonra sadece sol dis hat degismis; yeni sol kenarda en az 0,254 mm bakir acikligi ve daha siki kurallar korunmus; DRC/parite ve 3D kanitlari kayitli.
- [x] #3 PDF ile dogrulanmis encoder modeli, 3 mm duz panel, orta giris-merkezi saft yuksekligi ve 90 derece yonu olculu raporlanmis; kullanici duzeltmesine gore saft disari tasabilir.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Uygulama sirasinda kullanici karari: Duz dis panele monte et; saft disari tasabilir. Onceki saft ucu-USB giris duzlemi esitligi kaldirildi. Diger konum ve sabit port sartlari korunuyor.

26.09.2026: TASK-094.01/02/03 tamamlandi. PCB SHA256=36cdde4500dcb4acb2f9057a8fbbcb46448c5125013eb7dcabe4655564c085ec kontrol edildi. 26 komponent iki blok halinde kart disinda; TASK-095 baslatilmadi. J7/J8 korunmus, yalniz sol kenar degismis. DRC yeni ihlal 0, 15 mevcut U2 kenar hatasi, parite 0, baglantisiz 360. CHANGES.TXT ve karar raporu guncel. Model/numune sinirlari raporda acik; kart uretime hazir degil.
<!-- SECTION:NOTES:END -->
