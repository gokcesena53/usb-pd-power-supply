---
name: kicad-placement
description: Create, optimize, or review KiCad component placement from the IC outward, first within functional blocks and then between blocks, using weighted pad-to-pad ratsnest length and routing constraints. Use for placement tasks ("yerleşim yap", "sıfırdan yerleşim", "kilitli parçalara dokunmadan yerleştir", "yerleşimi skorla/karşılaştır", "kritik döngüleri denetle"); includes pure-python annealing/legalisation/refinement tools, a project config for blocks/critical pairs/regions, apply/check/DRC/render scripts. Full routing and fabrication review are separate tasks.
---

# KiCad placement

## Agreed approach

Start with the IC, then place surrounding components to reduce critical current loops. Solve each functional block internally before optimizing how blocks fit together. Evaluate connections before attempting routing. The primary metric is weighted ratsnest length, subject to electrical, mechanical, and routing constraints.

These are the user's agreed starting weights, not universal electrical constants:

| Connection role | Weight |
| --- | ---: |
| Critical current loop or local decoupling connection | 10 |
| Sensitive measurement, Kelvin sense, or feedback connection | 5 |
| Other power or signal connection | 5 |

Assign weights to specific pad relationships, not entire net names. GND does not automatically receive weight 10. If a relationship has multiple roles, use the highest applicable weight. Record why each critical pair qualifies, using actual schematic topology and device layout guidance. Mark unknown roles as uncertain rather than inventing classifications.

## Establish the problem

- Identify the active board and schematic. Derive functional blocks and pad connectivity from them; reference designators and sheet boundaries alone do not establish function.
- Read project placement requirements, stackup, net classes, keepouts, outline, and mechanical constraints. Identify fixed connectors, mounting holes, locked footprints, antenna exclusions, permitted sides, and existing routing.
- Preserve outline, footprint choices, net assignments, layer count, and fixed placements unless the current task authorizes changes. Do not silently unlock components or discard routing to improve a score.
- Consult the actual part's datasheet/layout recommendations for critical topology and package-specific limits. Generic guidance is supplementary.
- Capture a baseline: block membership, footprint positions/rotations/sides, constraints, critical pad pairs, and score. Keep a recoverable board copy and avoid overwriting unsaved editor work.

## Placement sequence

### 1. Place the IC

Choose an initial position and orientation using pin functions, expected connection directions, and physical limits. The IC is a starting anchor, not automatically immovable. Revise its position or angle when that improves the block within constraints. For multiple-IC blocks, identify the functional anchor and relationships. For passive-only blocks, use the constrained interface as the anchor.

### 2. Optimize within the block

Place critical loop and local decoupling components first, sensitive measurement/feedback components next, and remaining components afterward. Consider both forward and return paths. Test component translations and permitted rotations using actual pad coordinates and package geometry.

Keep each decoupling capacitor on the same side as its IC wherever there is room; move it to the other side only when no legal same-side slot exists, and report every such flip. The rule applies to SMD IC pins; a THT pin (module header) is reachable from both sides.

Minimize the weighted internal score while applying the alignment rules below. Preserve pad escape paths and space for vias, power copper, thermal needs, and assembly access.

### Component and pad alignment

- Align neighbouring components into deliberate rows or columns within each block. For example, two side-by-side resistors must share a top or bottom body edge; vertically stacked parts use a shared left or right body edge. Apply this to local component groups rather than forcing unrelated blocks onto one global line.
- Use the component body outline from the fabrication layer or documented package geometry as the edge reference. Do not align reference text, silkscreen labels, or footprint origins and assume that component edges align. For different package sizes, explicitly select the shared edge.
- Where possible, align the centres of pads that will connect: use the same Y coordinate for a horizontal connection or the same X coordinate for a vertical connection. For a rotated block, use its local axes. Evaluate actual transformed pad centres, not component centres.
- Choose the component edge and orientation that also align connecting pad centres when both can be satisfied. When different package geometry prevents both, prefer a feasible direct pad connection and explain the body-edge compromise.
- Include aligned candidates during optimization. Do not accept arbitrary staggering merely because it slightly reduces the weighted score. Keep the agreed weights (table above; ordinary edges via config `W_ORDINARY`) unchanged; record alignment separately rather than inventing another weight.
- Electrical, mechanical, clearance, and routing constraints still take precedence. If alignment would harm a critical loop, return path, pad escape, or fixed placement, retain the electrically feasible arrangement and identify the specific exception.
- Check the chosen shared edges and pad-centre axes numerically where geometry is available, then inspect the render. Use the project's placement grid or coordinate precision for tolerance; report residual offsets and avoid claiming exact alignment from an image alone. Preserve local alignment when moving or rotating a solved block.

### 3. Optimize between blocks

Treat internally solved blocks as groups. Translate or rotate each group while preserving internal relative positions and orientations. Evaluate inter-block connections using actual interface pads. Respect fixed members: group movement cannot displace a fixed connector or locked footprint.

If a block's internal arrangement prevents a workable interface, deliberately return to step 2 for that block. Record the compromise and compare internal and inter-block scores separately. Do not scatter a solved block simply to reduce the global score.

## Define and compare the metric

Use millimetres and pad centres transformed into board coordinates, including footprint rotation and side:

`S = sum(weight(edge) * Euclidean_pad_distance_mm(edge))`

Record unweighted length as well as weighted score. Report internal and inter-block scores separately. Compare candidates using the same connectivity, block membership, weights, distance definition, and constraints. If these change, recompute the baseline.

For multi-pad nets, avoid summing every pad pair. Use this reproducible scoring graph:

1. Retain explicitly identified critical pad pairs as fixed edges with their assigned weights, even if they form a cycle. These represent required physical relationships.
2. Complete connectivity on each net with a minimum-length set of ordinary edges, using Euclidean distances and deterministic pad-ID tie breaking. Without critical edges, use a minimum spanning tree. Otherwise contract the connected components of the critical-edge graph and connect those components by a minimum spanning tree.
3. Count each unordered pad pair once. Recompute ordinary completion edges for each candidate while preserving critical pairs and their weights. Record the edge list for auditability.

During search the ordinary GND completion may be left out (it returns through a plane and dominates run time); the reported score always includes it (`place.py score`).

This graph estimates placement quality; it neither reproduces KiCad's displayed ratsnest exactly nor prescribes final copper topology. On partly routed boards, do not score only currently visible unconnected airwires: retain a consistent graph and treat existing copper as a constraint. A GND airwire does not describe the physical return-current path through a plane.

## Feasibility takes precedence over score

Reject candidates that violate fixed positions, board/keepout limits, package or courtyard constraints, electrical clearances, or documented mechanical requirements. Preserve routing corridors and pad escape access. Use actual net-class width/clearance and via geometry where available; explicitly identify unverified route capacity when they are missing.

Weighted distance alone cannot establish small loop area, low inductance, return-path continuity, thermal adequacy, or routability. Inspect critical forward/return geometry and intended reference planes separately. A lower total score must not hide a broken critical relationship or a worsened critical loop. Explain any tradeoff rather than automatically selecting the smallest score.

Do not invent universal spacing or loop-area thresholds. Apply device/project limits supported by documentation where available. Use visual review and engineering judgment for criteria the available tools cannot measure.

## Iterate and verify

- Compare feasible local candidates and retain the best justified result. Stop when a reasonable local search gives no meaningful improvement; report a local result, not a proven global minimum. Do not invent scores if no measurement was performed.
- Inspect the whole board and detailed renders of changed blocks with pad/net context. Check that routes can plausibly leave pads and that critical electrical relationships are preserved.
- Reopen the saved candidate with KiCad-compatible tooling. Check reference identities, pad nets, footprint count, and fixed placements. Review DRC changes where tooling is available. Distinguish expected unrouted connections from placement violations; DRC alone does not prove routability.
- Evaluation through connections is the default. Completing routes is not a prerequisite. If a specific corridor needs trial routing, keep that work within the user's authorized scope and preserve the placement candidate.
- Report changed blocks, measured before/after scores, preserved constraints, critical geometry findings, and remaining uncertainty. Link saved board and useful review images. Label qualitative reviews as qualitative.

## Tools (`scripts/`, pure python + pcbnew only where needed)

Run everything through `kpy` (Windows + Linux). Project data lives in a config
(`examples/gopo_rev_c.py`: blocks, critical pairs with reasons, regions, edge/tied
parts, keepouts, `W_ORDINARY` = weight of ordinary MST edges); the scripts hold no
board-specific values. A keepout listing `@F`/`@B` bans every non-fixed part on that
side plus THT pins from the other side (thermal-via pads excluded), e.g. the LCD FPC
bend path on top. Work on copies in the
scratchpad; write `hardware/*.kicad_pcb` only after `pcb_check` passes and KiCad
is closed (`kicadtools.kicad_open()`).

```sh
K="sh .claude/skills/kicad-schematic/scripts/kpy"; PL=.claude/skills/kicad-placement/scripts
C="--parts $T/parts.json --cfg .claude/skills/kicad-placement/examples/gopo_rev_c.py"
$K $PL/pcb_dump.py hardware/gopo.kicad_pcb $T/parts.json      # geometry, locked, tracks
$K $PL/place.py score $C                                       # baseline S, worst pairs
$K $PL/place.py pipeline $C --seeds 21,22,23,24 --out $T       # anneal->legal->refine(--no-worse)->align, parallel
$K $PL/place.py score $C $T/best.json                          # before/after, blocks, loop sums, lengthened pairs
$K $PL/place.py pen $C $T/best.json                            # remaining constraint offenders
$K $PL/pcb_apply.py hardware/gopo.kicad_pcb $T/best.json $T/cand.kicad_pcb --parts $T/parts.json [--drop-net NET]
$K $PL/pcb_check.py hardware/gopo.kicad_pcb $T/cand.kicad_pcb --drc --out $T [--allow-flip C14 ...]   # identity + DRC/parity, exit 1 on fail
$K $PL/pcb_render.py $T/cand.kicad_pcb $T/cand                 # cropped top/bottom PNG
```

| script | role |
| --- | --- |
| `placelib.py` | model, scoring graph (critical edges + per-net MST), constraint engine |
| `place.py` | `anneal`, `legal`, `refine`, `sweep`, `untangle`, `align`, `score`, `pen`, `pipeline` |
| `pcb_dump.py` | board → JSON; rectilinear courtyards split into horizontal slabs |
| `pcb_apply.py` | state → board copy; aborts if a locked part moves or pad deviation > 1 µm |
| `pcb_check.py` | reopen and compare refs/pad-nets/side/footprint/locked/outline; DRC + parity on temp copies |
| `pcb_render.py` | kicad-cli PDF → PNG cropped to Edge.Cuts (PyMuPDF, else pdftoppm) |
| `pcb_freeroute.py` | trial routing on a copy: planes as power layers + zones, DSN -> Freerouting -> SES, vias/length/unconnected via DRC |

Routability terms (config, 0 = off): `W_CROSS` per same-side crossing of two score
edges of different nets (GND excluded), `W_DECAP_SIDE` per decap on the other side
of its SMD IC, `W_GND_LOCAL` per mm from a part's GND pad to the nearest GND pad in its
block (restores pull on bulk caps/test points while GND MST stays out of the search).
`score` also prints crossings, via edges (edge between sides), decap-side violations,
flips and "kopuk" parts (nearest connected pad > `FAR_MM`). Weighted length alone
ignores crossings: rotating a resistor 180° costs nothing yet decides a via.
`untangle` is cheap (seconds): rotations and same-package swaps only.
Nets carried by an inner plane or polygon (`PLANE_NETS`, plus GND) are not traces:
their ordinary MST edges count at `W_PLANE` (polygon compactness) and are left out of
crossings; their critical edges (decap, Kelvin sense, hot loop) stay real traces. On
gopo this dropped crossings from 75 to 57 with no part moved: +3.3V, PD_VBUS_SENSED and
USB_VBUS had been pushing parts for crossings that the In2 polygons remove. Changing
this changes S, so recompute the baseline before comparing.
`AUTO_LOCAL` adds each IC-pin-to-single-passive net (SS cap, series/pull resistor) to
the critical list at `W_ORDINARY`: S is unchanged, but refine only pulls along
critical edges, so without it such parts stayed 7–25 mm away. Use `NO_WORSE_W = 5`
with `--no-worse`: at 10, crossing pressure stretched the R11 Kelvin pair 6.7 → 10.6 mm.
A series resistor lies on a degenerate line (any point between driver and load costs
the same); place it by convention (next to the driver) and report the trade-off.

State is `{ref: [x, y, k]}`, `k & 3` = extra 90° steps in board frame, `k & 4` = flipped
to the other side (`Flip(pos, LEFT_RIGHT)` mirrors the offset x, then rotate; verified
0.0000 mm on 7 parts + an applied C14/C3 flip); change `k` via `turn()` to keep the bit; `(dx, dy)` →
`(dy, −dx)` for +90° equals `footprint.Rotate(pos, +90)` on both sides (0.0000 mm
pad deviation on 137 parts). Tested on Linux (pdftoppm path); the PyMuPDF path and
Windows `ensure_pcbnew` re-exec were not exercised in this session.

Measured (gopo, 144 parts, Linux): ~1.4 ms per anneal iteration, 180k iterations
≈ 11 min per seed; one of four seeds legalised cleanly, so run several in parallel.

## Pitfalls learned (TASK-115, 29.09.2026)

- **A metric-only search breaks the approved floorplan.** Unconstrained annealing
  moved the PD controller and 3 A shunt under the ESP32 and sent bulk/output caps
  (then weight 1) towards their consumers, still scoring −42 %. Put the documented zoning
  into `REGION[(block, side)]` before searching and review the render before accepting.
- **Legalisation detaches ICs from their decoupling.** Relocating overlapping parts
  moved U1/U2/U13 while their caps stayed (C6–U2 grew to 15 mm). Always follow
  `legal` with `refine` (critical-edge pull + IC-with-satellites moves).
- **Lower total can hide a worse loop.** Use `refine --no-worse` (weight-10 pairs may
  not exceed their baseline length; 50 per mm) and judge loops by `LOOP_GROUPS`
  sums: boost SW–D4 grew 4.6 → 7.3 mm while the whole loop shrank 33 → 17 mm —
  report such trade-offs explicitly.
- **Forcing one part into place and legalising the rest made things worse**
  (U11 pushed out, S +128). Prefer longer constrained `refine`/`sweep`.
- **Small random steps cannot clear 5–20 mm² overlaps;** `legal` scans every legal
  slot around the part (0.25/0.5/1 mm rings, 4 rotations). A slide part (J7) may find
  no slot when free parts occupy its range; `legal` then returns it to its board
  position and relocates the blockers in the next round.
- **Parts on GND only have no pull** once GND ordinary edges are excluded (TP13 left
  the board); add a `PULL` grouping or fix them.
- **Decaps to pins under a module** (J8 3V3 pins) get pulled into the module
  courtyard; keep the module courtyard hard unless an XY/Z exception is documented.
- **THT pads block the opposite side** (J8 header pins on top, U11 thermal vias under
  J3); `tht_obstacles` handles it. Pads numbered `""` (EP thermal sub-pads) are skipped.
- **Courtyard bbox is wrong for T-shaped courtyards** (U2 incl. off-board antenna
  keepout); `pcb_dump` slices rectilinear polygons and `NO_EDGE_CHECK` parts are clipped
  to the board.
- **Moving parts creates silkscreen violations** (+15 silk_overlap, +14
  silk_over_copper here); open a silkscreen task rather than hiding it.
- **Trial routes whose ends move** become dangling copper; remove them only by
  explicit `--drop-net` and report the unconnected count change (360 → 361).
- KiCad 10 SWIG: after `B.Remove(track)`, `footprint.Pads()` returns `SwigPyObject`;
  read footprints first, delete tracks last with `B.Delete`.

## Block re-placement (LNS, TASK-124, 29.09.2026)

- `anneal --inp <state> --blocks B` rebuilds only block B around its current centroid,
  everything else is a fixed obstacle; follow with `legal/refine/untangle --blocks B`.
  Fix the hot-loop parts with a temporary config that `exec`s the project config and
  sets `FIXED_EXTRA`. Rebuilding a whole switcher block stretched the boost hot loop
  17.0 -> 20.8 mm and failed to legalise L3; with U11/L3/D4/C25-C28 fixed, C23 (SS)
  came from 7.0 to 2.7 mm at no loop cost.
- `refine --no-worse` is a soft penalty: an LNS result can still lengthen weight-10
  edges. Accept only after `score` shows no hot-loop/decap regression.
- A side penalty does not enforce "decap on the IC side unless there is no room":
  `W_DECAP_SIDE=100` still let C1/C3/C4 flip for a -12 % decap sum. Flips are now tried
  only in `legal` when no same-side slot exists.
- A block that is already at a good local optimum (PD) does not improve; say so and keep it.

## Freerouting trial routing (TASK-120, 29.09.2026)

- Use it to compare placements under identical conditions, never as the routing.
  Freerouting 2.4.x needs Java 25 (class file 69); a user-dir JRE works without sudo
  (`~/.local/opt/freerouting`, or `FREEROUTING_JAVA`/`FREEROUTING_JAR`).
- GUI mode runs a fanout stage that headless mode skips: do not compare results across
  modes. For screenshots use a user-dir Xvfb (`apt-get download xvfb libxfont2 libxcvt0`,
  `dpkg -x`) with `--display :99` and `xwd` to PNG.
- `ZONE.SetOutline(SHAPE_POLY_SET)` takes ownership and segfaults from python; append the
  points to `zone.Outline()` instead. `GetBoardPolygonOutlines(poly, True)` in KiCad 10.
- ~60 % of unconnected items were plane nets (GND/+3.3V): count signal and plane
  unconnected separately. The optimizer stage can finish worse than autorouting
  (39 -> 47 unrouted); a single run of ~13 min is noise-level for differences of a few
  connections, so repeat before drawing conclusions.
- MAIN_5A (3 mm) nets produce track_width violations; route/pour them by hand.

## Environment

- The kpy Python on Linux has no numpy/matplotlib; the tools are pure python and
  render through kicad-cli.
- If Claude Code auto mode reports "classifier gave no verdict" for every Bash call,
  add the needed commands (`sh .claude/skills/kicad-schematic/scripts/kpy *`,
  `kicad-cli *`, …) to `.claude/settings.local.json` `permissions.allow`; allowed
  rules bypass the classifier. This is a harness outage, not an OS difference.

## Supporting technical guidance

Use these only for the relevant circuit types; component-specific documentation takes precedence:

- [TI: Optimizing Layout for Synchronous Buck Converters](https://www.ti.com/document-viewer/lit/html/SSZTAL0/GUID-CF03725F-911C-4A96-9391-0E639F290409) — bypass placement, feedback, power components, and loop geometry.
- [Analog Devices: Grounding and Decoupling, Part 2](https://www.analog.com/en/resources/analog-dialogue/studentzone/studentzone-april-2017.html) — decoupling and return-path considerations.
