import json

with open("scratch/task099_audit_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("================ RELATIONS & MEASUREMENTS ================")
for r in data['relations']:
    print(f"\n--- {r['name']} ---")
    for k, v in r.items():
        if k != 'name':
            print(f"  {k}: {v}")

print("\n================ INTER-IC RELATIONS ================")
for ic in data['inter_ic']:
    print(f"\n--- {ic['pair']} ---")
    for k, v in ic.items():
        if k != 'pair':
            print(f"  {k}: {v}")
