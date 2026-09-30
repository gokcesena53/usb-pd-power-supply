---
id: TASK-109
title: PCB güç ve kontrol hiyerarşisini gerçek netlerle düzelt
status: To Do
assignee: []
created_date: '2026-09-28 13:46'
labels:
  - layout
  - schematic
  - docs
milestone: m-1
dependencies:
  - TASK-101
references:
  - hardware/docs/reports/flow-space-plan-20260928/PLAN.md
  - hardware/gopo.kicad_pcb
priority: high
ordinal: 195000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
PLAN.md bölüm 2 temelinde güncel şema/PCB netlerinden iki ayrı güç kolunu ve kontrol akışını doğrula. Eski tek seri güç zinciri anlatımını ve hatalı pin/kapasitör rollerini düzelt. Bu görev yerleşim ve routing çalışmalarının mimari temelidir.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 J7/R11 sonrasında Q5-shunt-J4 kullanıcı çıkışı ve Q3-boost-V_PRE-buck dahili besleme kolları pin/net kanıtıyla ayrı gösterilmiş.
- [ ] #2 U3 ve MCU üzerinden U13/SW_EN, U12/Q5 ve Q4/Q6 deşarj ilişkileri belgelenmiş; 15 KiCad grubunun işlev haritası hazırlanmış.
- [ ] #3 C16 çıkış, C12/C13 giriş, U5 pin5 COMP ve pad9 VIN; U1 güncel parça kimliği doğrulanmış. Eski TASK-101 raporu ve ilgili karar belgelerine açık düzeltme eklenmiş.
- [ ] #4 Şema/PCB hash ve net tablosu kayıtlı; mevcut dört iz ve dolgusuz kart durumu doğru belirtilmiş; net topolojisi değiştirilmemiş.
<!-- AC:END -->

## Definition of Done
<!-- DOD:BEGIN -->
- [ ] #1 Kanıt (ERC/netlist/ölçüm/commit) Implementation Notes'a yazıldı
- [ ] #2 Karar değiştiyse design_decisions/ ve CHANGES.TXT güncellendi
<!-- DOD:END -->
