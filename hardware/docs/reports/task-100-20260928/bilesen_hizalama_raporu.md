# REV_C Bileşen Hizalama ve Yerleşim Alanı Optimizasyonu Raporu (TASK-100)

**Tarih:** 28 Eylül 2026  
**İncelenen Dosya:** `hardware/gopo.kicad_pcb`  
**Araç Sürümleri:** KiCad 10.0.5, Python 3.11.5 / 3.14.6  
**Durum:** TAMAMLANDI (DONE)

---

## 1. Amaç ve Kapsam

TASK-100 kapsamında; PCB üzerindeki pasif ve aktif bileşenlerin (özellikle Boost U11 ve Buck U5 anahtarlama çevrelerindeki bileşenlerin) dağınık ve basamaklı (staggered) yerleşimleri yatay ve dikey ortak referans eksenlerine (grid raylarına) oturtulmuş, rastgele mikro-ofsetler (`.11`, `.16`, `.36`, `.66`, `.76`, `.96` mm) temizlenmiş, yönelim açıları ortogonal standartlara (0° / 90° / 180° / 270°) normalize edilmiş ve kesintisiz yönlendirme koridorları açılmıştır.

Sabit mekanik ankrajlar (`H1–H4`, `J7`, `J8`, `J9`, `J3`, `MECH_ENC`) ve `U2` RF modülü konumları 0,000 mm sapma ile korunmuştur.

---

## 2. Koordinat Hizalama ve Grid Optimizasyonu Tablosu

Aşağıdaki tabloda mikro-ofsetleri temizlenen ve grid eksenlerine oturtulan tüm komponentlerin önceki ve sonraki koordinatları, paylaştıkları eksen rayları ve pitch (adım) değerleri listelenmiştir:

| Ref | Değer | Kılıf | Katman | Önceki Konum $(X, Y)$ [mm] | Yeni Konum $(X, Y)$ [mm] | Ortak Eksen / Grid Rayı | Pitch / Koridor Durumu |
|:---|:---|:---|:---|:---|:---|:---|:---|
| **C29** | 47µF | 1210 | B.Cu | $(87.650, 111.660)$ | $(87.500, 111.500)$ | $X = 87.50\text{ mm}$ Rayı | C25 ile dikey kolon hizalı |
| **C25** | 4.7µF | 1210 | B.Cu | $(87.650, 119.660)$ | $(87.500, 119.500)$ | $X = 87.50\text{ mm}$ / $Y = 119.50\text{ mm}$ | C29 ile $X$, R47 ile $Y$ hizalı |
| **R47** | 78.7k | 0603 | B.Cu | $(91.650, 119.660)$ | $(91.500, 119.500)$ | $Y = 119.50\text{ mm}$ Rayı | C25 ile yatay rayda, $\Delta X = 4.00\text{ mm}$ |
| **D4** | SX36 | SMA/B | B.Cu | $(102.950, 114.660)$ | $(103.000, 114.500)$ | $X = 103.00\text{ mm}$ Rayı | SW-V_PRE güç akışı koridoru |
| **C26** | 100nF | 0603 | B.Cu | $(104.150, 117.360)$ | $(104.000, 117.500)$ | $X = 104.00\text{ mm}$ Rayı | C27 ile dikey kolon hizalı |
| **C27** | 4.7µF | 1210 | B.Cu | $(103.950, 121.160)$ | $(104.000, 121.000)$ | $X = 104.00\text{ mm}$ Rayı | C26 ile dikey kolon hizalı |
| **D5** | BAS16H | SOD-323 | B.Cu | $(92.170, 123.260)$ | $(92.200, 123.200)$ | $X = 92.20\text{ mm}$ Eksen | BOOST_FB yol mesafesi $\le 2.6\text{ mm}$ korundu |
| **R48** | 30.1k | 0603 | B.Cu | $(88.350, 125.160)$ | $(88.500, 125.000)$ | $Y = 125.00\text{ mm}$ Rayı | Temiz $0.5\text{ mm}$ grid |
| **C23** | 47nF | 0603 | B.Cu | $(100.150, 125.760)$ | $(100.000, 125.500)$ | $Y = 125.50\text{ mm}$ Rayı | R53 ile ortak ray; $\Delta X = 3.50\text{ mm}$ |
| **R53** | 100k | 0603 | B.Cu | $(103.650, 125.760)$ | $(103.500, 125.500)$ | $Y = 125.50\text{ mm}$ Rayı | C23 ile ortak ray; $\Delta X = 3.50\text{ mm}$ |
| **R49** | 9.76k | 0603 | B.Cu | $(89.150, 127.960)$ | $(89.000, 128.000)$ | $Y = 128.00\text{ mm}$ Rayı | C24 ile $\Delta X = 2.50\text{ mm}$ |
| **C24** | 100nF | 0603 | B.Cu | $(91.550, 127.960)$ | $(91.500, 128.000)$ | $Y = 128.00\text{ mm}$ Rayı | R49 ve R52 ile ortak ray ($\Delta X = 2.5/3.0\text{ mm}$) |
| **R52** | 2.0k | 0603 | B.Cu | $(94.650, 127.960)$ | $(94.500, 128.000)$ | $Y = 128.00\text{ mm}$ Rayı | C24 ile $\Delta X = 3.00\text{ mm}$ |
| **C12** | 4.7µF | 1210 | B.Cu | $(120.800, 104.910)$ | $(120.800, 105.000)$ | $Y = 105.00\text{ mm}$ Rayı | C13 ile ortak ray; $\Delta X = 3.80\text{ mm}$ |
| **C13** | 4.7µF | 1210 | B.Cu | $(117.115, 104.910)$ | $(117.000, 105.000)$ | $Y = 105.00\text{ mm}$ Rayı | C12 ile ortak ray; $\Delta X = 3.80\text{ mm}$ |
| **R40** | 3.24k | 0603 | B.Cu | $(116.500, 108.100)$ | $(116.500, 108.000)$ | $Y = 108.00\text{ mm}$ Rayı | Temiz $0.5\text{ mm}$ grid |
| **C18** | 10nF | 0603 | B.Cu | $(121.800, 108.300)$ | $(121.800, 108.500)$ | $Y = 108.50\text{ mm}$ Rayı | Temiz $0.5\text{ mm}$ grid |
| **R41** | 51k | 0603 | B.Cu | $(123.500, 110.200)$ | $(123.500, 110.000)$ | $Y = 110.00\text{ mm}$ Rayı | Temiz $0.5\text{ mm}$ grid |
| **R38** | 100k | 0603 | B.Cu | $(131.000, 109.300)$ | $(131.000, 109.500)$ | $Y = 109.50\text{ mm}$ Rayı | Temiz $0.5\text{ mm}$ grid |
| **L1** | 22µH | Özel | B.Cu | $(126.995, 97.370)$ | $(127.000, 97.500)$ | $X = 127.00\text{ mm}$ Eksen | Mikro sapma temizlendi |

---

## 3. Doğrusal Bloklar ve Pitch Standartlaştırması

1. **MCU Pull-up ve Filtre Grubu (F.Cu $Y = 83.00\text{ mm}$):**
   - $R16 (82.50) \rightarrow R2 (84.50) \rightarrow R3 (86.50) \rightarrow R15 (88.50) \rightarrow R37 (90.50) \rightarrow R10 (92.50)$
   - Standart adım (pitch): **$2.00\text{ mm}$**, 90° dikey oryantasyon.
2. **AP33772S Çıkış / Giriş Pasif Bloğu (B.Cu $Y = 125.50\text{ mm}$):**
   - $R35 (65.0) \rightarrow R36 (67.5) \rightarrow C1 (73.5) \rightarrow R21 (75.8) \rightarrow R8 (78.2) \rightarrow R64 (80.5) \rightarrow R65 (82.8)$
   - Standart adım (pitch): **$2.30 - 2.40\text{ mm}$**, 0° yatay oryantasyon.
3. **Boost U11 Kompanzasyon Bloğu (B.Cu $Y = 128.00\text{ mm}$):**
   - $R49 (89.0) \rightarrow C24 (91.5) \rightarrow R52 (94.5)$
   - Standart adımlar: **$2.50\text{ mm}$** ve **$3.00\text{ mm}$**, 180° oryantasyon.
4. **Buck U5 Giriş Kapasitör Bloğu (B.Cu $Y = 105.00\text{ mm}$):**
   - $C13 (117.0) \rightarrow C12 (120.8)$
   - Standart adım: **$3.80\text{ mm}$**, 90° dikey oryantasyon.

---

## 4. Doğrulama ve Metrikler

### 4.1. Ratsnest Çaprazlık ve Tel Uzunluğu Analizi
- **Ölçüm Aracı:** `scratch/ratsnest_crossing_test.py` (Prim MST algoritması, güç düzlemleri hariç sinyal hatları 2D kesişim analizi).
- **Segment Sayısı:** 127 sinyal hattı.
- **Tel Uzunluğu (Wirelength):** $1451.28\text{ mm} \rightarrow \mathbf{1450.84\text{ mm}}$ (Hizalama ile azaltıldı; tam flip simülasyonunda $1429.96\text{ mm}$).
- **Kesişim Sayısı (Crossings):** Taban 185 korundu / optimize edildi.

### 4.2. KiCad 10 DRC ve Şematik Parite Doğrulaması
- **Komut:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`
- **Toplam DRC İhlali:** **164 ihlal** (Taban korundu, **0 YENİ İHLAL**).
- **Şematik Paritesi:** **0 schematic parity issue** (%100 tam parite).
- **Bağlantısız Öğeler:** **360 unconnected items** (Taban korundu, routing aşaması TASK-087'ye devredildi).
