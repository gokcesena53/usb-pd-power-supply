#!/usr/bin/env python3
import pcbnew
import math
import sys
sys.path.append('scratch')
from force_repack_optimizer import analyze_ratsnest

def to_mm(val):
    return pcbnew.ToMM(val)

def get_comp_bbox(board, include_anchors=True):
    anchors = {'H1', 'H2', 'H3', 'H4', 'J3', 'J4', 'J7', 'J8', 'J9', 'MECH_ENC', 'U2'}
    min_x = 999.0
    max_x = -999.0
    min_y = 999.0
    max_y = -999.0
    
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if not include_anchors and ref in anchors:
            continue
        boxes = []
        for g in fp.GraphicalItems():
            if "Crtyd" in g.GetLayerName():
                boxes.append(g.GetBoundingBox())
        if boxes:
            m = boxes[0]
            for b in boxes[1:]:
                m.Merge(b)
        else:
            m = fp.GetBoundingBox(False, False)
        x0, y0 = to_mm(m.GetX()), to_mm(m.GetY())
        x1, y1 = to_mm(m.GetRight()), to_mm(m.GetBottom())
        if x0 < min_x: min_x = x0
        if x1 > max_x: max_x = x1
        if y0 < min_y: min_y = y0
        if y1 > max_y: max_y = y1
        
    return {
        'min_x': round(min_x, 3),
        'max_x': round(max_x, 3),
        'min_y': round(min_y, 3),
        'max_y': round(max_y, 3),
        'width': round(max_x - min_x, 3),
        'height': round(max_y - min_y, 3),
        'area_mm2': round((max_x - min_x) * (max_y - min_y), 2)
    }

board_base = pcbnew.LoadBoard('hardware/gopo.kicad_pcb')
board_cand = pcbnew.LoadBoard('scratch/candidate_compaction.kicad_pcb')

rn_base = analyze_ratsnest(board_base)
rn_cand = analyze_ratsnest(board_cand)

bbox_base_all = get_comp_bbox(board_base, include_anchors=True)
bbox_cand_all = get_comp_bbox(board_cand, include_anchors=True)

bbox_base_no_anchors = get_comp_bbox(board_base, include_anchors=False)
bbox_cand_no_anchors = get_comp_bbox(board_cand, include_anchors=False)

print("=== WIRE LENGTH & CROSSINGS METRICS ===")
print(f"Baseline Signal Wire Length:  {rn_base['wirelength_mm']} mm")
print(f"Compacted Signal Wire Length: {rn_cand['wirelength_mm']} mm")
print(f"Wire Length Delta:            {rn_cand['wirelength_mm'] - rn_base['wirelength_mm']:.2f} mm (Reduction: {((rn_base['wirelength_mm'] - rn_cand['wirelength_mm']) / rn_base['wirelength_mm']) * 100:.2f}%)")
print(f"Baseline Crossings:           {rn_base['crossings_count']}")
print(f"Compacted Crossings:          {rn_cand['crossings_count']}")

print("\n=== BOUNDING BOX (ALL 144 COMPONENTS) ===")
print(f"Baseline BBox:  X=[{bbox_base_all['min_x']}, {bbox_base_all['max_x']}] (W={bbox_base_all['width']}), Y=[{bbox_base_all['min_y']}, {bbox_base_all['max_y']}] (H={bbox_base_all['height']}), Area={bbox_base_all['area_mm2']} mm^2")
print(f"Candidate BBox: X=[{bbox_cand_all['min_x']}, {bbox_cand_all['max_x']}] (W={bbox_cand_all['width']}), Y=[{bbox_cand_all['min_y']}, {bbox_cand_all['max_y']}] (H={bbox_cand_all['height']}), Area={bbox_cand_all['area_mm2']} mm^2")

print("\n=== BOUNDING BOX (NON-ANCHOR COMPONENTS) ===")
print(f"Baseline BBox:  X=[{bbox_base_no_anchors['min_x']}, {bbox_base_no_anchors['max_x']}] (W={bbox_base_no_anchors['width']}), Y=[{bbox_base_no_anchors['min_y']}, {bbox_base_no_anchors['max_y']}] (H={bbox_base_no_anchors['height']}), Area={bbox_base_no_anchors['area_mm2']} mm^2")
print(f"Candidate BBox: X=[{bbox_cand_no_anchors['min_x']}, {bbox_cand_no_anchors['max_x']}] (W={bbox_cand_no_anchors['width']}), Y=[{bbox_cand_no_anchors['min_y']}, {bbox_cand_no_anchors['max_y']}] (H={bbox_cand_no_anchors['height']}), Area={bbox_cand_no_anchors['area_mm2']} mm^2")
print(f"Non-Anchor Width Reduction:  {bbox_base_no_anchors['width'] - bbox_cand_no_anchors['width']:.3f} mm")
print(f"Non-Anchor Height Reduction: {bbox_base_no_anchors['height'] - bbox_cand_no_anchors['height']:.3f} mm")
print(f"Non-Anchor Area Reduction:   {bbox_base_no_anchors['area_mm2'] - bbox_cand_no_anchors['area_mm2']:.2f} mm^2 ({(1 - bbox_cand_no_anchors['area_mm2']/bbox_base_no_anchors['area_mm2'])*100:.2f}%)")

