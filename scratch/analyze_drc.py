import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('gopo-drc.rpt', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's extract all violations
violations = re.findall(r'\[([a-zA-Z0-9_]+)\]:\s+(.*?)\n(.*?)(?=\n\[|\n\*\* Found|\n\*\* End)', text, re.DOTALL)
print(f"Total parsed violations: {len(violations)}")

types = {}
tp_related = []
for vtype, desc, details in violations:
    types[vtype] = types.get(vtype, 0) + 1
    if any(f'TP{i}' in details for i in range(1, 20)):
        tp_related.append((vtype, desc, details.strip()))

print("\nViolations by type:")
for t, c in sorted(types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {t}: {c}")

print(f"\nTP related violations ({len(tp_related)}):")
for vtype, desc, details in tp_related:
    print(f"  [{vtype}] {desc}")
    for l in details.splitlines()[:3]:
        print("   ", l.strip())
