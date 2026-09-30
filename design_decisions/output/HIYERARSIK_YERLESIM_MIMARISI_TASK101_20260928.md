# PCB Güç ve Sinyal Akışı İçin Hiyerarşik Yerleşim Mimarisi Kararı (TASK-101)

**Tarih:** 28 Eylül 2026  
**Durum:** ONAYLANDI / UYGULANDI  
**Etkilenen Dosyalar:** `hardware/gopo.kicad_pcb`  
**Referans Rapor:** `hardware/docs/reports/task-101-20260928/hiyerarsik_yerlesim_mimarisi_raporu.md`  

---

## 1. Karar Özeti

1. **Soldan Sağa Doğrusal Güç Boru Hattı:**  
   Kart üzerindeki ana güç zinciri 7 aşamada kesin ve monoton bir $X$ ekseni artışıyla soldan sağa yapılandırılmıştır:
   - Aşama 1: J7/U10 ($X = 58.66\text{ mm}$, F.Cu)
   - Aşama 2: U1/Q3 ($X = 77.17\text{ mm}$, B.Cu)
   - Aşama 3: U11/L3/D4 ($X = 98.04\text{ mm}$, B.Cu)
   - Aşama 4: U5/L1 ($X = 122.88\text{ mm}$, B.Cu)
   - Aşama 5: Q5/U12 ($X = 134.50\text{ mm}$, F.Cu)
   - Aşama 6: RShunt1/U3 ($X = 137.98\text{ mm}$, B.Cu)
   - Aşama 7: J4 ($X = 145.00\text{ mm}$, B.Cu)
   Güç akışında geri dönüş (backtrack) ve dolambaçlı geçişler sıfırlanmıştır.

2. **Katman Hiyerarşisi ve Çift Taraflı Güç Dağılımı:**  
   B.Cu anahtarlamalı güç çeviricilerin ana katmanı olarak belirlenmiş; LM74801 (U12) ve güç MOSFET'i Q5, alan ve termal dağılım verimliliği amacıyla F.Cu katmanında (Buck U5/L1'in tam karşısında) konumlandırılmıştır. B.Cu ile F.Cu arasındaki güç aktarımı TASK-087 genel routing aşamasında çoklu via matrisleri ile gerçekleştirilecektir.

3. **3 Kademeli Fonksiyonel Zonlama (Zoning):**  
   - **Kuzey Zonu ($Y < 90\text{ mm}$):** Düşük gürültülü dijital/RF/haberleşme (U2 ESP32-C6, anten keepout $Y < 69.48\text{ mm}$, J8 Ethernet mezanini, U4/Y1 RTC, seviye dönüştürücüler ve butonlar).
   - **Orta Zon ($Y = 90 - 105\text{ mm}$):** Kullanıcı arayüzü geçiş koridoru (J3 LCD FPC, J9 Enkoder).
   - **Güney Zonu ($Y > 90\text{ mm}$):** Yüksek akımlı anahtarlamalı güç dönüşümü (Boost, Buck, Güç MOSFET'leri, Şöntler).

4. **Gürültülü Düğümlerin Fiziksel İzolasyonu:**  
   $L1$ ve $L3$ güç bobinleri ve $SW/LX$ yüksek $dv/dt$ düğümleri ile hassas analog devreler (INA226 Kelvin şöntü, RTC kristali Y1, MCU dahili osilatör) arasında minimum $17.56\text{ mm}$ (ortalama $> 35\text{ mm}$) fiziksel mesafe ve In1.Cu katı GND kalkanlaması garanti altına alınmıştır.

5. **DRC ve Şematik Paritesi:**  
   KiCad 10 DRC doğrulanmış; 164 ihlal tabanı (0 yeni hata), %100 şematik paritesi (0 parity issue) ve 360 bağlantısız öğe tabanı korunmuştur.
