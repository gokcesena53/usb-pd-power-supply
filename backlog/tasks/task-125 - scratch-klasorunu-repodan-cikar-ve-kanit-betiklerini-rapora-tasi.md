---
id: TASK-125
title: scratch klasorunu repodan cikar ve kanit betiklerini rapora tasi
status: In Progress
assignee: []
created_date: '2026-09-30 06:42'
updated_date: '2026-09-30 06:49'
labels:
  - docs
dependencies: []
references:
  - design_decisions/output/SCRATCH_KLASORU_DEPO_DISI_TASK125_20260930.md
  - CHANGES.TXT
ordinal: 211000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
`scratch/` klasoru 795e911 (26.09) ve 44d5015 (28.09) toplu commit'leriyle repoya girdi (297 dosya, ~50 MB). Tanimli akista gecici calisma repo disindaki oturum scratchpad'inde tutulur (kicad-schematic/SKILL.md, kicad-placement/SKILL.md, skill-update/SKILL.md); `scratch/` bu kurala aykiri bir sizinti. Ancak task-100/105/106/107/108 raporlari, gorevleri ve design_decisions dosyalari 7 dosyaya kanit olarak yol veriyor.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Referans verilen 7 dosya (+2 cikti) hardware/docs/reports/task-XXX-20260928/scripts/ altina git mv ile tasindi
- [x] #2 `git grep scratch/ -- ':!scratch' ':!CHANGES.TXT'` referans gecmis tarih kaydi disinda sonuc vermiyor
- [x] #3 Tasinan betiklerin kendi icindeki scratch/ yollari yeni konuma guncellendi
- [x] #4 .gitignore'da scratch/ satiri var; `git ls-files scratch` 0 dosya donuyor
- [x] #5 design_decisions/ karar dosyasi, CHANGES.TXT kaydi ve CLAUDE.md 'Nerede ne tutulur' satiri eklendi
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Kanit (30.09.2026, rev_c, commit oncesi):
- 9 dosya git mv ile tasindi (git status: R/RM): task-100 (ratsnest_crossing_test.py), task-105 (audit_task104_compliance.py/.json, task105_current_drc.rpt), task-106 (force_repack_optimizer.py, execute_final_optimization.py), task-107 (audit_task107_final.py, task107_drc.rpt), task-108 (execute_task108_compaction.py).
- 15 dosyada yol guncellendi, diff 26+/26-. Betiklerde yalniz yol stringleri ve sys.path degisti.
- `git grep scratch/` (CHANGES.TXT tarihcesi, .claude skill `<scratch>` yer tutuculari, bu gorevin kendi dokumanlari haric): 0 sonuc.
- `git ls-files scratch` = 0; `git check-ignore scratch/x` eslesiyor. Yerel diskte 324 oge duruyor.
- 6 betik ast.parse ile gecti; ratsnest_crossing_test.py depo kokunden calisti (guncel PCB: MST 960.70 mm).
- .gitignore, CLAUDE.md (Nerede ne tutulur: 3 satir), CHANGES.TXT (30.09 kaydi), design_decisions karar dosyasi eklendi.
Done icin kalan: commit hash.
<!-- SECTION:NOTES:END -->
