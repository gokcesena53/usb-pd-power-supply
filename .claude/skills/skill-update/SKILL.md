---
name: skill-update
description: Bir çalışma oturumunda öğrenilenleri ilgili skill'e geri işle veya bu derslerden yeni bir skill oluştur. Kullanıcı "öğrendiklerini skill'e ekle", "skill.md'yi güncelle", "geliştirdiğin tool'ları scripts'e koy", "bu oturumdan ders çıkar", "bundan yeni bir skill oluştur/ayır" dediğinde veya bir skill ile yapılan iş birkaç düzeltme turu gerektirdikten sonra kullan. Oturumda yazılan geçici betikleri skill'in scripts dizinine Windows + Linux'ta çalışacak şekilde genelleştirerek taşır, SKILL.md'ye ölçülü kurallar ve tuzaklar ekler, gerekirse yeni skill'in iskeletini kurar ve dersleri eski skill'den taşır.
---

# Skill güncelleme — oturumdan kalıcı bilgiye

Amaç: bir sonraki oturumun aynı hataları yapmaması ve aynı araçları yeniden
yazmaması. Çıktı iki şeydir: güncellenmiş `SKILL.md` ve `scripts/` altında test
edilmiş araçlar. Sohbette kalan bilgi kaybolur; skill'e girmeyen ders yoktur.

## 1. Hedef skill'i belirle ve tamamını oku

- Oturumda hangi skill kullanıldıysa o (`.claude/skills/<ad>/`). Birden fazlaysa
  her dersi ait olduğu skill'e yaz.
- `SKILL.md`'yi, `scripts/` altındaki her dosyayı ve `references/`'i **baştan sona**
  oku. Mevcut API'yi ve mevcut kuralları bilmeden ekleme yaparsan tekrar ve
  çelişki üretirsin.
- Hiçbir skill uygun değilse ya da derslerin çoğu mevcut skill'in konusunun
  dışında kalıyorsa **yeni skill öner, kullanıcı onaylarsa 1b'yi uygula**.
  Kullanıcı yeni skill'i zaten istediyse sormadan 1b'ye geç.
- Paylaşılan ortam katmanını da oku: `kicad-schematic/scripts/kicadtools.py` ve
  `kpy` (tüm skill'lerin OS farkını çözdüğü tek yer).

## 1b. Yeni skill oluştur (gerekiyorsa)

Ne zaman: oturum ayrı bir **iş akışı** üretti (kendi tetik cümleleri, kendi
doğrulama döngüsü, kendi araçları) ve bunu mevcut skill'e eklemek onu dağınık
yapar. Tek bir tuzak veya tek fonksiyon için yeni skill açma, mevcut skill'e yaz.
Örnek: 23.09'da footprint + 3D model dersleri `kicad-schematic`'ten
`kicad-footprint`'e ayrıldı (ölçme → kifp → fp_check → step_boxes akışı).

1. **İskelet:** `.claude/skills/<ad>/SKILL.md` (+ `scripts/`, gerekirse
   `examples/`, `references/`). Ad kebab-case, konuyu söyler (`kicad-footprint`).
2. **Frontmatter:** `name: <ad>`; `description` tetiklenmenin tek dayanağıdır:
   kullanıcının söyleyeceği iş cümlelerini ve nesneleri say ("... çizerken",
   "... üretirken", "... doğrularken kullan"). Türkçe, depo diliyle.
3. **Paylaşılan araç kopyalanmaz.** Ortam ve ortak yardımcılar tek yerde kalır;
   yeni skill'in betikleri `sys.path.insert(0, <HERE>/../../kicad-schematic/scripts)`
   ile içe aktarır. Kopya iki yerde ayrı ayrı bozulur.
4. **Dersleri taşı, ikilenmesin:** eski skill'de yeni konuya ait maddeleri
   (ör. land pattern ölçme, footprint önizleme tuzakları) yeni skill'e taşı, eski
   yerde tek satırlık yönlendirme bırak ("... `kicad-footprint` skill'inde").
5. **Tetikleri ayır:** eski skill'in `description`'ından yeni skill'e geçen işi
   çıkar; iki skill aynı cümleyle tetiklenmesin.
6. **Çapraz bağlantı:** iki SKILL.md birbirini adıyla ansın (hangi iş hangisinde).
7. **Örnek betik:** oturumdaki gerçek işi (örn. Waveshare footprint + STEP) yeni
   araçlarla yeniden üreten `examples/<iş>.py` yaz. Hem belge hem eşdeğerlik
   testi olur (§4): çıktısı oturumda üretilen dosyayla aynı olmalı.

## 2. Dersleri topla (oturumu tara)

Konuşmayı baştan tara ve şu türleri çıkar. Her birini tek cümleyle yaz, yanına
kanıtını koy (hangi hata çıktısı, hangi render, hangi ölçüm):

| tür | işaret | örnek |
|---|---|---|
| **Tuzak** | bir deneme başarısız oldu, sebebi bulundu | ayna dönüşümü yanlış modellendi → netlist'te `unconnected-(Q6-…)` |
| **Ölçüm** | sayıyla ifade edilen, deneme ile bulunan değer | 1.27 mm font ≈ 1.11 mm/karakter; kondansatör aralığı ≥ 15.24 mm |
| **Yöntem** | birden çok turda işe yarayan sıra/strateji | temizle → taşı → yeniden çiz; planarlık sorusu |
| **Ortam** | araç/OS/PATH/satır sonu sorunu | kicad-cli PATH'te yok; CRLF; `.kicad_pro` kirlenmesi |
| **Doğrulanmış gerçek** | datasheet/kaynakla teyit edilen, tekrar sorulacak bilgi | LM74502 CVCAP: VCAP–VS arası |
| **Kullanıcı düzeltmesi** | kullanıcı "böyle değil" dedi | — |

Eleme kuralları:
- **Tekrar olacak mı?** Yalnız bu işe özgü koordinat/değer ders değildir; ancak
  kuralı somutlaştıran *örnek* olarak kullanılabilir.
- **Koddan veya git geçmişinden okunabiliyor mu?** Okunabiliyorsa yazma.
- **Zaten skill'de var mı?** Varsa ekleme; eksik/yanlışsa **o maddeyi düzelt**.
  Yeni bilgi eski bir cümleyle çelişiyorsa eskiyi sil, çelişkiyi bırakma.
- **Doğrulandı mı?** Tahmin olan şeyi kural diye yazma. Ampirik ise nerede
  doğrulandığını yaz ("Q5/Q6 üzerinden doğrulandı").

## 3. Araçları genelleştir

Oturumda scratchpad'de yazılan betikleri gözden geçir. Birden fazla yerde işe
yaradıysa veya bir sonraki benzer işte tekrar yazılacaksa skill'e taşı.

1. **Önce mevcut araçları genişlet, yeni dosya en son.** Aynı işi yapan fonksiyon
   varsa ona parametre ekle (geriye uyumlu, varsayılan eski davranış). Yeni
   sorumluluk alanıysa ayrı modül (ör. üretim `kisch.py` / düzenleme
   `kisch_edit.py` / ortam `kicadtools.py`).
2. **Oturuma özgü olanı ayıkla:** mutlak scratchpad yolları, sabit koordinatlar,
   dosya adları, kullanıcıya özel PATH'ler. Yol bulma gerekiyorsa ortam değişkeni
   + makul arama listesi.
3. **Oturumda bulunan hatayı araçta düzelt**, yalnız dokümana yazma. (Örn.
   ayna modeli yanlışsa `xf` doğru modeli uygulasın.)
4. Her fonksiyona **neden** var olduğunu ve hangi tuzağı önlediğini anlatan kısa
   docstring. Modül başına kullanım örneği.
5. Deterministik denetim yazılabiliyorsa yaz (lint, fark, assert). Görsel
   kontrolün yakaladığı bir hata sınıfı kodla yakalanabiliyorsa kodla yakala.
6. Depo biçimine uy: satır sonu (CRLF/LF), dil (yorum ve mesajlar), mevcut
   isimlendirme.
7. **Windows + Linux'ta aynı komutla çalışsın.** Depo iki ortamda geliştiriliyor;
   oturumda Windows'a/Linux'a özel yama yaptıysan (yol, yorumlayıcı adı,
   eksik araç) onu betikte değil ortam katmanında çöz:
   - Yorumlayıcı adı yazma: çağrı `sh $SK/kpy betik.py` (Windows'ta `python3`
     Store kısayoluna düşer, Linux'ta `python` olmayabilir). Hook ve belge
     komutları da `kpy` ile.
   - Araç/dizin yolu yazma: `kicadtools.kicad_cli()`, `kicad_share(...)`,
     `kicad_python()`; yeni bir araç gerekiyorsa aynı kalıpla (ortam değişkeni >
     PATH > Windows/Linux/macOS kurulum dizinleri) oraya ekle.
   - Yalnız bir yorumlayıcıda bulunan modül (pcbnew) için `ensure_pcbnew()`
     kalıbı: betik kendini doğru yorumlayıcıda yeniden başlatır.
   - Eksik olabilen araç için yedek yol (PyMuPDF ↔ pdftoppm) ve açık hata mesajı.
   - Dosyayı `encoding='utf-8'` ile aç; satır sonunu okunduğu gibi koru.
8. **Üretim betikleri deterministik olsun:** rastgele uuid (uuid4) ve saat
   damgası yerine ada bağlı uuid5 ve sabit damga; aynı girdiyle ikinci çalıştırma
   git'te fark yaratmamalı (`kifp`/`step_boxes` böyle).

## 4. Araçları test et — gerçek dosyalarda, yan etkisiz

Taşınan/değişen her araç için:
- **Eşdeğerlik:** yeni fonksiyon, oturumda elle yapılan işlemin sonucunu birebir
  üretiyor mu? (Örn. `git show HEAD:<dosya>` üzerinde çalıştır, mevcut dosyayla
  karşılaştır.)
- **İdempotentlik:** zaten uygulanmış dosyada ikinci çağrı değişiklik üretmemeli.
- **No-op:** kimlik fonksiyonuyla çağrıldığında hiçbir dosya değişmemeli.
- **Doğrulama zinciri** (skill'in kendi `verify`/`render` adımları) yeni
  araçlarla tekrar çalışmalı ve oturum sonundaki sonucu vermeli.
- Test bir kusur bulursa (ör. lint yeni bir sorun raporlarsa) onu da düzelt ve
  kullanıcıya bildir.
- `git status` ile beklenmeyen dosya değişikliği olmadığını kontrol et
  (araçların yan etkisi, ör. `.kicad_pro`).
- **Testleri `kpy` üzerinden çalıştır** (belgedeki komutun kendisiyle).
  Yalnız bir OS'ta test edebildiysen raporda hangi OS'ta doğrulandığını ve
  diğerinde hangi kod yolunun denenmediğini yaz (ör. Linux'ta `pdftoppm` yedeği).
- Kullanıcının açık KiCad'ine dokunma: yazan araçları projenin scratchpad
  kopyasında test et (`kicad-schematic` → "KiCad açıkken kuru çalıştırma").

## 5. SKILL.md'yi yaz

- **Yapıyı koru**, dersleri ait oldukları bölüme koy: komutlar "Temel döngü"ye,
  ortam sorunları "Ortam"a, ölçülü değerler "Yerleşim/kurallar"a, bir kez
  yakıcı olan hatalar "Tuzaklar"a. Yeni bölüm yalnız birden çok madde varsa.
- Her tuzak: **ne olur → neden → ne yapmalı → hangi araç**. Belirti (ERC/netlist
  mesajı) varsa aynen yaz; bir sonraki oturum hatayı onunla tanır.
- Ölçüleri sayıyla yaz, kaynağını belirt ("render'dan ölçüldü").
- Modül tablosunu ve kullanım örneklerini yeni API ile güncelle. Artık var
  olmayan fonksiyon adı bırakma; örnek kodu gerçekten çalışır tut.
- `description` frontmatter'ını skill'in yeni kapsamını kapsayacak şekilde
  güncelle (tetiklenme buna bağlı).
- Kısa tut: tekrar eden, oturum anlatısı gibi okunan ("önce şunu denedim…")
  cümleleri at. Kural + neden + araç.

## 6. Raporla

Kullanıcıya kısa özet:
- eklenen/değişen dersler (başlık düzeyinde),
- eklenen/değişen araçlar ve ne işe yaradıkları,
- testlerin sonucu ve bulunan yeni kusurlar,
- commit edilmediğini (istenmedikçe commit etme; edilecekse yalnız ilgili
  dosyaları ekle, `git add -A` kullanma).

## Kontrol listesi

- [ ] Hedef skill'in tüm dosyaları ve ortak ortam katmanı okundu
- [ ] Yeni skill gerekiyorsa: iskelet, description, paylaşılan araç içe aktarımı,
      taşınan dersler + eski yerde yönlendirme, ayrılmış tetikler, örnek betik
- [ ] Dersler türlerine ayrıldı, elendi, kanıtları var
- [ ] Çelişen eski maddeler düzeltildi/silindi
- [ ] Scratch araçlar genelleştirildi, sabit yollar kaldırıldı
- [ ] Araçlarda yorumlayıcı adı / OS yolu yok; `kpy` ile çalıştı, hangi OS'ta test edildi yazıldı
- [ ] Üretim betikleri deterministik (ikinci çalıştırma git farkı üretmiyor)
- [ ] Eşdeğerlik + idempotentlik + no-op testleri geçti
- [ ] Skill'in doğrulama zinciri yeni araçlarla çalıştı
- [ ] `git status` temiz (beklenmeyen değişiklik yok)
- [ ] SKILL.md örnekleri gerçek API ile uyumlu, description güncel
