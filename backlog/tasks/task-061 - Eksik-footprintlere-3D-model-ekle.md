---
id: TASK-061
title: Eksik footprintlere 3D model ekle
status: Done
assignee: []
created_date: '2026-09-23 20:33'
updated_date: '2026-09-23 20:51'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_pcb
  - hardware/datasheets/korchip_dcl.pdf
  - hardware/datasheets/KLS1-242I.pdf
  - hardware/datasheets/FPI0705-220K.pdf
  - hardware/datasheets/sqjb60ep.pdf
  - hardware/datasheets/L-KLS4-EC1121S-E5A-F12.5.pdf
modified_files:
  - >-
    hardware/libraries/Connector_FPC_Custom.pretty/KLS_L-KLS1-242I-2.0-30_1x30-2MP_P0.50mm_Horizontal.kicad_mod
  - >-
    hardware/libraries/Inductor_Custom.pretty/L_CoreMaster_FPI0705_7.8x7.0mm_H5.0.kicad_mod
  - >-
    hardware/libraries/Package_SO_Custom.pretty/Vishay_PowerPAK_SO-8L_Dual.kicad_mod
  - >-
    hardware/libraries/Power_Output_Custom.pretty/Korchip_DCL_H-Type_D19.0mm_P20.00mm_Horizontal.kicad_mod
  - >-
    hardware/libraries/L-KLS4-EC1121S-E5A-F12.5.pretty/L-KLS4-EC1121S-E5A-F12.5.kicad_mod
  - hardware/libraries/Connector_FPC_Custom.3dshapes/
  - hardware/libraries/Inductor_Custom.3dshapes/
  - hardware/libraries/Package_SO_Custom.3dshapes/
  - >-
    hardware/libraries/Power_Output_Custom.3dshapes/Korchip_DCL_H-Type_D19.0mm_P20.00mm_Horizontal.step
  - hardware/libraries/L-KLS4-EC1121S-E5A-F12.5.3dshapes/
  - hardware/libraries/Generic_Custom.3dshapes/
  - hardware/gopo.kicad_pcb
  - CHANGES.TXT
  - .claude/skills/kicad-footprint/examples/gopo_basic_models.py
  - .claude/skills/kicad-footprint/scripts/step_boxes.py
  - .claude/skills/kicad-footprint/scripts/model_scan.py
  - .claude/skills/kicad-footprint/SKILL.md
priority: high
ordinal: 101000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Yükseklik tabanlı top/bottom ayrımı ve LCD/kutu çakışma kontrolü için her parçanın 3D gövdesi gerekli. 23.09.2026 taramasında PCB'deki 139 footprint'ten 20'sinde (model) yok:

- C33 Power_Output_Custom:Korchip_DCL_H-Type_D19.0mm_P20.00mm_Horizontal
- J3 Connector_FPC_Custom:KLS_L-KLS1-242I-2.0-30_1x30-2MP_P0.50mm_Horizontal
- L1 Inductor_Custom:L_CoreMaster_FPI0705_7.8x7.0mm_H5.0
- Q3, Q5 Package_SO_Custom:Vishay_PowerPAK_SO-8L_Dual
- SW3 L-KLS4-EC1121S-E5A-F12.5
- TP1..TP14 TestPoint_Pad_D1.0mm (düz ped, model gerekmez)

Üretici STEP'i varsa o, yoksa datasheet ölçü çiziminden basitleştirilmiş STEP üretilir (kicad-footprint skill'i; J8 için yapılanla aynı yöntem). Modeller proje kütüphanesinin .3dshapes dizinine konur ve kütüphane footprint'ine atanır, PCB'de yenilenir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 C33, J3, L1, Q3, Q5, SW3 footprintlerinde 3D model var; model yolu ${KIPRJMOD} ile çözülüyor (mutlak yol yok)
- [x] #2 Model gövde yükseklikleri datasheet ile ±0,2 mm uyumlu: L1 5,0 mm, J3 2,0 mm (KLS1-242I-2.0), C33/SW3 datasheet değeri Implementation Notes'a yazılmış
- [x] #3 PCB'de tüm footprintler taranmış: TP dışında modelsiz footprint 0; atanmış ama dosyası bulunamayan model 0
- [x] #4 kicad-cli pcb render (izometrik) ve pcb export step hatasız; ekranda modelsiz parça yok
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026: Basitlestirilmis STEP'ler (step_boxes, footprint koordinati, offset/rotate 0) `.claude/skills/kicad-footprint/examples/gopo_basic_models.py` ile uretildi; mevcut footprint'lere yalniz (model ...) blogu eklendi (CRLF korundu, ped degismedi). Yukseklikler (kart ustu, datasheet):
- J3 KLS1-242I-2.0: 2.00 +-0.15 (model 2.00; flip kapak ACIKKEN 3.1 -> TASK-064 ZIF alani)
- L1 FPI0705: C 5.0 +-0.3 (model 5.0; on render ~5.1 olculdu)
- Q3/Q5 PowerPAK SO-8L Dual: A 1.00/1.07/1.14 (model 1.07)
- C33 Korchip DCL H-type: H 6.5 +-0.5 (model 6.5, coin D19 yatik; maks 7.0), bacaklar kart altina 3.5
- SW3 EC1121S-E5A-F12.5: bushing E -> D=5, F mil L=12.5 -> govde 4.5, bushing ustu 9.5, mil ucu 17.0; pinler kart altina 3.5
fp_check --3d: kati sayilari kutu+1 ile ayni (J3 37, L1 5, Q 8, C33 15, SW3 27); izometrik/on/ust render'larda modeller yerinde.

23.09.2026: PCB taramasinda ek bulgu: 6 standart footprint'in modeli PCB'de atali ama KiCad 10 3dmodels kurulumunda dosyasi YOK (KiCad sessizce modelsiz ciziyordu): L3 L_7.3x7.3_H4.5, U12 WSON-12 3x3, U2 ESP32-C6-MINI-1, Y1 ABS25, J4 SolderWire-1.5sqmm, U5 SOIC-8-1EP EP2.71x3.7. Ikame STEP'ler libraries/Generic_Custom.3dshapes/ (L3 SRI0704 7.3x7.3x4.5 maks, U12 DRR 0.75 (0.8 maks), U2 13.2x16.6x2.4 anten -y, Y1 8.0x3.8x2.5, J4 dik 10 mm kablo zarfi OD3.9); U5 ayni govdeli KiCad SOIC-8-1EP_EP2.41x3.81 modeline yonlendirildi. PCB'de yol metin olarak degistirildi (--pcb). Not: bu standart footprint'ler --refresh edilirse yol eski haline doner.

23.09.2026 kanit: update_pcb.py --keep-tracks --refresh J3 L1 Q3 Q5 SW3 C33 (yalniz 6 YENILE). Yedekle karsilastirma: 139 footprint konum/katman farki YOK, segment 0/0, via 2/2, zone 16/16; UUID degisikligi yalniz yenilenen 6 parcada. model_scan.py: 139 footprint, cozulen model 125, modelsiz (TP haric) 0, dosyasi yok 0. kicad-cli pcb drc --schematic-parity: parity 0 (once/sonra), ihlal 423 -> 421 (yerlesim oncesi courtyard/silk; yenilemeyle gelen yeni ihlal yok), unconnected 356 degismedi. pcb render (izometrik) basarili; pcb export step 218 kati, eksik model uyarisi yok (yalniz 'Board outline is malformed' -> mevcut Edge.Cuts, TASK-062). pcbnew kaydi dosyayi normalize etti (~9k satir diff, cogu bicim).

Commit: f27e168 (kutuphane footprint + STEP + skill + CHANGES.TXT), 5faafa5 (PCB yenileme ve kirik model yollari).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
PCB'de TP disinda modelsiz footprint ve kirik model yolu kalmadi (model_scan: 125 cozulen, 0 eksik). J3, L1, Q3/Q5, C33, SW3 icin datasheet zarfindan STEP; KiCad 10'da bulunmayan standart modeller (L3, U12, U2, Y1, J4) icin ikame, U5 esdeger modele yonlendirildi. Yukseklikler TASK-065 icin notlarda. Schematic parity 0, yerlesim degismedi.
<!-- SECTION:FINAL_SUMMARY:END -->
