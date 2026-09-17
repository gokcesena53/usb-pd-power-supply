# gopo — Masaüstü Güç Kaynağı

USB-C PD beslemeli, ESP32-C6 tabanlı, TFT ekranlı ve döner enkoderli masaüstü
ayarlanabilir güç kaynağı. Şematik ve PCB tasarımı KiCad ile yapılmıştır.

Depo yapısı [Open Hardware Template](https://github.com/mfhepp/open_hardware_template)
şablonunu izler.

## İçerik

- **Donanım:** KiCad projesi, projeye özel sembol ve footprint kütüphaneleri — `hardware/`
- **Tasarım kararları:** hesaplamalar, inceleme ve doğrulama notları — `design_decisions/`
- **Yazılım:** firmware ve yardımcı betikler — `software/`

Aktif revizyon REV_B'dir. Değişiklik kaydı için `CHANGES.TXT` dosyasına bakınız.

## Tasarım kuralları ve PCB üretimi

Tasarım kuralları `hardware/gopo.kicad_dru` dosyasındadır. Üretime göndermeden önce
seçtiğiniz üreticinin yeteneklerine uyduğunu doğrulayın.

PCB ipek baskısına ve şematiğe "Licensed under CERN OHL v.1.2" metnini eklemeyi unutmayın.

## Sorumluluk reddi

BU TASARIM VE YAZILIM, AÇIK VEYA ZIMNİ HİÇBİR GARANTİ OLMAKSIZIN "OLDUĞU GİBİ"
SAĞLANMAKTADIR. YAZARLAR VEYA TELİF HAKKI SAHİPLERİ, TASARIMIN VEYA YAZILIMIN
KULLANIMINDAN DOĞAN HİÇBİR TALEP, ZARAR VEYA SORUMLULUKTAN SORUMLU TUTULAMAZ.
