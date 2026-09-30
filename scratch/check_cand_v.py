import re

with open("gopo-drc.rpt", "r", encoding="utf-8") as f:
    base_rpt = f.read()

with open("gopo_test-drc.rpt", "r", encoding="utf-8") as f:
    cand_rpt = f.read()

def parse_violations_only(rpt):
    m = re.search(r'\*\* Found ([0-9]+) DRC violations \*\*(.*?)(?=\*\* Found|\Z)', rpt, re.DOTALL)
    if not m:
        return []
    content = m.group(2)
    v_blocks = re.findall(r'\[(.*?)\]: (.*?)\n(.*?)(?=\n\[|\Z)', content, re.DOTALL)
    return [(b[0], b[1].strip(), b[2].strip()) for b in v_blocks]

base_v = parse_violations_only(base_rpt)
cand_v = parse_violations_only(cand_rpt)

print(f"Base DRC violations: {len(base_v)}")
print(f"Cand DRC violations: {len(cand_v)}")

for kind, title, body in cand_v:
    if "R2" in body or "R3" in body or "R34" in body or "R35" in body or "R36" in body:
        print(f"[{kind}] {title}")
        for l in body.splitlines()[:3]:
            print("   ", l)
