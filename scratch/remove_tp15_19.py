import re

pcb_path = "usb-pd-power-supply/hardware/gopo.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# We want to remove footprints TP15, TP16, TP17, TP18, TP19
# And also remove TP15 uuid from (group "TEST NOKTALARI" ...) if present

target_refs = {"TP15", "TP16", "TP17", "TP18", "TP19"}
removed_uuids = set()

# Parse footprints by tracking parentheses or lines
new_lines = []
skip = False
paren_depth = 0
current_fp_lines = []

i = 0
while i < len(lines):
    line = lines[i]
    if line.strip().startswith('(footprint "TestPoint:TestPoint_Pad_D1.0mm"'):
        # collect the full footprint block
        fp_block = [line]
        depth = line.count('(') - line.count(')')
        j = i + 1
        ref = None
        uuid = None
        while j < len(lines) and depth > 0:
            cur = lines[j]
            fp_block.append(cur)
            depth += cur.count('(') - cur.count(')')
            if '(property "Reference"' in cur:
                m = re.search(r'\(property "Reference" "([^"]+)"', cur)
                if m:
                    ref = m.group(1)
            if '(uuid "' in cur and uuid is None:
                m_u = re.search(r'\(uuid "([^"]+)"', cur)
                if m_u:
                    uuid = m_u.group(1)
            j += 1
        
        if ref in target_refs:
            print(f"Removing {ref} (uuid: {uuid}) at line {i+1} to {j}")
            if uuid:
                removed_uuids.add(uuid)
            i = j
            continue
        else:
            new_lines.extend(fp_block)
            i = j
            continue
    else:
        new_lines.append(line)
        i += 1

# Now check removed_uuids in group "TEST NOKTALARI"
final_lines = []
for line in new_lines:
    for uid in removed_uuids:
        if uid in line:
            line = line.replace(f' "{uid}"', '').replace(f'"{uid}"', '')
    final_lines.append(line)

with open(pcb_path, "w", encoding="utf-8") as f:
    f.writelines(final_lines)

print(f"Removed {len(removed_uuids)} footprints. New total lines: {len(final_lines)}")
