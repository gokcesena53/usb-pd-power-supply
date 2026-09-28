import uuid

print("Test UUID generation:")
for i in range(15, 20):
    print(f"TP{i}:")
    print(f"  sym_uuid: {uuid.uuid4()}")
    print(f"  pin_uuid: {uuid.uuid4()}")
    print(f"  fp_uuid:  {uuid.uuid4()}")
    print(f"  pad_uuid: {uuid.uuid4()}")
