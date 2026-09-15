# REV_B birlikte çalışma sırası

1. Yeni 60 × 40 mm PCB tabanını ve dört açık köşe yontusunu görsel olarak kontrol et.
2. REV_B şematiğinde footprint ataması eksik komponent olup olmadığını kontrol et.
3. Schematic Editor içinde **Tools → Update PCB from Schematic (F8)** komutunu birlikte aç.
4. Güncelleme listesindeki eklenen footprintleri ve uyarıları birlikte incele.
5. **Update PCB** komutuyla footprintleri aktar; ilk grubu kart dışında geçici çalışma alanına bırak.
6. Kasa/panel bileşenlerini önce yerleştir: USB-C, çıkış konnektörleri, TFT, rotary encoder, CR2032 ve programlama konnektörü.
7. ESP32 anten kenarını ve keepout alanını kilitle.
8. Güç, ölçüm, MCU/RTC ve kullanıcı arayüzü bloklarını ayrı ayrı kart içine yerleştir.
9. Yerleşim onayından sonra güç yolları, USB çifti, hassas ölçüm hatları ve diğer sinyaller yönlendirilir.

Komponent aktarımı kullanıcıyla birlikte yapılacağı için PCB tabanı şu anda bilinçli olarak boştur.
