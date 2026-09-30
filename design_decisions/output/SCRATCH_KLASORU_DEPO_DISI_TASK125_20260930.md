# scratch/ klasörü depo dışı (30 Eylül 2026)

Görev: TASK-125.

## Durum

`scratch/` klasörü iki toplu commit'le depoya girdi: `795e911` (26.09, 77 dosya)
ve `44d5015` (28.09, 220 dosya). Toplam 297 dosya (~50 MB): 172 `.py`, 30 aday
`.kicad_pcb` ve bunların `.kicad_pro`/`.kicad_dru` kopyaları, DRC `.rpt` ve `.json`
çıktıları. İçerik TASK-098…108 yerleşim denemelerine ait. Sonuçlar zaten
`hardware/gopo.kicad_pcb`'ye ve görev raporlarına aktarılmıştı.

Tanımlı akışta geçici çalışma repo dışındaki oturum scratchpad'inde yapılır:

- `kicad-schematic/SKILL.md`: "Betiği scratchpad'de tut; depoya yalnız sonuç
  şema girer."
- `kicad-placement/SKILL.md`: kopyalar scratchpad'de; `hardware/*.kicad_pcb`'ye
  `pcb_check` geçtikten sonra yazılır.
- `skill-update/SKILL.md`: işe yarayan scratchpad betiği genelleştirilip
  skill'in `scripts/` klasörüne taşınır.

Depodaki `scratch/` bu kuralın dışında kalan bir sızıntıydı.

## Karar

1. `scratch/` `.gitignore`'a eklendi. Dosyalar `git rm --cached` ile git'ten
   çıkarıldı; yerel diskte ve eski commit'lerde durur.
2. Rapor, görev veya karar dosyalarının kanıt olarak yol verdiği dosyalar
   ilgili görevin rapor klasörüne `git mv` ile taşındı:

   | Dosya | Yeni yer (`hardware/docs/reports/…/scripts/`) |
   | --- | --- |
   | `ratsnest_crossing_test.py` | `task-100-20260928` |
   | `audit_task104_compliance.py`, `.json`, `task105_current_drc.rpt` | `task-105-20260928` |
   | `force_repack_optimizer.py`, `execute_final_optimization.py` | `task-106-20260928` |
   | `audit_task107_final.py`, `task107_drc.rpt` | `task-107-20260928` |
   | `execute_task108_compaction.py` | `task-108-20260928` |

   Betiklerin içindeki `scratch/` yolları (varsayılan girdi/çıktı yolları ve
   `sys.path`) yeni konuma çevrildi. Betiklerin mantığı değiştirilmedi.
   Betiklerde sabit KiCad yolu (`C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`)
   ve kök dizine yazılan `audit_compliance.json` gibi eski davranışlar olduğu
   gibi duruyor. Bunlar tarihsel kanıt betikleri; yeniden kullanılacaksa
   `kicadtools.py` ile genelleştirilip bir skill'e taşınmalı.
3. `CHANGES.TXT`'deki eski kayıtlarda geçen `scratch/…` yolları tarihçe
   olduğu için değiştirilmedi; taşıma yeni bir kayıtla belgelendi.

## Bundan sonra

| Ne | Nerede |
| --- | --- |
| Deneme betiği, aday PCB, ara DRC çıktısı | Repo dışı oturum scratchpad'i |
| Görevin kanıtı olan betik/çıktı | `hardware/docs/reports/<görev>/scripts/` |
| Tekrar kullanılacak araç | `.claude/skills/<skill>/scripts/` |
