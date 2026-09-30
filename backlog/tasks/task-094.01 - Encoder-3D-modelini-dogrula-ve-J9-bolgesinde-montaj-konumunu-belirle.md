---
id: TASK-094.01
title: Encoder 3D modelini dogrula ve J9 bolgesinde montaj konumunu belirle
status: Done
assignee: []
created_date: '2026-09-25 13:22'
updated_date: '2026-09-26 10:52'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf
  - >-
    hardware/libraries/L-KLS4-EC1121S-E5A-F12.5.3dshapes/L-KLS4-EC1121S-E5A-F12.5.step
  - design_decisions/output/ENCODER_SOL_PANEL_GOREV_KAPSAMI_20260925.md
  - design_decisions/output/ENCODER_SOL_PANEL_TASK094_20260925.md
  - hardware/libraries/Mechanical_Custom.3dshapes/Encoder_Panel_EC1121S.step
parent_task_id: TASK-094
priority: high
ordinal: 178000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PDF ile encoder STEP modelini dogrula ve J9 bolgesinde 3 mm DUZ DIS PANEL montajini belirle. Kullanici uygulama sirasinda saft ucunun USB giris yuzeyiyle ayni duzlemde olmasi sartini kaldirdi: saft disari tasabilir. Govde on yuzu panel ic yuzune oturur; saft sol panele dik, taban PCB topa 90 derece. Saft yuksekligi USB ve RJ45 kablo giris merkezlerinin ortalamasi. J7/J8 guncel konumlari sabit; bloklarin etki envanteri sonraki alt goreve verilir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Guncel J7/J8 x/y/aci/yuz ve 3D donusumlari, USB/RJ45 kablo giris merkezleri ile USB giris yuzeyi ortak XYZ sisteminde kayitli; govde bounding-box merkezi giris merkezi yerine kullanilmamis.
- [x] #2 PDF sayfa/olcu referanslariyla encoder govde, saft, montaj ve lehim uclari dogrulanmis; mevcut STEP dogrulama sonucu veya duzeltilmis model teslim edilmis.
- [x] #3 J9 bolgesindeki aday, ust ve sol panel gorunumlerinde olculu; encoder/panel/PCB/LCD/RJ45/USB/kablo hacimleri ve etkilenen ref-blok listesi belirlenmis; J9 pinleri 1=A,2=GND,3=B,4=SW,5=GND korunmus.
- [x] #4 3 mm duz dis panel montaji, taban acisi 90 derece, giris merkezlerinin orta yuksekligi ve panelden saft cikintisi sayisal dogrulanmis. Kullanici duzeltmesiyle saft-USB uc duzlemi esitligi aranmaz; J7/J8 tasinmaz.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
26.09.2026 kapanis: PDF olculeriyle duzeltilmis silindirik/F-duzluklu panel STEP olusturuldu. USB giris Z=3,325, RJ45 model giris Z=-9,585; saft Z=-3,130 (PCB topa gore -4,725), Y=112,400. Kullanici duzeltmesine gore 3 mm duz panel, saft cikintisi 9,5 mm. Panel ic yuz X=49,8; PCB ile 0,5 mm montaj payi varsayimi raporda. MECH_ENC sadece mekanik model, SW3 semada panel parcasi. Model sadelestirmeleri ve numune sinirlari raporda; mechanical-analysis.json, solid-check.json ve mounting-review.png kanitlari mevcut.
<!-- SECTION:NOTES:END -->
