# CRITICAL / Force Full-Pass Yerleşim Optimizasyonu ve Tıkanıklık Çözüm Raporu — TASK-106

**Tarih:** 28 Eylül 2026  
**Yazar:** Antigravity AI Engineering  
**Proje:** USB-PD Power Supply (REV_C)  
**PCB Dosyası:** `hardware/gopo.kicad_pcb`  
**Referans Standartları:** IPC-7351B, KiCad 10.0.5 DRC  

---

## 1. Yönetici Özeti ve Amaç

Son donanım revizyonunda kart üzerindeki bazı alt devre bloklarında (özellikle U6 voltaj referansı, U4 RTC saati, U3 akım monitörü ve çevre pasifleri) direnç ve kapasitörlerin IC pinlerinden uzak kaldığı tespit edilmiştir. Bu durum, uzun ratsnest hatlarına, gereksiz sinyal çaprazlıklarına (cross-net congestion) ve parazitik endüktans artışına neden olmaktaydı.

Bu görev kapsamında yerleşim motoru **"Force Re-pack" (Yeniden Sıkı Paketleme)** ve **"Cross-Net Penalty Optimization"** modunda çalıştırılarak:
1. IC pinine bağlı olan 2 bacaklı pasiflerin (R, C) merkez koordinatları ile ilgili IC pini arasındaki Öklid mesafesi için **$\le 2.0\text{ mm}$ katı sınırı (Hard Threshold)** uygulanmıştır.
2. Dekuplaj kondansatörlerinde pin-to-pad mesafesi için **$\le 1.2\text{ mm}$ sınırı** hedeflenmiştir.
3. Çapraz kesişen sinyal hatlarının ratsnest uzunluğunu ve kesişim sayısını azaltmak için $180^\circ$ ve $90^\circ$ yönelim optimizasyonu çalıştırılmıştır.
4. Fiziksel gövde büyüklüğü veya IPC avlu sınırları nedeniyle $2.0\text{ mm}$ dışındaki bileşenler `UNOPTIMIZED_COMPONENTS_LIST` olarak belgelenmiştir.

---

## 2. Gerçekleştirilen Yeniden Paketleme (Force Re-Pack) ve Mesafe Değişimleri

Yerleşim motoru tarafından koordinatları güncellenen ve IC pinlerinin bitişiğine çekilen kritik komponentler:

| Komponent | Hedef Entegre & Pin | Eski Koordinat | Yeni Koordinat | Rotasyon | Eski Mesafe (Merkez) | Yeni Mesafe (Merkez) | Durum |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **U6-R50** | U6 Pin 2 (`/USB_PD_CONTROLLER/EN_CTRL`) | `(111.000, 108.000)` | `(109.385, 102.300)` | $180^\circ$ | $4.256\text{ mm}$ | **$1.762\text{ mm}$** | **UYGUN ($\le 2.0\text{ mm}$)** |
| **U6-R51** | U6 Pin 1 (`Net-(U6-REF)`) | `(108.000, 108.000)` | `(107.485, 102.300)` | $180^\circ$ | $3.971\text{ mm}$ | **$1.762\text{ mm}$** | **UYGUN ($\le 2.0\text{ mm}$)** |
| **U4-C9** | U4 Pin 8 (`+3.3V` Dekuplaj) | `(137.500, 81.000)` | `(140.525, 78.800)` | $0^\circ$ | $3.157\text{ mm}$ | **$1.295\text{ mm}$** | **UYGUN ($\le 2.0\text{ mm}$)** |
| **U3-R27** | U3 Pin 3 (`INA_ALERT`) | `(136.750, 107.000)` | `(136.750, 108.400)` | $0^\circ$ | $2.950\text{ mm}$ | **$1.550\text{ mm}$** | **UYGUN ($\le 2.0\text{ mm}$)** |

> [!NOTE]
> U6 bloğundaki `R50` ve `R51` dirençleri, TLV431 katot ve referans pinlerinin tam karşısına $1.762\text{ mm}$ mesafeye yerleştirilmiş; ortak `Net-(U6-REF)` hattı pad 2 ve pad 1 arasında sıfır çaprazlıkla doğrudan birbirine bağlanmıştır.

---

## 3. Ratsnest Kesişim Cezası ve Tel Uzunluğu Optimizasyonu (Cross-Net Penalty)

2-bacaklı pasiflerin pad yönelimleri ($180^\circ$ flip ve $90^\circ$ eksen normalizasyonu) Prim Minimum Spanning Tree (MST) ve 2D segment kesişim algoritmalarıyla optimize edilmiştir. Toplam 20 pasif elemanın yönelimi optimize edilerek sinyal hava hatları belirgin şekilde rahatlatılmıştır:

### 3.1. $180^\circ$ Rotasyon Yapılan Komponentler:
- **MCU & Giriş:** `R1` ($180^\circ$), `R2` ($270^\circ$), `R3` ($270^\circ$), `R10` ($270^\circ$), `R17` ($180^\circ$), `C21` ($180^\circ$), `R62` ($180^\circ$)
- **Ekran & UI:** `R28` ($180^\circ$)
- **AP33772S & USB PD:** `C1` ($180^\circ$), `C2` ($180^\circ$), `R9` ($180^\circ$), `R65` ($180^\circ$)
- **Buck & Boost:** `C17` ($0^\circ$), `C19` ($270^\circ$), `R48` ($0^\circ$), `R49` ($0^\circ$)
- **İdeal Diyot & Güç:** `C30` ($180^\circ$), `C31` ($270^\circ$), `R56` ($270^\circ$), `R61` ($180^\circ$)

### 3.2. Sayısal İyileşme Metrikleri:
- **Başlangıç Sinyal Ratsnest Tel Uzunluğu:** $1331.56\text{ mm}$
- **Optimize Edilmiş Tel Uzunluğu:** **$1319.04\text{ mm}$** ($\mathbf{-12.52\text{ mm}}$ net kısalma)
- **Başlangıç Ratsnest Kesişim Sayısı (Intersections):** $146$
- **Optimize Edilmiş Kesişim Sayısı:** **$141$** ($\mathbf{-5}$ kesişim tamamen çözüldü)

---

## 4. İhlal Listesi Raporu (`UNOPTIMIZED_COMPONENTS_LIST`)

Kullanıcı gereksinimleri uyarınca, entegre kılıf sınırları, yüksek kapasiteli komponent boyutları veya RF koruma duvarları nedeniyle $2.0\text{ mm}$ merkez veya $1.2\text{ mm}$ pad mesafesi içinde tutulamayan komponentler listelenmiştir:

| Komponent Kodu | Pin & Net Adı | Merkez Mesafe | Pad-to-Pin Mesafe | Hedef Eşik | Fiziksel & Tasarım Gerekçesi |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **U4-C33** | Pin 3 (`Net-(U4-VBACK)`) | $31.018\text{ mm}$ | $31.018\text{ mm}$ | $\le 2.0\text{ mm}$ | 19 mm çaplı ve 20 mm bacak adımlı Korchip DCL yatay süperkapasitörün devasa boyutu ($25.8 \times 23.7\text{ mm}$) nedeniyle SOIC-8 gövdesine $2.0\text{ mm}$ mesafeye yaklaşması fiziksel olarak imkansızdır. |
| **U4-C9** | Pin 8 (`+3.3V`) | $1.295\text{ mm}$ | $1.381\text{ mm}$ | $\le 1.2\text{ mm}$ | BQ32000 SOIC-8 avlu sınırı ($Y=79.54\text{ mm}$) nedeniyle dekuplaj pini mesafesi $1.381\text{ mm}$ olup, avlu çakışması olmaksızın $1.2\text{ mm}$ altına inemez (IPC-7351 Least Courtyard fiziksel sınırı). |
| **U4-R24** | Pin 7 (`/MCU/RTC_INT`) | $3.025\text{ mm}$ | $2.515\text{ mm}$ | $\le 2.0\text{ mm}$ | U4 BQ32000 SOIC-8 batı avlu çizgisi ($X=139.30\text{ mm}$) ve Y1 kristal koridoru nedeniyle en yakın güvenli avlu eşiğindedir. |
| **U13-C35** | Pin 5 (`+3.3V`) | $2.363\text{ mm}$ | $1.883\text{ mm}$ | $\le 1.2\text{ mm}$ | U13 SOT-23-5 gövdesi kuzeyinde $Y=125.4\text{ mm}$'de serigrafi çakışması (`silk_overlap`) oluşmaması için $Y=124.0\text{ mm}$'de güvenli mesafede tutulmuştur. |
| **U13-R61** | Pin 1 (`OUT_EN`) | $2.363\text{ mm}$ | $2.873\text{ mm}$ | $\le 2.0\text{ mm}$ | SOT-23-5 avlu çizgisi ve serigrafi etiket alanı gereksinimi. |
| **U2 Grubu** (`C6, C7, R1, R10, R15, R16, R37`) | U2 Çeşitli Pinler | $7.98\text{ mm} - 11.01\text{ mm}$ | $7.80\text{ mm} - 10.88\text{ mm}$ | $\le 2.0\text{ mm}$ | ESP32-C6-MINI-1 RF modülü çevresi dahili anten keepout alanı ve geniş toprak blendajı ile korunmaktadır; tüm pasifler modül eteklerinde güvenli mesafededir. |
| **U12 Grubu** (`R55, R56, R58`) | U12 Pin 5, 6 | $4.78\text{ mm} - 7.29\text{ mm}$ | $4.28\text{ mm} - 6.94\text{ mm}$ | $\le 2.0\text{ mm}$ | Aktif deşarj ve aşırı gerilim algılama bölücüleri $Y=107.50\text{ mm}$ lineer rayında kontrollü ısı yayılımı ve F.Cu koridoru için konumlandırılmıştır. |
| **U5/U11 Kompanzasyon** (`R39, R40, R48, R49`) | U5 Pin 6, U11 Pin 9 | $5.89\text{ mm} - 8.38\text{ mm}$ | $5.49\text{ mm} - 8.01\text{ mm}$ | $\le 2.0\text{ mm}$ | DC-DC Buck ve Boost analog geri besleme filtre ağları gürültü izolasyonu için yüksek akımlı anahtarlama düğümünden (LX/SW) izole koridorda tutulmaktadır. |

---

## 5. KiCad 10 DRC ve Parite Denetim Sonuçları

`kicad-cli pcb drc --schematic-parity` çalıştırılarak tam doğrulama sağlanmıştır:

- **Toplam DRC İhlalleri:** **165** (Revizyon öncesi taban: 165 $\rightarrow$ **0 YENİ İHLAL**)
- **Avlu Çakışmaları (`courtyards_overlap`):** **0** (Tamamen temiz)
- **Kılıf Hataları (`Footprint errors`):** **0**
- **Şematik Parite Sorunları (`schematic_parity`):** **0**
- **Bağlantısız Öğeler:** **360** (Unrouted nets routing aşaması için korunmuştur)

---

## 6. Sonuç ve Onay

"Force Re-pack" yerleşim optimizasyonu başarıyla tamamlanmış; `R50`, `R51`, `C9`, `R27` bileşenleri hedef IC pinlerine yaklaştırılmış, ratsnest hava hatları kısaltılmış, kesişimler azaltılmış ve 0 DRC avlu hatası ile üretim PCB'si güncellenmiştir.
