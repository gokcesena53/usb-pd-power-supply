---
id: TASK-049
title: R59 bleed direncini SW_EN kontrollü deşarj devresiyle değiştir
status: Done
assignee:
  - '@claude'
created_date: '2026-09-23 11:23'
updated_date: '2026-09-23 11:34'
labels:
  - schematic
  - procurement
milestone: m-0
dependencies:
  - TASK-048
references:
  - hardware/usb_pd_controller.kicad_sch
  - hardware/datasheets/LM7480-Q1.pdf
  - 'https://cdn.ozdisan.com/public/product/assets/NXP_BSS138P.pdf'
documentation:
  - design_decisions/output/CIKIS_DESARJI_20260923.md
modified_files:
  - hardware/usb_pd_controller.kicad_sch
  - hardware/mcu.kicad_sch
  - design_decisions/output/CIKIS_DESARJI_20260923.md
  - CHANGES.TXT
  - software/FIRMWARE_GEREKSINIMLERI.md
priority: high
ordinal: 46000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
R59 (OUT_POS–GND, 10 kΩ) çıkışı çok yavaş boşaltıyor: 1000 µF kullanıcı yükünde 28 V → 1 V ~33 s. LM74801'in DGATE tarafı ters akımı engellediği için gerilim düşürmede (28 → 5 V) çıkış eski gerilimde kalıyor; firmware'in "OUT_EN low → yeni PDO → doğrula" sırası tıkanıyor. R59 ayrıca şöntün yük tarafında olduğu için INA226 akım okumasına 28 V'ta +2,8 mA hata ekliyor (ofset ±2 mA).

LM74801'de çıkış deşarj özelliği yok (datasheet SNOSD95C incelendi). Kullanıcı kararı (23.09.2026): ekstra GPIO kullanmadan, SW_EN'i transistörlü NOT kapısıyla ters çevirip deşarj FET'ini sürmek. Deşarj; OUT_EN low, INA_ALERT ve kartta güç yokken kendiliğinden açılır. Gate beslemesi SW_OUT'tan (şönt öncesi) alınır, 12 V zener ile sınırlanır. Bilinen bedel: çıkış kapalıyken OUT_POS'a dış kaynak bağlanırsa deşarj sürekli açık kalır; R_dis bunu sürekli taşıyacak güçte seçilmeli.

Parça kararı: FET'ler Q1/Q2 ile aynı BSS138P,215 (60 V, VGS(th) 0,9–1,5 V; tek BOM kalemi). 2N7002K VGS(th) maks 2,5 V olduğu için 3,3 V'luk I2C seviye dönüştürücüde (Q1/Q2) daha zayıf; bu yüzden Q1/Q2 değiştirilmez, yeni FET'ler onlara uyar. R_dis 560 Ω/2 W Özdisan'da yok; 470 Ω/2 W 30,4 V'ta %98 yük. 1 kΩ/2 W anti-surge (PS122WF1001T4E) seçildi.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Şemada deşarj devresi var: NOT kapısı FET'i (gate=SW_EN), deşarj FET'i, R_dis (OUT_POS–drain), R_pu 100k (SW_OUT–DISCH_G), 12 V zener (DISCH_G–GND); netlist ile doğrulandı
- [x] #2 R59 100k 0603 (gate eşiğinin altındaki son gerilim + INA226 Vbus tanımlı kalsın)
- [x] #3 R_dis kayıp hesabı: 30,4 V OV eşiğinde sürekli kayıp ≤ %50 anma gücü
- [x] #4 Yeni ve değişen parçaların MPN/SelectionNote alanları Özdisan stok kaydıyla dolduruldu; Q1/Q2 alanları BSS138P datasheet değerleriyle düzeltildi
- [x] #5 ERC hata sayısı değişiklik öncesinden fazla değil; netlist farkı yalnız beklenen netler
- [x] #6 design_decisions/output altında karar dosyası, CHANGES.TXT girişi ve software/FIRMWARE_GEREKSINIMLERI.md'de deşarj/dış kaynak davranışı yazıldı
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Bağımlılık: TASK-048 (seviye dönüştürücü taşınınca usb_pd_controller'da x 322.58–406.4, y 139.7–198 boşalır).
1. Yeni blok "CIKIS DESARJI" bu alana: SW_OUT etiketi → R66 100k (R_pu) → DISCH_G düğümü; Q4 BSS138P (NOT kapısı: G=SW_EN etiketi, D=DISCH_G, S=GND); D10 BZT52C12 (K=DISCH_G, A=GND); Q6 BSS138P (G=DISCH_G, S=GND, D → R67 1k 2W 2512 → OUT_POS global etiketi).
2. R59: 10k 0805 → 100k 0603 (CRCW0603100KFKTBBC), yerinde kalır.
3. Alanlar: Q4/Q6 = Q1/Q2 alanları (BSS138P,215, Özdisan 737689); D10 = D6 alanları; R66/R59 CRCW0603100KFKTBBC (Özdisan 1089735); R67 PS122WF1001T4E (Özdisan 746122). Q1/Q2 Description/VoltageDS/VgsThreshold/RdsOn/CurrentID/GateCharge BSS138P datasheet'inden.
4. verify --against: beklenen fark = yeni netler DISCH_G, Net-(Q6-D), SW_OUT/SW_EN/OUT_POS/GND'ye eklenen pinler; R59 değer değişimi.
5. design_decisions/output/CIKIS_DESARJI_20260923.md, CHANGES.TXT, FIRMWARE_GEREKSINIMLERI.md.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanıt (verify.py --against taşıma sonrası netlist, gerçek dosya): ERC 0 ihlal (0 hata, 0 uyarı), 108 -> 110 net. Fark yalnız beklenen netler: YENI /USB_PD_CONTROLLER/DISCH_G = D10.1, Q4.3, Q6.1, R66.2; YENI Net-(Q6-D) = Q6.3, R67.2; SW_EN += Q4.1; SW_OUT += R66.1; OUT_POS += R67.1; GND += D10.2, Q4.2, Q6.2. R59 değer 10k -> 100k, footprint 0805 -> 0603 (netlist bağlantısı aynı). E.lint(blok) boş; readability.py toplam bulgu HEAD ile aynı (10), yeni blokta bulgu yok; render ile bakıldı (not metni önce GND sembollerine biniyordu, aşağı alınıp çerçeve y=201.93'e uzatıldı).

R67 hesabı: 1k, 28 V -> 0.78 W (%39), 30.4 V OV eşiği -> 0.92 W (%46 < %50). 560R/2W Özdisan'da stokta yok (arama 23.09.2026), 470R/2W 30.4 V'ta %98. 1000 uF 28->5 V 1.72 s, 28->2 V 2.64 s.

Refs: Q4 (NOT kapısı), Q6 (deşarj), D10, R66, R67 — boş numaralar. Betik: scratchpad step2_discharge.py (kopyada doğrulandı, gerçek dosyaya uygulandı, kopya ile netlist farkı YOK).
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
R59 tek başına bleed olmaktan çıktı; OUT_POS'a SW_EN kontrollü aktif deşarj eklendi (usb_pd_controller, "CIKIS DESARJI" bloğu, eski seviye dönüştürücü yeri).

- Q4 BSS138P: SW_EN NOT kapısı (G=SW_EN, D=DISCH_G, S=GND).
- Q6 BSS138P + R67 1k 2W 2512 anti-surge (PS122WF1001T4E): OUT_POS deşarjı.
- R66 100k (SW_OUT → DISCH_G, şönt öncesi): gate beslemesi; kart güçsüzken de çalışır.
- D10 BZT52C12: DISCH_G ≤ 12 V.
- R59 10k 0805 → 100k 0603 (CRCW0603100KFKTBBC).
- Q1/Q2 değiştirilmedi (zaten BSS138P,215; 2N7002K VGS(th) maks 2.5 V ile seviye dönüştürücüde daha zayıf). Yeni FET'ler aynı kaleme uyduruldu, Q1/Q2 alanları datasheet'e göre düzeltildi.

Doğrulama: ERC 0/0, netlist farkı yalnız beklenen netler, lint boş, render. Dokümanlar: design_decisions/output/CIKIS_DESARJI_20260923.md, CHANGES.TXT, FIRMWARE_GEREKSINIMLERI.md §3.

Riskler: dış kaynak bağlıyken deşarj kapatılamaz (R67 sürekli ~0.9 W); PCB'de R67 bakır alanı ve R59 footprint değişimi TASK-006/008'de. Ölçümler TASK-050'de. Commit edilmedi.
<!-- SECTION:FINAL_SUMMARY:END -->
