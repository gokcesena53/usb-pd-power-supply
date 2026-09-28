import re
from collections import Counter

def parse_rpt(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    violations = re.findall(r'\[(.*?)\]: (.*?)\n\s*@(.*?):', text)
    return violations

base_v = parse_rpt('gopo-drc.rpt')
cand_v = parse_rpt('candidate_task104-drc.rpt')

print(f"Base violations: {len(base_v)}")
print(f"Cand violations: {len(cand_v)}")

base_counts = Counter([v[0] for v in base_v])
cand_counts = Counter([v[0] for v in cand_v])

print("\nCounts comparison:")
all_keys = set(base_counts.keys()) | set(cand_counts.keys())
for k in sorted(all_keys):
    print(f"  {k:25}: base={base_counts.get(k, 0):3} -> cand={cand_counts.get(k, 0):3} (diff: {cand_counts.get(k, 0) - base_counts.get(k, 0):+3})")

# Print new violation details
base_set = set((v[0], v[1].strip()) for v in base_v)
print("\nNew violations details:")
for v in cand_v:
    key = (v[0], v[1].strip())
    if key not in base_set:
        print(f"  [{v[0]}] {v[1]} at {v[2]}")
