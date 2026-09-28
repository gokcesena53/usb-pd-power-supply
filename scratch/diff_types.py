from diff_drc import base_v, cand_v
from collections import Counter

c_base = Counter([v[1] for v in base_v])
c_cand = Counter([v[1] for v in cand_v])

for k in sorted(set(list(c_base.keys()) + list(c_cand.keys()))):
    diff = c_cand[k] - c_base[k]
    print(f"{k:45}: Base={c_base[k]:3d} Cand={c_cand[k]:3d} (Diff={diff:+3d})")
