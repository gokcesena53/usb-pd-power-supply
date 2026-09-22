# gopo — Claude çalışma kuralları

## İş takibi: Backlog.md

Yapılacaklar `backlog/` altında Backlog.md ile tutulur (`todo.txt` kaldırıldı).
Görevleri MCP (`backlog` sunucusu) veya `backlog` CLI ile oku/güncelle; dosyaları
elle düzenleme.

- **Durumlar:** `To Do`, `In Progress`, `Blocked`, `Done`. Numune, PCB veya
  tedarik bekleyen iş `Blocked`; neyi beklediği bağımlılık olarak girilir.
- **Etiketler süreç bazlıdır** (tasarımın hangi adımında yapılacağı):
  `schematic`, `layout`, `procurement` (parça seçimi/tedarik/BOM),
  `sample-eval` (numune ile doğrulama), `fabrication` (Gerber, üretim, dizgi),
  `bring-up` (prototip ölçüm ve doğrulama), `firmware`, `docs`. Her görevde en
  az bir etiket; iki sürece yayılan iş iki etiket alabilir.
- **Milestone'lar** revizyon aşamasıdır: `REV_C şema`, `REV_C PCB-üretim`,
  `REV_C prototip`, `Firmware v1`.
- **Kabul kriterleri ölçülebilir olsun** (eşik, pin, ref). Doğrulama görevinde
  ölçüm sonucu Implementation Notes'a yazılır.
- **Done'a almadan önce kanıt:** ERC/netlist çıktısı, ölçüm veya commit hash'i
  Implementation Notes'a yazılır.
- Yeni iş, ertelenen karar veya `TBD` parça için görev aç; kod/şema yorumuna
  "todo" bırakma.
- Görev başlıkları Türkçe olabilir, kısa tut. **Dosya adları ASCII olmalı:**
  Backlog.md başlığı dosya adına Türkçe karakterleriyle çevirir; görev
  oluşturduktan sonra `python software/backlog_ascii.py` çalıştır (Claude'da
  `.claude/settings.json` hook'u bunu otomatik yapar).

## Nerede ne tutulur

| Ne | Nerede |
| --- | --- |
| Yapılacak iş | `backlog/tasks/` |
| Tasarım kararı, hesap, inceleme | `design_decisions/` (tek kaynak; `backlog/decisions` kullanılmaz) |
| Firmware'in donanımdan beklediği davranış | `software/FIRMWARE_GEREKSINIMLERI.md` |
| Lisans gereği değişiklik kaydı | `CHANGES.TXT` (CERN OHL 3.4.b) |

Karar görev sırasında değişirse ilgili `design_decisions/` dosyasını ve
`CHANGES.TXT`'yi de güncelle; görev bu dosyalara `--ref`/`--doc` ile bağlanır.

## Dallar

Uzun ömürlü `rev_c` dalı ve `main` var. Görev dosyalarını aynı anda iki dalda
düzenleme; backlog değişiklikleri aktif revizyon dalında (`rev_c`) yapılır.
