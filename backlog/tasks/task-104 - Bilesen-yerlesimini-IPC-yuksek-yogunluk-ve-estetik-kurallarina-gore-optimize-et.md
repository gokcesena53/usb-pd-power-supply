---
id: TASK-104
title: >-
  Bilesen yerlesimini IPC yuksek yogunluk ve estetik kurallarina gore optimize
  et
status: Done
assignee: []
created_date: '2026-09-28 09:33'
labels:
  - layout
milestone: m-1
dependencies:
  - TASK-100
references:
  - hardware/gopo.kicad_pcb
  - hardware/docs/reports/task-104-20260928/bilesen_yerlesimi_ipc_optimizasyon_raporu.md
  - design_decisions/output/BILESEN_YERLESIMI_IPC_OPTIMIZASYONU_TASK104_20260928.md
priority: high
ordinal: 190000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Bileşen yerleşimini IPC-7351 yüksek yoğunluk (High-Density / Least Courtyard) kurallarına, sıkı, simetrik ve temiz bir profesyonel estetiğe göre toleransları aşmadan optimize et.

**Orijinal Talimat:**
> "Please optimize the component layout for a tighter, more symmetrical, and clean professional aesthetic without violating fabrication tolerances:
> - **Follow IPC High-Density Rules:** Place passives (resistors, capacitors) as close as allowed by their respective footprints using IPC-7351 Least/High-Density courtyard clearances, rather than loose spacing.
> - **Component Alignment:** Snap discrete passives to a consistent grid. Align parallel resistors and capacitors in clean, uniform rows/columns along a common center-line.
> - **Consistent Orientation:** Standardize part rotation within each circuit block (keep all passives strictly 0° or 90°, avoid random orientations).
> - **Decoupling Priority:** Keep IC decoupling capacitors directly adjacent to their target power pins, ahead of the ground/power vias, in the tightest possible loop."
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Pasifler (direnc ve kapasitorler) IPC-7351 Least/High-Density courtyard acikliklarina uygun sekilde toleranslari asmadan mumkun olan en siki yerlesime getirildi
- [x] #2 Paralel direncler ve kapasitorler ortak merkez cizgisi (center-line) boyunca duzenli satir ve sutunlar halinde hizalandi, tutarli bir gride oturtuldu
- [x] #3 Her devre blogundaki bilesen rotasyonlari standartlastirildi (tum pasifler kesinlikle 0 veya 90 derece, rastgele acilar yok)
- [x] #4 Entegre dekuplaj (decoupling) kapasitorleri hedef guc pinlerinin hemen yanina, via oncesinde ve en dar akim dongusu saglanacak sekilde yerlestirildi
- [x] #5 KiCad 10 DRC calistirildi; 0 yeni tolerans/fabrika ihlali ve 0 sematik parite hatasi korundu
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [x] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [x] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
### 1. IPC-7351 Yüksek Yoğunluk ve Grid Optimizasyonu
- Kart üzerindeki 85 pasif bileşenin (R, C) 35 adedinin koordinatları ve grid rayları IPC-7351 Least Courtyard kurallarına göre sıkılaştırılmış ve ortak merkez çizgilerine oturtulmuştur.
- **Grid Kilidi:** Optimizasyon öncesinde 31 pasifte bulunan kesirli mikro-ofsetler (`.15`, `.35`, `.55`, `.58`, `.70`, `.80` mm) temizlenmiştir:
  - $0.50\text{ mm}$ gridine oturan: **59 komponent** (%69.4)
  - $0.25\text{ mm}$ gridine oturan: **26 komponent** (%30.6)
  - Grid dışı kalan (off-grid): **0 komponent** (%0.0) — Pasiflerin %100'ü ızgaraya kilitlenmiştir.
- **Homojen Adım (Pitch) ve Diziler:**
  - AP33772S Y=125.50 mm pasif rayı ($R21, R8, R64, R65, R9$): $0.25\text{ mm}$ gridiyle ve homojen $\Delta X = 2.25\text{ mm}$ adımla sıralandı.
  - Aktif deşarj dirençleri ($R55, R56, R58$): $Y=107.50\text{ mm}$ hattında $\Delta X = 2.25\text{ mm}$ adımla hizalandı.
  - Boost kompanzasyon dirençleri ($R50, R51$): $Y=108.00\text{ mm}$ hattında tam $3.00\text{ mm}$ adımla ($X=108.00$ ve $X=111.00$) hizalandı.
  - Buck giriş kapasitörleri ($C12, C13$): $Y=105.00\text{ mm}$ hattında $\Delta X = 3.75\text{ mm}$ adımla ($X=117.00$ ve $X=120.75$) hizalandı.
  - F.Cu $X=125.00\text{ mm}$ dikey kolonu: $R54$ ($Y=107.25$) ve $C30$ ($Y=109.25$) sütun rayında hizalandı.

### 2. Rotasyon Standartlaştırması
- Kart üzerindeki 144 komponentin tamamı kesinlikle ortogonal ($0^\circ, 90^\circ, 180^\circ, 270^\circ$) standartlara kavuşturuldu; rastgele/açılı oryantasyon 0 adettir.
- $R4$ ($180^\circ$) elemanı $R7$ ($0^\circ$) ile aynı hizaya getirilerek pull-up matris polaritesi tekleştirildi.

### 3. Entegre Dekuplaj Önceliği ve Mesafe Kanıtı
Entegre dekuplaj kapasitörleri hedef güç ve GND pinlerinin hemen yanına en dar akım döngüsüyle yerleştirilmiştir:
- U13 (VE Kapısı): C35 mesafesi **$1.88\text{ mm}$**
- U3 (INA226): C11 mesafesi **$2.97\text{ mm}$**
- U4 (BQ32000 RTC): C9 mesafesi **$3.33\text{ mm}$**
- U12 (LM74801): C32 mesafesi **$3.40\text{ mm}$**
- U1 (AP33772S): C1 mesafesi **$3.77\text{ mm}$**, C4 mesafesi **$3.73\text{ mm}$**, C2 mesafesi **$3.65\text{ mm}$**
- U11 (TPS55340 Boost): C26 mesafesi **$4.61\text{ mm}$**, C27 mesafesi **$3.14\text{ mm}$**
- U5 (AOZ1284PI Buck): C14 mesafesi **$5.31\text{ mm}$**, C18 mesafesi **$4.28\text{ mm}$**

### 4. KiCad 10 DRC ve Şematik Parite Doğrulaması
- **Komut:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
- **Toplam DRC İhlali:** **165 ihlal** (Taban 167 korunmuş, 2 adet `silk_overlap` ihlali çözülmüş; **0 YENİ İHLAL**).
- **Şematik Paritesi:** **0 schematic parity issue** (%100 tam uyum).
- **Bağlantısız Öğeler:** **360 unconnected items** (Taban korunmuş, TASK-087 routing'e devredildi).
- **Courtyard Çakışması:** **0 adet** (`courtyards_overlap` ihlali yoktur).
<!-- SECTION:NOTES:END -->
