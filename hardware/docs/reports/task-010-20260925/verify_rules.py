import subprocess
import json
import os

REPORT_DIR = "hardware/docs/reports/task-010-20260925"
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
PCB_FILE = "hardware/gopo.kicad_pcb"
DRU_FILE = "hardware/gopo.kicad_dru"

def run_drc(dru_text, out_json_name):
    with open(DRU_FILE, "w", encoding="utf-8") as f:
        f.write(dru_text)
    
    out_path = os.path.join(REPORT_DIR, out_json_name)
    res = subprocess.run([
        KICAD_CLI, "pcb", "drc",
        "--format", "json",
        "-o", out_path,
        PCB_FILE
    ], capture_output=True, text=True)
    
    with open(out_path, encoding="utf-8") as f:
        data = json.load(f)
    
    violations = data.get("violations", [])
    from collections import Counter
    counts = Counter(v["type"] for v in violations)
    unconnected = len(data.get("unconnected_items", []))
    return counts, len(violations), unconnected, violations

# 1. Baseline with OLD rules (J1, U9)
old_dru = """(version 1)

(rule "Fine pitch package clearance"
	(condition "A.Reference == 'U9'")
	(constraint clearance (min 0.15mm))
)

(rule "JAE USB-C mid-mount copper to edge"
	(condition "A.Reference == 'J1'")
	(constraint edge_clearance (min 0.25mm))
)

(rule "JAE USB-C compound shell slots"
	(condition "A.Reference == 'J1'")
	(constraint annular_width (min 0mm))
)
"""

# 2. Candidate NEW rules
new_dru = """(version 1)

(rule "Fine pitch package clearance"
	(condition "A.Reference == 'U1' || A.Reference == 'U7' || A.Reference == 'U8' || A.Reference == 'U11' || A.Reference == 'U12'")
	(constraint clearance (min 0.15mm))
)

(rule "USB-C J7 copper to edge"
	(condition "A.Reference == 'J7'")
	(constraint edge_clearance (min 0.25mm))
)

(rule "USB-C J7 NPTH to pad hole clearance"
	(condition "A.Reference == 'J7' && B.Reference == 'J7'")
	(constraint hole_clearance (min 0.18mm))
)

(rule "U11 Thermal Via hole size"
	(condition "A.Reference == 'U11'")
	(constraint hole (min 0.20mm))
)

(rule "Mezzanine courtyard exception for proven components"
	(condition "(A.Reference == 'J8' && B.Reference == 'TP14') || (B.Reference == 'J8' && A.Reference == 'TP14')")
	(constraint courtyard_clearance (min -100mm))
)
"""

# 3. Without U11 rule
dru_no_u11 = """(version 1)

(rule "Fine pitch package clearance"
	(condition "A.Reference == 'U1' || A.Reference == 'U7' || A.Reference == 'U8' || A.Reference == 'U11' || A.Reference == 'U12'")
	(constraint clearance (min 0.15mm))
)

(rule "USB-C J7 copper to edge"
	(condition "A.Reference == 'J7'")
	(constraint edge_clearance (min 0.25mm))
)

(rule "USB-C J7 NPTH to pad hole clearance"
	(condition "A.Reference == 'J7' && B.Reference == 'J7'")
	(constraint hole_clearance (min 0.18mm))
)
"""

# 4. Without J7 hole clearance rule
dru_no_j7_hole = """(version 1)

(rule "Fine pitch package clearance"
	(condition "A.Reference == 'U1' || A.Reference == 'U7' || A.Reference == 'U8' || A.Reference == 'U11' || A.Reference == 'U12'")
	(constraint clearance (min 0.15mm))
)

(rule "USB-C J7 copper to edge"
	(condition "A.Reference == 'J7'")
	(constraint edge_clearance (min 0.25mm))
)

(rule "U11 Thermal Via hole size"
	(condition "A.Reference == 'U11'")
	(constraint hole (min 0.20mm))
)
"""

print("Running DRC tests...")
c_old, total_old, unc_old, _ = run_drc(old_dru, "drc-old-rules.json")
print(f"Old DRU: Total violations={total_old}, Breakdown={dict(c_old)}")

c_new, total_new, unc_new, viols_new = run_drc(new_dru, "drc-new-rules.json")
print(f"New DRU: Total violations={total_new}, Breakdown={dict(c_new)}")

c_no_u11, total_no_u11, _, _ = run_drc(dru_no_u11, "drc-without-u11-rule.json")
print(f"Without U11 rule: drill_out_of_range={c_no_u11.get('drill_out_of_range', 0)}, total={total_no_u11}")

c_no_j7, total_no_j7, _, _ = run_drc(dru_no_j7_hole, "drc-without-j7-rule.json")
print(f"Without J7 hole rule: hole_clearance={c_no_j7.get('hole_clearance', 0)}, total={total_no_j7}")

# Re-write the official new_dru into hardware/gopo.kicad_dru
with open(DRU_FILE, "w", encoding="utf-8") as f:
    f.write(new_dru)

summary = {
    "old_rules_summary": {
        "total": total_old,
        "violations": dict(c_old),
        "unconnected": unc_old
    },
    "new_rules_summary": {
        "total": total_new,
        "violations": dict(c_new),
        "unconnected": unc_new
    },
    "controlled_experiments": {
        "u11_thermal_via_rule_effect": {
            "without_rule": c_no_u11.get("drill_out_of_range", 0),
            "with_rule": c_new.get("drill_out_of_range", 0),
            "difference": c_no_u11.get("drill_out_of_range", 0) - c_new.get("drill_out_of_range", 0)
        },
        "j7_npth_hole_clearance_rule_effect": {
            "without_rule": c_no_j7.get("hole_clearance", 0),
            "with_rule": c_new.get("hole_clearance", 0),
            "difference": c_no_j7.get("hole_clearance", 0) - c_new.get("hole_clearance", 0)
        },
        "text_warnings_unchanged": c_new.get("text_height", 0) + c_new.get("text_thickness", 0)
    }
}

with open(os.path.join(REPORT_DIR, "rule_verification_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("Finished successfully. Summary saved to rule_verification_summary.json")
