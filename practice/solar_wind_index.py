# --- read_F10p7 ---
# Use the spaceweather python package to get the solar F10.7 index

import spaceweather as sw
import numpy as np

sw_indices = sw.sw_daily(update=True)
F10p7 = sw_indices['f107_obs']
print(sw_indices.loc['2025-6-1'])