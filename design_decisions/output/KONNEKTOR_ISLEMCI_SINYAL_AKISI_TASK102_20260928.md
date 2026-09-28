# Konnektör-İşlemci Sinyal Akışının Doğallığı ve Yönlendirme Yolları Kararı (TASK-102)

**Tarih:** 28 Eylül 2026  
**Durum:** ONAYLANDI / UYGULANDI  
**Etkilenen Dosyalar:** `hardware/gopo.kicad_pcb`  
**Referans Rapor:** `hardware/docs/reports/task-102-20260928/konnektor_islemci_sinyal_akisi_raporu.md`  

---

## 1. Karar Özeti

1. **J9 Enkoder Pull-Up Yerleşimi (R34–R36):**  
   `R34`, `R35`, `R36` (0402) pull-up dirençleri, B.Cu $Y=125.50\text{ mm}$ konumundan F.Cu $X=[65.0, 67.5, 70.0]\text{ mm}, Y=96.00\text{ mm}$ konumuna taşınmıştır. Bu sayede J9 ile U2 arasındaki 60 mm'lik yapay U dönüşü tamamen ortadan kaldırılmış, sinyallerin aynı katmanda (F.Cu) en kısa koridordan akması sağlanmıştır.
2. **USB D+/D- Serisi Dirençler (R2, R3):**  
   `R2` ve `R3` dirençleri, U2'nin doğusundaki $(84.50, 83.00)$ ve $(86.50, 83.00)$ basamaklı konumlarından alınarak F.Cu üzerinde $(66.00, 86.00)$ ve $(68.00, 86.00)$ koordinatlarına yerleştirilmiştir. USB diferansiyel çifti soldan sağa kesintisiz doğrusal akışa kavuşturulmuş, geri dönüş döngüsü (backtrack loop) sıfırlanmıştır.
3. **Kritik Arayüz Koridor Kuralları:**  
   - J3 LCD SPI veri yolu B.Cu'daki L3/U11 Boost anahtarlama alanından izole edilerek F.Cu kuzey-batı koridoruna tahsis edilmiştir.
   - J8 Ethernet UART sinyallerinin 21 mm'lik doğrudan yatay koridoru korunmuştur.
   - U3 INA226 ve I2C hatlarının Buck L1/U5 anahtarlama düğümlerini diyagonal kesmesi engellenmiş, emniyetli çevre koridorları tanımlanmıştır.
4. **Doğrulama ve Metrikler:**  
   - Ratsnest sinyal kesişimleri **185 $\rightarrow$ 161**'e düşürülmüştür (-24 kesişim).
   - Toplam sinyal tel uzunluğu **1450.84 mm $\rightarrow$ 1342.15 mm**'ye indirilmiştir (-108.69 mm kısalma).
   - KiCad 10 DRC: 0 hata, %100 şematik paritesi korunmuştur.
