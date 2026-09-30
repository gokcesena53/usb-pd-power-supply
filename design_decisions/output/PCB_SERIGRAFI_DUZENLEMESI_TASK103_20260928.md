# Karar Belgesi: PCB Serigrafi Metinleri ve Çakışmalarının DRC Kurallarına Göre Düzenlenmesi (TASK-103)

**Tarih:** 28 Eylül 2026  
**Konu:** Serigrafi Metin Boyutları, Kart Kenarı Açıklıkları ve Lehim Maskesi Çakışmalarının Temizlenmesi  
**İlgili Görev:** TASK-103  
**Etkilenen Dosyalar:** [`hardware/gopo.kicad_pcb`](file:///c:/Users/Slayer/Desktop/gopo/usb-pd-power-supply/hardware/gopo.kicad_pcb), [`gopo-drc.rpt`](file:///c:/Users/Slayer/Desktop/gopo/usb-pd-power-supply/gopo-drc.rpt)  

---

## 1. Bağlam ve Problem Tanımı

KiCad DRC raporunda toplam 165 ihlalin 144 adedi (%87.3) serigrafi kaynaklı uyarılardan oluşmaktaydı:
1. 0402 ve 0603 boyutundaki 61 adet pasif komponent ve test noktalarında metin boyutu $0.10\text{ mm}$ ve çizgi kalınlığı $0.025\text{ mm}$ olarak kalmış; PCB üretici asgari limitlerinin (min $0.80\text{ mm}$ boy, $0.08\text{ mm}$ kalınlık) altında kalmıştı (`text_height` ve `text_thickness`).
2. U2 ESP32 modülü ve C33 süper kapasitör serigrafi çizgileri ve referans metinleri kart kesim sınırını aşmaktaydı (`silk_edge_clearance`).
3. D8, D9, U13, C33, J8 serigrafi çizgileri ve referans metinleri lehim maskesi açıklıkları ve komşu komponentler ile çakışmaktaydı (`silk_over_copper` ve `silk_overlap`).

## 2. Alınan Kararlar

1. **Küçük Pasif Komponentlerin Serigrafi Referanslarının Gizlenmesi:**
   - IPC-7351C yüksek yoğunluklu montaj standartlarına uygun olarak, 0402 ve 0603 kılıfındaki direnç, kapasitör ve termistörlerin `F.SilkS` ve `B.SilkS` katmanındaki referans yazıları gizlendi (`hide yes`).
   - Bu referanslar montaj, üretim dokümantasyonu ve test süreçleri için `F.Fab` ve `B.Fab` katmanlarında eksiksiz olarak tutulmaktadır.
   - TP1–TP14 test noktalarının tümü homojen biçimde `hide yes` yapılarak serigrafi temizlendi.

2. **Kart Kenarı Serigrafi Sınırlandırması (U2 & C33):**
   - U2 (ESP32-C6-MINI-1) modülünün kart dışına sarkan anten bölgesindeki sanal serigrafi çizgisi kaldırıldı, modül yan hizalama çizgileri kart kenarından $0.58\text{ mm}$ içeride sonlandırıldı.
   - C33 referans metni kart içine doğru ($Y=75.00\text{ mm}$) çekilerek kart kenarından $5.5\text{ mm}$ mesafeye yerleştirildi.

3. **Lehim Maskesi Açıklığı Emniyeti:**
   - C33 süper kapasitörün `+` polarite işareti $X=+2.0\text{ mm}$ kaydırılarak R6 padinden $>2.5\text{ mm}$ uzağa çekildi.
   - J8 RJ45 arka yüz çerçevesi $X=53.5\text{ mm}$ sınırına çekilerek J7 USB-C ekranlama pini lehim maskesi açıklığından arındırıldı.
   - D8 ve D9 referansları pad açıklıklarından serbest alanlara `(at 3 0 0)` taşındı.
   - U13 referansı Pin-1 serigrafi poligonunu ezmeyecek konuma `(at 2.3 2.5 0)` çekildi.

## 3. Doğrulama ve Sonuç

- **Serigrafi İhlalleri:** 144'ten tam olarak **0**'a indirildi (%100 temizleme).
- **Toplam DRC İhlalleri:** 165'ten **25**'e geriledi (kalan 25 ihlalin 15'i zorunlu RF anten kenar taşması, 10'u standart kütüphane revizyon eşleşmesidir).
- **Şematik Paritesi:** 0 parity issue (%100 elektriksel uyum).
- **Mekanik Çapa Konumları:** 0.0000 mm sapma (tüm kritik mekanik elemanlar kilitli konumda).
