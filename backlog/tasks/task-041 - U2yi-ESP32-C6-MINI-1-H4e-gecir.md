---
id: TASK-041
title: U2'yi ESP32-C6-MINI-1-H4'e geçir
status: Done
assignee: []
created_date: '2026-09-23 04:54'
updated_date: '2026-09-23 05:07'
labels:
  - schematic
  - procurement
milestone: m-0
dependencies: []
priority: high
ordinal: 101000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Modül varyantı kesinleşti: ESP32-C6-MINI-1-H4 (4 MB flash). Mevcut şema ESP32-C6-WROOM-1 kullanıyor; MINI-1 daha küçük gövde, farklı pin dizilişi ve daha az GPIO sunuyor. Sembol, footprint, pin atamaları ve BOM güncellenmeli.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 MINI-1 pinout'u datasheet'ten doğrulandı ve tasarımın GPIO ihtiyacını karşıladığı gösterildi
- [x] #2 Sembol ve footprint projeye alındı (kaynak belirtildi)
- [x] #3 U2 değiştirildi, pinler yeniden bağlandı, ERC temiz ve netlist farkı beklenen netlerle sınırlı
- [x] #4 Alanlar güncellendi (Value, MPN, Footprint, Package, SelectionNote)
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
ESP32-C6-MINI-1-H4: 4 MB flash, -40..105 C, 13,2x16,6x2,4 mm (datasheet v1.5 Tablo 1-2).
Pinout (Tablo 3-1) ile karsilastirma: MINI-1 IO10/IO11 vermiyor. Yeniden atama TFT_CS GPIO10 -> GPIO14 (pin 19), TFT_DC GPIO11 -> GPIO7 (pin 16). Kullanilan GPIO 0-9 ve 12-23; modulun verdigi kumeyle birebir ortusuyor, bos GPIO kalmadi. Strapping (4/5/8/9/15) rolleri degismedi.
Sembol/footprint KiCad standart kutuphanesinden: RF_Module:ESP32-C6-MINI-1 (yeni cizim gerekmedi; PCM_Espressif kopyasi artik kullanilmiyor).
Sema: swap_lib + yeniden cizim. IO8/IO9 MINI'de sol kenarda oldugu icin R37/R15/TP9 ve R10/SW1 sol alta tasindi, iki pull-up tek +3.3V rayini paylasiyor (#PWR023 kaldirildi). USB seri dirençleri yerinde kaldi, tasidiklari sinyal yer degistirdi (R2 -> D-, R3 -> D+; USB_DM/USB_DP etiketleri satir degistirdi). Blok basligi ve U2 alanlari guncellendi.
Kanit: netlist karsilastirmasi (U2 pin numaralari haric her net uyelerini korudu; GND'ye modulun tum toprak pedleri katildi), ERC 0 hata / 0 uyari, okunabilirlik denetimi 3 bulgu (ucu de eskiden beri var: SW2 x2, TP9), lint temiz, render kontrol edildi.
Kayit: design_decisions/output/PARCA_TEDARIK_KARARLARI_20260922.md, CHANGES.TXT REV_C, software/FIRMWARE_GEREKSINIMLERI.md pin haritasi, TASK-006 footprint listesi.
<!-- SECTION:NOTES:END -->
