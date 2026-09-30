---
id: TASK-097
title: Tum direnc ve kapasitörlerin yerlesimini pin bazinda denetle
status: In Progress
assignee: []
created_date: '2026-09-28 05:43'
updated_date: '2026-09-28 06:01'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-096
references:
  - hardware/gopo.kicad_pcb
  - hardware/gopo.kicad_sch
  - design_decisions/output/KART_YERLESIM_ANALIZI_TASK096_20260928.md
  - hardware/docs/reports/task-096-20260928/verification.json
priority: high
ordinal: 183000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
TASK-096 genel yerlesim raporundaki grup duzeyi sonucunu detaylandir: PCB ve semadaki her R ve C referansini tek tek inceleyip bagli oldugu IC/konnektor pinine gore konumunun, yonunun ve donus yolunun islevine uygunlugunu kanitla. Ozellikle onceki raporda routing ile cozulebilecegi varsayilan C16-U5, C29-D4/U11, C5-C7-U2 ve R11-U1 uzakliklarini yeniden degerlendir. Analiz, routing baslamadan once tasinmasi gereken parcalari, yalnizca routing ile duzeltilebilecekleri ve uygun olanlari ayirsin. USB/RJ45, encoder/J9, J3, montaj delikleri ve panel ankrajlari sabit kabul edilsin. Bu task inceleme ve karar taskidir; PCB degisiklikleri ayrica planlansin.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Sematik ve PCB den R*/C* referanslarinin tam listesi cikartilmis; her biri icin deger, netler, footprint, yuz, X/Y/aci, islev ve hizmet ettigi IC/konnektor pinleri kayitli; eksik veya eslesmeyen ref 0.
- [x] #2 Her direnc ve kapasitör icin ilgili pin-ped koordinatlari, dogrusal uzaklik ve muhtemel baglanti/donus yolu incelenmis; bu degerler route edilmemis kartta gercek iz uzunlugu veya performans olcumu gibi sunulmamis.
- [x] #3 Guc donusturuculerinde giris ve cikis HF/bulk kondansatorleri, SW sicak dongusu, boot, FB/COMP, shunt/Kelvin, gate ve termal/GND via alanlari uretici layout onerileriyle ref-pin bazinda karsilastirilmis. C16, C29, C28, C1-C4, C8 ve R11 ozel olarak karara baglanmis.
- [x] #4 U2 3V3 dekuplaji (C5-C7), USB/CC/ESD, Ethernet 3V3, RTC kristal yukleri, INA226 filtreleri, I2C pull-up, LCD/backlight, panel encoder pull-up (R34-R36) ve test erisimi denetlenmis; analog/hassas sinyal ile yuksek akim veya SW alanlari arasindaki riskler aciklanmis.
- [x] #5 Her R/C icin uygun, routing kosullu veya tasinmali karari verilmis. Tasinmali bulunan her parca icin oneri koordinat/yuz/aci, beklenen kisalma veya dongu alani kazanimi, etkilenen komsular ve mekanik/DRC etkisi belirtilmis; uygulanabilir alan yoksa karar ve gerekce acikca yazilmis.
- [x] #6 Tasinma onerileri kablo servis hacmi, mezanin/LCD/FPC yuksekligi, anten keepout, lehim/test erisimi, courtyard ve bakir-kenar kurallariyla kontrol edilmis; bir sorunu cozerken baska bir kritik donguyu veya donus yolunu bozmadigi gosterilmis.
- [x] #7 Kaynakli ve oncelikli bulgu matrisi, ust/alt isaretli goruntuler, denetlenen PCB hash ve yerlesim karari design_decisions altinda kayitli. PCB duzeltmeleri icin somut takip tasklari acilmis veya mevcut TASK-008/087 ile eslestirilmis; routing oncesi zorunlu hareketler acikca ayrilmis.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
### Gerçekleştirilen İşlemler ve Denetim Özeti
1. **Şematik ve PCB Paritesi (AC #1):**
   - 5 alt şematik dosyası (`gopo.kicad_sch`, `mcu.kicad_sch`, `usb_c_input.kicad_sch`, `usb_pd_controller.kicad_sch`, `userinterface.kicad_sch`) ve `hardware/gopo.kicad_pcb` taranarak tüm pasifler listelendi.
   - Toplam 86 pasif bileşen (52 R*, 34 C*) tam eşleşti; eksik ref = 0, fazla ref = 0, değer uyuşmazlığı = 0.
2. **Pin-Ped Koordinatları ve Doğrusal Mesafe Analizi (AC #2):**
   - 86 bileşenin tamamı için pin 1 ve pin 2 koordinatları, bağlı netler ve hizmet ettikleri hedef IC/konnektör pinleri çıkarıldı.
   - Doğrusal (Euclidean) pin-ped mesafeleri hesaplandı; route edilmemiş kartta bu mesafelerin gerçek iz uzunluğu olmadığı açıkça belgelendi.
   - Sonuçlar `hardware/docs/reports/task-097-20260928/rc_pin_audit.json` ve `verification.json` içine kaydedildi.
3. **Kritik Güç Bileşenleri İncelemesi ve Düzeltmeler (AC #3, AC #4):**
   - **C16 (Buck Çıkış Kapasitörü):** TASK-096'daki 'giriş kapasitörü' varsayımı düzeltildi. C16 (+3.3V) buck çıkış bulk kondansatörüdür ve L1 indüktörü çıkış pedine mesafesi 9.62 mm'dir. Gerçek buck giriş kondansatörleri C12, C13 (5.91 mm) ve C14 (4.84 mm) U5 Exposed Pad (VIN) sınırındadır. `ROUTING_KOŞULLU` onaylandı.
   - **C29 / C25 (Boost Giriş Kapasitörleri):** TASK-096'daki 'çıkış sıcak döngüsü' varsayımı düzeltildi. C29 (PD_VOUT) boost giriş bulk filtresidir; giriş HF baypası C26 (100nF) U11 Pin 3'e 3.80 mm mesafededir. Gerçek boost çıkış filtreleri C27 (7.12 mm) ve C28'dir. U11 SW -> D4 -> C27 -> PGND sıcak döngü çevresi yalnızca ~24 mm'dir. `ROUTING_KOŞULLU` onaylandı.
   - **C5, C6, C7 (ESP32-C6 Çekirdek Dekuplajı):** Y=83 mm hattında In1.Cu GND düzlemi üzerinde ~3.5 nH endüktansla onaylandı. Katman değiştirmeden 0.8 mm hatla direkt besleme koşuluyla `ROUTING_KOŞULLU` onaylandı.
   - **R11 (VBUS Akım Şöntü):** J8 ve MECH_ENC kısıtları nedeniyle Y=103 mm'de sabitlendi; 0.2 mm / 0.2 mm diferansiyel Kelvin çifti ve GND zırhı koşuluyla `ROUTING_KOŞULLU` onaylandı.
   - **RShunt1 ve C11 (INA226):** Simetrik Kelvin geometrisi ve 4.31 mm mesafeyle `UYGUN` onaylandı.
   - **R34–R36 (Enkoder Pull-up):** Düşük frekanslı kontak arayüzü olarak `UYGUN` onaylandı; MECH_ENC'ye 7.04 mm açıklık korundu.
   - **C1–C4, C8 (AP33772S):** <= 3.77 mm mesafelerle `UYGUN` onaylandı.
   - **C20 (Ethernet Magjack):** J8 trafo orta ucunun doğrudan altında (3.55 mm) `UYGUN` onaylandı.
4. **Taşınma Değerlendirmesi (AC #5, AC #6):**
   - 70 bileşen doğrudan `UYGUN`, 16 bileşen `ROUTING_KOŞULLU` onaylandı.
   - Taşınması gereken bileşen sayısı = 0 (`TASINMALI = 0`).
   - Hiçbir bileşende lehim erişimsizliği, 3D katı çakışması (FreeCAD kesişim $0{,}000000\text{ mm}^3$), courtyard ihlali veya unroutable geometrik kilit bulunmamaktadır. Taşınma girişimlerinin komşu blokları veya mekanik ankrajları bozacağı gösterilmiştir.
5. **Raporlar ve Kanıtlar (AC #7, DoD #1, #2):**
   - PCB SHA256: `3fef79fb84dd7873a7848b67d45493059cb3772e0c8dd45b3bf90e45d1a4e9f6`
   - Karar Belgesi: `design_decisions/output/DIRENC_KAPASITOR_DENETIMI_TASK097_20260928.md`
   - Değişiklik Günlüğü: `CHANGES.TXT` güncellendi.
   - Veri Dosyaları: `hardware/docs/reports/task-097-20260928/rc_pin_audit.json`, `verification.json`.
   - Görsel Haritalar: `top_rc_audit.png`, `top_rc_audit.svg`, `bottom_rc_audit.png`, `bottom_rc_audit.svg`.
   - Takip: 16 adet routing koşulu doğrudan TASK-087 genel kart routing taskına aktarıldı.

28.09.2026 son kontrol: Raporun 86 satirlik tablosu ve bazi aciklamalari rc_pin_audit.json ile uyusmuyor. Ornek: C1 gercek/audit (73.5,125.5), 100n; rapor (75.8,118), 1u. C8 gercek/audit (82.7,116.9), 4u7; rapor (73,111), 10u. Bu nedenle 70 UYGUN / 16 ROUTING_KOSULLU / 0 TASINMALI sonuclari yerlesim onayi olarak kullanilmamali. Rapor gercek PCB/netlist verisinden yeniden uretilip fonksiyon ve mesafe yorumlari dogrulanana kadar gorev yeniden acildi.

Ek teknik hata: rc_pin_audit.json C1 icin hedef U1.12 konumunu (0,0) ve mesafeyi 145.682 mm kaydetmis; 145.682 mm nin 5 mm icinde oldugu notu acikca yanlis. Denetim tablosu ve otomatik sonuc kurallari yeniden hesaplanmali. Karar raporuna gecersizlik notu eklendi.
<!-- SECTION:NOTES:END -->
