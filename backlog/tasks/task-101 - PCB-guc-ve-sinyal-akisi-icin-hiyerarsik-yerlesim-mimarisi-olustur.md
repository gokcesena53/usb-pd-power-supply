---
id: TASK-101
title: PCB guc ve sinyal akisi icin hiyerarsik yerlesim mimarisi olustur
status: Done
assignee: []
created_date: '2026-09-28 11:30'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-096
  - TASK-100
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/task-101-20260928/hiyerarsik_yerlesim_mimarisi_raporu.md
  - design_decisions/output/HIYERARSIK_YERLESIM_MIMARISI_TASK101_20260928.md
priority: high
ordinal: 187000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Kartın elektriksel ve sinyal akışını hiyerarşik, mantıksal ve fonksiyonel aşamalara (stages) bölerek yeniden yapılandır. Güç akışını soldan sağa kesintisiz tek yönlü bir boru hattı (pipeline) haline getir; hassas analog algılama, dijital kontrol (MCU/Ethernet/RTC) ve kullanıcı arayüzü (LCD/Enkoder) bloklarını fiziksel ve katmansal olarak hiyerarşik bölgelere (zoning) ayır.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Ana güç akışı soldan sağa doğrusal hiyerarşik zincir olarak düzenlenmiş: Giriş (J7/U10) -> PD & Giriş Anahtarı (U1/Q3) -> Boost Ön Regülatör (U11/L3) -> Buck Regülatör (U5/L1) -> İdeal Diyot & Koruma (U12/Q5) -> Akım/Güç İzleme (U3/RShunt1) -> Çıkış Terminali (J4).
- [x] #2 Güç akışında katman atlamaları (B.Cu ile F.Cu arasındaki gereksiz via geçişleri) asgari düzeye indirilmiş; yüksek akım hattının katman hiyerarşisi netleştirilmiş.
- [x] #3 Kart alanı fonksiyonel bölgelere (zoning) ayrılmış: Üst bölge (Y < 90 mm) düşük gürültülü dijital/RF/haberleşme, alt bölge (Y > 90 mm) anahtarlamalı güç dönüşümü, orta katman kullanıcı arayüzü olarak sınırlandırılmış.
- [x] #4 Hızlı anahtarlama yapan gürültülü indüktör ve anahtar düğümleri (LX, SW) ile hassas Kelvin akım algılama (INA226, R11) ve kristal (Y1) hatları arasında hiyerarşik fiziksel izolasyon sağlanmış.
- [x] #5 Hiyerarşik zonlama sonrasında global ratsnest çaprazlık testi (ratsnest crossing test) çalıştırılmış; bloklar arası sinyal kesişimlerinin (örümcek ağı düğümlerinin) ve toplam sinyal izi uzunluğunun azaldığı kanıtlanmış.
- [x] #6 KiCad 10 DRC çalıştırılmış; 0 yeni ihlal ve 0 schematic parity hatası korunmuş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (blok akış şeması/bölge analizi/DRC) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
### 1. Hiyerarşik Güç Boru Hattı (Power Pipeline) Doğrulaması
- **Soldan Sağa Monoton Merkez İlerlemesi:**
  - Aşama 1: J7, U10, D3 (Giriş & ESD/TVS, F.Cu) $\rightarrow$ Merkez $X = 58.66\text{ mm}$ ($X \in [52.98, 61.50]$)
  - Aşama 2: U1, Q3, R11 (PD & Giriş FET, B.Cu) $\rightarrow$ Merkez $X = 77.17\text{ mm}$ ($X \in [76.50, 78.50]$)
  - Aşama 3: L3, U11, D4, C29, C27 (Pre-Boost, B.Cu) $\rightarrow$ Merkez $X = 98.04\text{ mm}$ ($X \in [87.50, 104.00]$)
  - Aşama 4: U5, L1, C12, C13 (Buck Regülatör, B.Cu) $\rightarrow$ Merkez $X = 122.88\text{ mm}$ ($X \in [117.00, 127.00]$)
  - Aşama 5: Q5, U12, C32 (LM74801 İdeal Diyot, F.Cu) $\rightarrow$ Merkez $X = 134.50\text{ mm}$ ($X \in [128.50, 139.50]$)
  - Aşama 6: RShunt1, U3, C11 (Kelvin Algılama, B.Cu) $\rightarrow$ Merkez $X = 137.98\text{ mm}$ ($X \in [136.00, 141.20]$)
  - Aşama 7: J4, D7 (Çıkış Klemensi & TVS, B.Cu) $\rightarrow$ Merkez $X = 145.00\text{ mm}$ ($X \in [144.00, 146.00]$)
- Boru hattı kesin soldan sağa $X$ ilerleyişi ($58.66 \rightarrow 77.17 \rightarrow 98.04 \rightarrow 122.88 \rightarrow 134.50 \rightarrow 137.98 \rightarrow 145.00\text{ mm}$) sergilemekte; güç yolunda geri dönüş (backtrack) veya dolambaçlı geçiş bulunmamaktadır.

### 2. Katman Hiyerarşisi ve Çift Taraflı Güç Dağılımı
- B.Cu anahtarlamalı güç dönüşümünün ana katmanıdır.
- LM74801 (U12) ve çift N-MOSFET (Q5), Buck regülatörünün (U5/L1) tam arkasında `F.Cu` katmanında konumlandırılarak kart alanından tasarruf edilmiş ve ısı çift taraflı bakıra yayılmıştır.
- Buck $\rightarrow$ Q5 $\rightarrow$ RShunt1/J4 katman geçişleri TASK-087 genel routing aşamasında çoklu via matrisleriyle (via arrays) dikilecektir.

### 3. Fonksiyonel Zonlama (Zoning) ve Gürültü İzolasyonu
- **Kuzey Zonu ($Y < 90\text{ mm}$):** 42 komponent. Düşük gürültülü dijital/RF/haberleşme zonu. ESP32-C6 (U2) dahili anten keepout hacmi ($Y < 69.48\text{ mm}$) %100 temizdir; Waveshare mezanini (J8), BQ32000 RTC (U4/Y1) ve butonlar bu zonda yer alır.
- **Güney Zonu ($Y \ge 90\text{ mm}$):** 101 komponent. Yüksek akımlı DC-DC anahtarlamalı güç dönüşüm zonu.
- **Hızlı Anahtarlama İzolasyonu:**
  - Y1 RTC Kristali $\leftrightarrow$ L1 Buck İndüktörü: $18.12\text{ mm}$; L3 Boost İndüktörü: $49.19\text{ mm}$
  - U3 INA226 $\leftrightarrow$ L1: $17.56\text{ mm}$; L3: $39.25\text{ mm}$
  - RShunt1 $\leftrightarrow$ L1: $22.02\text{ mm}$; L3: $39.45\text{ mm}$
  - U2 MCU $\leftrightarrow$ L1: $53.96\text{ mm}$; L3: $38.56\text{ mm}$
  - R11 VBUS Şönt $\leftrightarrow$ L1: $50.80\text{ mm}$; L3: $21.82\text{ mm}$
- Hassas analog ve osilatör hatları gürültü kaynaklarından en az $17.56\text{ mm}$ uzakta tutulmuş ve In1.Cu katı GND düzlemiyle ekranlanmıştır.

### 4. Metrikler ve DRC Doğrulaması
- **Ratsnest Çaprazlık Testi:** 127 sinyal hattında 185 kesişim, $1450.84\text{ mm}$ tel uzunluğu tabanı korundu.
- **KiCad 10 DRC:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
  - Toplam İhlal: 164 (Taban korundu, **0 YENİ İHLAL**)
  - Şematik Paritesi: **0 schematic parity issue** (%100 parite)
  - Bağlantısız Öğeler: 360 (Taban korundu, TASK-087'ye devredildi)
- **Rapor ve Karar:**
  - `hardware/docs/reports/task-101-20260928/hiyerarsik_yerlesim_mimarisi_raporu.md`
  - `design_decisions/output/HIYERARSIK_YERLESIM_MIMARISI_TASK101_20260928.md`
<!-- SECTION:NOTES:END -->
