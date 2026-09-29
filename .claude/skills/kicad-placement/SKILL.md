---
name: kicad-placement
description: Create, optimize, or review KiCad component placement from the IC outward, first within functional blocks and then between blocks, using weighted pad-to-pad ratsnest length and routing constraints. Use for placement tasks; full routing and fabrication review are separate tasks.
---

# KiCad placement

## Agreed approach

Start with the IC, then place surrounding components to reduce critical current loops. Solve each functional block internally before optimizing how blocks fit together. Evaluate connections before attempting routing. The primary metric is weighted ratsnest length, subject to electrical, mechanical, and routing constraints.

These are the user's agreed starting weights, not universal electrical constants:

| Connection role | Weight |
| --- | ---: |
| Critical current loop or local decoupling connection | 10 |
| Sensitive measurement, Kelvin sense, or feedback connection | 5 |
| Other power or signal connection | 1 |

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

Minimize the weighted internal score while applying the alignment rules below. Preserve pad escape paths and space for vias, power copper, thermal needs, and assembly access.

### Component and pad alignment

- Align neighbouring components into deliberate rows or columns within each block. For example, two side-by-side resistors must share a top or bottom body edge; vertically stacked parts use a shared left or right body edge. Apply this to local component groups rather than forcing unrelated blocks onto one global line.
- Use the component body outline from the fabrication layer or documented package geometry as the edge reference. Do not align reference text, silkscreen labels, or footprint origins and assume that component edges align. For different package sizes, explicitly select the shared edge.
- Where possible, align the centres of pads that will connect: use the same Y coordinate for a horizontal connection or the same X coordinate for a vertical connection. For a rotated block, use its local axes. Evaluate actual transformed pad centres, not component centres.
- Choose the component edge and orientation that also align connecting pad centres when both can be satisfied. When different package geometry prevents both, prefer a feasible direct pad connection and explain the body-edge compromise.
- Include aligned candidates during optimization. Do not accept arbitrary staggering merely because it slightly reduces the weighted score. Keep the agreed 10/5/1 weights unchanged; record alignment separately rather than inventing another weight.
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

## Supporting technical guidance

Use these only for the relevant circuit types; component-specific documentation takes precedence:

- [TI: Optimizing Layout for Synchronous Buck Converters](https://www.ti.com/document-viewer/lit/html/SSZTAL0/GUID-CF03725F-911C-4A96-9391-0E639F290409) — bypass placement, feedback, power components, and loop geometry.
- [Analog Devices: Grounding and Decoupling, Part 2](https://www.analog.com/en/resources/analog-dialogue/studentzone/studentzone-april-2017.html) — decoupling and return-path considerations.
