import json
import numpy as np

with open("outputs/part_3_output.json") as f:
    data = json.load(f)

with open("outputs/output.json") as f:
    data2 = json.load(f)


amul_a = np.asarray(data["a"], dtype=np.float32)
a = np.asarray(data2["a"], dtype=np.float32)

cntnot0_amul = 0
cntnot0_us = 0
for i in range(a.shape[0]):
    for j in range(a.shape[1]):
        if abs(amul_a[i][j]) > 1e-20:
            cntnot0_amul += abs(amul_a[i][j])
        if abs(a[i][j]) > 1e-20:
            cntnot0_us += abs(a[i][j])

print(cntnot0_amul, cntnot0_us) 