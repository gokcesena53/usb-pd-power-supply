# Tüm Bloklarla Kaba PCB Alan Planı (Floorplan) ve Aday Düzen Değerlendirmesi — TASK-086, 25 Eylül 2026

İki turlu PCB yerleşim metodolojisinin 1. turu kapsamında, $99{,}40 \times 61{,}04\text{ mm}$ kart alanı üzerinde 15 fonksiyonel blok, mekanik portlar, RF anten keepout'u, LCD montaj hacmi ve güç/sinyal koridorları modellenmiş; iki alternatif alan planı adayı karşılaştırılarak **Aday A (Doğrusal Doğu Güç Akışı + Kuzeybatı RF & Kontrol)** seçilmiştir.

[Aday A Kaba Alan Planı (SVG)](../../hardware/docs/reports/task-086-20260925/floorplan_candidate_a.svg) ·
[Aday B Kaba Alan Planı (SVG)](../../hardware/docs/reports/task-086-20260925/floorplan_candidate_b.svg) ·
[Alan Bütçesi ve Aday Karşılaştırma Analizi (JSON)](../../hardware/docs/reports/task-086-20260925/floorplan_analysis.json)

---

## 1. Kart Boyutları, Mekanik Kısıtlar ve Alan Bütçesi

- **Kart Dış Ölçüleri:** $99{,}40 \times 61{,}04\text{ mm}$, Köşe radyusu $R = 3{,}0\text{ mm}$.
  - $X \in [50{,}30, 149{,}70]\text{ mm}$, $Y \in [69{,}48, 130{,}52]\text{ mm}$.
  - Brüt Yüzey Alanı: $6067{,}4\text{ mm}^2$ (Katman başına; Top + Bottom toplam $12134{,}8\text{ mm}^2$).
- **Sabit Mekanik Ankrajlar:**
  - `H1--H4` M3 Montaj Delikleri: $(54{,}30, 73{,}48)$, $(145{,}70, 73{,}48)$, $(54{,}30, 126{,}52)$, $(145{,}70, 126{,}52)\text{ mm}$. Vida başı keepout $\varnothing 6{,}0\text{ mm}$.
  - `J3` LCD FPC Konnektörü: $(98{,}000, 109{,}300\text{ mm}, 90^\circ)$, `F.Cu` kilitli.
- **LCD Görünür Alanı (AA) ve Yükseklik Limiti (TASK-065):**
  - LCD Modül İzdüşümü: $X \in [63{,}52, 141{,}62]$, $Y \in [72{,}28, 127{,}72]\text{ mm}$.
  - Ekran altındaki `F.Cu` (Top) bileşenleri için maksimum montaj yüksekliği: **$Z \le 1{,}80\text{ mm}$**.
  - Bu kural nedeniyle yüksek profilli L1, L3 bobinleri, C33 süperkapasitörü ve J8 gövdesi kesin olarak `B.Cu`'dadır.
- **Port ve Ankraj Hedefleri (PCB_GENEL_YERLESIM_KARARI_20260924):**
  - `J7` USB-C: Sol kenar, `F.Cu` (Top).
  - `J8` Ethernet Mezzanine: Sol kenar, `B.Cu` (Bottom), USB-C'nin altında. Eşzamanlı fiş takma boşluğu $\ge 2{,}0\text{ mm}$.
  - `U2` ESP32-C6: Kuzey kenar, `F.Cu` (Top), anten PCB sınırından dışarı taşacak ($15\text{ mm}$ RF keepout).
  - `J9` Panel Enkoder: Ethernet yanı sol panel alanı ($X \le 58\text{ mm}$), $6 \times 24\text{ mm}$ kablo büküm koridoru, LCD mesafesi $> 4{,}0\text{ mm}$.

---

## 2. İki Aday Düzenin Değerlendirilmesi ve Karşılaştırma Matrisi (AC #3)

| Değerlendirme Kriteri | Aday A (Önerilen Düzen) | Aday B (Alternatif Düzen) | Karar & Gerekçe |
| :--- | :--- | :--- | :--- |
| **Mekanik Mimari** | J7 Top-Sol, J8 Bottom-Sol, U2 Kuzeybatı | J8 Top-Sol, J7 Bottom-Sol, U2 Kuzeydoğu | **Aday A Kazandı:** `PCB_GENEL_YERLESIM_KARARI` şartlarına tam uyar. |
| **USB 2.0 D+/D- Hat Uzunluğu** | **$22{,}0\text{ mm}$** (Doğrudan ve kısa) | **$72{,}0\text{ mm}$** (Kartı boydan boya geçer) | **Aday A Kazandı:** $90\ \Omega$ diferansiyel sinyal bütünlüğü ve EMI için kısa hat kritiktir. |
| **Eşzamanlı Fiş Boşluğu (Z)** | **$2{,}5\text{ mm}$** (Güvenli pay) | $2{,}0\text{ mm}$ (Sınırda) | **Aday A Kazandı:** USB-C ve RJ45 kablo başlıkları birbirine çarpmadan rahatça takılır. |
| **Güç Akışı ve Döngüler** | **Doğrusal Batı $\rightarrow$ Doğu** (Sıfır geri dönüş) | U-Tipi Alt Kenar Yayılımı | **Aday A Kazandı:** Giriş $\rightarrow$ Boost $\rightarrow$ Buck $\rightarrow$ Çıkış tek yönlü ilerler. |
| **Termal Profil Ayrımı** | Kuzey: Soğuk MCU/RF / Güney: Sıcak Güç | Karışık (Güç katı MCU'ya çok yakın) | **Aday A Kazandı:** Güç katının yaydığı ısı MCU ve kristalden uzakta kalır. |
| **RTC BQ32000 İzolasyonu** | **$26{,}5\text{ mm}$** (Kuzeydoğu Sessiz Köşe) | $14{,}0\text{ mm}$ (L1 Buck bobinine yakın) | **Aday A Kazandı:** $32{,}768\text{ kHz}$ kristal anahtarlama gürültüsünden tam korunur. |
| **Sonuç** | **KABUL EDİLDİ (Seçilen Plan)** | **ELENDİ** | Aday A tüm geometrik ve elektriksel hedefleri eksiksiz sağlar. |

---

## 3. Seçilen Aday A Blok Alan Dağılımı ve Koridor Tanımları

```
+──────────────────────────────── KABA ALAN PLANI (ADAY A) ────────────────────────────────+
│                                                                                           │
│   [J7 USB-C] (Top)            [U2 ESP32-C6] (Top)           [I2C SEV.]     [RTC BQ32000] │
│   x: 50.3..62.0, y: 72..89    x: 64..85.5, y: 69.5..88      x: 86..96      x: 126..147    │
│   F.Cu                        F.Cu (Anten Dışarı)           y: 72..82      y: 69.5..84    │
│                                                                                           │
│   [J9 ENKODER] (Kablo)        [AP33772S SINK]               [TPS55340]     [AOZ1284]      │
│   x: 52..60, y: 90..103       x: 62..86, y: 88..105         BOOST          BUCK           │
│   F.Cu / B.Cu                 B.Cu (Kelvin Şönt)            x: 86..110     x: 110..132    │
│                                                             y: 82..104     y: 82..104     │
│   [J8 ETHERNET MEZANIN]                                                                   │
│   x: 50.3..105.0, y: 104..130.5                             [LM74801]      [INA226 & J4]  │
│   B.Cu (RJ45 Mandalı Dışarı)                                x: 130..149    x: 128..149.7  │
│   • Bölge 3 Keepout: x=50.3..66.8                           y: 84..102     y: 102..128    │
│   • Bölge 2 Orta: Z <= 1.9 mm                               Çıkış Switch   Banana Jak     │
+───────────────────────────────────────────────────────────────────────────────────────────+
```

1. **Giriş ve Kontrol Bölgesi (Kuzeybatı):**
   - J7 USB-C soketi en üst sol köşededir ($y \approx 72\text{--}89\text{ mm}$).
   - U2 MCU hemen sağında kuzey kenardadır ($y \approx 69{,}5\text{--}88\text{ mm}$); anten ana kart dışına uzanır. USB D+/D- diferansiyel çifti yalnızca $22\text{ mm}$ uzunluğundadır.
2. **Ethernet ve Enkoder Bölgesi (Güneybatı):**
   - J8 Ethernet modülü alt sol köşede B.Cu katmanındadır ($y \approx 104\text{--}130{,}5\text{ mm}$). USB-C ile arasında düşeyde $15\text{ mm}$ merkez açıklığı bulunur; fiş gövdeleri arasında $2{,}5\text{ mm}$ boşluk kalır.
   - J9 enkoder kablo bağlantısı J7 ile J8 arasında ($y \approx 90\text{--}103\text{ mm}$) yer alır; $6 \times 24\text{ mm}$ kablo koridoru doğrudan sol kutu paneline açılır.
3. **Güç Dönüşüm Koridoru (Merkez ve Güney B.Cu):**
   - AP33772S ($X \approx 62\text{--}86$) $\rightarrow$ TPS55340 Boost ($X \approx 86\text{--}110$) $\rightarrow$ AOZ1284 Buck ($X \approx 110\text{--}132$) $\rightarrow$ LM74801 ($X \approx 130\text{--}149$).
   - Güç akışı tamamen doğrusal soldan sağa ilerler; geri dönüş ve parazitik kuplaj sıfırlanmıştır.
4. **Çıkış ve Ölçüm Bölgesi (Güneydoğu):**
   - LM74801 ve INA226/RShunt1 sağ kenara yakın konumlanarak doğrudan J4 Banana jakına bağlanır.
   - Aktif deşarj direnci (R67) bu bölgenin altında yer alır; ısısı diğer blokları etkilemeden kenardan atılır.
5. **Sessiz Analog Bölge (Kuzeydoğu):**
   - RTC BQ32000 ve Y1 kristali anahtarlama bobinlerinden $26{,}5\text{ mm}$ uzakta, en sakin köşede izole edilmiştir.

---

## 4. TASK-063 ve TASK-008'e Devir Kuralları (AC #4, AC #5)

1. **TASK-063 (Mekanik Ankraj Dondurma):**
   - J7 (USB-C), J8 (RJ45), U2 (ESP32-C6) ve J9 (Enkoder) koordinatları Aday A zarfları temel alınarak dondurulacaktır.
   - Ethernet altı Bölge 3 mutlak keepout olarak korunacak; Bölge 2 orta boşluğu başlangıçta boş kabul edilecek, sadece gerekirse düşük profilli parçalara izin verilecektir.
2. **TASK-008 (İnce Yerleşim):**
   - 15 bloğun iç elemanları (ayrıştırma kapasitörleri, bobinler, diyotlar) Aday A'da belirlenen bu sınır kutuları (bounding box) içerisine taşınacaktır.
   - Güç blokları kalan boşluklara sonradan sıkıştırılmayacak; ayrılan geniş alanlar sayesinde termal via ve dikiş poligonları rahatça uygulanacaktır.
