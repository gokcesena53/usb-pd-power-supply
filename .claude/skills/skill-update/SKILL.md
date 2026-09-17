---
name: skill-update
description: Bir çalışma oturumunda öğrenilenleri ilgili skill'e geri işle. Kullanıcı "öğrendiklerini skill'e ekle", "skill.md'yi güncelle", "geliştirdiğin tool'ları scripts'e koy", "bu oturumdan ders çıkar" dediğinde veya bir skill ile yapılan iş birkaç düzeltme turu gerektirdikten sonra kullan. Oturumda yazılan geçici betikleri skill'in scripts dizinine genelleştirerek taşır, SKILL.md'ye ölçülü kurallar ve tuzaklar ekler.
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
- Hiçbir skill uygun değilse yeni skill önermeden önce kullanıcıya sor.

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

- [ ] Hedef skill'in tüm dosyaları okundu
- [ ] Dersler türlerine ayrıldı, elendi, kanıtları var
- [ ] Çelişen eski maddeler düzeltildi/silindi
- [ ] Scratch araçlar genelleştirildi, sabit yollar kaldırıldı
- [ ] Eşdeğerlik + idempotentlik + no-op testleri geçti
- [ ] Skill'in doğrulama zinciri yeni araçlarla çalıştı
- [ ] `git status` temiz (beklenmeyen değişiklik yok)
- [ ] SKILL.md örnekleri gerçek API ile uyumlu, description güncel
