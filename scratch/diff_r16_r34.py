with open("hardware/gopo.kicad_pcb", "r", encoding="utf-8") as f:
    text = f.read()

from compare_blocks import get_block

r16 = get_block('R16', text)
r34 = get_block('R34', text)

# Print first 25 lines of both
print("--- R16 ---")
for l in r16.splitlines()[:25]:
    print(l)

print("\n--- R34 ---")
for l in r34.splitlines()[:25]:
    print(l)
