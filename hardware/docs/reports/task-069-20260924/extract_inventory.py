"""Extract complete inventory for TASK-069."""
import json
from datetime import datetime
from pathlib import Path
import pcbnew as p

here = Path(__file__).resolve().parent
root = here.parents[3]
b = p.LoadBoard(str(root / 'hardware/gopo.kicad_pcb'))

# Outline
bb = b.GetBoardEdgesBoundingBox()
board_bbox = dict(
    left=round(p.ToMM(bb.GetLeft()), 4),
    top=round(p.ToMM(bb.GetTop()), 4),
    right=round(p.ToMM(bb.GetRight()), 4),
    bottom=round(p.ToMM(bb.GetBottom()), 4),
    width=round(p.ToMM(bb.GetWidth()), 4),
    height=round(p.ToMM(bb.GetHeight()), 4)
)

# Groups
groups_dict = {}
for g in b.Groups():
    name = g.GetName()
    fps = [it for it in g.GetItems() if isinstance(it, p.FOOTPRINT)]
    if fps:
        refs = sorted(f.GetReference() for f in fps)
        xs = [p.ToMM(f.GetPosition().x) for f in fps]
        ys = [p.ToMM(f.GetPosition().y) for f in fps]
        layers = sorted(list(set(f.GetLayerName() for f in fps)))
        groups_dict[name] = dict(
            count=len(refs),
            members=refs,
            layers=layers,
            bbox=[round(min(xs), 3), round(min(ys), 3), round(max(xs), 3), round(max(ys), 3)]
        )

# Footprints
grouped_refs = {r for g in groups_dict.values() for r in g['members']}
all_fps = sorted(b.GetFootprints(), key=lambda f: f.GetReference())
fp_list = []
group_lookup = {r: name for name, g in groups_dict.items() for r in g['members']}

for f in all_fps:
    ref = f.GetReference()
    pos = f.GetPosition()
    box = f.GetBoundingBox(False, False)
    pads = []
    for a in f.Pads():
        p_pos = a.GetPosition()
        pads.append([
            a.GetNumber(),
            a.GetNetname(),
            [round(p.ToMM(p_pos.x), 4), round(p.ToMM(p_pos.y), 4)]
        ])
    pads.sort(key=lambda x: str(x[0]))
    fp_list.append(dict(
        ref=ref,
        value=f.GetValue(),
        footprint=f.GetFPID().GetUniStringLibId(),
        layer=f.GetLayerName(),
        xy=[round(p.ToMM(pos.x), 4), round(p.ToMM(pos.y), 4)],
        angle=round(f.GetOrientationDegrees(), 2),
        locked=f.IsLocked(),
        group=group_lookup.get(ref),
        uuid=f.m_Uuid.AsString(),
        pads=pads,
        bbox=[
            round(p.ToMM(box.GetLeft()), 4),
            round(p.ToMM(box.GetTop()), 4),
            round(p.ToMM(box.GetRight()), 4),
            round(p.ToMM(box.GetBottom()), 4)
        ]
    ))

ungrouped_refs = sorted(list(set(f.GetReference() for f in all_fps) - grouped_refs))

# Tracks
tracks = []
for t in b.GetTracks():
    p1 = t.GetStart()
    p2 = t.GetEnd()
    tracks.append(dict(
        uuid=t.m_Uuid.AsString(),
        net=t.GetNetname(),
        layer=t.GetLayerName(),
        length_mm=round(p.ToMM(t.GetLength()), 6),
        start=[round(p.ToMM(p1.x), 4), round(p.ToMM(p1.y), 4)],
        end=[round(p.ToMM(p2.x), 4), round(p.ToMM(p2.y), 4)],
        width_mm=round(p.ToMM(t.GetWidth()), 4)
    ))

# Anchors
anchor_refs = 'J7 J3 J9 H1 H2 H3 H4 D5 U11'.split()
anchors = {f['ref']: f for f in fp_list if f['ref'] in anchor_refs}

# Load current DRC report from task-080
drc_data = json.loads((root / 'hardware/docs/reports/task-080-20260924/drc-after.json').read_text(encoding='utf-8'))
violations = drc_data['violations']
unconnected = drc_data.get('unconnected_items', [])
parity = drc_data.get('schematic_parity', [])

from collections import Counter
violation_types = Counter(v['type'] for v in violations)

out = dict(
    metadata=dict(
        task="TASK-069",
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        board_file="hardware/gopo.kicad_pcb",
        schematic_file="hardware/gopo.kicad_sch"
    ),
    board_outline=board_bbox,
    total_footprints=len(fp_list),
    total_groups=len(groups_dict),
    grouped_footprints_count=len(grouped_refs),
    ungrouped_footprints=ungrouped_refs,
    groups=groups_dict,
    anchors=anchors,
    pre_existing_tracks=dict(
        count=len(tracks),
        net="/USB_PD_CONTROLLER/BOOST_FB",
        source="TASK-058 (D5.2 to U11.9 FB trace on B.Cu)",
        total_length_mm=round(sum(t['length_mm'] for t in tracks), 6),
        segments=tracks
    ),
    drc_baseline=dict(
        total_violations=len(violations),
        unconnected_items_count=len(unconnected),
        schematic_parity_issues_count=len(parity),
        violation_types=dict(violation_types)
    ),
    footprints=fp_list
)

(here / 'inventory.json').write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"Exported complete inventory with {len(fp_list)} footprints, {len(groups_dict)} groups, {len(tracks)} tracks to {here / 'inventory.json'}")
