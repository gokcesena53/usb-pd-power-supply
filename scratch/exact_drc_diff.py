import re
from collections import Counter

def parse_rpt_blocks(fname):
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Split by violation markers: "[...]: ..."
    blocks = re.split(r'\n(?=\[[a-zA-Z0-9_]+\]:)', text)
    violations = []
    for b in blocks:
        m = re.match(r'\[([a-zA-Z0-9_]+)\]: (.*)', b.strip())
        if m:
            vtype = m.group(1)
            vdesc = m.group(2).split('\n')[0].strip()
            # extract items
            items = re.findall(r'@\([^\)]+\):\s*(.*)', b)
            violations.append((vtype, vdesc, tuple(sorted(items))))
    return violations

base_v = parse_rpt_blocks('gopo-drc.rpt')
test_v = parse_rpt_blocks('gopo_test-drc.rpt')

print(f"Base total: {len(base_v)}")
print(f"Test total: {len(test_v)}")

base_counts = Counter([v[0] for v in base_v])
test_counts = Counter([v[0] for v in test_v])

for k in sorted(set(base_counts.keys()) | set(test_counts.keys())):
    print(f"  {k:25}: base={base_counts.get(k, 0):3} test={test_counts.get(k, 0):3} (diff: {test_counts.get(k, 0) - base_counts.get(k, 0):+3})")

base_set = set(base_v)
print("\n--- VIOLATIONS IN TEST BUT NOT IN BASE ---")
new_v = [v for v in test_v if v not in base_set]
print(f"Count: {len(new_v)}")
for v in new_v[:20]:
    print(f"[{v[0]}] {v[1]}")
    for it in v[2]:
        print(f"     -> {it}")
