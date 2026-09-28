import re

with open("gopo-drc.rpt", "r", encoding="utf-8") as f:
    base_rpt = f.read()

with open("candidate_task102-drc.rpt", "r", encoding="utf-8") as f:
    cand_rpt = f.read()

def parse_violations(rpt):
    # Split by ** Violation or [[warning]]
    v_blocks = re.findall(r'\[(.*?)\]: (.*?)\n(.*?)(?=\n\[|\Z)', rpt, re.DOTALL)
    res = []
    for kind, title, body in v_blocks:
        res.append((kind, title.strip(), body.strip()))
    return res

base_v = parse_violations(base_rpt)
cand_v = parse_violations(cand_rpt)

print(f"Base violations: {len(base_v)}")
print(f"Cand violations: {len(cand_v)}")

# Print new violations in cand_v not in base_v
# Group by title
cand_titles = [v[1] for v in cand_v]
base_titles = [v[1] for v in base_v]

from collections import Counter
c_cand = Counter(cand_titles)
c_base = Counter(base_titles)

print("\nDifferences in violation counts:")
for t in set(list(c_cand.keys()) + list(c_base.keys())):
    if c_cand[t] != c_base[t]:
        print(f"  {t:40}: Base={c_base[t]}, Cand={c_cand[t]} (Diff: {c_cand[t] - c_base[t]:+d})")

print("\n--- Details of new violations in Candidate ---")
for kind, title, body in cand_v:
    if "R2" in body or "R3" in body or "R34" in body or "R35" in body or "R36" in body:
        print(f"[{kind}] {title}")
        for l in body.splitlines()[:5]:
            print("   ", l)
