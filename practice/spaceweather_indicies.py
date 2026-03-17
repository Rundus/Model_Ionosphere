# --- read_F10p7 ---
# Use the spaceweather python package to get the solar F10.7 index

import spaceweather as sw
import numpy as np

sw_indices = sw.sw_daily(update=True)
print(sw_indices.keys())
F10p7 = sw_indices['f107_obs'].loc['2025-6-1']
ap = 7
aps = [[ap] * 7]
print(aps)
for i in range(8):
    val = 3*i
    print(sw_indices[f'Ap{val}'].loc['2025-6-1'])
