# Test Noktaları Haritası ve Doğrulama Raporu (TASK-098)

**Tarih:** 28 Eylül 2026  
**Revizyon:** Rev_C  
**Kapsam:** TP1 – TP14 Test Noktaları, Mekanik Erişim Analizi, Güç Rayı Prob Kılavuzu ve Şematik/PCB Eşliği  

---

## 1. Genel Bakış ve Amaç

TASK-098 kapsamında gopo USB-PD Masaüstü Güç Kaynağı kartı üzerindeki mevcut test noktaları (TP1–TP14) mekanik, katman ve elektriksel açıdan incelenmiş, şematiğe müdahale edilmeden aşağıdaki yerleşim optimizasyonları yapılmıştır:
1. **TP9 ve TP10:** 3.2" LCD ekran altında kaldığı için ekran montajı sonrası problanamayan noktalar kartın alt yüzüne (`B.Cu`) taşınmıştır.
2. **TP11, TP12, TP13 (UART):** LCD modülünün üst çerçevesine ($Y = 72.48\text{ mm}$) çok yakın olan hücre, $Y = 70.70\text{ mm}$ koordinatına kaydırılarak **1.78 mm** (kriter $\ge 1.5\text{ mm}$) güvenli koridor elde edilmiştir. Kart kenarına mesafe $1.22\text{ mm} \ge 0.5\text{ mm}$'dir.
3. **TP14 (ETH_RUN):** J8 Ethernet mezanin konnektörüne çok yakın olan konum ($X = 107.00\text{ mm}$), $X = 110.50\text{ mm}$'ye çekilerek mezanin modülü takılıyken bile prob erişimine uygun hale getirilmiştir.
4. **Şematik Korunumu:** Şematiğe yeni komponent eklenmemiş; +3.3V, V_PRE, OUT_POS, SW_EN ve I2C GND hatları için mevcut komponent padleri üzerinden bring-up prob kılavuzu tanımlanmıştır.

---

## 2. Güncel Test Noktaları Haritası (TP1 – TP14)

| TP No | Net / Sinyal Adı | Şematik Sayfası | Katman | Konum $(X, Y)$ [mm] | Açıklama ve Kullanım Amacı |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **`TP1`** | `USB_VBUS` | `usb_pd_controller` | `B.Cu` | $(71.50, 101.30)$ | USB-C Tip-C giriş gerilimi (5V–20V ham VBUS) |
| **`TP2`** | `/USB_PD_CONTROLLER/PD_VBUS_SENSED` | `usb_pd_controller` | `B.Cu` | $(82.00, 102.50)$ | AP33772S dahili VBUS gerilim algılama girişi |
| **`TP3`** | `PD_VOUT` | `usb_pd_controller` | `B.Cu` | $(90.80, 103.60)$ | Pre-boost giriş ana güç barası (Q3 geçişi sonrası) |
| **`TP4`** | `PD_5V` | `usb_pd_controller` | `B.Cu` | $(70.00, 127.50)$ | AP33772S dahili 5V LDO regülatör çıkışı |
| **`TP5`** | `/USB_PD_CONTROLLER/PD_GATE` | `usb_pd_controller` | `B.Cu` | $(74.00, 113.50)$ | Giriş anahtarı Q3 P-MOSFET kapı (gate) kontrol gerilimi |
| **`TP6`** | `PD_I2C_SCL_3V3` | `mcu` | `B.Cu` | $(74.00, 72.00)$ | MCU $\leftrightarrow$ AP33772S/INA226 I2C saat hattı (3.3V) |
| **`TP7`** | `PD_I2C_SDA_3V3` | `mcu` | `B.Cu` | $(77.00, 72.00)$ | MCU $\leftrightarrow$ AP33772S/INA226 I2C veri hattı (3.3V) |
| **`TP8`** | `PD_INT_3V3` | `mcu` | `B.Cu` | $(80.00, 72.00)$ | AP33772S PD kesme (interrupt) sinyali (3.3V) |
| **`TP9`** | `/MCU/ETH_CFG0` | `mcu` | `B.Cu` | $(107.50, 82.50)$ | CH9121 Ethernet konfigürasyon pin 0 (alt kata taşındı) |
| **`TP10`** | `/MCU/ETH_PWR_EN` | `mcu` | `B.Cu` | $(107.50, 79.50)$ | Ethernet mezanin modül besleme enable kontrolü (alt kata taşındı) |
| **`TP11`** | `/MCU/UART_TX` | `mcu` | `F.Cu` | $(133.00, 70.70)$ | MCU UART seri port konsol vericisi (LCD'den 1.78 mm ötede) |
| **`TP12`** | `/MCU/UART_RX` | `mcu` | `F.Cu` | $(135.50, 70.70)$ | MCU UART seri port konsol alıcısı (LCD'den 1.78 mm ötede) |
| **`TP13`** | `GND` | `mcu` | `F.Cu` | $(138.00, 70.70)$ | UART hücresi referans toprağı (konsol kablosu GND bağlantısı) |
| **`TP14`** | `/MCU/ETH_RUN` | `mcu` | `B.Cu` | $(110.50, 82.50)$ | CH9121 Ethernet durum/çalışma göstergesi (J8'den ferahlatıldı) |

---

## 3. Güç Rayları ve Sinyaller İçin Alternatif Prob Kılavuzu

Şematik ve BOM bütünlüğünü değiştirmemek adına, ilave komponent eklenmeksizin ilk çalıştırma (bring-up) ve hata ayıklamada kullanılabilecek mevcut komponent bacakları ve açık test noktaları:

| Sinyal / Ray | Alternatif Prob Noktası | Katman | Açıklama |
|---|---|---|---|
| **`+3.3V`** | `C16` (Pin 1) veya `U5` (Pin 4 çıkış) | `F.Cu` / `B.Cu` | Buck çıkış filtre kapasitörü üzerinden ana 3.3V lojik rayı probu |
| **`V_PRE`** | `C27` / `C28` (Pin 1) veya `D4` (Katot) | `F.Cu` / `B.Cu` | Boost regülatörü çıkışı / buck girişi ara barası probu |
| **`OUT_POS`** | `J4` Vidalı Terminal Pedi veya `C31` (Pin 1) | `F.Cu` / `B.Cu` | Güç kaynağının pozitif çıkış terminali doğrudan probu |
| **`SW_EN`** | `R27` (Pin 1) veya `U13` (Pin 1) | `F.Cu` / `B.Cu` | Regülatör anahtarlama izin kontrol pini |
| **`I2C GND`** | `TP13` (F.Cu) veya Mezanin `J8` (Pin 2/Pin 10 GND) | `F.Cu` / `B.Cu` | Osiloskop şasi krokodili için en yakın düşük endüktanslı referans |

---

## 4. Mekanik ve Montaj Erişilebilirlik Analizi

### 4.1. LCD Modülü (F.Cu) Sınırları ve Ayrım
- LCD modül sınır kutusu: $X \in [63.72, 141.42]\text{ mm}$, $Y \in [72.48, 127.52]\text{ mm}$.
- **TP9 ve TP10:** Eski konumları `F.Cu` üzerinde ekran panelinin arkasında kalıyordu. Yeni konumları `B.Cu` katmanında $(107.50, 82.50)$ ve $(107.50, 79.50)$ olarak ekran montajından tamamen bağımsız ve erişilebilir hale getirilmiştir.
- **TP11, TP12, TP13:** `F.Cu` üzerinde $Y = 70.70\text{ mm}$'ye çekilmiştir. $72.48 - 70.70 = 1.78\text{ mm} \ge 1.50\text{ mm}$ açıklık sayesinde ekran çerçevesi prob yerleşimine engel teşkil etmemektedir. Kart üst kenarına ($Y = 69.48\text{ mm}$) mesafe $1.22\text{ mm}$ olup DRC edge clearance sınırının ($0.5\text{ mm}$) güvenle üzerindedir.

### 4.2. Ethernet Mezanin Modülü (B.Cu J8) Sınırları
- Waveshare Ethernet modül izdüşümü: $X \in [51.23, 104.47]\text{ mm}$, $Y \in [77.38, 99.62]\text{ mm}$.
- TP9 $(107.50, 82.50)$, TP10 $(107.50, 79.50)$ ve TP14 $(110.50, 82.50)$ test noktaları $X \ge 107.50\text{ mm}$ koordinatında konumlandırılmıştır.
- Mezanin modül sınırına ($X = 104.47\text{ mm}$) olan net açıklık **$\ge 3.03\text{ mm}$**'dir. Mezanin kartı takılı durumdayken prob ucuyla rahatça erişilebilir.

---

## 5. Doğrulama ve DRC Sonuçları

- **KiCad Sürümü:** 10.0.5  
- **Komut:** `kicad-cli pcb drc --schematic-parity hardware/gopo.kicad_pcb`  
- **Schematic Parity Violations:** **0** (Şematik dokunulmamış, %100 kusursuz şematik - PCB netlist uyumu).
- **DRC Violations:** 164 (Başlangıç taban değeri 168 idi; serigrafi optimizasyonlarıyla 4 ihlal azaltılmıştır; **0 yeni ihlal**).
- **Unconnected Items:** 360 (Tasarım taban değeri korunmuştur; bağlantısız test noktası eklenmemiştir; genel routing TASK-087 kapsamındadır).
