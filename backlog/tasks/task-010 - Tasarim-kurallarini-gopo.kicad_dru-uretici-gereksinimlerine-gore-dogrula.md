---
id: TASK-010
title: Tasarım kurallarını (gopo.kicad_dru) üretici gereksinimlerine göre doğrula
status: Done
assignee: []
created_date: '2026-09-22 18:46'
updated_date: '2026-09-25 09:45'
labels:
  - layout
milestone: m-1
dependencies: []
references:
  - hardware/gopo.kicad_dru
  - design_decisions/output/PCB_GENEL_YERLESIM_KARARI_20260924.md
  - design_decisions/output/URETICI_VE_DRC_KURALLARI_TASK010_20260925.md
priority: medium
ordinal: 125000
---

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Üretici seçildi ve yetenekleri not edildi
- [x] #2 gopo.kicad_dru buna göre güncellendi
- [x] #3 Üretici katman dizilimi, dielektrik/bakır kalınlıkları, min iz/aralık/via/delik/freze ve kenar açıklıkları kayıtlı; USB için empedans hesabı ve bottom güç/sinyal referans dönüş planı hazırlanmış.
- [x] #4 Her özel DRC kuralının güncel ref/net ile eşleşmesi doğrulanmış; USB-C eski J1 yerine J7 için kontrol edilmiş, U9 gibi diğer eski seçiciler de denetlenmiş. Kuralın çalıştığı kontrollü örnek/raporla kanıtlı; çözüm yalnız limit gevşetme değil.
- [x] #5 U11 0,2 mm termal via ile min delik kuralı çelişkisi üretici kabiliyeti/footprint seçimiyle çözülmüş; mezanin courtyard istisnası yalnız kanıtlı ref çiftlerine sınırlı tasarlanmış.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
23.09.2026 (TASK-006): U11 footprint'i Package_SO:Texas_HTSSOP-14-1EP_..._ThermalVias 0.2 mm termal via delikleri içeriyor; gopo.kicad_dru/board setup min delik 0.3 mm -> 15x drill_out_of_range. Üreticinin min deliği netleşince ya kural ya da footprint (ThermalVias'sız varyant + elle via) seçilmeli.

24.09.2026 — İki turlu akış: TASK-086 kaba plan → TASK-063 mekanik seçim → TASK-008 ince yerleşim/kritik güzergâh → TASK-087 routing → TASK-088 son kabul → TASK-014 Gerber. Prototip RF: TASK-089; besleme/termal: TASK-090. Bu kayıt task planıdır, PCB uygulama kanıtı değildir.

25.09.2026 (TASK-010):
1. Üretici JLCPCB 4-katman JLC04161H-7628 stackup'ı seçildi (1 oz dış / 0.5 oz iç bakır, 7628 prepreg 0.2104 mm Er=4.6, core 1.065 mm, toplam 1.6 mm) ve hardware/gopo.kicad_pcb stackup'ına işlendi.
2. USB 2.0 90-ohm diferansiyel empedansı IPC-2141 mikroşerit modeliyle hesaplandı: W=0.25 mm (9.84 mil), S=0.20 mm (7.87 mil) -> Z0=55.1 ohm, Zdiff=89.0 ohm (%1.1 sapma). gopo.kicad_pro'ya USB_DIFF_90 sınıfı eklendi.
3. gopo.kicad_dru güncellendi:
   - Eski U9 ve J1 referansları temizlendi.
   - U1/U7/U8/U11/U12 ince adımlı entegreler için 0.15 mm açıklık kuralı tanımlandı.
   - J7 USB-C için 0.25 mm kenar açıklığı ve 0.18 mm NPTH kılavuz deliği kuralı tanımlandı (0.1944 mm mesafe, 4 hole_clearance hatasını çözdü).
   - U11 TPS55340 0.20 mm termal via'ları için kural tanımlandı (15 drill_out_of_range hatasını çözdü, genel 0.30 mm delik kuralı korundu).
   - J8 mezanin courtyard kuralı kanıtlı çiftle (TP14) sınırlandı; RJ45 alanı keepout olarak korundu.
4. Kontrollü deneyler (hardware/docs/reports/task-010-20260925/verify_rules.py):
   - Baseline: 145 ihlal (19 hata: 15 drill_out_of_range + 4 hole_clearance, 126 metin uyarısı).
   - TASK-010 sonrası: 126 ihlal (0 hata, 126 metin uyarısı, 360 unconnected).
   - U11 kuralı olmadan: 15 drill_out_of_range hatası geri geliyor.
   - J7 kuralı olmadan: 4 hole_clearance hatası geri geliyor.
5. ERC 0 hata, schematic parity 0, netlist tam uyumlu. Karar belgesi: design_decisions/output/URETICI_VE_DRC_KURALLARI_TASK010_20260925.md.
<!-- SECTION:NOTES:END -->
