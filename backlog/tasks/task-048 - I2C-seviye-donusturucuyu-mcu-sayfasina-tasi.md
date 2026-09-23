---
id: TASK-048
title: I2C seviye dönüştürücüyü mcu sayfasına taşı
status: Done
assignee:
  - '@claude'
created_date: '2026-09-23 11:22'
updated_date: '2026-09-23 11:34'
labels:
  - schematic
milestone: m-0
dependencies: []
references:
  - hardware/usb_pd_controller.kicad_sch
  - hardware/mcu.kicad_sch
modified_files:
  - hardware/mcu.kicad_sch
  - hardware/usb_pd_controller.kicad_sch
  - .claude/skills/kicad-schematic/scripts/kisch_sheet.py
  - CHANGES.TXT
priority: medium
ordinal: 105000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
"I2C SEVIYE DONUSTURUCU 5V <-> 3.3V" bloğu (Q1/Q2 BSS138P, R4–R7 4k7) usb_pd_controller sayfasında duruyor. Blok yalnız MCU tarafının I2C'sini 5V'luk PD tarafına bağlıyor; güç sayfasında yer kaplıyor. Taşınınca usb_pd_controller'da INA226 bloğunun altında boşalan alan, R59 yerine gelecek çıkış deşarj bloğu için kullanılacak. mcu sayfası A4'te boş alan yok (en büyük boşluk ~150×35 mm, blok 84×56 mm).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Q1, Q2, R4, R5, R6, R7 ve blok çerçevesi/başlığı mcu.kicad_sch'de; usb_pd_controller.kicad_sch'de artık yok
- [x] #2 verify.py --against (taşıma öncesi netlist): baglanti farki YOK (yalnız net yeniden adlandırma)
- [x] #3 ERC hata/uyarı sayısı taşıma öncesinden fazla değil
- [x] #4 readability.py mcu.kicad_sch taşınan blokta yeni bulgu vermiyor; render ile bakıldı
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. verify.py --save ile referans netlist (base.net).
2. mcu.kicad_sch kağıdını A3'e çıkar (A4'te 84×56 mm boşluk yok).
3. kisch_sheet.move_block('usb_pd_controller', 'mcu', kutu (322.58,139.7,406.4,195.58), dx=-38.1, dy=-111.76) → blok RTC çerçevesinin sağına (x 284.48–368.3, y 27.94–83.82).
4. verify --against: bağlantı farkı YOK; readability + render.
KiCad açık olduğu için önce proje kopyasında (scratchpad/proj) çalıştır, kapanınca gerçek dosyaya uygula.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
kisch_sheet.move_block/ensure_lib_symbol_from hatası bulundu ve düzeltildi: hedef önbelleğe kopyalanan sembol tanımı tek sekmeyle başlıyordu; missing_lib_symbols ("\n\t\t(symbol") onu görmedi ve verify.py 'Transistor_FET:BSS138 onbellekte yok' uyarısı verdi. Düzeltme .claude/skills/kicad-schematic/scripts/kisch_sheet.py (önek '\t').

Kanıt (verify.py --against önceki netlist, gerçek dosya): ERC 0 ihlal (0 hata, 0 uyarı), 108 net, netlist farki: YOK. mcu.kicad_sch paper A4 -> A3; blok x 284.48-368.3, y 27.94-83.82 (RTC çerçevesinin sağı). readability.py: HEAD'de 10 bulgu, sonrasında 10 (R4.Reference/Value bulgusu blokla birlikte taşındı, önceden vardı). Render ile bakıldı. Betik: scratchpad step1_move.py (KiCad açıkken proje kopyasında doğrulandı, kapanınca gerçek dosyaya uygulandı; kopya ile gerçek netlist farkı YOK).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
I2C seviye dönüştürücü (Q1, Q2, R4–R7, çerçeve ve başlık) usb_pd_controller'dan mcu sayfasına taşındı; mcu sayfası A3'e çıkarıldı, blok RTC'nin sağında. Bağlantı değişmedi (verify --against: netlist farki YOK, ERC 0/0). Taşıma sırasında kisch_sheet.ensure_lib_symbol_from'daki girinti hatası düzeltildi (önbelleğe kopyalanan tanım araçlarca görünmüyordu). CHANGES.TXT'ye işlendi. Boşalan alan TASK-049'un deşarj bloğu için kullanıldı. Commit edilmedi.
<!-- SECTION:FINAL_SUMMARY:END -->
